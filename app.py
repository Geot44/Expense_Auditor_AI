import streamlit as st
import PIL.Image
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="Expense Auditor", page_icon="🛡️")
st.title("🛡️ Policy-First Expense Auditor")

# Securely get your API Key from the Sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.write("### 1. Upload Evidence")
    receipt_file = st.file_uploader("Upload Receipt (Image)", type=['png', 'jpg', 'jpeg'])
    
    # Requirement: Justification Capture [cite: 152]
    purpose = st.text_area("What was the Business Purpose of this expense?")

    st.write("### 2. Policy Reference")
    policy_file = st.file_uploader("Upload Company Policy (PDF)", type=['pdf'])

    if st.button("Run Audit"):
        if receipt_file and policy_file and purpose:
            with st.spinner("Analyzing compliance against policy..."):
                # Load files
                img = PIL.Image.open(receipt_file)
                pdf_reader = pypdf.PdfReader(policy_file)
                policy_text = ""
                for page in pdf_reader.pages:
                    policy_text += page.extract_text()

                # The "Magic" Prompt: Combining receipt, purpose, and policy [cite: 144, 159]
                prompt = f"""
                You are a strict Corporate Finance Auditor. 
                1. Extract Merchant, Date, Amount, and Currency from this receipt.
                2. Read the following Company Policy: {policy_text[:5000]} 
                3. The employee justification is: "{purpose}"
                4. Compare the receipt and purpose against the policy rules.
                
                Return a response in this EXACT format:
                STATUS: [Approved / Flagged / Rejected]
                EXPLANATION: [1-sentence citing the specific policy rule]
                EXTRACTED DATA: [Merchant, Date, Amount]
                """
                
                response = model.generate_content([prompt, img])
                
                # Traffic Light Visualization 
                if "Approved" in response.text:
                    st.success(response.text)
                elif "Flagged" in response.text:
                    st.warning(response.text)
                else:
                    st.error(response.text)
        else:
            st.warning("Please provide a receipt, a policy file, and a business purpose.")
