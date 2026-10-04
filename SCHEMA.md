# WARP machine-readable layers

Canonical source: https://ericstrate.com/warp/

Founder and original proposer: Eric Strate. Original live test bed: EricStrate.com.

WARP deliberately separates two machine-readable concerns:

1. **Standard semantic JSON-LD** uses established Schema.org vocabulary to mirror visible content.
2. **The WARP protocol map** uses ordinary `application/json` to express WARP-specific A → F → E relationships.

This separation avoids inventing unsupported Schema.org properties for WARP-only concepts.

## Standard JSON-LD

The reference example represents A objects with `ItemList → ListItem → DefinedTerm` and visible F nodes with `Question → acceptedAnswer → Answer`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ItemList",
      "@id": "https://example.com/warp-example/#answers",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "item": {
            "@type": "DefinedTerm",
            "@id": "https://example.com/warp-example/#a1",
            "name": "What is WARP?",
            "description": "WARP is Eric Strate's proposed publishing architecture for concise publisher-authored answers, optional fan-out retrieval intents, visible addressable evidence, and aligned machine-readable representations.",
            "url": "https://example.com/warp-example/#a1"
          }
        },
        {
          "@type": "ListItem",
          "position": 2,
          "item": {
            "@type": "DefinedTerm",
            "@id": "https://example.com/warp-example/#a2",
            "name": "How does WARP handle evidence?",
            "description": "WARP gives visible supporting evidence stable E identifiers so an F answer can point to the precise support it needs without requiring that evidence to be duplicated inside the F answer.",
            "url": "https://example.com/warp-example/#a2"
          }
        }
      ]
    },
    {
      "@type": "Question",
      "@id": "https://example.com/warp-example/#a1-f1",
      "url": "https://example.com/warp-example/#a1-f1",
      "name": "What is a WARP fan-out node?",
      "acceptedAnswer": {
        "@type": "Answer",
        "@id": "https://example.com/warp-example/#a1-f1-answer",
        "text": "A WARP fan-out node is a publisher-modeled secondary retrieval intent nested beneath a canonical Answer Object."
      }
    },
    {
      "@type": "Question",
      "@id": "https://example.com/warp-example/#a1-f2",
      "url": "https://example.com/warp-example/#a1-f2",
      "name": "Does WARP claim to know an AI system's private fan-out queries?",
      "acceptedAnswer": {
        "@type": "Answer",
        "@id": "https://example.com/warp-example/#a1-f2-answer",
        "text": "No. WARP F nodes are publisher-authored retrieval hypotheses and do not claim to reproduce private system queries or ranking logic."
      }
    },
    {
      "@type": "Question",
      "@id": "https://example.com/warp-example/#a2-f1",
      "url": "https://example.com/warp-example/#a2-f1",
      "name": "Can evidence live outside the F answer?",
      "acceptedAnswer": {
        "@type": "Answer",
        "@id": "https://example.com/warp-example/#a2-f1-answer",
        "text": "Yes. An E node can remain in normal visible supporting content and be referenced by stable ID from the F answer."
      }
    }
  ]
}
```

Each A `DefinedTerm` mirrors one visible canonical answer. Each F `Question.name` matches the visible F question, and each `acceptedAnswer.text` matches the visible focused F answer.

WARP does not require `FAQPage`, `QAPage`, or a custom Schema.org type.

## WARP protocol map

The same page can expose protocol-specific relationships separately:

```json
{
  "protocol": "WARP",
  "spec": "https://ericstrate.com/warp/",
  "page": "https://example.com/warp-example/",
  "terminology": {
    "A": "canonical publisher answer",
    "F": "publisher-modeled fan-out retrieval intent",
    "E": "visible uniquely addressable evidence"
  },
  "designGoals": [
    "minimum sufficient context",
    "selective retrieval",
    "semantic diversity",
    "evidence mapping",
    "progressive disclosure"
  ],
  "answers": [
    {
      "id": "a1",
      "selector": "#a1",
      "supportSelector": "#support-a1",
      "queryIntent": "protocol definition",
      "fanOut": [
        {
          "id": "a1-f1",
          "question": "What is a WARP fan-out node?",
          "answerSelector": "#a1-f1-answer",
          "evidence": ["#a1-f1-e1"]
        },
        {
          "id": "a1-f2",
          "question": "Does WARP claim to know an AI system's private fan-out queries?",
          "answerSelector": "#a1-f2-answer",
          "evidence": ["#a1-f2-e1"]
        }
      ]
    },
    {
      "id": "a2",
      "selector": "#a2",
      "supportSelector": "#support-a2",
      "queryIntent": "evidence design",
      "fanOut": [
        {
          "id": "a2-f1",
          "question": "Can evidence live outside the F answer?",
          "answerSelector": "#a2-f1-answer",
          "evidence": ["#a2-f1-e1"]
        }
      ]
    }
  ]
}
```

`spec` identifies the permanent WARP specification. `page` identifies the canonical implementation URL. They are separate because WARP can be implemented on pages other than the specification itself.

The external USER QUESTION is conceptual and is not a required WARP map field. Per-answer `queryIntent` metadata describes the broad information need without pretending to enumerate infinite query phrasings.

Replace `example.com` with the actual canonical implementation URL. Preserve appropriate existing page-level structured data; WARP's semantic objects do not need to replace it.

This is WARP's experimental use of existing web vocabulary. It is not official Schema.org approval of WARP and does not imply search-feature eligibility or platform adoption.
