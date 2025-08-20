# AI Agent Squad: Data Standardization & Learning

A multi-agent system that collaborates to validate, standardize, and enrich company data in real-time, featuring a human-in-the-loop learning mechanism.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/AI%20Model-Gemini-blue?logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Embeddings-SentenceTransformers-yellow" alt="SentenceTransformers">
  <img src="https://img.shields.io/badge/Library-Pandas-purple?logo=pandas" alt="Pandas">
  <img src="https://img.shields.io/badge/Library-Scikit--learn-orange?logo=scikit-learn" alt="Scikit-learn">
</p>

---

### Team Members
* Aline Athaydes
* [Add other team members here]

### The Problem ⚠️
In any data-driven organization, free-text fields are a major source of inconsistency. User input variations, including typos, abbreviations, and semantic differences (e.g., "Quantum Dyn.", "quantum dynamics", "Quantum Dynamics LLC"), lead to data fragmentation. This fragmentation corrupts analytics, breaks reporting, and makes it impossible to get a reliable single source of truth, directly impacting business intelligence and operations.

### The Solution 🚀
We built the **AI Agent Squad**, an intelligent system that intercepts new data entries in real-time. It's not a single model but a collaborative pipeline of specialized AI agents that analyze, verify, and standardize information. The system features a **Human-in-the-Loop** mechanism, allowing it to learn from admin feedback and become smarter over time.

### System Architecture 🏗️
Our architecture is designed for efficiency and robustness, ensuring that simple cases are handled instantly and complex cases receive deep analysis.

1.  **UI Layer (Streamlit):** A clean and intuitive web interface for user data entry and an "Admin Validation Queue" for reviewing flagged entries.
2.  **Orchestrator Core:** The central brain of the application that manages the flow of data through the agent pipeline.
3.  **The Agent Squad:** A team of specialized agents that work in sequence.
4.  **Learning Loop:** A feedback mechanism where an admin's decisions in the Validation Queue can be used to update the system's knowledge base, improving future performance.
5.  **Data Layer:** Utilizes local CSV files to simulate a database, storing both canonical data and synthetic user inputs.

### The Agent Squad 🤖
Our solution's core is a team of three specialist agents:

* **`TriageAgent` (The Lexical Analyst):** Uses the Jaro-Winkler algorithm for high-speed lexical similarity checks. It resolves obvious typos and variations instantly.
* **`SemanticSearchAgent` (The Context Expert):** Leverages a Sentence Transformer model to find the best match based on contextual meaning, understanding nuances beyond simple spelling.
* **`DecisionAgent` (The Final Arbiter):** A Google Gemini-powered LLM that analyzes a full dossier of evidence from the other agents and makes a final, reasoned judgment based on a "Rule of Consensus".

### Interaction Flow ➡️
1.  A user enters data (e.g., "Rodes cates cat") into the "New Employee" form and submits.
2.  The **`Orchestrator`** initiates the mission and passes the input to the **`TriageAgent`**.
3.  The `TriageAgent` finds an ambiguous lexical match ("Rod Cute Cats") and escalates the case.
4.  The **`SemanticSearchAgent`** analyzes the input's meaning and also finds a strong contextual match with "Rod Cute Cats".
5.  The `Orchestrator` compiles a dossier with both analyses and presents it to the **`DecisionAgent`**.
6.  The `DecisionAgent` (Gemini) applies the "Rule of Consensus," sees that both agents agree, and returns a final verdict: **AUTO_CORRECT**.
7.  If the verdict were **FLAG_FOR_REVIEW**, the entry would appear in the **Admin Validation Queue**, where an admin's decision would provide a learning opportunity for the system.
8.  The UI displays the final, reasoned verdict to the user.

### Project Setup & Execution ⚙️

**1. Prerequisites**
* This project uses [Conda](https://www.anaconda.com/products/distribution) for environment management.

**2. Clone the Repository**
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd data-standardizer-hackathon
