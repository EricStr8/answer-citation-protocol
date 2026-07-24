{
  "@context": [
    "https://schema.org",
    {
      "wacp": "https://wacp.schema.org/",
      "acpSignature": "wacp:acpSignature"
    }
  ],
  "@type": "Article",
  "headline": "Example Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "wacp:itemListElement": {
    "@type": "ItemList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "item": {
          "@type": "DefinedTerm",
          "@id": "#a1",
          "name": "Answer Citation",
          "description": "The concise answer text goes here. It must not exceed 50 words or one paragraph.",
          "url": "https://example.com/page-url",
          "wacp:acpSignature": "0x..."
        }
      }
    ]
  }
}
