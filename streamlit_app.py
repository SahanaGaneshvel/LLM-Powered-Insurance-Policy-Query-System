import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Policy Query System", layout="centered")
st.title("LLM-Powered Insurance Policy Query System")

# Tabs for main actions
tabs = st.tabs(["Index Documents", "Query Policies", "Weekly Report"])

# --- Index Documents Tab ---
with tabs[0]:
    st.header("Index Policy Documents")
    st.write("Process and index all policy documents in /data/policies/.")
    if st.button("Index Documents", key="index_btn"):
        with st.spinner("Indexing documents..."):
            try:
                resp = requests.post(f"{API_URL}/index")
                if resp.status_code == 200:
                    st.success(resp.json().get("status", "Indexing complete."))
                else:
                    st.error(f"Indexing failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Query Policies Tab ---
with tabs[1]:
    st.header("Query Policies")
    st.write("Enter your insurance query to retrieve relevant policy clauses and get an LLM-powered decision.")
    query = st.text_area("Your insurance query:", "46-year-old male, knee surgery in Pune, 3-month-old insurance policy", key="query_input")
    top_k = st.slider("Number of relevant clauses to retrieve", 1, 10, 5, key="topk_slider")
    if st.button("Submit Query", key="query_btn"):
        with st.spinner("Processing query..."):
            try:
                resp = requests.post(f"{API_URL}/query", json={"query": query, "top_k": top_k})
                if resp.status_code == 200:
                    data = resp.json()
                    st.subheader("LLM Decision")
                    st.markdown(f"**Decision:** {data['decision'].get('decision', 'N/A').capitalize()}")
                    st.markdown(f"**Amount:** {data['decision'].get('amount', 'N/A')}")
                    st.markdown(f"**Justification:** {data['decision'].get('justification', 'N/A')}")
                    st.markdown("**References:**")
                    for ref in data['decision'].get('references', []):
                        st.markdown(f"- {ref}")

                    with st.expander("Show Structured Query"):
                        st.json(data["structured"])
                    with st.expander("Show Top Clauses"):
                        for i, clause in enumerate(data["clauses"], 1):
                            st.markdown(f"**{i}. {clause['doc_name']} (Page {clause['page']})**")
                            st.markdown(f"> {clause.get('text', '')[:300]}{'...' if len(clause.get('text', '')) > 300 else ''}")
                else:
                    st.error(f"Query failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Weekly Report Tab ---
with tabs[2]:
    st.header("Weekly Policy Improvement Report")
    st.write("Analyze common failure reasons and query statistics.")
    if st.button("Show Report", key="report_btn"):
        with st.spinner("Fetching report..."):
            try:
                resp = requests.get(f"{API_URL}/report")
                if resp.status_code == 200:
                    report = resp.json()
                    st.markdown(f"**Total Queries:** {report.get('total_queries', 0)}")
                    st.markdown(f"**Total Rejections:** {report.get('total_rejections', 0)}")
                    st.markdown("**Common Failure Reasons:**")
                    for reason, count in report.get('common_failure_reasons', {}).items():
                        st.markdown(f"- {reason} ({count})")
                else:
                    st.error(f"Could not fetch report: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}") 