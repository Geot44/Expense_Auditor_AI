import streamlit as st
import PIL.Image

st.set_page_config(page_title="Expense Auditor", page_icon="🛡️")

st.title("🛡️ Policy-First Expense Auditor")
st.subheader("Mid-Term Hackathon Prototype")

# 1. Sidebar for Configuration
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 2. File Uploaders
st.write("### 1. Upload Evidence")
receipt_file = st.file_uploader("Upload Receipt (Image)", type=['png', 'jpg', 'jpeg'])

st.write("### 2. Policy Reference")
policy_file = st.file_uploader("Upload Company Policy (PDF)", type=['pdf'])

# 3. Action Button
if st.button("Run Audit"):
    if receipt_file and policy_file:
        with st.spinner("Analyzing compliance..."):
            # This is a placeholder for your Week 2 logic
            st.success("Files received! Extraction engine initialized.")
            st.info("Status: System is currently identifying Merchant and Amount...")
            
            # Show the image to prove the upload works
            img = PIL.Image.open(receipt_file)
            st.image(img, caption="Uploaded Receipt", width=300)
    else:
        st.warning("Please upload both a receipt and a policy file.")
