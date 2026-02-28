Here is a clean, structured **Tokenization.md** file ready to place in your repository.

---

# Tokenization

## 1. Why Tokenization Exists

Large Language Models (LLMs) do not process text.
They process sequences of integers.

Tokenization is the transformation:

```
Human Language → Subword Units → Integer IDs
```

Without tokenization, neural networks cannot operate on text.
Tokenization is the language-to-tensor contract.

---

## 2. Mental Model Reset

### Deterministic Systems

* Same input → Same output
* Rule-based
* Logic-driven

### Probabilistic Systems (LLMs)

* Output is a probability distribution
* Next-token prediction
* Optimized for fluency, not truth

Tokenization defines the discrete symbols over which probability is computed.

---

## 3. What Is a Token?

A token is not necessarily a word.

It can be:

* A whole word
* A subword fragment
* A punctuation mark
* A space
* A special symbol

Example:

```
"Architecting"
```

May become:

```
["Ar", "ch", "ite", "cting"]
```

Then mapped to:

```
[4321, 85, 962, 1442]
```

---

## 4. The Core Mathematical View

Language modeling is:

P(next_token | context)

Where context is a sequence of token IDs:

```
[15496, 995, 318, 257]
```

The tokenizer defines:

* Vocabulary size (|V|)
* Sequence length
* Embedding table size
* Model memory usage

---

## 5. Major Tokenization Algorithms

### 5.1 Byte Pair Encoding (BPE)

Mechanism:

1. Start with characters
2. Count most frequent adjacent pair
3. Merge them
4. Repeat until vocab size reached

Used in:

* GPT-2
* GPT-3
* GPT-4 style models

Strengths:

* Deterministic merges
* Strong compression for English
* Robust to noise (Byte-level variant)

Weaknesses:

* Can split rare domain words awkwardly
* Whitespace handling differs across implementations

---

### 5.2 WordPiece

Similar to BPE but:

* Uses likelihood-based scoring
* Used in BERT family

Optimizes:
Likelihood of training corpus under vocabulary.

---

### 5.3 SentencePiece (Unigram Model)

Mechanism:

* Starts with large candidate vocab
* Removes tokens based on probability contribution
* Probabilistic segmentation

Used in:

* T5
* LLaMA
* Many multilingual models

Strengths:

* Strong multilingual handling
* Cleaner whitespace modeling

Weaknesses:

* Slightly different inductive bias
* More probabilistic segmentation

---

## 6. Vocabulary Size Tradeoff

Increasing vocabulary size:

Pros:

* Fewer tokens per sentence
* Better domain term capture
* Shorter sequences

Cons:

* Larger embedding table
* Higher memory usage
* More parameters

Decreasing vocabulary size:

Pros:

* Smaller embedding table
* Lower memory footprint

Cons:

* More tokens per sentence
* Longer sequences
* Higher compute per request

Tradeoff:

Embedding Memory ∝ Vocabulary Size
Compute Cost ∝ Sequence Length

---

## 7. Token Inflation and Compression

Two critical metrics:

### Tokens per Character

Lower is better.

### Characters per Token

Higher is better.

Token inflation directly affects:

* Context window utilization
* Inference cost
* Training cost
* Scaling laws

Since scaling is measured in tokens, not words.

---

## 8. Whitespace and Case Sensitivity

Example:

```
"Architecting systems"
" Architecting systems"
```

Leading space can change tokenization completely.

Similarly:

```
Apple
apple
```

Different token IDs.

A space is not empty.
It changes the probability trajectory.

---

## 9. Failure Modes

Tokenizers struggle with:

* Rare domain terms
* Mixed casing
* JSON blobs
* Code snippets
* URLs
* Random IDs

Improper tokenization leads to:

* Higher token inflation
* Context window waste
* Increased hallucination risk
* Poor embedding similarity

---

## 10. Tokenization and Scaling Laws

Training cost scales with tokens processed.

If token inflation increases by 8%:

* Training cost increases by 8%
* GPU hours increase proportionally
* Energy usage increases
* Inference cost increases

Tokenizer choice affects economic efficiency.

---

## 11. Tokenization and Hallucination

Longer token sequences:

* Increase autoregressive error compounding
* Increase drift probability
* Increase generation instability

Better compression → shorter sequences → reduced drift exposure.

---

## 12. Tokenization in Production Systems

Tokenizer decisions affect:

* RAG chunk sizing
* Embedding storage size
* Context window limits
* API cost estimation
* Multilingual deployment
* Prompt engineering outcomes

It is not preprocessing.
It is architectural.

---

## 13. Strategy

To tokenization effectively:

1. Begin with deterministic vs probabilistic systems
2. Derive BPE merges manually
3. Train a tokenizer on a small corpus
4. Compare token splits visually
5. Measure token inflation
6. Connect results to inference cost

Students must move from:

“How does tokenization work?”

To:

“How does tokenizer design change system economics?”

---

## 14. Final Mental Model

LLMs do not see words.
They see integer sequences.

Tokenization defines:

* The model’s perception resolution
* The geometry of embedding space
* The scaling trajectory
* The cost structure of intelligence

Understanding tokenization deeply is foundational to becoming a system-level AI architect.

---

## Next Let us also look into: 

* Embeddings.md
* Sampling.md
* Hallucination.md
* Scaling_Laws.md
* RAG_and_Tokenization.md

To make a complete GenAI Systems Foundations documentation set.
