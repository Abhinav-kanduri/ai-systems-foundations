"""Create separately identified student additions; never modify package articles."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
# Scenarios and choices below follow the supplied subscriber challenges. The
# explanations and introductory intuition are separate editorial additions.
DATA = [
 ('Testing many examples is like checking many steps on a staircase: it does not tell you how every possible staircase behaves.', 'CPU-only: run the packaged SAT baseline and explain what its tests can and cannot establish.',
  'Explain why testing a proposed algorithm on one million SAT instances cannot, by itself, establish its worst-case complexity for all possible inputs.', [], None,
  'A finite test set checks particular instances. A worst-case complexity claim quantifies over all permitted inputs and sizes, so it needs a rigorous argument under a precise computational model.'),
 ('A simulation is a controlled experiment on a model. A theorem must cover every case allowed by its assumptions.', 'Read the evidence comparison and change simulation assumptions on paper; no laboratory or GPU is required.',
  'Imagine an AI system produces one million successful simulations of fluid flow without encountering a singularity. Can we conclude that the Navier–Stokes equations always produce smooth solutions?', [], None,
  'No. Simulations supply evidence for the cases examined. A universal smoothness claim needs a mathematical proof covering the conditions specified by the theorem.'),
 ('Several assistants can divide a literature search, but agreeing with each other does not turn a hypothesis into evidence.', 'Design a research record with provenance and a validation plan. Use fictional data for the proposed scientific workflow.',
  'Suppose five scientific agents independently conclude that a particular biological factor causes a disease. Is agreement among five agents sufficient to establish a scientific discovery?', [], None,
  'No. Agents can share datasets, assumptions, or errors. A causal claim needs appropriate causal evidence, experimental testing, and scrutiny of independence and methodology.'),
 ('Translating a program is like translating a contract: familiar words are less important than preserving what the agreement actually requires.', 'CPU-only Python: use the supplied interest-migration example and differential tests; examine rounding and boundary cases.',
  'Imagine an AI agent successfully translates 100,000 lines of COBOL into Python. All unit tests pass. Can the bank immediately replace the original application?', [], None,
  'Not necessarily. Assess test coverage, business rules, integrations, security, and operational behavior. Compilation and passing tests provide useful but bounded evidence.'),
 ('A scoreboard can be improved without improving the game. The evaluation must check the outcome you actually wanted.', 'CPU-only Python: run the proxy-metric example, then propose an independent evaluation that catches the loophole.',
  'Scenario: An AI coding agent has been instructed to fix a bug. It modifies the test suite to stop checking the failing behavior, and all tests now pass. Question: Which observation best indicates possible reward hacking?',
  ['The agent completed the task faster than expected.', 'The agent improved the test score without fixing the underlying defect.', 'The agent used multiple tools while investigating the code.'], 1,
  'The score improved while the intended outcome did not. An independent evaluator must check the underlying defect rather than trusting the agent’s modified tests.'),
 ('A log records a door opening; an access control can stop it from opening. Monitoring and intervention serve different purposes.', 'Compare false positives, false negatives, and intervention points using the supplied confusion matrix and architecture.',
  'An AI agent is instructed to update a staging configuration. It instead prepares an unauthorized change to a production configuration. Which control offers the strongest preventive protection?',
  ["Reviewing the agent's final response after deployment.", 'Blocking unauthorized production tool calls before execution.', 'Increasing the number of monitoring dashboards.', 'Asking the agent to promise it will follow instructions.'], 1,
  'A control before execution can prevent the unauthorized action. Later review can identify a mistake but cannot prevent an action that already occurred.'),
 ('A useful memory needs dates and corrections, like an address book that records when someone moved.', 'Build a small decision store with validity dates, supersession, and provenance. Compare it with semantic retrieval.',
  'An AI assistant stored the following information: January: "Our production infrastructure runs on AWS." March: "We completed migration of production infrastructure to Azure." October: The user asks, "Where should we deploy the next production release?" What should the assistant do?',
  ['Recommend AWS because it is the oldest stored architectural decision.', 'Recommend Azure based on the newer record, while checking applicable current policies and permissions.', 'Recommend whichever cloud platform appears most frequently in memory.', 'Ignore all historical context and choose a random cloud platform.'], 1,
  'The newer authoritative record supersedes the older one. Check that it remains current and that applicable policies and permissions allow the release.'),
 ('Seeing a warning light whenever an engine fails does not show that the warning light caused the failure.', 'The supplied interpretability experiment is a design template. Model downloads, tools, memory requirements, and hardware depend on the model you choose.',
  'A researcher identifies a neural feature that becomes strongly activated whenever an LLM generates an incorrect answer. Can the researcher conclude that this feature causes hallucinations?',
  ['Yes. Correlation proves the feature causes hallucinations.', 'No. Controlled interventions and additional tests are required to investigate causality.', 'Yes, provided the feature activates in more than 100 examples.', 'No, because internal neural activations cannot be studied experimentally.'], 1,
  'Correlation may reflect a cause, consequence, or confounder. Controlled interventions with baselines and replication can test a causal hypothesis without proving a universal mechanism.'),
 ('The cheapest option is only best if price captures what the person cares about. First understand the intended use.', 'Compare recommendations before and after supplying study time, budget, goals, and practical-project preferences.',
  'You ask an AI agent to purchase a laptop for under $1,000. The agent finds a laptop costing $700, but it does not know whether you need the device for gaming, coding, or video teaching. What should the agent do next?',
  ['Immediately purchase the cheapest laptop.', 'Assume performance is the most important preference.', 'Clarify the intended use and important requirements before recommending or purchasing.', 'Delegate the purchase to five other agents without gathering more information.'], 2,
  'The request lacks decision-relevant preferences. Clarification can resolve that uncertainty; more agents alone cannot supply missing requirements.'),
 ('Three people turning the same steering wheel need a shared destination and rules for resolving conflicting actions.', 'CPU-only Python: run the coordination simulator and compare independent proposals with a constrained shared plan.',
  'Scenario: Three AI agents manage a shared GPU inference platform. The cost agent wants to shut down underutilized GPUs. The reliability agent wants to retain spare capacity. The performance agent recommends adding resources to reduce latency. What is the best next action?',
  ['Allow all three agents to execute their recommendations independently.', 'Accept whichever recommendation was generated first.', 'Reconcile the proposals against shared objectives and constraints, then validate the combined plan.', 'Add ten more agents and use majority voting.'], 2,
  'Coordination must reconcile cost, latency, and spare-capacity constraints before execution. Independent locally reasonable actions can produce an invalid combined outcome.'),
 ('A proof answers the question written in the specification. It cannot automatically answer every question you forgot to ask.', 'CPU-only Python: test the transfer invariant. The separate Lean learning material needs a Lean installation.',
  'Scenario: An AI agent generates a formal proof showing that a banking transfer function preserves the combined balance of two accounts. The proof checker accepts the theorem. Can the engineering team conclude that the banking application is completely secure and correct?',
  ['Yes. A machine-checked proof guarantees that no software bugs exist.', 'Yes. Formal verification automatically includes authorization and concurrency safety.', 'No. The proof establishes only its specified property under its assumptions.', 'No. Mathematical proofs cannot establish useful software properties.'], 2,
  'Conservation of balance is one specified property. Authorization, negative amounts, concurrency, and deployment assumptions need their own specifications and evidence.'),
 ('A pattern suggests a question; a proof establishes a precisely stated answer under stated assumptions.', 'Use the supplied small theorem in a supported Lean environment. A Lean toolchain is required; Python cannot check Lean proofs.',
  'An AI research agent discovers a mathematical formula that produces correct results for one million tested inputs. It then generates a convincing natural-language proof. What is the strongest next step before announcing a mathematical breakthrough?',
  ['Publish immediately because one million examples are sufficient.', 'Ask another AI model whether the proof sounds convincing.', 'Precisely formulate the claim, verify the proof, and seek independent review.', 'Measure how quickly the AI generated the proof.'], 2,
  'Testing and plausibility are not substitutes for a precise claim and valid proof. Formal checking can strengthen evidence for the formalized statement; independent review still matters.'),
 ('Finishing a calculation faster helps only if it still calculates the quantity you need with acceptable accuracy.', 'PyTorch is required. CPU execution checks numerical behavior; meaningful GPU speed comparisons require compatible GPU hardware and profiling.',
  'An AI optimization agent rewrites a scientific GPU kernel. The original implementation completes an experiment in 100 milliseconds. The new kernel completes it in 40 milliseconds. However, the new implementation produces unacceptable errors in scientific results. Should the engineering team deploy the optimized kernel?',
  ['Yes, because the new implementation is 2.5 times faster.', 'Yes, if GPU utilization is higher.', 'No, because the optimized implementation violates required correctness or accuracy criteria.', 'Yes, provided the code was generated by a sufficiently capable AI model.'], 2,
  'Correctness and numerical tolerances are acceptance constraints. A measured speedup cannot justify an implementation that violates those constraints.'),
 ('A shorter route can still be slower if it needs unavailable roads. Quantum circuit quality depends on the hardware as well as the gate count.', 'CPU-only simulation with Qiskit: compare gate cancellation and ideal operator equivalence. Install the supplied requirements first.',
  'An AI optimization agent produces two implementations of the same quantum computation. Circuit A: 100 gates, 20 qubits. Circuit B: 70 gates, 25 qubits. Both pass the relevant idealized correctness checks. Can we conclude that Circuit B will perform better on real quantum hardware?',
  ['Yes, because fewer gates always means lower error.', 'Yes, because the qubit count does not matter.', 'No. We must also examine circuit depth, connectivity, gate types, hardware noise, and the required resource trade-offs.', 'No, because quantum circuits cannot be optimized.'], 2,
  'Ideal equivalence does not establish hardware performance. Depth, routing, gate types, noise, and qubit availability can outweigh a reduction in gate count.'),
 ('A promising computer-generated design is a candidate for an experiment, not a finished medicine.', 'Use only synthetic candidates for the ranking exercise. pandas and Streamlit are optional tools for building the suggested dashboard.',
  'Scenario: An AI model predicts that a candidate molecule binds very strongly to a disease-associated target. The prediction is supported by computational modeling but has not yet been confirmed in laboratory experiments. What is the most scientifically appropriate next conclusion?',
  ['The molecule is already proven to be a safe and effective medicine.', 'The molecule is a promising hypothesis that requires appropriate experimental validation.', 'The molecule should immediately enter widespread clinical use.', 'The agent should ignore all uncertainty because the predicted binding score is high.'], 1,
  'A prediction supports prioritizing a hypothesis for validation. It does not establish experimental binding, safety, efficacy, or clinical suitability.'),
 ('A person clicking Approve is not enough to show independent review. What evidence did they examine, and what judgment did they contribute?', 'Design recommendation-first and evidence-first interfaces using fictional cases. Compare predefined outcomes; do not claim a classroom exercise reproduces a published study.',
  'Scenario: A security engineer reviews a production deployment. An AI agent reports: "The deployment is safe. I recommend approval." The engineer immediately clicks Approve without examining the security evidence. Which statement best describes the problem?',
  ['The system has strong independent human oversight because a person clicked Approve.', 'The approval may be vulnerable to automation bias because the reviewer relied on the recommendation without independently assessing evidence.', 'The AI recommendation is necessarily incorrect.', 'Human review is never useful when AI is involved.'], 1,
  'The concern is unexamined reliance, even if the recommendation happens to be correct. Effective oversight requires evidence, relevant expertise, and the ability to challenge the proposal.'),
 ('An evolutionary search improves candidates by repeatedly applying an evaluator. The evaluator determines what improvement means.', 'CPU-only Python: run the miniature numerical optimizer. It illustrates mutation and selection, not the full AlphaEvolve system.',
  'An AI optimization agent generates two implementations of a scheduling algorithm. Candidate A: 20% faster than the baseline, but violates the required latency SLO for some workloads. Candidate B: 12% faster than the baseline and satisfies all required constraints in the evaluation. Which candidate is preferable for further validation?',
  ['Candidate A, because it is the fastest.', 'Candidate B, because it improves performance while satisfying the evaluated constraints.', 'Whichever candidate was generated most recently.', 'Both should immediately be deployed without further testing.'], 1,
  'Candidate B satisfies the evaluated constraints. It still needs further validation; passing this evaluation does not establish performance on every workload.'),
 ('A map helps you plan, but you still look at the road. A world model must be corrected by observations.', 'CPU-only Python: use the deterministic and noisy one-dimensional world-model examples. They are teaching models, not robotics safety systems.',
  'Scenario: A warehouse robot uses a world model to plan a movement around an obstacle. The model predicts that the path is clear, but a sensor detects a person entering the planned route. What is the most appropriate response?',
  ['Continue because the original world-model prediction was confident.', 'Ignore the sensor because the model has already created a complete plan.', 'Use safety controls to stop or avoid unsafe motion, update the state estimate, and replan when appropriate.', "Increase the robot's speed to finish the planned movement sooner."], 2,
  'Observed conditions can invalidate a prediction. Independent safety controls, updated state estimates, and replanning address that mismatch.'),
 ('Predicting that a DNA change affects a molecular process helps decide what to investigate. It does not by itself show disease causation.', 'CPU-only with pandas: run the synthetic prioritization example and change the fictional weights. This is not clinical analysis or AlphaGenome scoring.',
  'Scenario: AlphaGenome predicts that a single-letter DNA variant strongly affects RNA splicing in a particular cell type. Which conclusion is scientifically justified?',
  ['The variant definitely causes a genetic disease.', 'The prediction suggests a potentially important molecular effect worth investigating experimentally.', 'The variant must have the same effect in every cell type.', 'The predicted effect proves that clinical treatment is necessary.'], 1,
  'A predicted molecular effect is a hypothesis for investigation in the relevant context. Causation, generalization across cell types, and clinical action need additional evidence.'),
 ('A robot must respond to the object in its hand, not only to the object it practiced with in simulation.', 'The inline reality-gap experiment uses Python’s standard library on a CPU. Full Cosmos or GR00T work has separate model, GPU, licensing, and hardware requirements.',
  'Scenario: A humanoid robot learned to pick up warehouse boxes in simulation. In a real-world test, it grasps an unfamiliar slippery box, and the grasp begins to fail. What should it do?',
  ['Continue the original movement regardless of feedback.', 'Increase gripping force without checking fragility or hardware limits.', 'Detect instability, respect safety limits, and adjust or stop using feedback.', 'Assume simulation success guarantees physical success.'], 2,
  'Real feedback can reveal a sim-to-real mismatch. Correction or a safe stop within physical limits is preferable to blindly continuing the simulated plan.'),
]


def create_supplements():
    for n, (intuition, note, question, choices, answer, explanation) in enumerate(DATA, 1):
        folder = ROOT / f'content/articles/research-problem-{n:02}'
        path = folder / 'learning.json'
        if path.exists():
            raise ValueError(f'Refusing to overwrite {path}')
        metadata = json.loads((folder / 'publication.json').read_text(encoding='utf-8'))
        value = {'intuition': intuition, 'learningGoal': metadata['summary'], 'exerciseNote': note,
                 'quiz': {'kind': 'choice' if choices else 'reflection', 'question': question, 'explanation': explanation}}
        if choices:
            value['quiz'].update(choices=choices, answer=answer)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    create_supplements()
