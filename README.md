Answer Citation Protocol (ACP)
Version: 1.0.0
Author: Eric Strate | ericstrate.com

Overview
The Answer Citation Protocol (ACP) is a web architecture standard designed to optimize content for Retrieval-Augmented Generation (RAG) systems and Large Language Models (LLMs). It introduces a dual-layer approach: separating human-readable narrative from machine-readable semantic answers.

By explicitly defining concise answers within JSON-LD, publishers can reduce token consumption for AI crawlers while ensuring accurate attribution in search results.

Core Principles
Token Efficiency: LLMs retrieve the specific answer block rather than parsing the entire DOM of a page.
Attribution: Every generated answer is explicitly linked to its source via a unique identifier (e.g., [a1]).
Human-Agnostic: The machine-readable layer can be hidden visually (via CSS) without hiding it from crawlers, maintaining clean UI design.
Implementation Summary
ACP utilizes standard JSON-LD schema markup embedded within the page header or body. It defines a specific answerCitation object containing an ID and text payload.

Visual Reference:
A human user sees a superscript marker (e.g., [a1]) at the end of a sentence. When clicked or hovered, it reveals the content defined in the JSON-LD block.
