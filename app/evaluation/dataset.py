evaluation_dataset = [

# ---------------- SINGLE-DOCUMENT FACTUAL QUESTIONS ----------------

{
    "question": "What are the three downstream systems the Payment Service writes to according to the architecture diagram?",

    "expected_answer": "Redis, PostgreSQL, and Kafka",

    "source_documents":[
        "architecture.png"
    ]
},

{
    "question": "What is the total pod restart count shown on the dashboard?",

    "expected_answer": "3",

    "source_documents":[
        "grafana_dashboard.png"
    ]
},

{
    "question": "What is the current number of active Redis connections shown on the dashboard?",

    "expected_answer": "128",

    "source_documents":[
        "grafana_dashboard.png"
    ]
},

{
    "question": "What issue is associated with a pod stuck downloading its container image, per the Kubernetes runbook?",

    "expected_answer": "ImagePullBackOff",

    "source_documents":[
        "kubernetes_runbook.pdf"
    ]
},

{
    "question": "What resolution is suggested when a pod is OOMKilled?",

    "expected_answer": "Increase resources",

    "source_documents":[
        "kubernetes_runbook.pdf"
    ]
},

{
    "question": "What payment success rate should be achieved after resolution, per the payment runbook?",

    "expected_answer": "Above 99%",

    "source_documents":[
        "payment_runbook.pdf"
    ]
},

{
    "question": "What causes are listed for HTTP 500 errors on payment requests?",

    "expected_answer": "Redis unavailable, PostgreSQL unavailable, Kafka broker unreachable, or connection pool exhausted",

    "source_documents":[
        "payment_runbook.pdf"
    ]
},

{
    "question": "What tool is used to build container images in the CI/CD pipeline?",

    "expected_answer": "Docker (Docker Build)",

    "source_documents":[
        "deployment_guide.txt"
    ]
},

{
    "question": "What tool orchestrates deployment to Kubernetes in this pipeline?",

    "expected_answer": "Helm",

    "source_documents":[
        "deployment_guide.txt"
    ]
},

{
    "question": "What was the customer-facing impact of the payment API outage?",

    "expected_answer": "Customers were unable to complete payment",

    "source_documents":[
        "incident_postmortem.txt"
    ]
},

{
    "question": "How many consumer replicas were scaled to after the Kafka incident?",

    "expected_answer": "5 (scaled from 2 to 5)",

    "source_documents":[
        "kafka_incident.txt"
    ]
},

{
    "question": "What verification confirmed the Kafka consumer lag incident was resolved?",

    "expected_answer": "Consumer lag returned to zero and messages were processed successfully",

    "source_documents":[
        "kafka_incident.txt"
    ]
},

{
    "question": "What latency threshold confirmed the nginx incident was resolved?",

    "expected_answer": "Latency below 100ms",

    "source_documents":[
        "nginx_incident.txt"
    ]
},

{
    "question": "What was logged immediately before the Redis reconnection in the production logs?",

    "expected_answer": "Retrying Request",

    "source_documents":[
        "production_logs.log"
    ]
},

{
    "question": "How many client connections were logged just before the connection pool exhaustion error in the Redis logs?",

    "expected_answer": "950",

    "source_documents":[
        "redis_logs.log"
    ]
},

{
    "question": "What command retrieves memory information for Redis, per the Redis runbook?",

    "expected_answer": "INFO memory",

    "source_documents":[
        "redis_runbook.txt"
    ]
},

{
    "question": "What command retrieves client connection information for Redis?",

    "expected_answer": "INFO clients",

    "source_documents":[
        "redis_runbook.txt"
    ]
},

{
    "question": "What symptoms indicate Redis problems according to the Redis runbook?",

    "expected_answer": "High latency, connection refused, OOM, and connection pool exhausted",

    "source_documents":[
        "redis_runbook.txt"
    ]
},

# ---------------- CROSS-DOCUMENT SYNTHESIS QUESTIONS ----------------

{
    "question": "What root cause connects the incident postmortem to the errors seen in the production logs around 10:07?",

    "expected_answer": "Both point to Redis: the postmortem's root cause is Redis connection pool exhaustion, and the production logs show a Redis Connection Timeout at 10:07:11 followed by a payment failure and HTTP 500.",

    "source_documents":[
        "incident_postmortem.txt",
        "production_logs.log"
    ]
},

{
    "question": "How does the Kafka consumer lag metric on the Grafana dashboard relate to the Kafka incident report?",

    "expected_answer": "The dashboard's Kafka Consumer Lag panel (topic_events: 10k, topic_logs: 5k) reflects the type of lag buildup described in the incident, which was caused by a crashed consumer pod and resolved by scaling consumers from 2 to 5.",

    "source_documents":[
        "grafana_dashboard.png",
        "kafka_incident.txt"
    ]
},

{
    "question": "Which commands would you run to fix the root cause identified in the incident postmortem?",

    "expected_answer": "Restart Redis via systemctl restart redis (Redis runbook) and increase the connection pool size (Payment Service runbook), matching the postmortem's actions of restarting Redis and increasing pool size.",

    "source_documents":[
        "incident_postmortem.txt",
        "redis_runbook.txt",
        "payment_runbook.pdf"
    ]
},

{
    "question": "Does the memory usage warning in the Redis logs align with the causes listed in the Redis runbook?",

    "expected_answer": "Yes. The Redis logs show a warning that memory usage exceeded 85%, which matches the runbook's listed common cause of the memory limit being reached.",

    "source_documents":[
        "redis_logs.log",
        "redis_runbook.txt"
    ]
},

{
    "question": "What deployment guide step would you use after applying the nginx incident's resolution?",

    "expected_answer": "After restarting the backend deployment and increasing replicas (nginx incident), you would use the deployment guide's kubectl rollout status command to verify the rollout, followed by smoke tests and checking the Grafana dashboard.",

    "source_documents":[
        "nginx_incident.txt",
        "deployment_guide.txt"
    ]
},

{
    "question": "Which component in the architecture diagram is implicated by the connection pool exhausted error in the Redis logs?",

    "expected_answer": "The Redis component, which the architecture diagram shows the Payment Service connecting directly to.",

    "source_documents":[
        "architecture.png",
        "redis_logs.log"
    ]
},

{
    "question": "What kubectl command from the Kubernetes runbook matches the investigation step used during the nginx incident?",

    "expected_answer": "kubectl get pods, which appears in both the Kubernetes runbook's general troubleshooting steps and the nginx incident's investigation steps (along with kubectl logs nginx).",

    "source_documents":[
        "kubernetes_runbook.pdf",
        "nginx_incident.txt"
    ]
},

{
    "question": "What do the resolution steps in the payment runbook have in common with the actions taken in the incident postmortem?",

    "expected_answer": "Both involve restarting Redis and addressing the exhausted connection pool by increasing its size.",

    "source_documents":[
        "payment_runbook.pdf",
        "incident_postmortem.txt"
    ]
},

# ---------------- QUESTIONS WITH NO ANSWER IN THE DOCUMENTS (should NOT be answered / should be flagged as unknown) ----------------

{
    "question": "What is the maximum number of retries configured for payment requests?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "Who is the on-call engineer responsible for the payment service?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What programming language is the Payment Service written in?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What is the SLA uptime target for the payment service?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What version of Kafka is used in this architecture?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What is the monthly infrastructure cost of running the Redis cluster?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What alerting or paging tool (e.g. PagerDuty) is integrated with this system besides Grafana?",

    "expected_answer": "Not found in the provided documents.",

    "source_documents":[
    ]
},

# ---------------- VAGUE OR OUT-OF-SCOPE QUESTIONS (unrelated to the corpus) ----------------

{
    "question": "What's the capital of France?",

    "expected_answer": "Not related to the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "How do I bake a chocolate cake?",

    "expected_answer": "Not related to the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "Who won the cricket World Cup in 2023?",

    "expected_answer": "Not related to the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "What is quantum computing?",

    "expected_answer": "Not related to the provided documents.",

    "source_documents":[
    ]
},

{
    "question": "Can you recommend a good restaurant in Delhi?",

    "expected_answer": "Not related to the provided documents.",

    "source_documents":[
    ]
},

# ---------------- VAGUE-BUT-RELATED / AMBIGUOUS QUESTIONS (require clarification or should not force a single-document guess) ----------------

{
    "question": "What's wrong with the system?",

    "expected_answer": "Ambiguous: multiple incidents exist in the corpus (Redis pool exhaustion outage, Kafka consumer lag, nginx 502 errors). A good RAG answer should surface all relevant incidents or ask for clarification rather than picking one arbitrarily.",

    "source_documents":[
        "incident_postmortem.txt",
        "kafka_incident.txt",
        "nginx_incident.txt"
    ]
},

{
    "question": "How do I fix the error?",

    "expected_answer": "Too vague to answer directly: 'the error' is not specified, and the corpus contains several distinct errors (Redis connection pool exhausted, Kafka consumer lag, 502 Bad Gateway). Should prompt for clarification.",

    "source_documents":[
    ]
},

]