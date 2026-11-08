import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import re

# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================
st.set_page_config(
    page_title="Audit COBIT 5 | CV Muria Maju Makmur",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# DESAIN: NATURAL DUSTY PINK, PASTEL, DAN TIPOGRAFI
# ==========================================================
st.markdown(
    r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --rose: #B77F8D;
        --rose-dark: #8C5D69;
        --rose-soft: #F5E9EC;
        --rose-pale: #FBF4F5;
        --sage: #8FA394;
        --sage-soft: #EEF2ED;
        --lavender: #B7A9BB;
        --sand: #F2ECE4;
        --ink: #443C40;
        --muted: #82777B;
        --line: #EAE0E2;
        --paper: #FFFFFF;
        --canvas: #FBF8F7;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', 'Segoe UI', sans-serif;
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(251, 248, 247, 0.94);
    }

    .block-container {
        max-width: 1260px;
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
    }

    h1, h2, h3, h4, h5, h6,
    [data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
        letter-spacing: -0.025em;
    }

    h1 { color: var(--rose-dark); font-weight: 800 !important; }
    h2, h3, h4 { color: var(--rose-dark); font-weight: 750 !important; }
    p, li, label, input, textarea, button, small { font-family: 'DM Sans', 'Segoe UI', sans-serif !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #FFFCFB;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--rose-dark);
    }
    .side-brand {
        background: linear-gradient(145deg, #F7E9ED, #F3EBE6);
        border: 1px solid #EEDDE1;
        border-radius: 16px;
        padding: 15px 16px;
        margin: 3px 0 18px 0;
    }
    .side-brand .side-kicker {
        color: #98727C;
        text-transform: uppercase;
        letter-spacing: .12em;
        font-size: .66rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .side-brand .side-title {
        color: #76515D;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 1.03rem;
        line-height: 1.35;
    }
    .side-brand .side-sub {
        color: #8D777D;
        font-size: .78rem;
        margin-top: 5px;
        line-height: 1.45;
    }

    /* Hero header */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(112deg, #F3E2E6 0%, #F8EFF0 57%, #EEF1EB 100%);
        border: 1px solid #EADDE0;
        border-radius: 23px;
        padding: 31px 34px 28px 34px;
        margin: 0 0 25px 0;
        box-shadow: 0 12px 34px rgba(111, 78, 87, 0.055);
    }
    .hero:after {
        content: '';
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        right: -72px;
        top: -115px;
        background: rgba(255,255,255,.32);
        border: 1px solid rgba(255,255,255,.55);
    }
    .hero-kicker {
        color: #956D78;
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 800;
        margin-bottom: 11px;
    }
    .hero-title {
        color: #674953;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: clamp(1.75rem, 3vw, 2.45rem);
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -.045em;
        margin: 0 0 10px 0;
        max-width: 760px;
    }
    .hero-description {
        color: #77666B;
        font-size: .98rem;
        line-height: 1.7;
        max-width: 780px;
        margin: 0;
    }
    .hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 19px;
    }
    .hero-tag {
        color: #76515D;
        background: rgba(255,255,255,.62);
        border: 1px solid rgba(183,127,141,.23);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: .75rem;
        font-weight: 700;
    }

    /* Section headings */
    .section-head {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #76515D;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.22rem;
        font-weight: 800;
        letter-spacing: -.025em;
        margin: 1.55rem 0 .25rem 0;
    }
    .section-mark {
        width: 7px;
        height: 24px;
        border-radius: 9px;
        background: linear-gradient(180deg, #C28E9B, #9B6C79);
        display: inline-block;
    }
    .section-sub {
        color: var(--muted);
        font-size: .88rem;
        line-height: 1.6;
        margin: 0 0 1.05rem 17px;
    }

    /* Progress and domain information */
    .progress-panel {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 15px;
        padding: 14px 17px 9px 17px;
        margin: 2px 0 17px 0;
        box-shadow: 0 4px 16px rgba(111,78,87,.035);
    }
    .domain-intro {
        background: linear-gradient(110deg, #F7ECEF, #F5F1ED);
        border: 1px solid #EDE0E3;
        border-left: 4px solid #B77F8D;
        color: #70545D;
        border-radius: 13px;
        padding: 14px 17px;
        margin: 5px 0 16px 0;
        font-size: .9rem;
        line-height: 1.6;
    }
    .domain-intro strong {
        color: #76515D;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .98rem;
    }
    .domain-count {
        display: inline-block;
        color: #8C6670;
        background: #FFFFFF;
        border: 1px solid #E9D8DD;
        border-radius: 999px;
        padding: 3px 9px;
        font-size: .7rem;
        font-weight: 700;
        margin-left: 7px;
    }

    /* Question cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,.96);
        border: 1px solid #EAE1E3;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(106, 76, 84, .035);
        padding: 2px 2px;
        margin-bottom: 12px;
    }
    .question-topline {
        display: flex;
        align-items: center;
        gap: 9px;
        margin: 2px 0 9px 0;
    }
    .question-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 34px;
        height: 27px;
        border-radius: 8px;
        color: #865C68;
        background: #F6E9EC;
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .02em;
    }
    .question-kicker {
        color: #9B8188;
        font-size: .69rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .1em;
    }
    .question-text {
        color: #494145;
        font-size: .94rem;
        line-height: 1.65;
        font-weight: 600;
        margin: 0 0 13px 0;
    }
    .field-caption {
        color: #897A7E;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .04em;
        margin-bottom: 3px;
    }
    .method-note {
        background: #F0F3EE;
        border: 1px solid #E0E8DF;
        border-radius: 12px;
        color: #667568;
        padding: 12px 15px;
        font-size: .82rem;
        line-height: 1.55;
        margin: 8px 0 14px 0;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #897C80;
        font-family: 'DM Sans', sans-serif !important;
        font-size: .88rem;
        font-weight: 700;
        padding: 12px 17px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #865B67;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #B77F8D;
        height: 3px;
        border-radius: 5px;
    }
    div[data-baseweb="tab-border"] { background-color: #EDE3E5; }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 10px;
        border-color: #E5D9DC;
        background: #FFFEFE;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #B77F8D;
        box-shadow: 0 0 0 1px #B77F8D;
    }
    [data-testid="stWidgetLabel"] p {
        color: #71666A;
        font-size: .78rem;
        font-weight: 700;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #EAE1E3;
        border-radius: 16px;
        padding: 15px 17px;
        box-shadow: 0 5px 17px rgba(106,76,84,.04);
        min-height: 112px;
    }
    div[data-testid="stMetricLabel"] {
        color: #887B7F;
        font-weight: 650;
        font-size: .78rem;
    }
    div[data-testid="stMetricValue"] {
        color: #76515D;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.55rem;
        font-weight: 800;
    }
    div[data-testid="stMetricDelta"] { font-size: .72rem; }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 11px;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700;
        min-height: 2.7rem;
        border: 1px solid #E4D1D7;
        transition: all .18s ease;
    }
    .stButton > button[kind="primary"] {
        background: #A96F7E;
        border-color: #A96F7E;
        color: #FFFFFF;
    }
    .stButton > button[kind="primary"]:hover {
        background: #8E5D69;
        border-color: #8E5D69;
        color: #FFFFFF;
        transform: translateY(-1px);
    }
    .stDownloadButton > button {
        background: #F6EAED;
        color: #76515D;
        border-color: #EAD8DE;
    }
    .stDownloadButton > button:hover {
        background: #EFDEE3;
        border-color: #D7B9C2;
        color: #684851;
    }

    /* Dataframe, progress, alerts */
    [data-testid="stDataFrame"] {
        border: 1px solid #EAE1E3;
        border-radius: 13px;
        overflow: hidden;
    }
    div[data-testid="stProgressBar"] > div > div > div {
        background: linear-gradient(90deg, #B77F8D, #D2A9B2);
    }
    [data-testid="stAlert"] { border-radius: 12px; }

    .footer {
        color: #8A7D81;
        font-size: .77rem;
        line-height: 1.7;
        border-top: 1px solid #EAE1E3;
        padding-top: 17px;
        margin-top: 30px;
    }

    @media (max-width: 780px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .hero { padding: 24px 21px; border-radius: 18px; }
        .hero-title { font-size: 1.75rem; }
        .section-head { font-size: 1.08rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# DATA INDIKATOR - SESUAI BAB III TUGAS 1
# ==========================================================
DOMAINS = {
    "EDM": [
        "Apakah manajemen telah menetapkan pihak yang bertanggung jawab dalam mengawasi penggunaan sistem informasi penjualan dan persediaan?",
        "Apakah manajemen melakukan evaluasi terhadap manfaat penggunaan sistem informasi dalam mendukung kegiatan operasional perusahaan?",
        "Apakah manajemen melakukan pemantauan terhadap risiko yang dapat memengaruhi transaksi penjualan, persediaan, dan ketersediaan sistem?",
        "Apakah manajemen memberikan arahan mengenai penggunaan sumber daya dan pengendalian sistem informasi sesuai kebutuhan perusahaan?",
        "Apakah manajemen melakukan pemantauan terhadap laporan dan tindak lanjut permasalahan sistem informasi?",
    ],
    "APO": [
        "Apakah perusahaan memiliki perencanaan atau prosedur pengelolaan sistem informasi yang mendukung kegiatan penjualan dan persediaan?",
        "Apakah kebutuhan sistem informasi telah disesuaikan dengan kebutuhan proses bisnis perusahaan?",
        "Apakah pengelolaan sistem informasi telah memperhatikan kesesuaian antara proses bisnis dan teknologi yang digunakan?",
        "Apakah perusahaan melakukan evaluasi terhadap kebutuhan pengembangan atau peningkatan sistem informasi?",
        "Apakah perusahaan mengidentifikasi dan mengelola risiko yang berkaitan dengan kesalahan transaksi, ketidaksesuaian stok, dan kehilangan data?",
    ],
    "BAI": [
        "Apakah kebutuhan sistem informasi penjualan dan persediaan telah dianalisis sebelum dilakukan pengembangan atau pengadaan sistem?",
        "Apakah pengembangan atau pengadaan sistem informasi dilakukan berdasarkan kebutuhan dan kriteria yang telah ditentukan?",
        "Apakah pengguna mendapatkan informasi atau pelatihan ketika terdapat penerapan atau perubahan sistem informasi?",
        "Apakah setiap perubahan pada aplikasi, konfigurasi, atau data sistem dilakukan melalui persetujuan dan dokumentasi?",
        "Apakah sistem atau pembaruan sistem diuji terlebih dahulu sebelum digunakan dalam kegiatan operasional?",
    ],
    "DSS": [
        "Apakah kegiatan operasional sistem informasi penjualan dan persediaan dipantau secara rutin untuk memastikan sistem berjalan dengan baik?",
        "Apakah gangguan atau keluhan pengguna terkait sistem informasi dicatat dan ditindaklanjuti?",
        "Apakah akses pengguna terhadap sistem informasi dibatasi berdasarkan tugas dan tanggung jawab masing-masing?",
        "Apakah perusahaan melakukan pencadangan data secara berkala dan memiliki prosedur pemulihan data apabila terjadi gangguan?",
        "Apakah transaksi penjualan, pembayaran, barang masuk, dan barang keluar diperiksa untuk memastikan kelengkapan serta keabsahan pencatatannya?",
    ],
    "MEA": [
        "Apakah kinerja sistem informasi dan aktivitas penjualan serta persediaan dipantau secara berkala?",
        "Apakah pengendalian terhadap pencatatan transaksi, persediaan, dan akses pengguna dievaluasi secara berkala?",
        "Apakah penggunaan sistem informasi dievaluasi berdasarkan kebijakan internal dan ketentuan yang berlaku?",
        "Apakah hasil pemantauan dan evaluasi sistem informasi digunakan sebagai bahan perbaikan pengelolaan sistem?",
        "Apakah permasalahan sistem informasi, kesalahan transaksi, dan ketidaksesuaian persediaan ditindaklanjuti sampai selesai?",
    ],
}

DOMAIN_NAMES = {
    "EDM": "Evaluate, Direct and Monitor",
    "APO": "Align, Plan and Organize",
    "BAI": "Build, Acquire and Implement",
    "DSS": "Deliver, Service and Support",
    "MEA": "Monitor, Evaluate and Assess",
}

DOMAIN_FOCUS = {
    "EDM": "Evaluasi, pengarahan, dan pemantauan tata kelola teknologi informasi.",
    "APO": "Penyelarasan, perencanaan, pengorganisasian, dan pengelolaan risiko TI.",
    "BAI": "Pembangunan, pengadaan, perubahan, dan penerapan solusi TI.",
    "DSS": "Operasional, layanan, keamanan, dan dukungan teknologi informasi.",
    "MEA": "Pemantauan, evaluasi, dan penilaian kinerja serta pengendalian TI.",
}

SCORE = {"Ya": 2, "Sebagian": 1, "Tidak": 0, "TDV": None, "TR": None}
OPTIONS = ["Ya", "Sebagian", "Tidak", "TDV", "TR"]

# ==========================================================
# SESSION STATE
# ==========================================================
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "evidence" not in st.session_state:
    st.session_state.evidence = {}
if "evidence_files" not in st.session_state:
    # Disimpan dalam memori sesi sampai paket audit diunduh.
    st.session_state.evidence_files = {}

# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
          <div class="side-kicker">Audit Information System</div>
          <div class="side-title">COBIT 5<br>Assessment Workspace</div>
          <div class="side-sub">CV Muria Maju Makmur · Penjualan & Persediaan</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Identitas Pemeriksaan")
    st.caption("Lengkapi identitas sebelum mengisi kuesioner.")
    auditor = st.text_input("Nama Auditor", placeholder="Nama lengkap auditor")
    audit_date = st.date_input("Tanggal Audit", value=date.today(), format="DD/MM/YYYY")
    respondent = st.text_input("Pihak yang Diaudit", placeholder="Nama atau jabatan responden")

    st.markdown("---")
    st.markdown("### Panduan Skor")
    st.markdown(
        "<div class='method-note'><b>Ya</b> = 2 &nbsp; · &nbsp; <b>Sebagian</b> = 1 &nbsp; · &nbsp; <b>Tidak</b> = 0<br><b>TDV</b> = Tidak Dapat Diverifikasi<br><b>TR</b> = Tidak Relevan</div>",
        unsafe_allow_html=True,
    )
    st.caption("TDV dan TR tidak dimasukkan dalam perhitungan. Pilih jawaban berdasarkan bukti pemeriksaan, bukan perkiraan.")
    st.markdown("---")
    st.markdown("**Objek audit**")
    st.caption("CV Muria Maju Makmur")
    st.markdown("**Ruang lingkup**")
    st.caption("Sistem Informasi Penjualan dan Persediaan")

# ==========================================================
# HEADER UTAMA
# ==========================================================
st.markdown(
    """
    <section class="hero">
      <div class="hero-kicker">Tugas 2 · Audit Sistem Informasi</div>
      <div class="hero-title">Dashboard Audit COBIT 5</div>
      <p class="hero-description">Instrumen penilaian tata kelola dan pengendalian Sistem Informasi Penjualan dan Persediaan pada CV Muria Maju Makmur.</p>
      <div class="hero-tags">
        <span class="hero-tag">CV Muria Maju Makmur</span>
        <span class="hero-tag">5 Domain COBIT 5</span>
        <span class="hero-tag">25 Indikator Pemeriksaan</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# HITUNG PROGRES
# ==========================================================
answered_count = sum(
    1
    for domain, questions in DOMAINS.items()
    for idx in range(1, len(questions) + 1)
    if st.session_state.answers.get(f"{domain}_{idx}", "TDV") not in ["TDV", "TR"]
)

st.markdown(
    "<div class='section-head'><span class='section-mark'></span>Formulir Pemeriksaan</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-sub'>Isi jawaban untuk setiap indikator dan lengkapi bukti atau keterangan pendukung.</div>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    top_progress, top_count = st.columns([4, 1])
    with top_progress:
        st.progress(answered_count / 25, text=f"Indikator yang sudah dinilai: {answered_count} dari 25")
    with top_count:
        st.metric("Total indikator", "25")

# ==========================================================
# TAB DOMAIN DAN KARTU PERTANYAAN
# ==========================================================
tabs = st.tabs([f"{domain}  ·  05" for domain in DOMAINS])
for tab, (domain, questions) in zip(tabs, DOMAINS.items()):
    with tab:
        st.markdown(
            f"<div class='domain-intro'><strong>{domain} — {DOMAIN_NAMES[domain]}</strong><span class='domain-count'>5 indikator</span><br>{DOMAIN_FOCUS[domain]}</div>",
            unsafe_allow_html=True,
        )
        for idx, question in enumerate(questions, start=1):
            key = f"{domain}_{idx}"
            current = st.session_state.answers.get(key, "TDV")
            if current not in OPTIONS:
                current = "TDV"

            with st.container(border=True):
                st.markdown(
                    f"<div class='question-topline'><span class='question-badge'>{idx:02d}</span><span class='question-kicker'>Indikator {domain}-{idx:02d}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='question-text'>{question}</div>", unsafe_allow_html=True)
                answer_col, evidence_col = st.columns([1, 2.25], gap="large")
                with answer_col:
                    selected = st.selectbox(
                        "Jawaban pemeriksaan",
                        OPTIONS,
                        index=OPTIONS.index(current),
                        key=f"answer_{key}",
                    )
                    st.session_state.answers[key] = selected
                with evidence_col:
                    evidence_value = st.text_input(
                        "Bukti / keterangan pendukung",
                        value=st.session_state.evidence.get(key, ""),
                        key=f"evidence_{key}",
                        placeholder="Tuliskan sumber atau ringkasan bukti pemeriksaan",
                    )
                    st.session_state.evidence[key] = evidence_value

                uploaded_files = st.file_uploader(
                    "Lampirkan dokumen atau foto bukti (opsional)",
                    type=["pdf", "doc", "docx", "xls", "xlsx", "csv", "txt", "png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    key=f"upload_{key}",
                    help="Format: PDF, Word, Excel, CSV, TXT, PNG, JPG/JPEG. Beberapa file dapat dipilih sekaligus.",
                )
                if uploaded_files:
                    st.session_state.evidence_files[key] = [
                        {
                            "name": Path(item.name).name,
                            "type": item.type or "application/octet-stream",
                            "bytes": item.getvalue(),
                        }
                        for item in uploaded_files
                    ]
                elif key not in st.session_state.evidence_files:
                    st.session_state.evidence_files[key] = []

                current_files = st.session_state.evidence_files.get(key, [])
                if current_files:
                    st.caption("Lampiran: " + " · ".join(item["name"] for item in current_files))

# ==========================================================
# BENTUK DATA DAN REKAPITULASI
# ==========================================================
records = []
for domain, questions in DOMAINS.items():
    for idx, question in enumerate(questions, start=1):
        key = f"{domain}_{idx}"
        answer = st.session_state.answers.get(key, "TDV")
        records.append(
            {
                "Domain": domain,
                "Nomor": idx,
                "Indikator": question,
                "Jawaban": answer,
                "Nilai": SCORE[answer],
                "Bukti/Keterangan": st.session_state.evidence.get(key, ""),
                "Jumlah Lampiran": len(st.session_state.evidence_files.get(key, [])),
                "Nama File Lampiran": "; ".join(
                    item["name"] for item in st.session_state.evidence_files.get(key, [])
                ),
            }
        )

df = pd.DataFrame(records)
summary = []
for domain in DOMAINS:
    subset = df[df["Domain"] == domain]
    assessed = subset[subset["Nilai"].notna()]
    total = int(assessed["Nilai"].sum()) if len(assessed) else 0
    max_score = int(len(assessed) * 2)
    percent = (total / max_score * 100) if max_score else None

    if percent is None:
        category = "Belum dapat dihitung"
    elif percent >= 81:
        category = "Sangat Baik"
    elif percent >= 61:
        category = "Baik"
    elif percent >= 41:
        category = "Cukup"
    elif percent >= 21:
        category = "Kurang"
    else:
        category = "Sangat Kurang"

    summary.append(
        {
            "Domain": domain,
            "Indikator Dinilai": len(assessed),
            "Total Nilai": total,
            "Nilai Maksimal": max_score,
            "Persentase": round(percent, 2) if percent is not None else None,
            "Kategori": category,
        }
    )

summary_df = pd.DataFrame(summary)
valid = df[df["Nilai"].notna()]
not_assessed = int(df["Nilai"].isna().sum())
if len(valid):
    total_score = int(valid["Nilai"].sum())
    max_total = int(len(valid) * 2)
    overall = total_score / max_total * 100 if max_total else 0
else:
    total_score = 0
    max_total = 0
    overall = None

# ==========================================================
# DASHBOARD HASIL
# ==========================================================
st.markdown(
    "<div class='section-head'><span class='section-mark'></span>Ringkasan Hasil Audit</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-sub'>Nilai dihitung otomatis berdasarkan jawaban yang dapat dinilai (Ya, Sebagian, atau Tidak).</div>",
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4, gap="medium")
m1.metric("Indikator dinilai", f"{len(valid)} / 25")
m2.metric("Total nilai", f"{total_score} / {max_total}" if max_total else "—")
m3.metric("Persentase keseluruhan", f"{overall:.2f}%" if overall is not None else "—")
m4.metric("Belum dinilai", f"{not_assessed}")

summary_col, chart_col = st.columns([1.12, 1], gap="large")
with summary_col:
    with st.container(border=True):
        st.markdown("#### Rekapitulasi per Domain")
        display_summary = summary_df.copy()
        display_summary["Persentase"] = display_summary["Persentase"].apply(
            lambda value: f"{value:.2f}%" if pd.notna(value) else "—"
        )
        st.dataframe(display_summary, hide_index=True, width="stretch")
with chart_col:
    with st.container(border=True):
        st.markdown("#### Grafik Penilaian Domain")
        plot_df = summary_df.dropna(subset=["Persentase"])
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(6.2, 3.7))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")
            bars = ax.bar(
                plot_df["Domain"],
                plot_df["Persentase"],
                color=["#B77F8D", "#C99EAA", "#A7B7A7", "#B8AABD", "#D0BFAE"][: len(plot_df)],
                width=0.58,
                zorder=3,
            )
            ax.set_ylim(0, 112)
            ax.set_ylabel("Persentase (%)", color="#82777B", fontsize=9)
            ax.set_title("Persentase Penilaian per Domain", color="#76515D", fontsize=11, fontweight="bold", pad=13)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.spines["bottom"].set_color("#EAE0E2")
            ax.tick_params(axis="x", colors="#594E52", labelsize=9, length=0, pad=8)
            ax.tick_params(axis="y", colors="#8C8285", labelsize=8, length=0)
            ax.grid(axis="y", linestyle=(0, (3, 4)), color="#EDE6E7", linewidth=.8, zorder=0)
            ax.set_axisbelow(True)
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 2,
                    f"{height:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color="#594E52",
                    fontweight="bold",
                )
            fig.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        else:
            st.info("Grafik akan tampil setelah terdapat jawaban yang dapat dinilai.")

# ==========================================================
# EKSPOR TERPADU: SATU ZIP BERISI EXCEL + SEMUA LAMPIRAN
# ==========================================================
st.markdown(
    "<div class='section-head'><span class='section-mark'></span>Ekspor Hasil Pemeriksaan</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-sub'>Satu kali unduh untuk memperoleh seluruh 25 jawaban, rekap lima domain, identitas audit, dan file bukti yang dilampirkan.</div>",
    unsafe_allow_html=True,
)

# Susun identitas dan detail yang selalu berisi seluruh 25 indikator.
identity_df = pd.DataFrame([
    {"Keterangan": "Nama Perusahaan", "Isian": "CV Muria Maju Makmur"},
    {"Keterangan": "Objek Audit", "Isian": "Sistem Informasi Penjualan dan Persediaan"},
    {"Keterangan": "Kerangka Kerja", "Isian": "COBIT 5"},
    {"Keterangan": "Nama Auditor", "Isian": auditor or "Belum diisi"},
    {"Keterangan": "Tanggal Audit", "Isian": audit_date.strftime("%d-%m-%Y")},
    {"Keterangan": "Pihak yang Diaudit", "Isian": respondent or "Belum diisi"},
    {"Keterangan": "Waktu Ekspor", "Isian": datetime.now().strftime("%d-%m-%Y %H:%M:%S")},
])

# Daftar file bukti untuk sheet Excel dan isi folder ZIP.
evidence_records = []
attachment_payloads = []
for domain, questions in DOMAINS.items():
    for idx, question in enumerate(questions, start=1):
        key = f"{domain}_{idx}"
        for file_item in st.session_state.evidence_files.get(key, []):
            safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(file_item["name"]).name).strip("._")
            if not safe_name:
                safe_name = "lampiran"
            archive_path = f"bukti/{domain}/{domain}_{idx:02d}_{safe_name}"
            evidence_records.append({
                "Domain": domain,
                "Nomor Indikator": idx,
                "Indikator": question,
                "Nama File": file_item["name"],
                "Tipe File": file_item["type"],
                "Lokasi dalam ZIP": archive_path,
            })
            attachment_payloads.append((archive_path, file_item["bytes"]))

evidence_df = pd.DataFrame(
    evidence_records,
    columns=["Domain", "Nomor Indikator", "Indikator", "Nama File", "Tipe File", "Lokasi dalam ZIP"],
)

# Buat workbook Excel dengan 4 sheet.
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    identity_df.to_excel(writer, sheet_name="Identitas Audit", index=False)
    export_df = df.copy()
    export_df.insert(0, "Nama Auditor", auditor or "Belum diisi")
    export_df.insert(1, "Tanggal Audit", audit_date.strftime("%d-%m-%Y"))
    export_df.insert(2, "Pihak yang Diaudit", respondent or "Belum diisi")
    export_df.to_excel(writer, sheet_name="Detail Pemeriksaan", index=False)
    summary_df.to_excel(writer, sheet_name="Rekap Domain", index=False)
    evidence_df.to_excel(writer, sheet_name="Daftar Lampiran", index=False)

    # Perapian workbook agar mudah dibaca saat dibuka di Excel.
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    header_fill = PatternFill("solid", fgColor="E8C9D0")
    header_font = Font(name="Aptos", bold=True, color="674953")
    for ws in writer.book.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 30
        for col_idx, column_cells in enumerate(ws.columns, start=1):
            values = [str(cell.value) if cell.value is not None else "" for cell in column_cells[:80]]
            max_len = max((len(v) for v in values), default=10)
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max(max_len + 3, 14), 58)
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)

excel_bytes = excel_buffer.getvalue()

# Satu paket ZIP: workbook dan semua file bukti asli.
zip_buffer = BytesIO()
with ZipFile(zip_buffer, "w", ZIP_DEFLATED) as archive:
    archive.writestr("Hasil_Audit_COBIT5_CV_Muria_Maju_Makmur.xlsx", excel_bytes)
    for archive_path, file_bytes in attachment_payloads:
        archive.writestr(archive_path, file_bytes)
    readme = (
        "PAKET HASIL AUDIT COBIT 5 - CV MURIA MAJU MAKMUR\n\n"
        "Hasil_Audit_COBIT5_CV_Muria_Maju_Makmur.xlsx berisi sheet: Identitas Audit, "
        "Detail Pemeriksaan (25 indikator), Rekap Domain, dan Daftar Lampiran.\n"
        "Folder bukti/ berisi file pendukung yang diunggah untuk masing-masing indikator.\n\n"
        "Nilai TDV dan TR tidak masuk perhitungan. Kategori persentase adalah skala akademik "
        "tugas ini, bukan level kapabilitas resmi COBIT 5.\n"
    )
    archive.writestr("PETUNJUK.txt", readme)

attachment_count = len(attachment_payloads)
c1, c2, c3 = st.columns(3, gap="medium")
c1.metric("Jumlah indikator dalam ekspor", "25")
c2.metric("Jumlah lampiran", str(attachment_count))
c3.metric("Jawaban yang dinilai", f"{len(valid)} / 25")

st.info(
    "Ekspor ini selalu menyertakan seluruh 25 indikator. Jawaban yang belum diisi tetap tercatat sebagai TDV; "
    "jawaban yang sudah dipilih pada sesi ini ikut masuk bersama bukti teks dan lampiran file."
)
st.download_button(
    "Unduh Paket Audit Lengkap (Excel + Bukti) .ZIP",
    data=zip_buffer.getvalue(),
    file_name="Paket_Audit_COBIT5_CV_Muria_Maju_Makmur.zip",
    mime="application/zip",
    type="primary",
    width="stretch",
    help="Satu file ZIP berisi workbook Excel lengkap dan seluruh dokumen/foto bukti yang diunggah.",
)
st.caption(
    "Catatan penyimpanan: jawaban dan file unggahan berada di memori sesi aplikasi. Unduh paket secara berkala. "
    "Jika tab browser dimuat ulang, ditutup, atau server dihentikan, data sesi dapat hilang."
)

st.markdown(
    """
    <div class="footer">
      <b>Catatan metodologi</b><br>
      Jawaban TDV (Tidak Dapat Diverifikasi) dan TR (Tidak Relevan) tidak dimasukkan ke dalam perhitungan. Kategori persentase merupakan skala penilaian akademik pada tugas ini, bukan level kapabilitas resmi COBIT 5. Hasil penilaian bergantung pada jawaban dan bukti pemeriksaan yang dimasukkan auditor.<br><br>
      Dashboard Audit COBIT 5 · Sistem Informasi Penjualan dan Persediaan · CV Muria Maju Makmur<br>
      Jangan unggah dokumen rahasia perusahaan ke aplikasi publik tanpa izin. Untuk penggunaan bersama secara daring, siapkan autentikasi dan penyimpanan permanen yang aman.
    </div>
    """,
    unsafe_allow_html=True,
)
