# WACP 4.0 semantic mirror

Canonical source: https://ericstrate.com/wacp/

Founder and original proposer: Eric Strate. Original live test bed: EricStrate.com.

The published 4.0 profile uses ItemList → ListItem → DefinedTerm. This supersedes the unmerged WebPageElement recommendation previously drafted on this branch.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "@id": "https://example.com/wacp-example/#answers",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "item": {
        "@type": "DefinedTerm",
        "@id": "https://example.com/wacp-example/#a1",
        "name": "What is WACP?",
        "description": "WACP is Eric Strate's proposed publishing architecture for mapping questions to stable publisher-authored answers, visible supporting content, and a matching semantic representation.",
        "url": "https://example.com/wacp-example/#a1"
      }
    },
    {
      "@type": "ListItem",
      "position": 2,
      "item": {
        "@type": "DefinedTerm",
        "@id": "https://example.com/wacp-example/#a2",
        "name": "What does WACP 4.0 add?",
        "description": "WACP 4.0 adds explicit primary-query and fan-out-query metadata while retaining stable answer identifiers, visible support, and semantic mirroring.",
        "url": "https://example.com/wacp-example/#a2"
      }
    }
  ]
}
```

Each list entry represents one HTML answer. DefinedTerm `@id` and `url` reference its stable fragment; `name` matches the answer's question; `description` mirrors its concise answer. ListItem `position` records current display order without changing the answer identity.

The accompanying HTML declares document primary-query metadata and section primary/fan-out roles. No custom Schema.org query-role property is asserted.

Replace example.com with the actual canonical page URL. Preserve appropriate existing page-level structured data; this list need not replace it.

This is WACP's experimental use of existing vocabulary, not official Schema.org approval of WACP or guaranteed search-feature eligibility. Optional provenance extensions need separately documented mechanisms. Earlier custom-namespace experiments remain in Git history as research intended to inform a possible future inclusion proposal.
