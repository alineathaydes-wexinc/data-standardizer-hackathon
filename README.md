# AI Agent Squad: Data Standardization & Learning

A multi-agent system that collaborates to validate, standardize, and enrich company data in real-time, featuring a human-in-the-loop learning mechanism.

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" alt="Python Version">
<img src="https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit" alt="Streamlit">
<img src="https://img.shields.io/badge/AI%20Model-Gemini-blue?logo=google&logoColor=white" alt="Gemini">
<img src="https://img.shields.io/badge/Embeddings-SentenceTransformers-yellow" alt="SentenceTransformers">
<img src="https://img.shields.io/badge/Library-Pandas-purple?logo=pandas" alt="Pandas">
<img src="https://img.shields.io/badge/Library-Scikit--learn-orange?logo=scikit-learn" alt="Scikit-learn">
</p>

---

### Team Members:

  * Aline Athaydes

  * Jabari Chambers

  * Tiago Neves

### The Problem ⚠️

  In any data-driven organization, free-text fields are a major source of inconsistency. User input variations, including typos, abbreviations, and semantic differences (e.g., "Quantum Dyn.", "quantum dynamics", "Quantum Dynamics LLC"), lead to data fragmentation. This fragmentation corrupts analytics, breaks reporting, and makes it impossible to get a reliable single source of truth, directly impacting business intelligence and operations.

### The Solution 🚀

  We built the **AI Agent Squad**, an intelligent system that intercepts new data entries in real-time. It's not a single model but a collaborative pipeline of specialized AI agents that analyze, verify, and standardize information. The system features a Human-in-the-Loop mechanism, allowing it to learn from admin feedback and become smarter over time.

### System Architecture & Technical Deep Dive 🏗️

Our architecture is designed for efficiency and robustness, ensuring that simple cases are handled instantly and complex cases receive deep analysis.

1.  **UI Layer (Streamlit):** A clean and intuitive web interface for user data entry and an "Admin Validation Queue" for reviewing flagged entries.
2.  **Orchestrator Core:** The central brain of the application that manages the flow of data through the agent pipeline.
3.  **The Agent Squad:** A team of specialized agents that work in sequence.
4.  **Learning Loop:** A feedback mechanism where an admin's decisions in the Validation Queue can be used to update the system's knowledge base, improving future performance.
5.  **Data Layer:** Utilizes local CSV files to simulate a database, storing both canonical data and synthetic user inputs.

### The Agent Squad 🤖

  Our system operates as a collaborative multi-agent pipeline designed for robust and efficient data standardization. Each agent is a specialized module that contributes evidence towards a final decision, mimicking an expert data analysis team. The flow is managed by an Orchestrator Core that directs data through the agents.

* **`TriageAgent` (The Lexical Analyst):** Uses the Jaro-Winkler algorithm for high-speed lexical similarity checks. Acts as the first line of defense. It employs a high-speed, low-cost lexical similarity algorithm (Jaro-Winkler) to instantly resolve obvious cases, such as minor typos or suffix variations (e.g., "Corp." vs "Corporation"). Cases with very high confidence (>95%) are auto-corrected, while those with very low confidence (<70%) are immediately flagged. Ambiguous cases are escalated to the next agent.

* **`SemanticSearchAgent` (The Context Expert):** Specializes in contextual understanding. It leverages a Sentence Transformer model to convert user inputs and canonical company names into high-dimensional vector embeddings. By calculating the cosine similarity in this vector space, the agent identifies the closest match based on semantic meaning, not just character-level similarity. This allows it to understand nuanced inputs that lexical methods might miss.

* **`DecisionAgent` (The Final Arbiter):** Powered by Google's Gemini LLM, this agent serves as the final judge. It receives a comprehensive dossier containing the analyses from both the TriageAgent and the SemanticSearchAgent. Based on a set of predefined rules—primarily the "Rule of Consensus," where agreement between the first two agents provides strong evidence—the DecisionAgent makes a final, reasoned judgment to either auto-correct the data or flag it for the human-in-the-loop validation queue.

### Interaction Flow ➡️
1.  A user enters data (e.g., "Rodes cates cat") into the "New Employee" form and submits.
2.  The **`Orchestrator`** initiates the mission and passes the input to the **`TriageAgent`**.
3.  The `TriageAgent` finds an ambiguous lexical match ("Rod Cute Cats") and escalates the case.
4.  The **`SemanticSearchAgent`** analyzes the input's meaning and also finds a strong contextual match with "Rod Cute Cats".
5.  The `Orchestrator` compiles a dossier with both analyses and presents it to the **`DecisionAgent`**.
6.  The `DecisionAgent` (Gemini) applies the "Rule of Consensus," sees that both agents agree, and returns a final verdict: **AUTO_CORRECT**.
7.  If the verdict were **FLAG_FOR_REVIEW**, the entry would appear in the **Admin Validation Queue**, where an admin's decision would provide a learning opportunity for the system.
8.  The UI displays the final, reasoned verdict to the user.
   
**This hybrid, layered approach ensures both speed for simple cases and deep, multi-faceted analysis for complex ones.**

### Getting Started: Setup & Execution ⚙️
  Follow these steps to set up and run the project on your local machine.

#### 1. Prerequisites

  Conda: This project uses Conda for environment management. If you don't have it, we recommend installing Miniconda.

  (For Windows Users) WSL 2: It is highly recommended to run this project inside the Windows Subsystem for Linux (WSL 2) for better compatibility with Linux-based tools. You can install it by running this command in an admin PowerShell or Windows Terminal:

  **wsl --install**
  
#### 2. Clone the Repository

  Open your terminal (or WSL terminal) and clone the project.

  **git clone https://github.com/alineathaydes-wexinc/data-standardizer-hackathon.git**
  
  cd data-standardizer-hackathon
  
#### 3. Set Up the Conda Environment

  Create and activate a dedicated Conda environment with Python 3.10.

 **Create the environment**
  conda create --name hackathon-env python=3.10 -y

**Activate the environment**

  conda activate hackathon-env
  
#### 4. Install Dependencies

  All required Python libraries are listed in the requirements.txt file. Install them with a single command:

  **pip install -r requirements.txt**
  
  Developer Note: If you install new libraries, remember to update the requirements file by running: pip freeze > requirements.txt

#### 5. Configure Environment Variables

  The DecisionAgent requires a Google Gemini API key.

  Create a file named .env in the root directory of the project.

  Add your API key to this file like so:

  **GOOGLE_API_KEY="YOUR_API_KEY_HERE"**
  
#### 6. Generate Synthetic Data (Optional)

  The project includes a script to generate sample data for testing. To run it, execute:

  **python scripts/generate_enterprise_data.py**
  
#### 7. Run the Application

  With the environment active and dependencies installed, you can now start the Streamlit web application.

  **streamlit run app.py**
  
  Your browser should automatically open with the application running. If not, the terminal will provide a local URL (usually http://localhost:8501) that you can visit.
