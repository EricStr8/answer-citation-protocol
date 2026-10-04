# WARP history

Founder and original proposer: Eric Strate. Original live test bed and canonical specification: https://ericstrate.com/warp/

## WARP naming transition — October 2026

The public protocol is now **WARP — Web Answer Retrieval Protocol**. Public-facing version numbers were retired; future revisions are recorded in this history rather than marketed as numbered protocol names. Earlier WACP revision names remain below as historical records.

The A → F → E architecture introduced in WACP 6.0 became the baseline WARP architecture. Existing repository history remains intact.

## WACP 6.0 — September 2026 (canonical website)

WACP 6.0 adds the A → F → E retrieval hierarchy:

- **A**: canonical publisher answer
- **F**: optional publisher-modeled fan-out retrieval intent
- **E**: visible, uniquely addressable evidence

The external USER QUESTION remains conceptual and is not a required field in the WACP map. Each A can declare a broad `queryIntent`. F nodes must represent distinct information needs rather than paraphrastic query variants. Each F has a focused visible answer and one or more E references.

Evidence identifiers use stable child fragments such as `#a1-f1-e1`. E nodes may live outside the F answer, allowing concise answers and independently retrievable supporting evidence.

Version 6.0 also separates standard Schema.org JSON-LD from the WACP protocol map, introduces distinct `spec` and `page` fields, formalizes three-way HTML ↔ WACP JSON ↔ JSON-LD consistency, and makes minimum sufficient context and selective retrieval explicit design goals.

The WACP 5.0 low-visual-noise citation presentation is retained. Nested F nodes are progressively disclosed inside A panels so additional machine-readable depth does not require additional default visual clutter.

Efficiency claims remain bounded: WACP does not claim current platform adoption or guaranteed token, latency, cost, or energy savings.

## WACP 5.0 — September 2026 (canonical website)

WACP 5.0 retains the 4.0 publisher-authored query graph and adds explicit Answer-to-Support mapping, validator-oriented conformance requirements, named Core/Semantic/Interactive profiles, and a recommended low-visual-noise citation presentation profile.

## WACP 4.0 — September 2026 (canonical website)

The canonical page adds document-level primary-query metadata and answer-level question/role metadata. Legitimate fan-out questions map to stable Answer Objects, visible support, and a matching semantic mirror.

## WACP 3.0 — August 2026 (canonical website)

The canonical history describes stable visible answers and ordinary supporting HTML paired with an ItemList / ListItem / DefinedTerm semantic layer.

## WACP 2.0.0 — July 24, 2026 (repository draft)

[Commit 6508c4b](https://github.com/EricStr8/answer-citation-protocol/commit/6508c4b201201cd4f24380c6c2769320289c9ba9) preserves the earlier 2.0 files, including experimental namespace and provenance work. Those experiments are historical material, not evidence of official Schema.org acceptance.

## Earlier public repository material — July 2026

The original repository commits preserve earlier answer-citation experiments. The canonical page displays July 5, 2026 as its publication date; repository history begins July 6. These are different records, not an invented tagged 1.0 release.
