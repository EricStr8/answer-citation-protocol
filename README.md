# Web Answer Citation Protocol (WACP)

**Version: 3.0.0** | **Founder and original proposer: Eric Strate** | **Test bed: [EricStrate.com](https://ericstrate.com/)**

WACP is an experimental, independent web publishing protocol for connecting concise, publisher-authored answers with visible supporting content and aligned structured data.

Eric Strate founded and first publicly proposed the Web Answer Citation Protocol. EricStrate.com is the original live test bed, where the protocol is implemented, observed, and refined using real web pages.

## Why WACP exists

WACP gives each concise answer a stable identifier and connects it to:

1. a visible question or heading;
2. a concise answer in the rendered page;
3. supporting page content; and
4. an aligned machine-readable representation.

WACP does not replace good writing, evidence, HTML semantics, or established structured-data vocabularies. It is a publishing convention intended to make answer relationships clearer and easier to test.

## WACP 3.0 model

| Layer | Purpose |
| --- | --- |
| Stable identifier | Gives the answer a page-unique target such as `answer-a1` |
| Visible answer | Makes the concise answer available to people and rendered-page parsers |
| Supporting content | Provides context, evidence, and appropriate qualification |
| Structured representation | Describes the same answer using valid JSON-LD and established Schema.org vocabulary |

The visible answer and its structured representation must express the same material claim. Structured data must not introduce claims that users cannot find in the page content.

See [SPECIFICATION.md](SPECIFICATION.md) for normative requirements, [SCHEMA.md](SCHEMA.md) for the structured-data profile, and [EXAMPLES/basic.html](EXAMPLES/basic.html) for a working example.

## Schema.org research branch

WACP uses established Schema.org types and properties wherever possible. Experimental mappings are being tested on EricStrate.com to collect implementation evidence and determine whether a future Schema.org inclusion proposal is justified.

This research relationship does **not** mean that WACP is currently part of or endorsed by Schema.org. WACP does not use or claim a `schema.org` subdomain or unofficial Schema.org namespace. Any future inclusion request would be submitted through Schema.org's public proposal process and evaluated independently.

## Project status and limitations

WACP is an independent proposal created by Eric Strate. It is not an official W3C, Schema.org, Google, OpenAI, Microsoft, Anthropic, or other platform standard. Implementation does not guarantee crawling, indexing, ranking, retrieval, attribution, citation, or inclusion in an AI-generated answer.

Claims about crawler efficiency, model behavior, or citation performance require controlled evidence and are not normative features of WACP.

## Version history

- **1.0:** Original public answer-citation proposal and stable answer markers.
- **2.0:** Added JSON-LD answer mapping and provenance experiments.
- **3.0:** Requires alignment among identifiers, visible answers, supporting content, and structured representations; clarifies accessibility and independent status.

See [CHANGELOG.md](CHANGELOG.md) for details.

## Authorship and citation

> Strate, Eric. *Web Answer Citation Protocol (WACP)*, version 3.0.0. https://github.com/EricStr8/answer-citation-protocol

Machine-readable citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

WACP is released under the [MIT License](LICENSE). Historical commits, releases, and citation metadata document the protocol's public development and authorship.
