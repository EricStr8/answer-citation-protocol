# WARP implementation specification

Founder and original proposer: Eric Strate.  
Canonical source and original test bed: https://ericstrate.com/warp/

This document synchronizes repository guidance to the canonical WARP specification. The canonical page is the current public protocol; numbered revisions are retained only in project history.

## 1. Conceptual model

WARP distinguishes the external user request from the publisher's encoded retrieval structure.

**USER QUESTION** is conceptual and external to the WARP map. The same Answer Object may serve many phrasings, so WARP does not require publishers to enumerate every possible user question.

The encoded hierarchy begins at A:

**A = canonical publisher answer → F = optional publisher-modeled fan-out retrieval intent → E = visible, uniquely addressable evidence.**

A page can contain multiple A objects. Each A can declare a broad `queryIntent` describing the information need it is designed to resolve.

F nodes are publisher-authored retrieval hypotheses. They MUST represent materially different information needs and MUST NOT be presented as the private fan-out queries, ranking logic, or internal reasoning of a search engine or AI system.

E nodes are visible evidence spans. An E node MAY live outside the F answer and SHOULD remain independently addressable so a consuming system can retrieve only as much supporting context as needed.

## 2. Required relationships

### Answer Object (A)

Each A object MUST:

- have a unique stable fragment identifier such as `#a1`;
- expose a concise publisher-written or publisher-approved answer in ordinary visible HTML;
- associate that answer with visible supporting content;
- preserve important qualifications from its support;
- remain useful when WARP-specific attributes are ignored.

An A object MAY expose a broad `queryIntent`. Query intent is not a binding claim that one literal user query maps only to that A.

### Fan-Out node (F)

When fan-out is used, each F node MUST:

- have a unique stable child identifier such as `#a1-f1`;
- identify exactly one parent A;
- expose a visible human-readable question or retrieval-intent label;
- expose a visible focused answer;
- reference at least one E node;
- be materially distinct from sibling F nodes.

Exact or near-exact query paraphrases SHOULD be rejected editorially. Automated validators can catch exact duplication but cannot prove semantic diversity.

### Evidence Object (E)

Every referenced E node MUST:

- have a unique stable identifier such as `#a1-f1-e1`;
- resolve to exactly one visible DOM element;
- materially support the A or F answer that references it;
- remain part of the normal human-readable page.

Hidden, schema-only, or nonexistent evidence does not satisfy WARP.

E does not need to be contained inside the F answer. This separation allows concise F answers and independently retrievable supporting evidence.

## 3. Reference HTML mapping

A reference implementation may use:

- Document: `data-warp-document="true"`.
- Document intent: `data-primary-intent="..."`.
- Answer: `id="a1"`, `data-warp="answer"`, `data-answer-id="a1"`, and `data-support-ref="#support-a1"`.
- Fan-out: `id="a1-f1"`, `data-warp="fanout"`, `data-parent-answer="a1"`, `data-query="..."`, and `data-evidence-ref="#a1-f1-e1"`.
- Focused F answer: a stable element such as `id="a1-f1-answer"`.
- Evidence: `id="a1-f1-e1"`, `data-warp-evidence="true"`, and `data-evidence-for="a1-f1"`.
- Support block: `id="support-a1"`, `data-warp-support="true"`, and `data-supports-answer="a1"`.

The exact data-attribute names above define the repository reference profile. Other implementations can express equivalent relationships as long as they are unambiguous and machine-checkable.

## 4. Stable addressing

Published A, F, and E identifiers SHOULD remain stable across normal editing and reordering. Identifiers are identities, not instructions to renumber every time content moves.

A direct F fragment such as `#a1-f1` SHOULD reveal the parent A interaction and the targeted F branch in the Interactive profile.

## 5. WARP machine map

WARP-specific relationships belong in a separate JSON block, for example:

```html
<script type="application/json" id="warp-map">...</script>
```

The reference WARP map includes:

- `protocol`: `"WARP"`
- `spec`: canonical WARP specification URL
- `page`: canonical URL of the implementation being described
- `terminology`: definitions for A, F, and E
- `designGoals`: optional declared goals
- `answers`: encoded A objects

Each entry in `answers` SHOULD include `id`, `selector`, `supportSelector`, `queryIntent`, and `fanOut`.

Each F entry SHOULD include `id`, `question`, `answerSelector`, and `evidence`.

The top-level WARP map MUST NOT require a literal `userQuestion` field. The external user question is conceptual because many phrasings can resolve to the same A object.

`page` SHOULD match the implementation page's canonical URL exactly. `spec` identifies the canonical WARP specification separately.

## 6. Standard semantic layer

WARP separates standard semantics from protocol-specific mapping.

The recommended reference profile uses existing Schema.org vocabulary:

- A objects: `ItemList → ListItem → DefinedTerm`
- Visible F questions: `Question → acceptedAnswer → Answer`

The semantic layer MUST NOT introduce materially different claims from the visible page.

When JSON-LD represents an F node:

- `Question.name` SHOULD match the visible F question.
- `Answer.text` SHOULD match the visible focused F answer.

WARP does not require `FAQPage`, `QAPage`, a proprietary WARP Schema.org type, or a proprietary `fanOut` Schema.org property.

See [SCHEMA.md](SCHEMA.md).

## 7. Minimum sufficient context

Selective retrieval is a WARP design goal.

A compatible consuming system could retrieve A alone for a direct canonical answer, A + F for a focused secondary information need, or A + F + one or more E nodes when support or verification is needed.

This architecture is intended to reduce unnecessary retrieval or context processing when a consumer supports selective use of the structure. It does not establish that current systems consume WARP or that WARP guarantees token, latency, cost, or energy savings.

## 8. Presentation

WARP preserves the low-visual-noise presentation profile introduced in 5.0.

Recommended:

- small, link-colored A markers such as `[a1]`;
- no decorative background or pill;
- larger invisible interaction target for accessibility;
- progressively disclosed F nodes inside the A panel;
- ordinary evidence links rather than extra visible E badges where possible.

Visual styling remains non-normative.

## 9. Conformance profiles

### WARP Core

Core requires stable visible A objects, explicit visible A support, valid F → A relationships when F is used, valid F → E relationships when F is used, and visible, uniquely addressable E nodes.

### WARP Semantic

Semantic requires Core plus a WARP `application/json` map, valid standard JSON-LD where semantic mirroring is provided, and selector/reference parity among HTML, WARP JSON, and JSON-LD.

### WARP Interactive

Interactive requires Semantic plus tested interaction and accessibility behavior, including direct F fragments where the implementation exposes them.

## 10. Validator checks

A structural validator can check:

- every A, F, and E identifier is unique;
- every A support selector resolves;
- every F identifies one valid parent A;
- every F answer selector resolves;
- every F references at least one existing E;
- every E reference resolves to exactly one visible element;
- exact duplicate sibling F questions are rejected;
- WARP map selectors resolve to the HTML;
- `page` matches the canonical implementation URL;
- the WARP map does not encode a required `userQuestion`;
- JSON-LD F question and answer text match visible F content;
- WARP map F questions match JSON-LD F questions.

A validator cannot establish factual truth, authority, ranking, platform adoption, retrieval performance, or deep semantic diversity without additional review.

## 11. Interpretation

WARP is a publisher-side experimental architecture. F nodes describe information needs a publisher has prepared to resolve; they are not assertions about undisclosed system behavior.

Token efficiency, retrieval efficiency, latency reduction, and energy reduction remain testable design hypotheses. Publishers SHOULD use bounded language unless measured evidence from a consuming system exists.
