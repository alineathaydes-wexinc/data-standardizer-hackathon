# app.py
import streamlit as st
import pandas as pd
import time
import uuid

# These need to be imported to be used in the helper functions
from src.core.orchestrator import run_standardization_pipeline
from src.agents.semantic_agent import SemanticSearchAgent

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="AI Agent Squad")

# --- State Management ---
if 'flagged_items' not in st.session_state:
    st.session_state.flagged_items = []
if 'companies_df' not in st.session_state:
    st.session_state.companies_df = None
if 'employees_df' not in st.session_state:
    st.session_state.employees_df = None
# *** NEW: State for success message ***
if 'success_message' not in st.session_state:
    st.session_state.success_message = None

# --- Helper Functions ---
def save_dataframes():
    """Saves the current state of the DataFrames back to the CSV files."""
    try:
        st.session_state.companies_df.to_csv("data/enterprise_companies.csv", index=False)
        st.session_state.employees_df.to_csv("data/enterprise_employees.csv", index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save changes to CSV: {e}")
        return False

def add_employee_to_session(first_name, last_name, corrected_company_name, user_input):
    """Adds the new employee record to the session state DataFrame."""
    company_row = st.session_state.companies_df[st.session_state.companies_df['CompanyName'] == corrected_company_name]
    if not company_row.empty:
        company_id = company_row.iloc[0]['CompanyID']
        new_employee = {
            "EmployeeID": str(uuid.uuid4()), "FirstName": first_name, "LastName": last_name,
            "Email": f"{first_name.lower()}.{last_name.lower()}@example.com", "Title": "Newly Registered",
            "CompanyID": company_id, "SubmittedCompanyName": user_input
        }
        st.session_state.employees_df.loc[len(st.session_state.employees_df)] = new_employee
    else:
        st.error(f"Could not find CompanyID for '{corrected_company_name}'. Employee not saved.")

# --- Global Setup & Caching ---
@st.cache_resource
def get_semantic_agent(companies_df):
    """Loads the heavy semantic agent only once."""
    canonical_names = companies_df['CompanyName'].tolist()
    return SemanticSearchAgent(canonical_names=canonical_names)

def load_data():
    """Loads data into the session state."""
    if st.session_state.companies_df is None:
        try:
            st.session_state.companies_df = pd.read_csv("data/enterprise_companies.csv")
            st.session_state.employees_df = pd.read_csv("data/enterprise_employees.csv")
        except FileNotFoundError:
            return False
    return True

# --- Main App Execution ---
if not load_data():
    st.error("Data files not found. Please run `python scripts/generate_enterprise_data.py` first.")
else:
    semantic_agent = get_semantic_agent(st.session_state.companies_df)
    st.title("🛡️ AI Agent Squad: Data Standardization & Learning")
    
    # *** NEW: Display success message from previous action ***
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None # Clear message after showing it

    tab1, tab2 = st.tabs(["➡️ New Employee Entry", f"📝 Admin Validation Queue ({len(st.session_state.flagged_items)})"])

    with tab1:
        # ... (código do form da tab1 permanece o mesmo) ...
        col1, col2 = st.columns((1, 1.2))
        with col1:
            st.header("Registration Form")
            with st.form("employee_form"):
                first_name = st.text_input("First Name", "Alex")
                last_name = st.text_input("Last Name", "Taylor")
                user_input_company = st.text_input("Company Name", "Rodes cures cat")
                submitted = st.form_submit_button("Engage AI Agent Squad")

        with col2:
            # ... (código do mission log da tab1 permanece o mesmo) ...
            if submitted:
                # ... (o mesmo código para rodar o pipeline e mostrar o veredito) ...
                 with st.status("Agent Pipeline Initialized...", expanded=True) as status:
                    st.write("TriageAgent is performing a high-speed lexical scan...")
                    time.sleep(1)
                    final_result = run_standardization_pipeline(user_input_company, semantic_agent)
                    evidence = final_result.get("evidence", {})
                    if evidence:
                        st.write(f"TriageAgent Result: Ambiguous match (`{evidence.get('best_match_lexical')}`). Escalating...")
                        time.sleep(1); st.write("SemanticSearchAgent is analyzing contextual meaning...")
                        time.sleep(1); st.write(f"SemanticAgent Result: Strong semantic link to `{evidence.get('best_match_semantic')}`.")
                        time.sleep(1); st.write("DecisionAgent is reviewing all evidence...")
                        time.sleep(1)
                    status.update(label="Mission Complete!", state="complete", expanded=False)
                
                 st.subheader("Final Verdict")
                 action = final_result.get("action")
                 best_match = final_result.get("best_match")
                 reason = final_result.get("reason")
                
                 if action == "AUTO_CORRECT":
                    st.success(f"✅ **Action: Auto-Corrected to `{best_match}`**")
                    add_employee_to_session(first_name, last_name, best_match, user_input_company)
                    if save_dataframes():
                        st.toast("Employee record saved to CSV!", icon="💾")
                 else: # FLAG_FOR_REVIEW
                    st.error(f"🚩 **Action: Flag for Human Review**")
                    st.session_state.flagged_items.append({
                        "first_name": first_name, "last_name": last_name,
                        "user_input": user_input_company,
                        "best_guess": evidence.get('best_match_semantic', 'N/A'),
                        "is_editing": False
                    })
                
                 st.info(f"**Reasoning:** {reason}")
                 st.subheader("Final Payload"); st.json({"full_reasoning": final_result})

    with tab2:
        st.header("Human-in-the-Loop Feedback Center")
        
        if not st.session_state.flagged_items:
            st.success("The validation queue is empty. All data is clean!")
        else:
            for i, item in enumerate(st.session_state.flagged_items):
                with st.container(border=True):
                    # ... (código da fila de validação permanece o mesmo) ...
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"**Employee:** `{item['first_name']} {item['last_name']}`")
                    c1.write(f"**User Input:** `{item['user_input']}`")
                    c1.write(f"**AI Suggestion:** `{item['best_guess']}`")
                    
                    if item.get("is_editing"):
                        with c2.form(f"edit_form_{i}"):
                            st.write("**Add New Company Details**")
                            new_city = st.text_input("City", key=f"city_{i}")
                            new_state = st.text_input("State (Abbr.)", key=f"state_{i}")
                            new_country = st.text_input("Country (Abbr.)", value="USA", key=f"country_{i}")
                            if st.form_submit_button("Confirm & Save"):
                                new_id = st.session_state.companies_df['CompanyID'].max() + 1
                                new_row = {'CompanyID': new_id, 'CompanyName': item['user_input'], 'City': new_city, 'State': new_state, 'Country': new_country}
                                st.session_state.companies_df.loc[len(st.session_state.companies_df)] = new_row
                                add_employee_to_session(item['first_name'], item['last_name'], item['user_input'], item['user_input'])
                                if save_dataframes():
                                    st.session_state.success_message = f"✅ Success! New company '{item['user_input']}' and employee record were saved to CSV."
                                st.session_state.flagged_items.pop(i)
                                st.rerun()
                    else:
                        if c2.button("✅ Approve Suggestion", key=f"approve_{i}"):
                            add_employee_to_session(item['first_name'], item['last_name'], item['best_guess'], item['user_input'])
                            if save_dataframes():
                                st.session_state.success_message = f"✅ Success! Employee record for '{item['best_guess']}' was saved to CSV."
                            st.session_state.flagged_items.pop(i)
                            st.rerun()

                        if c2.button("🆕 Add New Company", key=f"create_new_{i}"):
                            st.session_state.flagged_items[i]["is_editing"] = True
                            st.rerun()