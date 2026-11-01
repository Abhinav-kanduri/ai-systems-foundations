## Research Problem 03: Distributed Scientific Agents

PROMPT & PULSE AI | RESEARCH TO REALITY | OPENAI RESEARCH DIRECTION

### 1. Problem statement

Can multiple AI agents collaborate as scientific researchers to analyze large amounts of information, discover hidden patterns, generate new hypotheses, and help scientists investigate complex problems?

Imagine researchers trying to discover why a particular medical treatment works for some patients but not others.

Relevant information may be spread across thousands of research papers, biological datasets, clinical observations, and experimental reports.

A single researcher—or a single AI agent—may struggle to investigate all these sources thoroughly.

Distributed scientific agents explore a different approach: divide a scientific investigation among specialized AI agents that work together.

### 2. Technical concepts

| Concept                         | What it means                                                           |
| ------------------------------- | ----------------------------------------------------------------------- |
| Multi-agent systems             | Multiple AI agents collaborate on a shared objective.                   |
| Task decomposition              | Breaking a large research problem into smaller investigations.          |
| Scientific literature retrieval | Finding relevant published research and supporting evidence.            |
| Evidence synthesis              | Combining findings from different sources into a coherent explanation.  |
| Hypothesis generation           | Proposing explanations that can be tested scientifically.               |
| Causal inference                | Investigating whether one factor actually causes another.               |
| Provenance                      | Tracking where a finding originated and which evidence supports it.     |
| Agent coordination              | Managing communication, dependencies, and disagreements between agents. |

### 3. Research goal

Develop AI systems that can accelerate scientific investigations by coordinating literature reviews, data analysis, hypothesis generation, and evidence verification.

The goal is to help scientists identify promising discoveries while maintaining scientific rigor and reproducibility.

### 4. End-to-end Mermaid diagram

\#chatgpt-mermaid-\_r_20i\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_20i\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_20i\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_20i\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_20i\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_20i\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_20i\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_20i\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_20i\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_20i\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_20i\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_20i\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_20i\_ p{margin:0;}#chatgpt-mermaid-\_r_20i\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_20i\_ .label text,#chatgpt-mermaid-\_r_20i\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .node rect,#chatgpt-mermaid-\_r_20i\_ .node circle,#chatgpt-mermaid-\_r_20i\_ .node ellipse,#chatgpt-mermaid-\_r_20i\_ .node polygon,#chatgpt-mermaid-\_r_20i\_ .node path{fill:rgb(19, 33, 54);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .rough-node .label text,#chatgpt-mermaid-\_r_20i\_ .node .label text,#chatgpt-mermaid-\_r_20i\_ .image-shape .label,#chatgpt-mermaid-\_r_20i\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_20i\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .rough-node .label,#chatgpt-mermaid-\_r_20i\_ .node .label,#chatgpt-mermaid-\_r_20i\_ .image-shape .label,#chatgpt-mermaid-\_r_20i\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_20i\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_20i\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_20i\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_20i\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_20i\_ .edgeLabel{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_20i\_ .edgeLabel p{background-color:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_20i\_ .edgeLabel rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_20i\_ .labelBkg{background-color:rgba(14, 14, 14, 0.5);}#chatgpt-mermaid-\_r_20i\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_20i\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_20i\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_20i\_ .icon-shape,#chatgpt-mermaid-\_r_20i\_ .image-shape{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_20i\_ .icon-shape p,#chatgpt-mermaid-\_r_20i\_ .image-shape p{background-color:rgb(14, 14, 14);padding:2px;}#chatgpt-mermaid-\_r_20i\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_20i\_ .image-shape .label rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_20i\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_20i\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_20i\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_20i\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_20i\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_20i\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_20i\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_20i\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_20i\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_20i\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_20i\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_20i\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_20i\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_20i\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .node rect,#chatgpt-mermaid-\_r_20i\_ .node circle,#chatgpt-mermaid-\_r_20i\_ .node ellipse,#chatgpt-mermaid-\_r_20i\_ .node polygon,#chatgpt-mermaid-\_r_20i\_ .node path{fill:rgb(24, 24, 24);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_20i\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_20i\_ .mermaid-decision .label-container{fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_20i\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_20i\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_20i\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}#chatgpt-mermaid-\_r_20i\_ .agent rect{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .agent polygon{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .agent ellipse{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .agent circle{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .agent path{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .agent tspan{fill:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_20i\_ .validation rect{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_20i\_ .validation polygon{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_20i\_ .validation ellipse{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_20i\_ .validation circle{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_20i\_ .validation path{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_20i\_ .validation tspan{fill:rgb(115, 69, 0)!important;}Scientific Research QuestionResearch Coordinator AgentLiterature Research AgentData Analysis AgentHypothesis Generation AgentExperimental Design AgentScientific PublicationsResearch DatasetsCandidate HypothesesProposed ExperimentsEvidence SynthesisIndependent Verification AgentEvidence sufficient?Identify gaps and revisehypothesesHuman Scientist ReviewLaboratory or Real-WorldExperimentsEvaluate Experimental ResultsScientific FindingsNoYes for reviewApprovedNew evidence

### 5. Practical example

Suppose a scientific team wants to investigate why a disease progresses faster in certain patients.

The literature agent gathers published findings. The data agent searches for statistical relationships. The hypothesis agent suggests possible biological explanations. The experiment-design agent proposes ways to test them.

A verification agent checks whether the hypotheses are actually supported by the available evidence.

Human scientists then decide which experiments to perform.

The key distinction: AI agents can help discover and prioritize hypotheses, but a plausible explanation is not automatically a scientifically established fact.

### 6. Research challenges

The main difficulties include conflicting evidence, hallucinated citations, correlated agent errors, incorrect causal assumptions, and inefficient collaboration.

For example, three agents agreeing that a particular gene causes a disease does not establish causation if all three relied on the same flawed study.

Independent evidence and experimental validation remain essential.

### 7. Interview perspective

Question: How would you design a multi-agent scientific research platform that generates trustworthy, evidence-backed hypotheses?

A strong answer should explain task decomposition, agent specialization, document retrieval, citation provenance, shared state, independent verification, uncertainty handling, and human experimental approval.

### Subscriber challenge

Suppose five scientific agents independently conclude that a particular biological factor causes a disease.

Is agreement among five agents sufficient to establish a scientific discovery?

No. Their conclusions may share the same data, assumptions, or methodological errors. The hypothesis still requires appropriate causal evidence and experimental testing.

Core takeaway: Distributed scientific agents aim to accelerate the process of scientific discovery, not replace scientific evidence or human validation.

Prompt & Pulse AI — Learn AI. Build AI. Stay Ahead.