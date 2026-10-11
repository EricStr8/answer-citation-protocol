#!/usr/bin/env python3
"""Validate commercial WARP pages against a canonical pricing page.

Works with locally saved WordPress HTML; does not fetch URLs or send prompts.
This checks structural/factual consistency, not AI search rankings or truth.
"""
import argparse
import json
import re
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


def norm(value):
    return re.sub(r"\s+", " ", unescape(str(value))).strip().casefold()


class Page(HTMLParser):
    def __init__(self, label, source):
        super().__init__(convert_charrefs=True)
        self.label = label
        self.ids = Counter()
        self.answers = {}
        self.fanouts = {}
        self.evidence = {}
        self.scripts = []
        self.visible = []
        self.script_type = None
        self.script_id = None
        self.script_data = []
        self.hidden_depth = 0
        self.feed(source)
        self.close()
        self.body_text = norm(" ".join(self.visible))
        self.graph = []
        self.warp = None
        for typ, sid, data in self.scripts:
            if typ not in ("application/ld+json", "application/json"):
                continue
            try:
                obj = json.loads(data)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{label}: invalid {typ} in {sid}: {exc}") from exc
            if typ == "application/json" and sid == "warp-map":
                if self.warp is not None:
                    raise ValueError(f"{label}: multiple WARP maps")
                self.warp = obj
            elif typ == "application/ld+json":
                for node in (obj if isinstance(obj, list) else obj.get("@graph", [obj])):
                    if isinstance(node, dict):
                        self.graph.append(node)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids[a["id"]] += 1
        if tag == "script":
            self.script_type = a.get("type", "")
            self.script_id = a.get("id", "")
            self.script_data = []
            return
        if tag in ("style", "noscript"):
            self.hidden_depth += 1
        if a.get("data-warp") == "answer":
            self.answers[a["id"]] = a
        if a.get("data-warp") == "fanout":
            self.fanouts[a["id"]] = a
        if a.get("data-warp-evidence") == "true":
            self.evidence[a["id"]] = a

    def handle_data(self, data):
        if self.script_type is not None:
            self.script_data.append(data)
        elif self.hidden_depth == 0:
            self.visible.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.script_type is not None:
            self.scripts.append((self.script_type, self.script_id, "".join(self.script_data)))
            self.script_type = None
            self.script_data = []
        elif tag in ("style", "noscript") and self.hidden_depth:
            self.hidden_depth -= 1

    def nodes(self, typ):
        return [n for n in self.graph if typ in (
            n.get("@type", []) if isinstance(n.get("@type"), list) else [n.get("@type")]
        )]


def verify_warp(page, problems):
    tag = page.label
    def fail(detail):
        problems.append(f"{tag}: {detail}")

    if not page.warp or page.warp.get("protocol") != "WARP":
        fail("missing or invalid WARP map")
        return
    duplicates = [key for key, count in page.ids.items() if count > 1]
    if duplicates:
        fail("duplicate HTML ids: " + ", ".join(duplicates[:10]))

    mapped_answers = {a.get("id") for a in page.warp.get("answers", [])}
    if mapped_answers != set(page.answers):
        fail("WARP map answer IDs disagree with HTML answer IDs")

    defined = {}
    for item_list in page.nodes("ItemList"):
        for element in item_list.get("itemListElement", []):
            term = element.get("item", {})
            if isinstance(term, dict) and term.get("@type") == "DefinedTerm":
                defined[term.get("@id", "").split("#")[-1]] = term
    for aid in page.answers:
        term = defined.get(aid)
        if not term:
            fail(f"{aid} lacks a JSON-LD DefinedTerm")
        elif not term.get("description") or norm(term["description"]) not in page.body_text:
            fail(f"{aid} schema answer is not present in readable page content")

    questions = {
        n.get("@id", "").split("#")[-1]: n
        for n in page.nodes("Question") if n.get("@id")
    }
    mapped_fanouts = set()
    for answer in page.warp.get("answers", []):
        aid = answer.get("id")
        for f in answer.get("fanOut", []):
            fid = f.get("id")
            mapped_fanouts.add(fid)
            markup = page.fanouts.get(fid)
            if not markup:
                fail(f"{fid} in WARP map but absent from HTML")
                continue
            if markup.get("data-parent-answer") != aid:
                fail(f"{fid} parent does not match {aid}")
            if f.get("question") != markup.get("data-query"):
                fail(f"{fid} question disagrees with visible markup")
            target = f.get("answerSelector", "").lstrip("#")
            if not target or page.ids[target] != 1:
                fail(f"{fid} has a missing or duplicated focused answer target")
            evidence = f.get("evidence", [])
            if not evidence:
                fail(f"{fid} has no evidence references")
            for ref in evidence:
                eid = ref.lstrip("#")
                ev = page.evidence.get(eid)
                if not ev or page.ids[eid] != 1 or ev.get("data-evidence-for") != fid:
                    fail(f"{fid} has a missing, duplicated or misassigned evidence target {eid}")
            q = questions.get(fid)
            if not q or q.get("name") != f.get("question"):
                fail(f"{fid} JSON-LD Question is missing or inconsistent")
            elif q.get("acceptedAnswer", {}).get("@id", "").split("#")[-1] != target:
                fail(f"{fid} JSON-LD acceptedAnswer target is inconsistent")
    if mapped_fanouts != set(page.fanouts):
        fail("HTML and WARP map fan-out IDs differ")


