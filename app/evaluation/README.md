Dataset size: 40 questions

1ST RUN

Question Categories
-------------------
Single-document: 18
Cross-document: 8
Unknown/No-answer: 7
Out-of-scope: 5
Ambiguous: 2

Runtime
-------
Error Rate: 0%

Latency
-------
P50: 0.45 s
P99: 3.58 s

Observations
------------
✓ Strong single-document retrieval
✓ Correct out-of-scope rejection
✓ No hallucinations observed
✗ Cross-document synthesis needs improvement
✗ OCR retrieval weak on architecture.png



======================================================================
Overall Retrieval Metrics
======================================================================
Questions Evaluated : 27
Average Recall@K    : 77.16%
Average Precision@K : 36.94%
Hit Rate            : 85.19%


Observations:
1. Strong retrieval for textual documents (runbooks, logs, incident reports).
2. Image-heavy documents (Architecture Diagram, Grafana Dashboard) showed lower retrieval performance due to OCR limitations.
3. Cross-document reasoning questions achieved partial retrieval, indicating that relevant documents were retrieved but not always all required supporting documents.
4. Precision is lower because Hybrid Retrieval intentionally returns multiple candidate documents before generation. This is expected without reranking.



======================================================================
Overall Citation Metrics
======================================================================
Citation Recall    : 77.16%
Citation Precision : 36.94%
Exact Match Rate   : 7.41%

Observations:
Citation Recall: 77.16% → This matches retrieval recall exactly, because citation evaluation is currently based on retrieved documents.
Citation Precision: 36.94% → Retriever is returning many extra documents.
Exact Match Rate: 7.41% → This is expected and not a good metric for RAG. Hybrid retrieval usually returns multiple supporting chunks, so requiring the retrieved set to exactly equal the expected set is overly strict.




======================================================================

Answer Accuracy Evaluation

======================================================================

Questions : 40

Correct   : 29

Incorrect : 11

Accuracy  : 72.50%


======================================================================

Observation:
1.OCR / Image Retrieval Failure (3 failures)
2.Multi-document Retrieval Failure (4 failures)
    example:
    Incident Postmortem
    +
    Production Logs
    model answer: I don't have enough information
3.Prompt / Reasoning Failure (2 failures)
    example:
    Payment Service
    vs
    Redis component

    The retriever returned both documents.
    The model simply reasoned incorrectly.

4.Conservative Guardrail (2 failures)
    example:
    What's wrong with the system?
   
    guardrail classified:
    Outside scope
    
    but expected:
    Ambiguous.






2ND RUN AFTER OCR EVAL

Question Categories
-------------------
Single-document: 18
Cross-document: 8
Unknown/No-answer: 7
Out-of-scope: 5
Ambiguous: 2

Runtime
-------
Error Rate: 0%

Latency
-------
P50: 0.64 s
P99: 4.83 s


======================================================================
Overall Retrieval Metrics
======================================================================
Questions Evaluated : 27
Average Recall@K    : 86.42%
Average Precision@K : 35.93%
Hit Rate            : 92.59%


======================================================================
Overall Citation Metrics
======================================================================
Citation Recall    : 86.42%
Citation Precision : 35.93%
Exact Match Rate   : 3.70%


======================================================================

Answer Accuracy Evaluation

======================================================================

Questions : 40

Correct   : 36

Incorrect : 4

Accuracy  : 90.00%


======================================================================