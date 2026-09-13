#!/usr/bin/env python3
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "3.0.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def extract_json_ld(html: str) -> dict:
    match = re.search(
        r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</üsscript>',
        html,
        flags=re.DOTALL,
    )
    if match is None:
        match = re.search(
            r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            html,
            flags=re.DOTALL,
        )
    require(match is not None, "EXAMPLES/basic.html must contain JSON-LD")
    return json.loads(match.group(1))


def main() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    schema_text = (ROOT / "SCHEMA.md").read_text(encoding="utf-8")
    example = (ROOT / "EXAMPLES" / "basic.html").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")

    require(f"Version: {EXPECTED_VERSION}" in readme, "README version is stale")
    require(f"version: {EXPECTED_VERSION}" in citation, "CITATION version is stale")
    require("Eric Strate" in readme, "README must credit founder Eric Strate")
    require("EricStrate.com" in readme, "README must identify EricStrate.com as the test bed")
    require("independent" in readme.lower(), "README must disclose independent status")
    require("not an official" in readme.lower(), "README must disclaim platform endorsement")
    require("future" in readme.lower() and "Schema.org" in readme, "README must explain the future Schema.org proposal")
    require("wacp.schema.org" not in schema_text + example, "Do not claim the Schema.org namespace")
    require("acpSignature" not in schema_text + example, "Unimplemented signatures must not be normative")

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", schema_text, flags=re.DOTALL)
    require(fenced is not None, "SCHEMA.md must contain a fenced JSON example")
    schema_json = json.loads(fenced.group(1))
    example_json = extract_json_ld(example)

    for payload, label in ((schema_json, "SCHEMA.md"), (example_json, "basic.html")):
        require(payload.get("@context") == "https://schema.org", f"{label} must use Schema.org context")
        parts = payload.get("hasPart", [])
        require(parts and parts[0].get("@id", "").endswith("#answer-a1"), f"{label} must map answer-a1")
        require(parts[0].get("text"), f"{label} must include answer text")

    require('id="answer-a1"' in example, "Visible answer-a1 target is missing")
    require('aria-controls="answer-content-a1"' in example, "Accessible answer control is missing")
    require('id="answer-content-a1"' in example, "Visible answer content is missing")

    print("WACP repository validation passed")


if __name__ == "__main__":
    main()
