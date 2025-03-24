import streamlit as st

def home_page():
    # Main title
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📄 AI Document Processor</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>An AI-powered tool to process, analyze, and extract insights from documents.</h3>", unsafe_allow_html=True)

    # Features Section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📂 *Upload PDF and Extract Text*\n\nEasily upload PDFs and extract data for further analysis.")
        st.success("📑 *Summarize Extracted Text*\n\nGenerate concise summaries using AI-based summarization.")

    with col2:
        st.warning("🌎 *Translate Text*\n\nTranslate extracted text into multiple languages with ease.")
        st.error("🖼 *Extract Images*\n\nAutomatically extract images from PDF documents.")

    with col3:
        st.info("🔍 *Search & Analyze*\n\nSearch, highlight, and analyze important keywords.")
        st.success("🔠 *Transliterate Text*\n\nConvert text between different scripts while preserving meaning.")

