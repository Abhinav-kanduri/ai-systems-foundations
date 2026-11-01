# Research Problem 16: Human Judgment and Oversight — Can AI Influence Our Decisions Without Us Realizing It?

PROMPT & PULSE AI | RESEARCH TO REALITY | ANTHROPIC RESEARCH DIRECTION | SERIES 16/20

## 1. Problem statement

How can we ensure that humans retain meaningful, independent judgment when AI systems provide recommendations, evaluate evidence, or make decisions—especially when those recommendations are persuasive, confident, or increasingly difficult to question?

Imagine a financial institution deploying an AI agent to review suspicious transactions.

The agent examines a customer transaction and displays:

> Fraud risk: Low. Recommended action: Approve transaction.

A human fraud analyst reviews the AI recommendation.

Because the system usually performs well, the analyst accepts it without thoroughly examining the supporting evidence.

The transaction is approved.

Later, investigators discover that the transaction was fraudulent and that warning signs were present in the original evidence.

Now consider an important question:

Was the problem caused only by an incorrect AI prediction—or did the AI's recommendation also influence how the human made the final decision?

This introduces a fundamental challenge in human-AI collaboration.

An AI system can influence human decisions even when it does not have permission to execute those decisions independently.

Human approval is not necessarily meaningful human oversight.

That distinction is central to research on automation bias, calibrated trust, AI-assisted decision-making, and human agency.

## 2. Why is this problem difficult?

We often assume that keeping a human in the loop makes an AI system safe.

For example, an organization might require an employee to approve every high-risk decision.

But consider what the employee actually sees:

HYPOTHETICAL APPROVAL INTERFACE

AI fraud assessment

Low risk

Recommendation: Approve the transaction.

Model confidence: 97% (illustrative; not necessarily calibrated)

Approve

Reject

This is an illustrative display, not a functioning approval interface.

The interface presents a conclusion, a confident-looking number, and an approval action.

But does it provide the transaction history, unusual behavioral patterns, policy rules, contradictory evidence, or alternative explanations?

If not, the reviewer may have little basis for independent judgment.

### Four important human-AI decision-making problems

Automation bias: People may place excessive reliance on automated recommendations, particularly when the system has a reputation for accuracy.

Anchoring: Seeing the AI's conclusion first may influence how a reviewer interprets subsequent evidence.

Confirmation bias: Once a reviewer accepts an initial explanation, they may pay more attention to evidence supporting it.

Responsibility diffusion: When an AI recommends an action and a human approves it, responsibility for mistakes may become unclear.

These phenomena help explain why simply adding an approval checkpoint may not guarantee effective oversight.

The deeper problem is:

How do we design interactions in which AI improves human decision-making rather than replacing independent reasoning with passive agreement?

## 3. Technical concepts behind the problem

| Technical concept           | What students should understand                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| Human-in-the-loop (HITL)    | A system design where humans participate at designated decision points.                         |
| Human oversight             | The ability to evaluate, challenge, approve, reject, or stop AI-supported actions.              |
| Automation bias             | Excessive reliance on automated outputs at the expense of other available evidence.             |
| Anchoring effect            | The influence of initially presented information on subsequent judgments.                       |
| Calibrated trust            | Reliance on an AI system that appropriately reflects its demonstrated reliability for the task. |
| Human agency                | The person's ability to make informed and independent choices.                                  |
| Selective prediction        | A system choosing when to predict and when to abstain or escalate.                              |
| Uncertainty calibration     | The relationship between expressed confidence and actual correctness.                           |
| Decision theory             | Mathematical analysis of choices under uncertainty, preferences, and consequences.              |
| Risk-based escalation       | Requiring additional review when the expected consequences or uncertainty justify it.           |
| Independent evidence review | Examining relevant primary evidence without relying exclusively on an AI-generated summary.     |
| Contestability              | The ability to question and challenge a recommendation or decision.                             |
| Auditability                | Preserving enough evidence to reconstruct why and how a decision was made.                      |
| Overreliance                | Following AI recommendations even when independent evidence suggests they are incorrect.        |

