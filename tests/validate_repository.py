#!/usr/bin/env python3
"""Structural repository checks; not a general WACP or Schema.org validator."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.answers = []
        self.primary = None
        self.role = None
        self.current = None
        self.capture = None
        self.script = ""
        self.in_json = False
        self.supports = 0
        self.details = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if a.get("data-wacp-document") == "true":
            assert a["data-wacp-version"] == "4.0"
            assert self.primary is None, "Multiple WACP documents in example"
            self.primary = a["data-primary-query"]
        if a.get("data-wacp-section") == "true":
            self.role = a["data-query-role"]
        if a.get("data-wacp") == "answer":
            assert a["data-wacp-version"] == "4.0"
            assert a["id"] == a["data-answer-id"]
            self.current = dict(id=a["id"], question=a["data-query"],
                                role=self.role, text="")
            self.answers.append(self.current)
        if a.get("data-wacp-answer-text") == "true":
            self.capture = tag
        if a.get("data-wacp-support") == "true":
            self.supports += 1
        if tag == "details":
            self.details += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_json = True

    def handle_data(self, data):
        if self.in_json:
            self.script += data
        if self.capture:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == self.capture:
            self.capture = None
        if tag == "script":
            self.in_json = False

def validate(html):
    page = Page()
    page.feed(html)
    assert page.primary, "Missing primary query"
    assert len(page.ids) == len(set(page.ids)), "Duplicate IDs"
    assert len(page.answers) >= 2, "Example must exercise primary and fan-out"
    assert {a["role"] for a in page.answers} == {"primary", "fan-out"}
    assert page.supports == len(page.answers), "Missing supporting blocks"
    assert page.details == len(page.answers), "Missing native disclosure"
    payload = json.loads(page.script)
    assert payload["@context"] == "https://schema.org"
    assert payload["@type"] == "ItemList"
    entries = payload["itemListElement"]
    assert len(entries) == len(page.answers), "Mirror count differs"
    for position, (answer, entry) in enumerate(zip(page.answers, entries), 1):
        assert entry["@type"] == "ListItem"
        assert entry["position"] == position
        item = entry["item"]
        assert item["@type"] == "DefinedTerm"
        assert item["@id"] == item["url"]
        assert item["@id"].split("#")[-1] == answer["id"]
        assert item["name"] == answer["question"]
        assert item["description"] == answer["text"].strip(), "Answer text mismatch"
        if answer["role"] == "primary":
            assert answer["question"] == page.primary
    return payload

def main():
    html = (ROOT / "EXAMPLES/basic.html").read_text()
    payload = validate(html)
    schema = (ROOT / "SCHEMA.md").read_text()
    assert json.loads(re.search(r"```json\s*(.*?)\s*```", schema, re.S).group(1)) == payload
    readme = (ROOT / "README.md").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    history = (ROOT / "CHANGELOG.md").read_text()
    assert "Version: 4.0.0" in readme and "version: 4.0.0" in citation
    assert "date-released:" not in citation
    assert "Unreleased" in history
    assert "Eric Strate" in readme and "EricStrate.com" in readme
    assert "https://ericstrate.com/wacp/" in citation
    assert "family-names: Strate" in citation and "given-names: Eric" in citation
    assert "future" in readme and "Schema.org" in readme
    assert "wacp.schema.org" not in html + schema
    # Negative controls: each corrupted example must fail.
    mutations = [
        html.replace('id="a2"', 'id="a1"'),
        html.replace('data-primary-query="What is WACP?"', ''),
        html.replace('data-query-role="fan-out"', 'data-query-role="primary"'),
        html.replace('<p data-wacp-answer-text="true">WACP', '<p data-wacp-answer-text="true">Changed'),
        html.replace('"position": 2', '"position": 1'),
    ]
    for mutation in mutations:
        try:
            validate(mutation)
        except (AssertionError, KeyError):
            pass
        else:
            raise AssertionError("Negative control incorrectly passed")
    print("PASS: WACP 4.0 example mappings, metadata, history; 5 negative controls")

if __name__ == "__main__":
    main()
