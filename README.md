# Web Answer Citation Protocol (WACP)

Version: 6.0.0 (canonical specification: 6.0)  
Status: Proposed and experimental publishing architecture

**Founder and original proposer: Eric Strate**

**Canonical specification and original live test bed: [EricStrate.com](https://ericstrate.com/wacp/)**

## Architecture

WACP 6.0 organizes publisher-authored answers for selective retrieval using three encoded layers:

**A = canonical publisher answer → F = optional publisher-modeled fan-out retrieval intent → E = visible, uniquely addressable evidence.**

The external **USER QUESTION** is a conceptual input to retrieval. It is not enumerated in the WACP JSON map because many surface phrasings may resolve to the same Answer Object.

A page may contain multiple A objects. Each A can declare a broad `queryIntent`. F nodes are publisher-authored retrieval hypotheses representing genuinely different information needs, not a claim to reproduce the private fan-out queries, ranking logic, or reasoning process of Google, ChatGPT, or another system. E nodes are visible DOM elements that materially support an A or F answer.

The design goal is **minimum sufficient context**: a compatible system could retrieve only the A/F/E units needed for a question instead of processing unrelated page content. Token, latency, cost, and energy savings are hypotheses to be measured by consuming systems, not guaranteed outcomes.

## Implementing version 6.0

- Give each Answer Object a stable fragment such as `#a1` and keep its concise answer in ordinary visible HTML.
- Associate each A with visible support and, when useful, a broad `queryIntent`.
- Add F nodes only for semantically distinct retrieval needs. Do not manufacture keyword or wording variants.
- Give every F a stable child ID such as `#a1-f1`, a visible focused answer, and at least one E reference.
- Give each E a stable ID such as `#a1-f1-e1`. Every referenced E must resolve to exactly one visible DOM element.
- E may live outside the F answer. This allows the F answer to remain concise while evidence stays independently retrievable.
- Use valid Schema.org JSON-LD for standard semantics. The reference profile mirrors A objects with `ItemList → ListItem → DefinedTerm` and visible F nodes with `Question → acceptedAnswer → Answer`.
- Use a separate `application/json` WACP map for protocol-specific A → F → E relationships. Do not invent Schema.org properties for `fanOut` or other WACP-only concepts.
- Keep `spec` and `page` distinct in the WACP map: `spec` identifies the canonical WACP specification, while `page` identifies the canonical URL of the implementation being described.
- Validate HTML, WACP JSON, and JSON-LD together. WACP 6.0 recognizes Core, Semantic, and Interactive conformance profiles.

The recommended visual profile remains deliberately quiet: small, link-colored A markers such as `[a1]`, no decorative pill or background, and progressively disclosed F nodes inside the A panel. Presentation remains non-normative.

See [SPECIFICATION.md](SPECIFICATION.md), [SCHEMA.md](SCHEMA.md), and the [working example](EXAMPLES/basic.html). When adapting the example, replace its `example.com` URL and author information with your own.

## Founder, canonical source, and history

Eric Strate is WACP's founder and original proposer. EricStrate.com is the original live test bed; its [WACP page](https://ericstrate.com/wacp/) is the permanent canonical specification. This repository supplies implementation guidance, examples, source-control history, and structural validation.

The [changelog](CHANGELOG.md) separates canonical website versions from repository synchronization. Existing commits remain intact.

## Schema.org experimentation

WACP 6.0 uses established Schema.org vocabulary where it accurately describes visible content. WACP does not require a proprietary Schema.org type or property.

The separate WACP map carries protocol-specific relationships. That separation is intentional: valid standard semantics stay standard, while WACP can evolve independently as an experimental publishing protocol.

WACP is independent and is not an official Schema.org or W3C standard. It is not endorsed by search engines or AI providers. WACP does not guarantee ranking, citations, adoption, cost savings, token savings, energy savings, or trust.

## Citation and license

Please credit Eric Strate and link to the canonical specification when discussing WACP. [CITATION.cff](CITATION.cff) supplies machine-readable attribution. Source and documentation retain the [MIT license](LICENSE); requested scholarly credit does not add restrictions to that license.

## Checks

Run:

```bash
python3 tests/validate_repository.py
```

The repository validator checks the reference example's A/F/E identifiers, evidence references, canonical/page relationship, WACP map, JSON-LD parity, and selected negative controls. It does not certify factual truth, semantic diversity beyond machine-checkable duplication, platform recognition, ranking impact, or retrieval-performance claims.
