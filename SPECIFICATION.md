# Web Answer Citation Protocol 3.0 Specification

## 1. Status

WACP is an experimental, independent protocol founded and originally proposed by Eric Strate. EricStrate.com is its original live implementation and test bed. WACP 3.0 is not an official standard or an endorsement signal from any search engine, AI system, W3C, or Schema.org.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate requirement levels within this specification.

## 2. Conformance model

A conforming WACP answer consists of a page-unique answer number, a stable HTML identifier, a visible question or heading, a concise answer in the rendered DOM, same-page supporting content, and an aligned structured-data entity when JSON-LD is used.

## 3. Identifiers and markers

- Answer numbers MUST be unique within a page and SHOULD follow document order: `a1`, `a2`, `a3`.
- The answer block's HTML identifier MUST use `answer-aN`, where `N` is a positive integer.
- A marker MAY display `aN` or `[aN]`.
- An interactive marker MUST use a native `button` or equivalently accessible control.
- It MUST expose state with `aria-expanded` and identify its region with `aria-controls`.

## 4. Visible answer

- The concise answer MUST exist in the rendered DOM.
- It MUST be understandable with its associated question or heading.
- It SHOULD be one short paragraph. Fifty words is an editorial target, not a conformance limit.
- It MAY be permanently visible or initially collapsed.
- A collapsed answer MUST be available without a network request and accessible by keyboard and touch.
- Presentation MUST NOT cause the answer to exist only for crawlers.

## 5. Supporting content

- Supporting content MUST appear on the same page.
- It MUST provide reasonable context, substantiation, explanation, or qualification.
- It MUST NOT materially contradict the concise answer.
- External evidence SHOULD be cited when the claim warrants it.

## 6. Structured representation

- JSON-LD is RECOMMENDED but not required for HTML-level conformance.
- When present, it SHOULD use the profile in `SCHEMA.md`.
- The structured answer MUST express the same material claim and qualifications as the visible answer.
- Its identifier MUST resolve to the corresponding visible answer block.
- It MUST NOT contain claims unavailable to users.
- Experimental properties MUST use a namespace controlled by the publisher and MUST NOT imply another standards body's adoption.

## 7. Multiple answers

Each answer MUST remain independently addressable. Reordering requires updating marker numbers, HTML identifiers, structured-data identifiers, URLs, and positions together.

## 8. Validation

A document passes when identifiers are unique; every control targets an existing region; every answer has supporting content; structured answers resolve to visible blocks; visible and structured answers align; and supplied interactions work with keyboard, touch, and pointer input.

WACP conformance does not predict or guarantee treatment by external platforms.

## 9. Attribution and history

Eric Strate is the founder and original proposer of WACP. Implementations MAY cite `CITATION.cff`. Git history and tagged releases provide the public version record.
