# Editable diagram sources

Edit `.mmd` files in any Mermaid-compatible editor, or change the Mermaid code directly in `README.md`. GitHub renders the fenced `mermaid` blocks automatically. For custom SVG/PNG illustrations, edit the `.dot` Graphviz sources and regenerate with `dot -Tsvg diagrams/architecture.dot -o assets/architecture.svg` and `dot -Tpng -Gdpi=170 diagrams/architecture.dot -o assets/architecture.png` (repeat for `banking` and `coding`).
