
---

### Question 1: Summarize your experience in solutioning or developing Agentic AI automation using specific GCP services / components.

In my architecture leadership across **WPP Media** (Prototype & Innovation) and hands-on architecture laboratory (**Ideas-to-Life**), I have designed and deployed cloud-native Agentic AI microservices and pattern libraries on **Google Cloud Platform (GCP)**.
#### Key GCP Services & Components Utilized:

1. **Google Cloud Run (Serverless Container Execution)**:
   - Architected serverless container deployments for multi-agent services, LiteLLM proxy gateways, and interactive agent pattern libraries.
   -  Defined Cloud Run dev auth patterns, container lifecycle management, and auto-scaling rules for agent workloads.
2. **GCP IAM & Workload Identity**:
   - Established zero-trust IAM authentication policies and keyless service account configurations for agent container communication with underlying Google Cloud resources.
3. **GCP Artifact Registry & Cloud Build**:
   - Built CI/CD containerisation pipelines via Docker and GCP Artifact Registry for packaging agent microservices and micro-frontend libraries.
4. **GCP API Gateway & Server-Sent Events (SSE)**:
   - Conducted architectural constraint analysis regarding GCP API Gateway streaming limitations for Server-Sent Events (SSE) in real-time agentic chat and event streams, designing proxy mitigations.
5. **Google Cloud Storage (GCS)**:
   - Solutioned persistent storage backends for Retrieval-Augmented Generation (RAG) vector documents, agent memory state, and artifact logs.
### Question 2: What kind of agentic design patterns have you designed, developed or implemented in your past projects?

I have authored design pattern specifications and built working implementations across **6 core agentic patterns**:
1. **Router Pattern**:
   - Designed intent-classification routing layers that evaluate incoming user requests and dynamically route execution to domain-specific worker agents (e.g. media planning vs. audience analysis). [^portfolio-wpp-work-ai-projects-gitlab-buyer-agent-ch-readme]

2. **Orchestrator-Workers (Supervisor Pattern)**:
   - Implemented hierarchical supervisor agents that break complex user goals into sub-tasks, delegate work to specialized worker agents, and aggregate results back to the caller.
3. **Agent-to-Agent (A2A) Peer Collaboration**:
   - Solutioned autonomous peer-to-peer agent protocols (`PCA Production Agents A2A`) where independent agents collaborate over standardized REST/gRPC interfaces without a single monolithic controller.
4. **ReAct (Reasoning + Acting) & Reflection Loops**:
   - Built multi-step reasoning loops combining thought, action (tool calling), observation, and self-reflection to validate intermediate tool outputs and recover from API/tool errors autonomously.
5. **Model Context Protocol (MCP) & Tool-Calling**:
   - Architected standardised tool interfaces connecting LLM agents directly to external APIs (Smartsheet, LeanIX, Git repositories, custom Python services) under strict input/output validation schema.
6. **Human-in-the-Loop (HITL) & Guardrail Controls**:
   - Designed stateful pause-and-resume mechanisms where agent execution halts before executing high-impact actions (e.g. external data mutation or code deployment) until human approval is granted. 
---

### Question 3: Do you have any experience in designing & developing a multi-agent architecture in your past projects?

I have extensive architecture and hands-on experience designing multi-agent systems across enterprise and research environments:
1. **WPP Media — PCA Production Agents & Media Buyer Agent System**:
   - Led the architecture for the **PCA Production Agents A2A** platform and **Media Buyer Agent (`buyer-agent-ch`)**.
   - Designed a decoupled multi-agent architecture where individual agents (e.g. Audience Agent, Inventory Agent, Execution Agent) run as independent containerized microservices communicating via standardized agent protocols.
   
2. **Ideas-to-Life
   - Built a multi-agent governance platform **Continuous Architecture System (CAS)** where specialized sub-agents perform static code analysis, validate Architecture Decision Records, analyze Git history, and generate structural documentation under an orchestrating governance agent.
   - Built a multi-agentic system **EA4ALL - Enterprise Architecture for ALL** automating various architecture workflows using Langgraph, CrewAI, MCP, FastAPI, RAG and more. 
---

### Question 4: Do you have any experience in designing & developing monitoring solutions for an Agentic AI platform?

Observability and monitoring are central pillars of my agentic architecture practice. I have designed and deployed end-to-end monitoring solutions covering latency, token cost, step-by-step agent trajectory, and evaluation accuracy: 
1. **Langfuse Session Tracing & Agent Trajectory Monitoring**:
   - Architected and configured **Langfuse** integration across TypeScript and Python agent implementations to capture step-by-step reasoning spans, prompt/response pairs, tool invocation outputs, and agent session state. 
2. **LiteLLM Enterprise Gateway & Cost / Performance Observability**:
   - Deployed **LiteLLM Proxy** as a unified LLM gateway to monitor token consumption, track model cost by team/agent, enforce rate limits, handle failover routing, and emit OpenTelemetry traces.
3. **Enterprise APM & GCP Cloud Logging Integration**:
   - Configured structured JSON logging and OpenTelemetry trace propagation linking LiteLLM proxy, agent microservices, and enterprise APM platforms (Datadog & GCP Cloud Logging).
4. **Agent Evaluation & Guardrail Benchmarking**:
   - Developed evaluation suites assessing agent completion rates, tool-calling precision, latency distribution, and failure recovery effectiveness across multi-step agent runs.
5. **Ideas-to-Life - Observability & Monitoring Platform**:
   - Built a custom multi-agent observability platform where specialised monitoring agents collect metrics, analyze agent performance, and generate dashboards for real-time operational insights.
   - Implemented LangSmith for agentic reasoning trace analysis, enabling root-cause analysis of agent failures and performance bottlenecks.

---
