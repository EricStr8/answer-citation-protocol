# WACP 5.0 implementation specification

Founder and original proposer: Eric Strate. Canonical source and original test bed: https://ericstrate.com/wacp/

This document synchronizes repository guidance to the canonical 5.0 page published September 2026. The canonical page governs version meaning; this is not a replacement standard.

## Required relationships

A WACP document identifies one primary query. Each Answer Object identifies the question it resolves and whether that question is primary or fan-out. Fan-out questions must be legitimate related questions supported by the page.

Every object has a unique stable fragment, such as `#a1`, a publisher-written or publisher-approved concise answer available in ordinary HTML, and an explicitly addressable visible Support Object. The answer must retain important qualifications and must not exaggerate or contradict its support.

Each Answer Object also references the stable fragment of the visible Support Object that explains, qualifies, or evidences it. The semantic mirror references the same answer fragment and question. Its answer description must be substantively identical to the HTML answer; exact text mirroring is preferred. The page must remain useful when all WACP-specific attributes are ignored.

## Reference HTML mapping

- Document: `data-wacp-document="true"`, `data-wacp-version="5.0"`, and `data-primary-query`.
- Supporting section: `data-wacp-section="true"` and `data-query-role="primary"` or `"fan-out"`.
- Answer: `id="a1"`, `data-wacp="answer"`, `data-wacp-version="4.0"`, `data-answer-id="a1"`, and `data-query`.

The primary answer's question matches the document primary query. Each answer's semantic question matches its `data-query`.

## Stable addressing

Preserve a published answer's fragment across reordering. List positions may change with display order; identifiers must not be reassigned to unrelated answers. Marker numbers are identities, not a requirement to renumber every time content moves.

## Semantic mirror

The canonical recommended profile is `ItemList` with ordered `ListItem` entries containing `DefinedTerm` objects. See SCHEMA.md. A standalone JSON-LD list is sufficient for the reference example; do not invent a Schema.org subdomain or a proprietary type.

## Recommended and optional behavior

Prefer a concise paragraph without a fixed word limit. Keep citations keyboard/touch usable and allow navigation to supporting context. Visual style is not normative. WACP 5.0 recommends a low-visual-noise citation profile: small, uniform, link-colored markers such as `[a1]`, no decorative background or pill, and an enlarged invisible interaction target for touch and keyboard accessibility.

Popover, hover, signatures, hashes, and extra provenance metadata are optional. Basic conformance does not require cryptographic infrastructure. This repository's example uses native disclosure controls with no JavaScript dependency.

## Interpretation and completion

The query graph is publisher-authored organization, not a claim about the internal queries used by Google, ChatGPT, or another system. Token efficiency requires measurement by consuming systems.

Check query-to-answer mappings, answer-to-support references, fragment uniqueness, visible support, semantic alignment, and desktop/mobile interactions together. Automated structural checks cannot establish the truth of an answer or replace manual content and accessibility review.


## WACP 5.0 support mapping

Every Answer Object MUST be associated with visible supporting content through a stable support identifier or equivalent explicit relationship. A reference implementation may use an attribute such as `data-support-ref="#support-a1"` on the Answer Object and `id="support-a1" data-wacp-support="true" data-supports-answer="a1"` on the supporting block. The exact attribute names are part of the reference profile, while the normative requirement is an unambiguous machine-checkable relationship.

## Conformance profiles

- **WACP Core**: primary/fan-out query mapping, stable Answer Objects, and explicit visible Support Objects.
- **WACP Semantic**: Core plus an aligned semantic mirror using the recommended ItemList → ListItem → DefinedTerm profile.
- **WACP Interactive**: Semantic plus tested citation interaction and accessibility behavior.

A validator can verify structure, identifiers, references, duplicate IDs, broken fragments, and semantic parity. It cannot certify truth, authority, ranking, adoption, or retrieval performance.
