# Research Problem 01: Mathematical Discovery and Computational Complexity

PROMPT & PULSE AI | RESEARCH TO REALITY | OPENAI RESEARCH DIRECTION

## 1. Problem statement

Can artificial intelligence discover better algorithms for computational problems that appear to require exponentially growing amounts of computation, and can those discoveries be mathematically verified?

Some problems are easy to verify once a solution is given, but extremely difficult to solve as the number of possible combinations grows.

For example, imagine a scheduling system trying to find a valid assignment for hundreds of interconnected tasks. As the number of constraints increases, exploring every possible combination may become computationally infeasible.

The central research challenge is whether AI can discover mathematical structures or algorithms that reduce the computational work required.

## 2. Concepts behind the problem

| Concept                  | Explanation                                                                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Computational complexity | Studies how computation time and memory requirements grow with input size.                                     |
| P versus NP              | Asks whether every problem whose proposed solution can be efficiently verified can also be efficiently solved. |
| SAT / 3-SAT              | Asks whether Boolean variables can be assigned values that satisfy logical constraints.                        |
| Exponential complexity   | Running time that grows rapidly, such as \\(O(2^n)\\).                                                         |
| ETH                      | Hypothesizes that 3-SAT cannot be solved in subexponential time in the number of variables.                    |
| Algorithm discovery      | Searching for new computational methods that solve problems more efficiently.                                  |
| Formal verification      | Using proof assistants, such as Lean, to check mathematical proofs of precisely stated claims.                 |

## 3. Research goal

Develop AI-assisted methods that can propose new algorithms, investigate their complexity, and help produce rigorous mathematical evidence supporting their correctness and performance claims.

The goal is not merely to generate code that runs faster on a few examples. It is to determine whether a method provides a genuine, generalizable algorithmic improvement under clearly defined assumptions.

## 4. End-to-end Mermaid diagram

Copy this Mermaid code into your newsletter documentation, GitHub README, or Mermaid Live Editor.

\#chatgpt-mermaid-\_r_25u\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_25u\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_25u\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_25u\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_25u\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_25u\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_25u\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_25u\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_25u\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_25u\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_25u\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_25u\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_25u\_ p{margin:0;}#chatgpt-mermaid-\_r_25u\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_25u\_ .label text,#chatgpt-mermaid-\_r_25u\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .node rect,#chatgpt-mermaid-\_r_25u\_ .node circle,#chatgpt-mermaid-\_r_25u\_ .node ellipse,#chatgpt-mermaid-\_r_25u\_ .node polygon,#chatgpt-mermaid-\_r_25u\_ .node path{fill:rgb(19, 33, 54);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .rough-node .label text,#chatgpt-mermaid-\_r_25u\_ .node .label text,#chatgpt-mermaid-\_r_25u\_ .image-shape .label,#chatgpt-mermaid-\_r_25u\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_25u\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .rough-node .label,#chatgpt-mermaid-\_r_25u\_ .node .label,#chatgpt-mermaid-\_r_25u\_ .image-shape .label,#chatgpt-mermaid-\_r_25u\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_25u\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_25u\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_25u\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_25u\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_25u\_ .edgeLabel{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_25u\_ .edgeLabel p{background-color:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_25u\_ .edgeLabel rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_25u\_ .labelBkg{background-color:rgba(14, 14, 14, 0.5);}#chatgpt-mermaid-\_r_25u\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_25u\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_25u\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_25u\_ .icon-shape,#chatgpt-mermaid-\_r_25u\_ .image-shape{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_25u\_ .icon-shape p,#chatgpt-mermaid-\_r_25u\_ .image-shape p{background-color:rgb(14, 14, 14);padding:2px;}#chatgpt-mermaid-\_r_25u\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_25u\_ .image-shape .label rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_25u\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_25u\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_25u\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_25u\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_25u\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_25u\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_25u\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_25u\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_25u\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_25u\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_25u\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_25u\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_25u\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_25u\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .node rect,#chatgpt-mermaid-\_r_25u\_ .node circle,#chatgpt-mermaid-\_r_25u\_ .node ellipse,#chatgpt-mermaid-\_r_25u\_ .node polygon,#chatgpt-mermaid-\_r_25u\_ .node path{fill:rgb(24, 24, 24);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_25u\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_25u\_ .mermaid-decision .label-container{fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_25u\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_25u\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_25u\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}#chatgpt-mermaid-\_r_25u\_ .problem rect{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .problem polygon{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .problem ellipse{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .problem circle{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .problem path{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .problem tspan{fill:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_25u\_ .research rect{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .research polygon{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .research ellipse{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .research circle{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .research path{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .research tspan{fill:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_25u\_ .validation rect{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_25u\_ .validation polygon{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_25u\_ .validation ellipse{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_25u\_ .validation circle{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_25u\_ .validation path{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_25u\_ .validation tspan{fill:rgb(115, 69, 0)!important;}Computational ProblemExample: Boolean SatisfiabilityUnderstand the problemVariables, constraints, inputsizeAnalyze existing algorithmsCorrectness and complexityAI-assisted algorithm discoveryGenerate candidate methodsBuild a candidate algorithmTest on small and difficult casesCorrect on tested cases?Reject or revise candidateMathematical complexityanalysisFormulate precise theoremAssumptions and claimedboundsConstruct mathematical proofFormalize in LeanWhere feasibleProof and theorem check?Revise proof or theoremIndependent scientific reviewReproducible algorithmic resultNoYesNoYes

## 5. A simple example: SAT

Consider:

\\[ (x_1\lor x_2)\land(\neg x_1\lor x_3) \\]

The question is: Can we assign true or false values to the variables so that the entire expression is true?

For example, choosing \\(x_1=\text{True}\\), \\(x_2=\text{False}\\), and \\(x_3=\text{True}\\) satisfies the formula.

A straightforward exhaustive approach tries all \\(2^n\\) combinations for \\(n\\) Boolean variables.

How quickly does exhaustive search grow?

Number of variables

## 20

Possible assignments

# 1,048,576

This represents exhaustive enumeration, not the running time of every SAT solver. Modern solvers exploit structure and pruning.

The important research question is whether a proposed method can achieve better asymptotic performance for the general problem, not just for selected examples.

## 6. What is still difficult?

An AI-generated algorithm might appear promising, but researchers must establish that it is correct, clarify its worst-case time complexity, and determine whether any assumptions restrict its applicability.

A Lean-checked proof provides confidence about a formal theorem, but independent reviewers must still check whether that theorem expresses the intended mathematical claim.

Also, refuting ETH would not automatically prove P = NP. ETH concerns a more specific exponential-time hypothesis, whereas P versus NP asks about polynomial-time solvability.

## 7. Interview perspective

Question: Suppose an AI research agent claims to have discovered a subexponential algorithm for 3-SAT. How would you evaluate that claim?

A strong answer would examine the exact algorithm, correctness proof, worst-case complexity, assumptions, input representation, and independent reproducibility. It would also distinguish empirical benchmarks from theoretical complexity guarantees.

Subscriber challenge: Explain why testing a proposed algorithm on one million SAT instances cannot, by itself, establish its worst-case complexity for all possible inputs.

Core takeaway: The breakthrough is not simply getting AI to propose a faster algorithm. It is discovering an improvement that can withstand rigorous mathematical analysis, formal checking where applicable, and independent scientific review.