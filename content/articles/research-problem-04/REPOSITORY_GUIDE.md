# Repository guide

Upload the contents of this folder (not just README.md) into the root of a GitHub repository. Relative image paths then resolve automatically.

- README.md: full Research Problem 04 learning document, editable embedded Mermaid.
- assets/: real PNG and SVG diagram images plus Prompt & Pulse AI logo.
- diagrams/: standalone Mermaid source (`.mmd`) and Graphviz source (`.dot`).
- examples/ and tests/: small illustrative executable case.

To render Graphviz images, install Graphviz and execute `dot -Tpng diagrams/modernization-workflow.dot -o assets/modernization-workflow.png`. To edit Mermaid use a Mermaid-compatible editor or GitHub's Markdown Mermaid support.
