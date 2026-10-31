# Writing library

Blogs, technical articles, and longer learning guides live here. Each piece has
one folder containing its Markdown source and any supporting images or examples.

## Read

| Title | Format | Topic |
| --- | --- | --- |
| [End-to-End FDE Learning Map](guides/end-to-end-fde-learning-map/README.md) | Learning guide | Forward deployed engineering |

The FDE guide is also available in the
[local Field Guide reader](http://localhost:8000/docs/#end-to-end-fde-learning-map).

## Structure

```text
content/
├── articles/                         Blogs and technical articles
│   └── README.md                     Article index
├── guides/                           Longer learning maps and tutorials
│   ├── README.md                     Guide index
│   └── end-to-end-fde-learning-map/
│       └── README.md                  Existing FDE guide source
├── templates/
│   ├── article.md                    Blog / technical article starting point
│   └── guide.md                      Learning guide starting point
└── README.md                         Writing index and conventions
```

## Add a new piece

1. Choose `articles/` for a focused blog or technical article, or `guides/` for
   an extended tutorial, learning map, or field guide.
2. Create a short, descriptive, lowercase slug: for example,
   `articles/why-rag-retrieval-fails/`.
3. Copy the matching [article](templates/article.md) or [guide](templates/guide.md)
   template into the new folder as `README.md`.
4. Fill in the metadata and replace the outline with your content. Delete
   sections that do not help the reader.
5. Add images under that piece's `assets/` folder and runnable examples under
   `examples/`, when needed. Use relative links such as `assets/retrieval-flow.svg`.
6. Add the title and relative link to the format index and the table above when
   the piece is ready for readers.

For example, a future article can contain:

```text
articles/why-rag-retrieval-fails/
├── README.md
├── assets/
│   └── retrieval-flow.svg
└── examples/
    └── retrieval-example.py
```

Create asset and example folders only when they contain files.

## Editorial conventions

- Keep a single source per piece. Change `status` from `draft` to `review` to
  `published` in the template metadata; keep the same folder throughout.
- Use `type: blog`, `type: technical-article`, or `type: guide`. Use `tags` for
  subjects such as RAG, evaluation, agents, or deployment.
- Set `published` when the piece first becomes public and `updated` when making
  a substantive revision. Use ISO dates (`YYYY-MM-DD`); leave unknown dates null.
- Keep the slug stable after sharing its link. Put revisions in the same source
  rather than creating `final`, `v2`, or duplicate published copies.
- Record external publication links in `canonical_url` once available. Leave it
  null while writing locally.
- The existing FDE guide retains its original text and headings; metadata is
  optional for existing material.

## Website rendering

The FDE reader uses the guide source in this library. Its existing
`#end-to-end-fde-learning-map` anchor stays the same. See
[website instructions](../docs/README.md) for preview and deployment details.

Adding an entry to this library makes it browsable as repository Markdown.
Additional pieces need a reader page or site integration to appear on the website.

Use [Foundations](../foundations/README.md) for concept reference notes and
[Career](../career/README.md) for career tools and GPT configuration.
