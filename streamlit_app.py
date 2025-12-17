import streamlit as st
from master_agent import run_pipeline
from report_generator import generate_pdf
import os

# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Agentic AI – Molecule Repurposing Demo",
    layout="wide"
)

# Title Section
st.markdown("""
# Agentic AI – Molecule Repurposing Prototype
This tool analyzes a molecule using mock clinical, market, patent, and scientific insights.
""")

st.markdown("---")

# ------------------------------
# User Input Section
# ------------------------------
st.subheader("Enter Your Query")
prompt = st.text_input(
    "Type a molecule analysis prompt:",
    value="Evaluate molecule_x for respiratory unmet need"
)

run_button = st.button("Run Analysis", type="primary")

# ------------------------------
# Run Pipeline
# ------------------------------
if run_button:
    with st.spinner("Analyzing data across modules…"):
        results = run_pipeline(prompt)

    st.success("Analysis completed successfully!")
    st.markdown("---")

    # ==========================
    # EXECUTIVE SUMMARY
    # ==========================
    st.markdown("## Executive Summary")
    st.info(results["summary"])
    st.markdown("---")

    # ==========================
    # MARKET INSIGHTS
    # ==========================
    with st.container():
        st.markdown("### Market Insights")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Therapy Area:** {results['market']['therapy_area']}")
            st.write(f"**Market Size (India):** {results['market']['market_size_patients_india']} patients")
            st.write(f"**CAGR:** {results['market']['cagr']*100:.1f}%")

        with col2:
            st.write("**Top Competitors:**")
            for comp in results["market"]["top_competitors"]:
                st.write(f"- {comp}")

        st.caption(results["market"]["notes"])
    st.markdown("---")

    # ==========================
    # CLINICAL TRIALS
    # ==========================
    st.markdown("### Clinical Trials Overview")
    if results["trials"]:
        for t in results["trials"]:
            with st.expander(f"Trial ID: {t['id']}"):
                st.write(f"**Indication:** {t['indication']}")
                st.write(f"**Phase:** {t['phase']}")
                st.write(f"**Sponsor:** {t['sponsor']}")
                st.write(f"**Status:** {t['status']}")
    else:
        st.warning("No clinical trials found for this molecule.")
    st.markdown("---")

    # ==========================
    # PATENT LANDSCAPE
    # ==========================
    st.markdown("###  Patent Landscape")
    if results["patents"]:
        for p in results["patents"]:
            with st.expander(f"Patent Family: {p['family']}"):
                st.write(f"**Title:** {p['title']}")
                st.write(f"**Expiry:** {p['expiry']}")
                st.write(f"**Risk Level:** {p['risk']}")
    else:
        st.warning("No patents identified for this molecule.")
    st.markdown("---")

    # ==========================
    # WEB INSIGHTS
    # ==========================
    st.markdown("###  Scientific & Web Insights")
    if results["web"]:
        for w in results["web"]:
            st.write(f"- **{w['source']}:** {w['snippet']}")
    else:
        st.warning("No web insights found.")
    st.markdown("---")

    # ==========================
    # INTERNAL NOTES
    # ==========================
    st.markdown("###  Internal Insights")
    for k, v in results["internal"].items():
        st.write(f"- **{k.replace('_', ' ').title()}:** {v}")
    st.markdown("---")

    # ==========================
    # SAVE RESULTS
    # ==========================
    st.session_state["results"] = results


# ------------------------------
# PDF Report Section
# ------------------------------
st.header("Download Full PDF Report")

if st.button(" Generate PDF Report"):
    if "results" not in st.session_state:
        st.error("Please run the analysis first!")
    else:
        pdf_path = generate_pdf(st.session_state["results"])
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name="opportunity_report.pdf",
                mime="application/pdf"
            )
