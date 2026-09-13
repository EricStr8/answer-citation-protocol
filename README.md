# Web Answer Citation Protocol (WACP)

Version: 4.0.0 (canonical specification: 4.0)
Status: Proposed and experimental publishing architecture

**Founder and original proposer: Eric Strate**

**Canonical specification and original live test bed: [EricStrate.com](https://ericstrate.com/wacp/)**

## Architecture

WACP connects a document's primary query and genuine related questions to publisher-approved Answer Objects. Each answer has a stable fragment, ordinary visible supporting HTML, and a matching semantic representation.

Primary query → fan-out question → Answer Object → visible support → semantic mirror.

The query graph describes the publisher's document organization. It does not reveal or reproduce a search engine's private query expansion. The normal page remains useful without WACP attributes.

## Implementing version 4.0

- Declare one primary query on the document.
- Associate each answer with its question and primary or fan-out role.
- Use stable fragments such as `#a1` and matching citations such as `[a1]`.
- Keep the concise answer in ordinary HTML and its support visible.
- Mirror answers one-to-one using `ItemList → ListItem → DefinedTerm`; match identifiers, questions, and answer descriptions.
- Choose an accessible interface. Popovers and hover behavior are optional, not protocol versions.

See [SPECIFICATION.md](SPECIFICATION.md), [SCHEMA.md](SCHEMA.md), and the two-answer [working example](EXAMPLES/basic.html). When adapting the example, replace its example.com URLs and author with your own.

## Founder, canonical source, and history

Eric Strate is WACP's founder and original proposer. EricStrate.com is the original live test bed; its [WACP page](https://ericstrate.com/wacp/) is the permanent canonical specification. This repository supplies implementation guidance, examples, and source-control history.

The [changelog](CHANGELOG.md) separates earlier committed drafts, canonical website versions, and this repository synchronization. Existing commits remain intact. The prior 3.0 rewrite on this review branch was an unmerged editorial draft, not a historical WACP release.

## Schema.org experimentation

The original Schema.org-related mapping was an experiment intended to gather evidence for a possible future inclusion request. That research intent is retained. Version 4.0 uses existing vocabulary; it does not depend on an accepted WACP-specific type. A future proposal remains subject to independent review.

WACP is independent and is not an official Schema.org or W3C standard. It is not endorsed by search engines or AI providers. A mapped namespace does not establish ownership or endorsement of that namespace.

Efficiency and improved retrieval are research goals, not guaranteed results. WACP does not guarantee ranking, citations, adoption, cost savings, or trust. Cryptographic provenance is optional future work, not a supplied signing or verification implementation.

## Citation and license

Please credit Eric Strate and link to the canonical specification when discussing WACP. [CITATION.cff](CITATION.cff) supplies machine-readable attribution. Source and documentation retain the [MIT license](LICENSE); requested scholarly credit does not add restrictions to that license.

## Checks

Run `python3 tests/validate_repository.py`. These repository checks cover the example's query metadata, identifiers, visible/semantic mirroring, and citation/history consistency. They do not certify platform recognition, semantic truth, or every external implementation.
