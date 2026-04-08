# 🛡️ Policy-First Expense Auditor
### **AI-Powered Compliance & Automated Receipt Auditing**

The **Policy-First Expense Auditor** is a professional-grade fintech tool designed to automate corporate expense verification. By leveraging Multimodal Large Language Models (LLMs), it eliminates "spend leakage" by cross-referencing physical receipts against complex, multi-page PDF corporate policies.

---

## 🚀 The Solution
Manual auditing is slow and prone to oversight. This application provides:
* **Instant Multimodal OCR:** High-precision extraction of Merchant, Date, and Amount from images.
* **Semantic Policy Reasoning:** "Reads" and interprets PDF policy clauses to identify spending caps or restricted categories.
* **Automated Flagging:** Categorizes expenses as **Approved**, **Flagged**, or **Rejected** with a clear explanation of the violated policy clause.

---

## 🛠️ Tech Stack
* **Core Engine:** Google Gemini 2.5 Flash
* **Interface:** Streamlit (Professional Wide-layout Dashboard)
* **Language:** Python 3.12
* **Key Libraries:**
    * `google-genai`: Utilizing the latest SDK for high-speed inference.
    * `pypdf`: For semantic text extraction from complex PDF layouts.
    * `Pillow`: For image preprocessing and previewing.
    * `pandas`: Powering session-based audit logs and data management.

---

## ✨ Advanced UX & Resiliency Features
This application is built with a focus on **production-ready resilience**:

* **Dynamic Model Discovery:** Automatically probes the API to find the best available model (2.0 Flash vs. 1.5 Flash), preventing crashes due to regional availability.
* **Exponential Backoff Retry:** Implements custom logic to handle `429 Resource Exhausted` errors, gracefully waiting and retrying during high-traffic periods.
* **Side-by-Side Verification:** A professional "Auditor View" that renders the raw evidence directly next to the AI's extracted data for instant human verification.
* **Session Audit Log:** Uses `st.session_state` to track all audits performed in the current session, allowing users to sort and review their work.

---

## ⚙️ Setup & Installation

### 1. Clone & Environment
Clone the repository and ensure you have Python 3.10 or higher installed.

### 2. Install Dependencies
```bash
pip install streamlit google-genai pypdf pillow pandas google-api-core
```

### 3. Configure API Key
Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/) and enter it into the application sidebar.

### 4. Launch Application
```bash
streamlit run app.py
```

---

## 📈 Future Roadmap
* **Fraud Detection:** Weekend-check logic to flag expenses incurred on non-business days.
* **Batch Auditing:** Support for ZIP file uploads for bulk processing.

---

> **Developer Note:** Built as part of the **Cymonic.ai Project-Based Internship Challenge (Batch 2K26)** by a student of Government Model Engineering College (MEC), Thrikkakara.