def amount(offer):
    spec = offer.get("priceSpecification", {})
    if not isinstance(spec, dict):
        spec = {}
    value = offer.get("price") or offer.get("minPrice") or spec.get("price") or spec.get("minPrice")
    try:
        price = Decimal(str(value).replace(",", ""))
    except (InvalidOperation, TypeError):
        price = None
    unit = norm(spec.get("unitText", offer.get("unitText", "")))
    return price, ("month" in unit)


def verify_services(page, provider_id, problems):
    tag = page.label
    if page.warp and page.warp.get("page"):
        canonical = page.warp["page"].rstrip("/")
        pages = page.nodes("WebPage")
        if pages and not any(n.get("@id", "").split("#")[0].rstrip("/") == canonical for n in pages):
            problems.append(f"{tag}: WARP map URL and WebPage schema URL differ")
    for node in page.nodes("Person"):
        if node.get("name") and node.get("@id") != provider_id:
            problems.append(f"{tag}: inconsistent Person @id: {node.get('@id')}")
    for node in page.graph:
        for key in ("provider", "seller"):
            ref = node.get(key)
            if isinstance(ref, dict) and ref.get("@id") and ref["@id"] != provider_id:
                problems.append(f"{tag}: {key} has different provider ID: {ref['@id']}")


def offers(page, problems):
    catalogs = page.nodes("OfferCatalog")
    if not catalogs:
        problems.append(f"{page.label}: missing OfferCatalog")
        return {}
    result = {}
    for catalog in catalogs:
        for offer in catalog.get("itemListElement", []):
            if offer.get("@type") != "Offer":
                continue
            name = offer.get("name", "")
            key = norm(name)
            if not key or key in result:
                problems.append(f"{page.label}: blank or duplicate offer {name}")
                continue
            price, monthly = amount(offer)
            if price is None:
                problems.append(f"{page.label}: price missing from {name}")
                continue
            if key not in page.body_text:
                problems.append(f"{page.label}: schema offer not named in visible content: {name}")
            display = "$" + f"{price:,.0f}"
            if norm(display) not in page.body_text:
                problems.append(f"{page.label}: {name} price {display} missing from readable content")
            result[key] = (price, monthly)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pricing", type=Path, required=True, help="saved HTML of canonical pricing page")
    parser.add_argument("--page", type=Path, action="append", required=True, help="saved HTML of another commercial page; repeatable")
    parser.add_argument("--provider-id", required=True, help="canonical Schema.org Person @id")
    args = parser.parse_args(argv)
    files = [args.pricing, *args.page]
    pages = [Page(str(path), path.read_text(encoding="utf-8")) for path in files]
    problems = []
    for page in pages:
        verify_warp(page, problems)
        verify_services(page, args.provider_id, problems)
    reference = offers(pages[0], problems)
    for page in pages[1:]:
        for name, details in offers(page, problems).items():
            if name not in reference:
                problems.append(f"{page.label}: offer not in canonical catalog: {name}")
            elif details != reference[name]:
                problems.append(f"{page.label}: offer price or billing differs: {name}")
    if problems:
        print("FAIL: commercial WARP consistency\n" + "\n".join("- " + issue for issue in problems))
        return 1
    print(f"PASS: {len(pages)} pages; WARP A/F/E, visible offers and prices, provider identity, JSON-LD alignment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
