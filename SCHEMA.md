# WACP 5.0 semantic mirror

Canonical source: https://ericstrate.com/wacp/

Founder and original proposer: Eric Strate. Original live test bed: EricStrate.com.

The published 5.0 profile uses ItemList → ListItem → DefinedTerm. This supersedes the unmerged WebPageElement recommendation previously drafted on this branch.

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
        "name": "What does WACP 5.0 add?",
        "description": "WACP 5.0 retains the 4.0 query graph and adds explicit Answer-to-Support mapping, validator-oriented conformance rules, named conformance profiles, and a recommended low-visual-noise citation presentation profile.",
        "url": "https://example.com/wacp-example/#a2"
      }
    }
  ]
}
```

Each list entry represents one HTML answer. DefinedTerm `@id` and `url` reference its stable fragment; `name` matches the answer's question; `description` mirrors its concise answer. ListItem `position` records current display order without changing the answer identity.

The accompanying HTML declares document primary-query metadata, section primary/fan-out roles, and explicit Answer-to-Support relationships. No custom Schema.org query-role property is asserted.

Replace example.com with the actual canonical page URL. Preserve appropriate existing page-level structured data; this list need not replace it.

This is WACP's experimental use of existing vocabulary, not official Schema.org approval of WACP or guaranteed search-feature eligibility. Optional provenance extensions need separately documented mechanisms. Earlier custom-namespace experiments remain in Git history as research intended to inform a possible future inclusion proposal.
