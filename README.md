Web Answer Citation Protocol (WACP)
Version: 2.0.0 | Author: Eric Strate | Contact: ericstrate.com

Overview
The Web Answer Citation Protocol (WACP) is a web architecture standard designed to optimize content for Retrieval-Augmented Generation (RAG) systems and Large Language Models (LLMs). WACP introduces a dual-layer approach: separating human-readable narrative from machine-readable semantic answers.

By explicitly defining concise, publisher-authored answers within JSON-LD, WACP reduces token consumption for AI crawlers while ensuring accurate attribution, data provenance, and compliance with modern W3C standards.

Core Principles
Token & Semantic Efficiency: LLMs retrieve specific answer blocks rather than parsing the entire DOM of a page, drastically reducing inference latency and computational waste.
Cryptographic Provenance: WACP v2.0 supports optional cryptographic verification parameters (e.g., acpSignature) to guarantee that structured answers originated from the publisher and have not been altered mid-transit by scrapers or injection attacks.
W3C Schema Compliance: The protocol leverages natively supported semantic blocks like DefinedTerm, DataFeed, and ItemList within an explicit @context declaration, ensuring seamless integration with existing search infrastructure without custom handling code.
Publisher Intent: Instead of forcing AI to infer relevance, WACP allows publishers to declare "This is the authoritative answer," shifting the focus from keyword density to accuracy.
Implementation Summary
WACP v2.0 utilizes standard JSON-LD schema markup embedded within the page header or body. It defines a structured ItemList array where each ListItem contains a DefinedTerm object representing a unique Answer Citation.

Visual Reference: A human user sees a superscript marker (e.g., [a1]) at the end of a sentence. When clicked or hovered, it reveals the content defined in the JSON-LD block.

Quick Start
Define your answer blocks in your HTML using unique identifiers (e.g., [a1]).
Embed the JSON-LD script in your page <head> utilizing the extended @context declaration.
Implement optional cryptographic signatures (acpSignature) for tamper-proof data provenance.
Deploy and verify using the WACP validator.
