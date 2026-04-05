import streamlit as st

st.set_page_config(
    page_title="Jaya Jaya Institut — Early Warning System",
    page_icon="assets/favicon.png" if False else "🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

FOOTER = """
<style>
.footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #0f172a;
    color: #64748b;
    font-size: 0.72rem;
    text-align: center;
    padding: 0.55rem 1rem;
    letter-spacing: 0.03em;
    z-index: 100;
}
.footer span { color: #94a3b8; }
</style>
<div class="footer">
    Jaya Jaya Institut &nbsp;·&nbsp; Sistem Deteksi Dini Dropout &nbsp;·&nbsp;
    Dikembangkan oleh <span>Achmad Miftachul Tama</span> &nbsp;·&nbsp; Model: Random Forest
</div>
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color: #cbd5e1 !important; }

[data-testid="stSidebar"] .stRadio > div { gap: 0.3rem; }
[data-testid="stSidebar"] .stRadio > div > label {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.9rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
    display: block;
    width: 100%;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: #334155 !important;
    border-color: #475569 !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-selected="true"] {
    background: #1d4ed8 !important;
    border-color: #3b82f6 !important;
    color: #fff !important;
}

/* Multiselect in sidebar */
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #1e293b !important;
    border-color: #334155 !important;
}

/* Remove default Streamlit top padding */
.block-container { padding-top: 1.75rem !important; padding-bottom: 4rem !important; }

/* Divider */
hr { border-color: #e2e8f0 !important; margin: 1rem 0 !important; }
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(FOOTER, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem">
        <div style="font-size: 1.1rem; font-weight: 700; color: #f1f5f9 !important;
                    letter-spacing: -0.02em;">Jaya Jaya Institut</div>
        <div style="font-size: 0.72rem; color: #64748b !important;
                    margin-top: 0.2rem; letter-spacing: 0.04em; text-transform: uppercase;">
            Sistem Deteksi Dini Dropout
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:.08em;'
                'text-transform:uppercase;color:#475569 !important;margin-bottom:.5rem">'
                'Halaman</div>', unsafe_allow_html=True)

    page = st.radio(
        label="page",
        options=["Dashboard Overview", "Prediksi Individual"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem;color:#475569 !important;line-height:1.6">
        Jaya Jaya Institut berdiri sejak 2000 dengan reputasi lulusan yang baik.
        Sistem ini membantu staf mendeteksi mahasiswa berisiko dropout sedini mungkin
        untuk pemberian bimbingan khusus.
    </div>
    """, unsafe_allow_html=True)

# ── Route ────────────────────────────────────────────────────────────────────
if page == "Dashboard Overview":
    from pages import overview
    overview.show()
else:
    from pages import prediction
    prediction.show()