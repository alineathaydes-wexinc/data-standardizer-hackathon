# app.py
import streamlit as st
import pandas as pd
import time
import urllib.parse
from src.core.orchestrator import run_standardization_pipeline
from src.agents.semantic_agent import SemanticSearchAgent

st.set_page_config(layout="wide", page_title="AI Agent Squad")

# --- State Management: A memória do nosso app ---
if 'flagged_items' not in st.session_state:
    st.session_state.flagged_items = []
if 'companies_df' not in st.session_state:
    st.session_state.companies_df = None
if 'employees_df' not in st.session_state:
    st.session_state.employees_df = None

# --- Global Setup & Caching ---
@st.cache_resource
def get_semantic_agent(companies_df):
    """Carrega o agente semântico, que é pesado."""
    canonical_names = companies_df['CompanyName'].tolist()
    return SemanticSearchAgent(canonical_names=canonical_names)

def load_data():
    """Carrega os dados para o estado da sessão se ainda não estiverem lá."""
    if st.session_state.companies_df is None:
        try:
            st.session_state.companies_df = pd.read_csv("data/enterprise_companies.csv")
            st.session_state.employees_df = pd.read_csv("data/enterprise_employees.csv")
        except FileNotFoundError:
            st.error("Data files not found. Please run `python scripts/generate_enterprise_data.py` first.")
            return False
    return True

# --- Main App Execution ---
if load_data():
    semantic_agent = get_semantic_agent(st.session_state.companies_df)

    st.title("🛡️ AI Agent Squad: Data Standardization & Learning")
    st.write("A multi-agent system that validates data and learns from user feedback.")
    st.divider()

    col1, col2 = st.columns((1, 1.2))

    # --- Column 1: Input Form ---
    with col1:
        st.header("New Employee Registration")
        with st.form("employee_form"):
            first_name = st.text_input("First Name", "Alex")
            last_name = st.text_input("Last Name", "Taylor")
            user_input_company = st.text_input("Company Name", "Rodes cates cat")
            submitted = st.form_submit_button("Engage AI Agent Squad")

    # --- Column 2: Agent Worklog & Results ---
    with col2:
        st.header("Agent Mission Log")
        if submitted:
            with st.status("Agent Pipeline Initialized...", expanded=True) as status:
                st.write("TriageAgent is performing a high-speed lexical scan...")
                time.sleep(1)
                final_result = run_standardization_pipeline(user_input_company, semantic_agent)
                evidence = final_result.get("evidence", {})
                
                if evidence:
                    st.write(f"TriageAgent Result: Ambiguous match (`{evidence.get('best_match_lexical')}`). Escalating...")
                    time.sleep(1)
                    st.write("SemanticSearchAgent is analyzing contextual meaning...")
                    time.sleep(1)
                    st.write(f"SemanticAgent Result: Strong semantic link to `{evidence.get('best_match_semantic')}`.")
                    time.sleep(1)
                    st.write("DecisionAgent is reviewing all evidence...")
                    time.sleep(1)
                
                status.update(label="Mission Complete!", state="complete", expanded=False)
            
            st.subheader("Final Verdict")
            action = final_result.get("action")
            best_match = final_result.get("best_match")
            reason = final_result.get("reason")
            
            if action == "AUTO_CORRECT":
                st.success(f"✅ **Action: Auto-Corrected to `{best_match}`**")
                st.info(f"**Reasoning:** {reason}")
            else: # FLAG_FOR_REVIEW
                st.error(f"🚩 **Action: Flag for Human Review**")
                st.info(f"**Reasoning:** {reason}")
                # Adiciona à fila de validação SE for para revisão
                st.session_state.flagged_items.append({
                    "user_input": user_input_company,
                    "best_guess": evidence.get('best_match_semantic', 'N/A')
                })
            
            st.subheader("Final Payload")
            st.json({"full_reasoning": final_result})
        else:
            st.info("Submit the form to engage the AI agents.")

    st.divider()

    # --- Validation Queue Section ---
    st.header("Admin Validation Queue")
    if not st.session_state.flagged_items:
        st.success("The validation queue is empty. All data is clean!")
    else:
        st.warning(f"You have {len(st.session_state.flagged_items)} items needing review.")
        
        for i, item in enumerate(st.session_state.flagged_items):
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 2, 1])
                c1.write(f"**User Input:** `{item['user_input']}`")
                c2.write(f"**AI Suggestion:** `{item['best_guess']}`")
                
                approve_key, create_new_key = f"approve_{i}", f"create_new_{i}"
                
                if c3.button("✅ Approve", key=approve_key):
                    # Lógica para notificar
                    subject = "Data Correction Approved"
                    body = f"The user input '{item['user_input']}' has been approved and corrected to '{item['best_guess']}'."
                    encoded_body = urllib.parse.quote(body)
                    st.link_button("📧 Notify Supervisor", f"mailto:supervisor@example.com?subject={subject}&body={encoded_body}")
                    
                    st.toast(f"Approved! '{item['user_input']}' marked for correction.")
                    st.session_state.flagged_items.pop(i)
                    st.rerun()

                if c3.button("🆕 Create New", key=create_new_key):
                    # Lógica para adicionar nova empresa e notificar
                    new_company_id = st.session_state.companies_df['CompanyID'].max() + 1
                    new_company_data = {'CompanyID': new_company_id, 'CompanyName': item['user_input']}
                    st.session_state.companies_df.loc[len(st.session_state.companies_df)] = new_company_data
                    
                    subject = "New Company Created"
                    body = f"A new company '{item['user_input']}' has been added to the system by an admin."
                    encoded_body = urllib.parse.quote(body)
                    st.link_button("📧 Notify Supervisor", f"mailto:supervisor@example.com?subject={subject}&body={encoded_body}")

                    st.toast(f"'{item['user_input']}' added as a new company!")
                    st.session_state.flagged_items.pop(i)
                    st.rerun()

    # Botão para salvar as mudanças de volta para os arquivos CSV
    if st.button("💾 Save All Changes to CSV"):
        try:
            st.session_state.companies_df.to_csv("data/enterprise_companies.csv", index=False)
            # A lógica para salvar 'employees' seria mais complexa, aqui estamos focando em 'companies'
            st.success("Changes saved successfully to data/enterprise_companies.csv!")
        except Exception as e:
            st.error(f"Failed to save changes: {e}")