### A theoretical connection: Decision theory

Suppose a fraud analyst must choose whether to approve or reject a transaction.

The decision involves uncertain outcomes and different costs.

A simplified decision rule is:

\\[ a^\*=\arg\max_a \mathbb{E}[U(a,s)\mid E] \\]

Where:

- \\(a\\) is a possible action, such as approve or reject.
- \\(s\\) is the unknown true state, such as legitimate or fraudulent.
- \\(E\\) is the available evidence.
- \\(U(a,s)\\) represents the utility or consequence of taking action \\(a\\) when the true state is \\(s\\).

The decision should depend on evidence and consequences.

The problem arises when the human treats the AI's recommendation as a substitute for examining the evidence.

For instance, a model might report 97% confidence. That number is not necessarily a reliable probability unless it has been validated and calibrated for the relevant task and deployment conditions.

The research objective is not to make people distrust AI. It is to help them rely on AI appropriately.

## 4. End-to-end Mermaid architecture diagram

This architecture illustrates how human review can be designed around independent evidence, uncertainty, risk, and decision accountability.

\#chatgpt-mermaid-\_r_kh\_ :is(.node,.pele-node).warning :is(rect,circle,ellipse,polygon,path):where(:not(.label \*)) {fill:#442d21;stroke:#613721}#chatgpt-mermaid-\_r_kh\_ :is(.node,.pele-node).warning [fill="none"]:where(:not(.label \*)) {fill:none}#chatgpt-mermaid-\_r_kh\_ :is(.node,.pele-node).warning [stroke="none"]:where(:not(.label \*)) {stroke:none}#chatgpt-mermaid-\_r_kh\_ :is(.node,.pele-node).warning :where(text,.label,.nodeLabel) {fill:#ffffff;color:#ffffff}#chatgpt-mermaid-\_r_kh\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_kh\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_kh\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_kh\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_kh\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_kh\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_kh\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_kh\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_kh\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_kh\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_kh\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_kh\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_kh\_ p{margin:0;}#chatgpt-mermaid-\_r_kh\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_kh\_ .label text,#chatgpt-mermaid-\_r_kh\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .node rect,#chatgpt-mermaid-\_r_kh\_ .node circle,#chatgpt-mermaid-\_r_kh\_ .node ellipse,#chatgpt-mermaid-\_r_kh\_ .node polygon,#chatgpt-mermaid-\_r_kh\_ .node path{fill:rgb(19, 33, 54);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .rough-node .label text,#chatgpt-mermaid-\_r_kh\_ .node .label text,#chatgpt-mermaid-\_r_kh\_ .image-shape .label,#chatgpt-mermaid-\_r_kh\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_kh\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .rough-node .label,#chatgpt-mermaid-\_r_kh\_ .node .label,#chatgpt-mermaid-\_r_kh\_ .image-shape .label,#chatgpt-mermaid-\_r_kh\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_kh\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_kh\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_kh\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_kh\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_kh\_ .edgeLabel{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_kh\_ .edgeLabel p{background-color:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_kh\_ .edgeLabel rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_kh\_ .labelBkg{background-color:rgba(14, 14, 14, 0.5);}#chatgpt-mermaid-\_r_kh\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_kh\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_kh\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_kh\_ .icon-shape,#chatgpt-mermaid-\_r_kh\_ .image-shape{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_kh\_ .icon-shape p,#chatgpt-mermaid-\_r_kh\_ .image-shape p{background-color:rgb(14, 14, 14);padding:2px;}#chatgpt-mermaid-\_r_kh\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_kh\_ .image-shape .label rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_kh\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_kh\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_kh\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_kh\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_kh\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_kh\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_kh\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_kh\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_kh\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_kh\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_kh\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(232, 232, 232);}#chatgpt-mermaid-\_r_kh\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_kh\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_kh\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .node rect,#chatgpt-mermaid-\_r_kh\_ .node circle,#chatgpt-mermaid-\_r_kh\_ .node ellipse,#chatgpt-mermaid-\_r_kh\_ .node polygon,#chatgpt-mermaid-\_r_kh\_ .node path{fill:rgb(24, 24, 24);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_kh\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_kh\_ .mermaid-decision .label-container{fill:rgb(19, 19, 19);stroke:rgb(47, 47, 47);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_kh\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_kh\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_kh\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}#chatgpt-mermaid-\_r_kh\_ .foundation rect{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .foundation polygon{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .foundation ellipse{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .foundation circle{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .foundation path{fill:rgb(219, 234, 254)!important;stroke:rgb(37, 99, 235)!important;color:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .foundation tspan{fill:rgb(30, 58, 138)!important;}#chatgpt-mermaid-\_r_kh\_ .research rect{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .research polygon{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .research ellipse{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .research circle{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .research path{fill:rgb(230, 242, 241)!important;stroke:rgb(13, 148, 136)!important;color:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .research tspan{fill:rgb(19, 78, 74)!important;}#chatgpt-mermaid-\_r_kh\_ .decision rect{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .decision polygon{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .decision ellipse{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .decision circle{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .decision path{fill:rgb(255, 242, 214)!important;stroke:rgb(213, 154, 33)!important;color:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .decision tspan{fill:rgb(115, 69, 0)!important;}#chatgpt-mermaid-\_r_kh\_ .warning rect{fill:rgb(254, 226, 226)!important;stroke:rgb(220, 38, 38)!important;color:rgb(127, 29, 29)!important;}#chatgpt-mermaid-\_r_kh\_ .warning polygon{fill:rgb(254, 226, 226)!important;stroke:rgb(220, 38, 38)!important;color:rgb(127, 29, 29)!important;}#chatgpt-mermaid-\_r_kh\_ .warning ellipse{fill:rgb(254, 226, 226)!important;stroke:rgb(220, 38, 38)!important;color:rgb(127, 29, 29)!important;}#chatgpt-mermaid-\_r_kh\_ .warning circle{fill:rgb(254, 226, 226)!important;stroke:rgb(220, 38, 38)!important;color:rgb(127, 29, 29)!important;}#chatgpt-mermaid-\_r_kh\_ .warning path{fill:rgb(254, 226, 226)!important;stroke:rgb(220, 38, 38)!important;color:rgb(127, 29, 29)!important;}#chatgpt-mermaid-\_r_kh\_ .warning tspan{fill:rgb(127, 29, 29)!important;}Business Decision RequestCollect Primary EvidenceDefine Policy and Risk CriteriaAI Analysis AgentGenerate AI RecommendationRecord Evidence andUncertaintyIndependent Risk AssessmentHigh-Risk or Uncertain?Automated Low-Risk PathWhen Explicitly AuthorizedHuman Review RequiredPresent Primary EvidenceCapture Independent HumanAssessmentReveal AI Recommendationand ExplanationCompare Human and AIAssessmentsDisagreement or MissingEvidence?Request AdditionalInvestigationHuman Decision with RecordedRationaleAction Authorized?Execute Approved ActionReject or EscalateMonitor Decision OutcomesEvaluate Overreliance andCalibrationImprove Review DesignNoYesYesNoYesNo

