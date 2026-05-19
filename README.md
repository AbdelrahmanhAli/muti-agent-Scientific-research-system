# Multi-Agent Scientific Research System

A powerful AI-driven multi-agent platform for autonomous scientific research, built using **LangChain** and **LangGraph**. The system simulates collaborative scientific reasoning through specialized AI agents that work together to search the web, retrieve literature, analyze papers, validate findings, generate hypotheses, review outputs, write reports, and **generate code** for research tasks.

## ✨ Features

- **Multi-Agent Collaboration**: Uses specialized agents (Research, Reviewer, Writer, Coordinator, Coder) coordinated via LangGraph stateful workflows.
- **Modular Architecture**: Each agent has a dedicated role, improving reasoning quality, task specialization, scalability, and scientific consistency.
- **Code Generation**: Coder agent can generate research-related code, data analysis scripts, and visualizations.
- **Research Capabilities**: Autonomous literature review, AI-assisted discovery, hypothesis generation, scientific critique, and academic writing automation.
- **RAG Pipeline**: Retrieval-Augmented Generation with vector stores (ChromaDB, FAISS, PGVector) and embeddings.
- **API Ready**: FastAPI backend for easy integration and deployment.

## 🏗️ System Architecture

```
                            ┌──────────────────┐
                            │   User Query     │
                            └────────┬─────────┘
                                     │
                                     ▼
                         ┌─────────────────────┐
                         │ Coordinator Agent   │
                         └────────┬────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
            ▼                     ▼                     ▼
    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │ Research Agent │  │ Reviewer Agent │  │  Writer Agent  │
    └──────┬─────────┘  └──────┬─────────┘  └──────┬─────────┘
           │                   │                   │
           ▼                   ▼                   ▼
     Web Search          Scientific Review     Final Report
     Paper Retrieval     Fact Validation       Summarization
     RAG Retrieval       Hallucination Check   Structured Writing

            ┌─────────────────────┼─────────────────────┐
            │                     
            ▼                                        
    ┌────────────────┐  
    │  Coder Agent   │    
    └────────────────┘
     Code Generation      
     Data Analysis        
     Visualization        
```

## 🤖 Agents

| Agent | Role | Key Capabilities |
|-------|------|------------------|
| **Coordinator** | Orchestrator | Manages execution, routes tasks, tracks graph state, controls workflow logic |
| **Research** | Information Collector | Web search, ArXiv retrieval, paper summarization, RAG, PDF parsing |
| **Reviewer** | Scientific Critic | Validates claims, checks factual consistency, detects hallucinations |
| **Writer** | Report Generator | Literature reviews, methodology explanations, structured academic documents |
| **Coder** | Code Generator | Research code, data analysis scripts, statistical models, visualizations |

## 🛠️ Technologies Used

- **AI Frameworks**: LangChain, LangGraph, OpenAI API, Gemini API, Claude API
- **Backend**: Python, FastAPI
- **Research Tools**: Tavily Search, ArXiv API, Semantic Scholar API, Web Scraping, PDF Parsing

## 📁 Project Structure

```
multi-agent-scientific-research-system/
│
├── agents/                    # Agent implementations
│   ├── coordinator_agent.py
│   ├── research_agent.py
│   ├── reviewer_agent.py
│   ├── writer_agent.py
│   └── coder_agent.py          # Coder agent (not memory agent)
│
├── graphs/                    # LangGraph workflow definitions
│   └── workflow.py
│
├── tools/                     # External tool integrations
│ 
│
├
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
└── README.md
```


## 📊 Workflow Example

**User Query:** "Analyze recent advancements in quantum machine learning for healthcare and generate a Python script to visualize the performance metrics"

**Execution Flow:**
1. Coordinator creates execution plan
2. Research Agent retrieves papers and web results
3. Reviewer Agent validates findings
4. Coder Agent generates analysis code and visualizations
5. Writer Agent generates literature review and methodology
6. Final scientific report with code returned

## 🔮 Future Improvements

- Multi-modal scientific reasoning
- Autonomous experimentation
- Knowledge graph integration
- Research benchmarking
- Long-term memory systems
- Tool-using autonomous agents
- Distributed agent execution
- Self-improving research workflows

## 🙏 Inspiration & References

This project is inspired by:
- [SciAgentsDiscovery](https://github.com/tianges/SCIAgents)
- Virtual Scientists (VirSci)
- [CMBAgent](https://github.com/zk-phi/CMBAgent)
- InternAgent
- Research Weaver

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Abdelrahman Hamdy**  
AI & Automation Developer  
Multi-Agent Systems | Scientific AI | Autonomous Research Systems
