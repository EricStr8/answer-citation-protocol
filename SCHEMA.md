# WACP 3.0 Structured-Data Profile

WACP 3.0 uses established Schema.org vocabulary. It does not claim a custom Schema.org namespace or imply that WACP is an accepted Schema.org extension.

## Recommended mapping

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://example.com/page/#article",
  "headline": "Example Article",
  "author": {
    "@type": "Person",
    "name": "Eric Strate",
    "url": "https://ericstrate.com/"
  },
  "hasPart": [
    {
      "@type": "WebPageElement",
      "@id": "https://example.com/page/#answer-a1",
      "name": "What does WACP provide?",
      "text": "WACP maps a concise, publisher-authored answer to visible supporting content and aligned structured data.",
      "position": 1,
      "url": "https://example.com/page/#answer-a1"
    }
  ]
}
```

## Mapping rules

- The fragment in `@id` and `url` MUST resolve to the visible answer block's HTML `id`.
- `name` MUST match or faithfully represent the visible question or heading.
- `text` MUST match the visible concise answer in meaning and material qualification.
- `position` SHOULD correspond to the answer marker number.
- Structured data MUST NOT contain an answer or claim absent from the visible page.
- Publishers SHOULD use absolute canonical URLs in JSON-LD.
- Multiple answers MUST be represented as separate `WebPageElement` objects.

## Experimental extensions

Custom WACP properties and cryptographic provenance fields are outside the normative WACP 3.0 profile. They may be explored in separately identified experiments, but an experiment must not use a `schema.org` subdomain or imply official Schema.org adoption.

EricStrate.com is the original live test bed. Results may inform a future Schema.org proposal after sufficient implementation evidence exists. Until such a proposal is accepted, only published Schema.org vocabulary should be represented as Schema.org vocabulary.
