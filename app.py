import streamlit as st
import streamlit.components.v1 as components
import time

from summarizer import summarize_text
from utils import extract_text_from_pdf
from keyword_extractor import extract_keywords

# ------------------ PAGE CONFIG ------------------

st.set_page_config(
    page_title="AI Document Summarizer Pro",
    page_icon="📄",
    layout="centered"
)

# ------------------ LOAD CSS ------------------

try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ------------------ TITLE ------------------

st.markdown("""
<div class="hero">

<h1>📄 AI Document Summarizer Pro</h1>

<p>
Summarize PDF and TXT documents using Natural Language Processing.
</p>

<div class="hero-features">

<span>📄 PDF Support</span>

<span>📁 TXT Support</span>

<span>🧠 NLP Powered</span>

<span>⚡ Instant Summary</span>

</div>

</div>
""", unsafe_allow_html=True)

# ------------------ FILE UPLOAD ------------------

uploaded_file = st.file_uploader(
    "Upload a TXT or PDF file",
    type=["txt", "pdf"]
)

text = ""

if uploaded_file is not None:

    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)

    else:
        text = uploaded_file.read().decode("utf-8")

# ------------------ TEXT AREA ------------------

text = st.text_area(
    "Or Paste Your Text",
    value=text,
    height=300,
    placeholder="Paste your article here..."
)



summary_type = st.selectbox(
    "📏 Summary Length",
    [
        "Short (2 sentences)",
        "Medium (4 sentences)",
        "Detailed (7 sentences)"
    ]
)

if st.button("🚀 Generate Summary"):

    if text.strip():

        # ---------------- Loading Animation ----------------

        progress = st.progress(0)

        status = st.empty()

        status.write("🧠 Initializing AI...")
        progress.progress(20)
        time.sleep(0.4)

        status.write("📖 Reading document...")
        progress.progress(40)
        time.sleep(0.4)

        status.write("📝 Understanding content...")
        progress.progress(70)
        time.sleep(0.4)

        status.write("✨ Generating summary...")

        if summary_type == "Short (2 sentences)":
            sentences = 2

        elif summary_type == "Medium (4 sentences)":
            sentences = 4

        else:
            sentences = 7

        summary = summarize_text(text, sentences)

        progress.progress(100)
        status.success("✅ Summary Generated!")

        time.sleep(0.5)

        progress.empty()
        status.empty()

        # ---------------- Statistics ----------------

        original_words = len(text.split())

        summary_words = len(summary.split())

        compression = round(
            
            (1 - summary_words / original_words) * 100,
            1
        )

        # ---------- Reading Time ----------

        original_reading_time = max(1, round(original_words / 200))
        summary_reading_time = max(1, round(summary_words / 200))
        time_saved = original_reading_time - summary_reading_time

        # ---------------- Analytics Dashboard ----------------

        st.markdown("## 📊 Document Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "📄 Original Words",
                f"{original_words:,}"
            )

        with col2:
            st.metric(
                "📝 Summary Words",
                f"{summary_words:,}"
            )

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "📉 Compression",
                f"{compression}%"
            )

        with col4:
            st.metric(
                "⚡ Time Saved",
                f"{time_saved} min"
            )

        st.divider()

        

        # ---------------- Summary ----------------

        st.subheader("📝 Generated Summary")

        st.text_area(
            "Summary",
            summary,
            height=220
        )

        import streamlit.components.v1 as components

col1, col2 = st.columns(2)

with col1:

    components.html(
        f"""
        <button
            onclick="
                navigator.clipboard.writeText(`{summary}`);
                this.innerHTML='✅ Copied!';
                setTimeout(() => {{
                    this.innerHTML='📋 Copy Summary';
                }}, 2000);
            "
            style="
                width:100%;
                height:50px;
                border:none;
                border-radius:10px;
                background:#2563EB;
                color:white;
                font-size:16px;
                font-weight:bold;
                cursor:pointer;
            "
        >
            📋 Copy Summary
        </button>
        """,
        height=60,
    )

with col2:

        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.subheader("🔑 Top Keywords")

        keywords = extract_keywords(text)

        cols = st.columns(len(keywords))

        for i, keyword in enumerate(keywords):
            cols[i].success(keyword)

        else:
            st.warning("⚠️ Please upload a file or paste some text.")