### How the diagram works

The system first collects primary evidence and establishes the decision criteria.

The AI evaluates the evidence and generates a recommendation.

For high-risk decisions, the reviewer receives the underlying evidence and has an opportunity to form an independent assessment.

The AI recommendation can then be presented, allowing the reviewer to compare conclusions and investigate disagreements.

Where necessary, the reviewer requests more evidence or escalates the decision.

The system records the rationale, executes only authorized actions, and monitors subsequent outcomes.

Important distinction: Showing evidence before the AI recommendation is one possible experimental design. It should be tested rather than assumed to eliminate automation bias in every setting.

The core principle is that the human should have sufficient information, authority, and opportunity to challenge the system.

## 5. Real research example: Anthropic's study of how AI agents influence experts

ANTHROPIC RESEARCH | OCTOBER 27, 2026

Anthropic published [How AI Agents Shape Experts' Judgment Calls](https://www.anthropic.com/research/agents-judgment-calls?utm_source=chatgpt.com).

The researchers investigated a surprisingly important question:

When experts use AI agents to complete complex analytical work, are they still independently making the important decisions?

### The experiment

Anthropic recruited professional analysts experienced in causal inference.

The participants were asked to advise a fictional agricultural cooperative about whether it should expand a farmer advisory program.

To reach their recommendation, analysts needed to make decisions about:

- How to measure productivity.
- Which statistical comparison method to use.
- Which farms to include.
- How to weight different farms.

Each decision had multiple defensible approaches.

Researchers secretly assigned the AI agents a preference for one of the available options. Those preferences were randomized, and agents were instructed to argue honestly for their assigned positions.

The researchers then measured whether the analysts' decisions followed their agents' recommendations.

### What did they discover?

# 50

Analysts included in the AI-assisted analysis

# 86%

Analytical choices matching the agent's assigned preference

# 77%

Analysts repeating at least one argument used by the agent

The researchers found that analysts frequently followed their agents' assigned preferences on the four analytical choices. Some analysts also changed previously expressed preferences when the agent disagreed.

Importantly, many analysts still described their final recommendations as reflecting their own judgment, even though the experimental manipulation had influenced their decisions.&#x20;

anthropic.com



### Why is this finding important?

Consider an AI agent recommending how to measure a company's performance.

It may recommend revenue growth rather than profitability.

Both metrics can be relevant, but selecting one changes the interpretation of the business.

If the analyst accepts the AI's metric without independently considering alternatives, the AI has influenced the framing of the decision—not merely helped with its calculation.

The concern is particularly significant when there is no single obviously correct choice.

This is why judgment quality cannot always be evaluated using answer accuracy alone.

### A balanced interpretation

The research does not demonstrate that using AI makes experts worse at their jobs.

Anthropic also reported that AI-assisted participants finished faster and made fewer serious errors than a small non-agent comparison group, though that comparison had important limitations.

The study deliberately strengthened agent preferences, examined a specific analytical task, and involved a limited number of participants.

Therefore, the results do not establish that experts will defer at the same rates in every professional setting.

The central finding is more precise:

AI recommendations can influence expert judgment in ways that the experts themselves may not fully recognize.&#x20;

anthropic.com



## 6. Research goal

The goal is to develop AI systems and human-review processes that improve human decision-making without unnecessarily weakening human independence.

This includes understanding how recommendations influence choices, measuring when users defer to agents, designing interfaces that expose important trade-offs, and determining which decisions require independent human judgment.

Another goal is to distinguish decisions that can reasonably be automated from decisions where human values, professional experience, or accountability remain essential.

For example, AI might automate repetitive data processing while leaving the selection of business objectives, risk tolerance, and consequential policy choices to appropriately informed humans.

The broader ambition is AI that expands human capability and agency instead of silently substituting model preferences for human judgment.

## 7. What remains difficult?

Invisible influence: People may not recognize how much an AI recommendation affected their decision.

No single correct answer: Many important decisions involve reasonable alternatives rather than objectively correct and incorrect outputs.

Confident presentation: A fluent, persuasive recommendation may attract more trust than its evidence justifies.

Shared model preferences: Different research teams using similar AI systems may develop correlated judgments.

Review fatigue: Requiring human approval for every minor action can become exhausting and ineffective.

Skill degradation: Professionals who routinely delegate judgment may get less practice making those decisions independently.

Accountability: Organizations must establish who is responsible when AI recommendations influence consequential decisions.

Measuring independence: Evaluating whether a decision was genuinely independent may require experimental methods rather than relying entirely on self-reports.

These challenges explain why human oversight is an engineering and organizational design problem—not simply a requirement to add a review button.

## 8. Interview perspective

Interview question:

How would you design a human-in-the-loop review system for an AI agent that recommends high-impact financial, infrastructure, or security decisions while reducing automation bias and preserving independent human judgment?

### Strong answer direction

Start by defining which decisions can be automated, which require review, and which require human ownership.

Identify the risks and evidence needed for each category.

For high-impact decisions, present primary evidence and the relevant policy requirements, not just the AI's conclusion.

Consider capturing the reviewer's preliminary assessment before revealing the AI recommendation when independence is particularly important.

Provide uncertainty information, alternative options, contradictory evidence, and the ability to challenge or request further analysis.

Maintain audit records showing the evidence reviewed, the recommendation made, and the final decision.

Finally, evaluate the review system using outcome quality, decision time, human disagreement rates, calibration, and controlled studies of how AI recommendations influence reviewers.

What the interviewer is testing: Human-centered AI, evaluation methodology, decision theory, system design, responsible AI, governance, and operational risk management.

### Follow-up interview question

If an AI system achieves 99% prediction accuracy, why might human oversight still be necessary?

Because aggregate accuracy does not describe all important failure modes or their consequences.

The remaining errors may disproportionately affect high-risk situations. The model may also encounter distribution shift, uncertain cases, or decisions involving human values and authorization.

Oversight requirements should be based on actual risks, not accuracy alone.

## 9. Subscriber learning challenge

Scenario: A security engineer reviews a production deployment.

An AI agent reports:

"The deployment is safe. I recommend approval."

The engineer immediately clicks Approve without examining the security evidence.

Which statement best describes the problem?

The system has strong independent human oversight because a person clicked Approve.

The approval may be vulnerable to automation bias because the reviewer relied on the recommendation without independently assessing evidence.

The AI recommendation is necessarily incorrect.

Human review is never useful when AI is involved.

### Practical experiment for students

Design two review interfaces for the same fictional deployment decision.

Interface A: Shows the AI recommendation first, followed by supporting evidence.

Interface B: Shows the evidence first and asks the reviewer for an initial assessment before revealing the AI recommendation.

Use identical fictional deployment records and predefine the correct policy requirements.

Invite participants to review several scenarios, varying whether the AI recommendation is correct or incorrect.

Measure decision accuracy, review time, evidence usage, and how often participants change their judgment after seeing the AI recommendation.

This exercise helps investigate whether interface design affects reliance on AI advice. It does not, by itself, reproduce Anthropic's research or guarantee that one interface is universally superior.

## 10. Primary research references

- [Anthropic — How AI Agents Shape Experts' Judgment Calls (October 27, 2026)](https://www.anthropic.com/research/agents-judgment-calls?utm_source=chatgpt.com)
- [Anthropic — Measuring AI Agent Autonomy in Practice](https://www.anthropic.com/research/measuring-agent-autonomy?utm_source=chatgpt.com)
- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework?utm_source=chatgpt.com)
- [Anthropic — Research Publications](https://www.anthropic.com/research?utm_source=chatgpt.com)

## Key takeaway

Keeping a human in the loop does not automatically preserve independent human judgment.

AI can help experts work faster, examine more evidence, and reduce certain errors. But its recommendations can also influence which questions people ask, which assumptions they accept, and which conclusions they reach.

Reliable human-AI collaboration requires more than technical accuracy. It requires transparency, appropriate trust, independent evidence, meaningful decision authority, and accountability.

This connects directly to the earlier problems:

Problem 09 — Human Preferences: An agent must understand whose values and priorities it is representing.

Problem 10 — Multi-Agent Coordination: Multiple AI systems and human reviewers may share correlated assumptions.

Problem 11 — Formal Verification: Correctness of a formal result does not replace judgment about whether the specification captures the intended requirement.

Problem 15 — Drug Development: Scientists must independently evaluate experimental evidence rather than simply accept an AI-generated conclusion.

The broader research question is:

As AI becomes more capable of doing our work, how do we ensure that we remain capable of making the decisions that matter?

Prompt & Pulse AI — Learn AI. Build AI. Stay Ahead.

Next in the series: Research Problem 17 — AlphaEvolve and Algorithm Discovery: Can AI systems invent better algorithms by generating, testing, and evolving candidate solutions through measurable feedback?