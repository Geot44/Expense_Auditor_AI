import streamlit as st
import PIL.Image
from google import genai
from google.api_core import exceptions
import pypdf
import time
import pandas as pd

# --- 1. INITIALIZATION & SESSION STATE ---
# This must run before any other Streamlit commands
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

# --- 2. RESILIENT AI LOGIC ---
def safe_generate_content(client, model, contents, max_retries=3):
    """Handles rate limits with exponential backoff."""
    delay = 5
    for i in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents)
        except exceptions.ResourceExhausted:
            if i < max_retries - 1:
                st.warning(f"Quota reached. Retrying in {delay} seconds (Attempt {i+1})...")
                time.sleep(delay)
                delay *= 2
            else:
                st.error("API Quota completely exhausted for today.")
                return None
        except Exception as e:
            st.error(f"AI Engine Error: {e}")
            return None

# --- 3. APP CONFIGURATION ---
st.set_page_config(page_title="Expense Auditor", page_icon="🛡️", layout="wide")
st.title("🛡️ Policy-First Expense Auditor")
st.markdown("Automated compliance auditing using Multimodal LLMs.")

# --- 4. SIDEBAR: AUTH & MODEL DISCOVERY ---
st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

target_model = "gemini-2.5-flash" # Default fallback

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        # Dynamic Discovery to avoid 404/Quota errors
        available_models = client.models.list()
        model_names = []
        for m in available_models:
            methods = getattr(m, 'supported_methods', getattr(m, 'supported_generation_methods', []))
            if "generateContent" in methods:
                model_names.append(m.name)
        
        # Priority: 2.0 Flash (Best OCR) -> 1.5 Flash (Stable)
        for p in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            for name in model_names:
                if p in name:
                    target_model = name
                    break
            if target_model: break
        
        st.sidebar.success(f"Connected: {target_model}")
    except Exception:
        st.sidebar.warning("Using default stable model.")

# --- 5. MAIN UI: SIDE-BY-SIDE EXPERIENCE ---
if api_key:
    col_input, col_preview = st.columns([1, 1])

    with col_input:
        st.write("### 1. Upload Evidence")
        receipt_file = st.file_uploader("Receipt Image", type=['png', 'jpg', 'jpeg'])
        purpose = st.text_area("Business Justification", placeholder="e.g., Client lunch in Kochi")
        
        st.write("### 2. Policy Context")
        policy_file = st.file_uploader("Company Policy (PDF)", type=['pdf'])

    with col_preview:
        st.write("### 3. Visual Verification")
        if receipt_file:
            st.image(receipt_file, caption="Receipt Preview", use_container_width=True)
        else:
            st.info("Upload a receipt to enable visual verification.")

    # --- 6. AUDIT EXECUTION ---
    if st.button("🚀 Run Intelligent Audit", type="primary"):
        if receipt_file and policy_file and purpose:
            with st.spinner("Analyzing compliance..."):
                # Process Files
                img = PIL.Image.open(receipt_file)
                pdf_reader = pypdf.PdfReader(policy_file)
                policy_text = "".join([p.extract_text() for p in pdf_reader.pages])

                prompt = f"""
                You are a Senior Corporate Auditor. 
                1. Extract Merchant, Date, and Total Amount from the receipt.
                2. Compare against this policy snippet: {policy_text[:8000]}
                3. Employee justification: "{purpose}"
                
                Format your response clearly:
                **STATUS**: [APPROVED / FLAGGED / REJECTED]
                **CONFIDENCE**: [Score 0-100%]
                **REASONING**: [Specific policy clause match]
                **ACTION**: [Next steps for the user]
                """

                response = safe_generate_content(client, target_model, [prompt, img])
                
                if response:
                    st.divider()
                    # Visual Flagging Logic
                    res_upper = response.text.upper()
                    status = "APPROVED" if "APPROVED" in res_upper else "FLAGGED" if "FLAGGED" in res_upper else "REJECTED"
                    
                    if status == "APPROVED": st.success("✅ SYSTEM APPROVED")
                    elif status == "FLAGGED": st.warning("⚠️ ATTENTION REQUIRED")
                    else: st.error("❌ POLICY VIOLATION")

                    st.markdown(response.text)

                    # Update History Table
                    st.session_state.audit_history.append({
                        "Time": time.strftime("%H:%M:%S"),
                        "Purpose": purpose[:30],
                        "Status": status,
                        "Model": target_model
                    })
        else:
            st.warning("Please provide all required inputs (Receipt, Policy, and Purpose).")

    # --- 7. SESSION HISTORY TABLE ---
    if st.session_state.audit_history:
        st.divider()
        st.subheader("📜 Session Audit Log")
        history_df = pd.DataFrame(st.session_state.audit_history)
        st.dataframe(history_df, use_container_width=True)
        
        if st.sidebar.button("Clear Session History"):
            st.session_state.audit_history = []
            st.rerun()

else:
    st.info("👋 Enter your API Key in the sidebar to begin.")