# WACP 4.0 implementation specification

Founder and original proposer: Eric Strate. Canonical source and original test bed: https://ericstrate.com/wacp/

This document synchronizes repository guidance to the canonical 4.0 page reviewed September 13, 2026. The canonical page governs version meaning; this is not a replacement standard.

## Required relationships

A WACP document identifies one primary query. Each Answer Object identifies the question it resolves and whether that question is primary or fan-out. Fan-out questions must be legitimate related questions supported by the page.

Every object has a unique stable fragment, such as `#a1`, a publisher-written or publisher-approved concise answer available in ordinary HTML, and visible supporting content. The answer must retain important qualifications and must not exaggerate or contradict its support.

The semantic mirror references the same fragment and question. Its answer description must be substantively identical to the HTML answer; exact text mirroring is preferred. The page must remain useful when all WACP-specific attributes are ignored.

## Reference HTML mapping

- Document: `data-wacp-document="true"`, `data-wacp-version="4.0"`, and `data-primary-query`.
- Supporting section: `data-wacp-section="true"` and `data-query-role="primary"` or `"fan-out"`.
- Answer: `id="a1"`, `data-wacp="answer"`, `data-wacp-version="4.0"`, `data-answer-id="a1"`, and `data-query`.

The primary answer's question matches the document primary query. Each answer's semantic question matches its `data-query`.

## Stable addressing

Preserve a published answer's fragment across reordering. List positions may change with display order; identifiers must not be reassigned to unrelated answers. Marker numbers are identities, not a requirement to renumber every time content moves.

## Semantic mirror

The canonical recommended profile is `ItemList` with ordered `ListItem` entries containing `DefinedTerm` objects. See SCHEMA.md. A standalone JSON-LD list is sufficient for the reference example; do not invent a Schema.org subdomain or a proprietary type.

## Recommended and optional behavior

Prefer a concise paragraph without a fixed word limit. Keep citations keyboard/touch usable and allow navigation to supporting context. Visual style is not normative.

Popover, hover, signatures, hashes, and extra provenance metadata are optional. Basic conformance does not require cryptographic infrastructure. This repository's example uses native disclosure controls with no JavaScript dependency.

## Interpretation and completion

The query graph is publisher-authored organization, not a claim about the internal queries used by Google, ChatGPT, or another system. Token efficiency requires measurement by consuming systems.

Check query-to-answer mappings, fragment uniqueness, visible support, semantic alignment, and desktop/mobile interactions together. Automated structural checks cannot establish the truth of an answer or replace manual content and accessibility review.
