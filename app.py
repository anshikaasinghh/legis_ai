# app.py

import streamlit as st
import json
import json
from agentic_engine import analyze_case_with_agents, create_pdf_report

import os
os.system("pip install google-generativeai==0.8.3")


# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="LegisAI - Legal Assistant")
st.title("⚖️ LegisAI - Agentic Legal Case Analyzer")

# Sidebar
st.sidebar.title("🧾 Past Interactions")

if st.session_state.chat_history:
    for idx, entry in enumerate(st.session_state.chat_history[::-1], 1):
        with st.sidebar.expander(f"Query {len(st.session_state.chat_history)-idx+1}: {entry['query'][:30]}..."):
            st.write("📌 **Summary**:")
            st.markdown(entry["response"]["summary"])
            st.write("📎 **Legal Issues**:")
            st.write(entry["response"]["legal_issues"])


uploaded_file = st.file_uploader("Upload a legal case (.txt)", type="txt")

if uploaded_file:
    raw_text = uploaded_file.read().decode()
    st.text_area("📄 Uploaded Case Preview", raw_text, height=200)

    query = st.text_input("Ask a legal question or click 'Auto Analyze'", value="Summarize and analyze this case.")

    if st.button("🔍 Run Agentic Analysis"):
        with st.spinner("Running multi-agent system..."):
            result = analyze_case_with_agents(query)

            # Save to session history
            st.session_state.chat_history.append({
                "query": query,
                "response": result
            })

            st.subheader("📌 Summary")
            st.write(result["summary"])

            st.subheader("📎 Legal Issues")
            st.write(result["legal_issues"])

            st.subheader("👥 Parties")
            st.write(result["parties"])

            st.subheader("⚠️ Risks")
            st.write(result["risks"])

            st.subheader("📚 Related Precedents")
            st.write(result["related_precedents"])

            # PDF Report Download
            pdf_path = create_pdf_report(result, file_name="case_analysis_report.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download PDF Report", f, file_name="legal_case_report.pdf")

            # JSON Download
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(result, indent=2),
                file_name="agentic_case_analysis.json",
                mime="application/json"
            )