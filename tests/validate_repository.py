#!/usr/bin/env python3
"""Structural checks for the WARP reference example."""
import json,re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXAMPLE_URL="https://example.com/warp-example/"
SPEC_URL="https://ericstrate.com/wacp/"

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.canonical=None;self.intent=None;self.role=None
        self.answers=[];self.a=None;self.cap_a=None;self.fanouts=[];self.f=None;self.cap_f=None
        self.evidence={};self.eid=None;self.cap_e=None;self.support_ids=set();self.support_links={}
        self.jsonld=[];self.wmap=None;self.stype=None;self.sid=None;self.stext=""
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        if tag=="link" and a.get("rel")=="canonical":self.canonical=a.get("href")
        if a.get("data-wacp-document")=="true":self.version=a.get("data-wacp-version");self.intent=a.get("data-primary-intent")
        if a.get("data-wacp-section")=="true":self.role=a.get("data-query-role")
        if a.get("data-wacp")=="answer":
            assert a["id"]==a["data-answer-id"] and a["data-wacp-version"]=="6.0" and a.get("data-support-ref")
            self.support_links[a["id"]]=a["data-support-ref"].lstrip("#");self.a={"id":a["id"],"role":self.role,"text":""};self.answers.append(self.a)
        if a.get("data-wacp-answer-text")=="true":self.cap_a=tag
        if a.get("data-wacp")=="fanout":
            refs=[x.lstrip("#") for x in a.get("data-evidence-ref","").split() if x]
            self.f={"id":a["id"],"parent":a.get("data-parent-answer"),"question":a.get("data-query"),"answer_id":a["id"]+"-answer","text":"","evidence":refs};self.fanouts.append(self.f)
        if a.get("data-wacp-fanout-answer-text")=="true":self.cap_f=tag
        if a.get("data-wacp-evidence")=="true":
            self.eid=a["id"];self.evidence[self.eid]={"for":a.get("data-evidence-for"),"text":"","tag":tag};self.cap_e=tag
        if a.get("data-wacp-support")=="true":self.support_ids.add(a["id"])
        if tag=="script":self.stype=a.get("type");self.sid=a.get("id");self.stext=""
    def handle_data(self,data):
        if self.cap_a and self.a:self.a["text"]+=data
        if self.cap_f and self.f:self.f["text"]+=data
        if self.cap_e and self.eid:self.evidence[self.eid]["text"]+=data
        if self.stype:self.stext+=data
    def handle_endtag(self,tag):
        if tag==self.cap_a:self.cap_a=None
        if tag==self.cap_f:self.cap_f=None
        if tag==self.cap_e:self.cap_e=None;self.eid=None
        if tag=="details" and self.f is not None:self.f=None
        if tag=="script" and self.stype:
            if self.stype=="application/ld+json":self.jsonld.append(json.loads(self.stext))
            elif self.stype=="application/json" and self.sid=="warp-map":self.wmap=json.loads(self.stext)
            self.stype=None;self.sid=None;self.stext=""

def graph(scripts):
    out=[]
    for p in scripts:out.extend(p.get("@graph",[]) if isinstance(p,dict) and isinstance(p.get("@graph"),list) else [p])
    return out

def validate(html):
    p=Page();p.feed(html);counts=Counter(p.ids)
    assert p.canonical==EXAMPLE_URL and p.intent
    assert all(v==1 for v in counts.values())
    assert len(p.answers)>=2 and {"primary","supporting"}<={a["role"] for a in p.answers}
    assert set(p.support_links.values())==p.support_ids
    aids={a["id"] for a in p.answers};fids={f["id"] for f in p.fanouts};eids=set(p.evidence)
    assert fids and eids
    sibling={}
    for f in p.fanouts:
        assert f["parent"] in aids and f["question"] and f["text"].strip() and f["answer_id"] in counts and f["evidence"]
        sibling.setdefault(f["parent"],[]).append(f["question"])
        for eid in f["evidence"]:
            assert eid in eids and p.evidence[eid]["for"]==f["id"] and p.evidence[eid]["text"].strip() and p.evidence[eid]["tag"]!="script"
    for qs in sibling.values():assert len(qs)==len(set(qs))

    w=p.wmap;assert w and w["protocol"]=="WARP" and "version" not in w and w["spec"]==SPEC_URL and w["page"]==p.canonical
    assert "userQuestion" not in w
    assert w["terminology"]=={"A":"canonical publisher answer","F":"publisher-modeled fan-out retrieval intent","E":"visible uniquely addressable evidence"}
    hf={f["id"]:f for f in p.fanouts};mapped=set()
    assert len(w["answers"])==len(p.answers)
    for a in w["answers"]:
        assert a["selector"]=="#"+a["id"] and a["selector"][1:] in counts and a["supportSelector"][1:] in p.support_ids and a.get("queryIntent")
        for f in a.get("fanOut",[]):
            mapped.add(f["id"]);x=hf[f["id"]]
            assert x["parent"]==a["id"] and f["question"]==x["question"] and f["answerSelector"]=="#"+x["answer_id"] and f["answerSelector"][1:] in counts
            assert [r.lstrip("#") for r in f["evidence"]]==x["evidence"] and all(r.lstrip("#") in eids for r in f["evidence"])
    assert mapped==fids

    g=graph(p.jsonld);lists=[n for n in g if n.get("@type")=="ItemList"];qs=[n for n in g if n.get("@type")=="Question"]
    assert len(lists)==1 and len(lists[0]["itemListElement"])==len(p.answers)
    for i,(a,e) in enumerate(zip(p.answers,lists[0]["itemListElement"]),1):
        item=e["item"];assert e["@type"]=="ListItem" and e["position"]==i and item["@type"]=="DefinedTerm"
        assert item["@id"]==item["url"] and item["@id"].split("#")[-1]==a["id"] and item["description"]==a["text"].strip()
    sem={n["@id"].split("#")[-1]:n for n in qs};assert set(sem)==fids
    for fid,x in hf.items():
        n=sem[fid];assert n["name"]==x["question"] and n["acceptedAnswer"]["@id"].split("#")[-1]==x["answer_id"] and n["acceptedAnswer"]["text"]==x["text"].strip()
    assert "function revealHashTarget" in html
    return w,p.jsonld

def main():
    html=(ROOT/"EXAMPLES/basic.html").read_text();w,scripts=validate(html)
    schema=(ROOT/"SCHEMA.md").read_text();blocks=[json.loads(x) for x in re.findall(r"```json\s*(.*?)\s*```",schema,re.S)]
    assert blocks[0]==scripts[0] and blocks[1]==w
    readme=(ROOT/"README.md").read_text();citation=(ROOT/"CITATION.cff").read_text();history=(ROOT/"CHANGELOG.md").read_text();spec=(ROOT/"SPECIFICATION.md").read_text()
    assert "Version:" not in readme and "version:" not in citation and "WACP 6.0" in history
    assert "A → F → E" in readme+history and "minimum sufficient context" in (readme+spec).lower()
    assert "`spec`" in spec and "`page`" in spec and "userQuestion" in spec and "date-released:" not in citation
    assert "Eric Strate" in readme and "EricStrate.com" in readme and SPEC_URL in citation
    assert "family-names: Strate" in citation and "given-names: Eric" in citation and "warp.schema.org" not in html+schema+spec
    mutations=[
      html.replace('data-evidence-ref="#a2-f1-e1"','data-evidence-ref="#missing"'),
      html.replace('id="a1-f1-e1"','id="a1-f2-e1"'),
      html.replace('"queryIntent": "evidence design"','"queryIntent": ""'),
      html.replace('"name": "Can evidence live outside the F answer?"','"name": "Changed semantic question"'),
      html.replace('"page": "https://example.com/warp-example/"','"page": "https://example.com/wrong/"'),
      html.replace('"designGoals": [','"userQuestion": "What is WARP?",\n  "designGoals": ['),
      html.replace('data-query="Does WARP claim to know an AI system\'s private fan-out queries?"','data-query="What is a WARP fan-out node?"')
    ]
    for m in mutations:
        try:validate(m)
        except (AssertionError,KeyError,json.JSONDecodeError):pass
        else:raise AssertionError("Negative control incorrectly passed")
    print("PASS: WARP A/F/E HTML, evidence references, WARP map, JSON-LD parity, canonical mapping; 7 negative controls")

if __name__=="__main__":main()
