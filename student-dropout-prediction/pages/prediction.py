def show():
    import streamlit as st
    import pandas as pd
    import joblib
    import plotly.graph_objects as go

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .field-label {
        font-size: 0.7rem; font-weight: 600; letter-spacing: .08em;
        text-transform: uppercase; color: #94a3b8; margin-bottom: .6rem;
    }
    .result-panel {
        border-radius: 12px;
        border: 1px solid;
        padding: 1.5rem 1.75rem;
        margin-top: .5rem;
    }
    .result-title {
        font-size: 0.7rem; font-weight: 700; letter-spacing: .12em;
        text-transform: uppercase; margin-bottom: .5rem;
    }
    .result-prob {
        font-family: 'DM Mono', monospace;
        font-size: 3rem; font-weight: 500; line-height: 1;
    }
    .result-sub {
        font-size: 0.8rem; color: #64748b; margin-top: .35rem;
    }
    .rec-item {
        display: flex; gap: .75rem; align-items: flex-start;
        padding: .7rem .9rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        margin-bottom: .5rem;
        font-size: .875rem;
    }
    .rec-dot {
        width: 8px; height: 8px; border-radius: 50%;
        margin-top: .35rem; flex-shrink: 0;
    }
    .rec-title { font-weight: 600; margin-bottom: .15rem; font-size: .85rem; }
    .rec-desc  { color: #64748b; font-size: .83rem; line-height: 1.5; }

    .form-section {
       background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.3rem 0.5rem;
        margin-bottom: 0.5rem;
    }

    .stButton > button {
        background: #1e293b; color: white;
        border: none; border-radius: 8px;
        padding: .65rem 1.25rem;
        font-weight: 600; font-size: .9rem;
        transition: background .15s;
        width: 100%;
    }
    .stButton > button:hover { background: #334155; }
    </style>
    """, unsafe_allow_html=True)

    # ── Load ─────────────────────────────────────────────────────────────────
    @st.cache_resource
    def load_assets():
        model     = joblib.load('model/model_rf_dropout.pkl')
        defaults  = joblib.load('model/default_values.pkl')
        cols      = joblib.load('model/feature_columns.pkl')
        threshold = joblib.load('model/threshold.pkl')
        return model, defaults, cols, threshold

    model, defaults, cols, best_threshold = load_assets()

    COURSE_MAP = {
        33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design',
        8014: 'Social Service (Evening)', 9003: 'Agronomy', 9070: 'Communication Design',
        9085: 'Veterinary Nursing', 9119: 'Informatics Engineering', 9130: 'Equinculture',
        9147: 'Management', 9238: 'Social Service', 9254: 'Tourism', 9500: 'Nursing',
        9556: 'Oral Hygiene', 9670: 'Advertising and Marketing Management',
        9773: 'Journalism and Communication', 9853: 'Basic Education',
        9991: 'Management (Evening)',
    }
    course_options = {v: k for k, v in COURSE_MAP.items()}

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("### Prediksi Risiko Individual")
    st.caption(
        "Masukkan data mahasiswa untuk mendapatkan estimasi risiko dropout "
        "berdasarkan model Random Forest yang telah dilatih."
    )
    st.divider()

    # ── Form sections ─────────────────────────────────────────────────────────
    # Section 1 — Identitas
    st.markdown('<div class="field-label">Identitas Mahasiswa</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        selected_course = st.selectbox("Program Studi", options=list(course_options.keys()))
    with c2:
        age = st.number_input("Usia saat Mendaftar", min_value=15, max_value=60, value=20)
    with c3:
        adm_grade = st.number_input("Nilai Seleksi Masuk (0–200)", min_value=0.0,
                                     max_value=200.0, value=125.0, step=0.5)
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2 — Finansial
    st.divider()
    st.markdown('<div class="field-label">Status Finansial</div>', unsafe_allow_html=True)
    cf1, cf2 = st.columns(2)
    with cf1:
        tuition_raw = st.radio("Pembayaran SPP", ["Lancar", "Ada Tunggakan"], horizontal=True)
        tuition = 1 if tuition_raw == "Lancar" else 0
    with cf2:
        scholar_raw = st.radio("Status Beasiswa", ["Penerima", "Non-penerima"], horizontal=True)
        scholarship = 1 if scholar_raw == "Penerima" else 0
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 3 — Akademik (enrolled di luar form agar reaktif)
    st.divider()
    st.markdown('<div class="field-label">Performa Akademik</div>', unsafe_allow_html=True)

    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown("**Semester 1**")
        s1_enroll = st.number_input("Matkul Diambil", 0, 26, 6, key="s1_enroll")
    with cp2:
        st.markdown("**Semester 2**")
        s2_enroll = st.number_input("Matkul Diambil", 0, 26, 6, key="s2_enroll")

    with st.form("pred_form"):
        fp1, fp2 = st.columns(2)
        with fp1:
            s1_app = st.slider(
                f"Matkul Lulus Sem 1  (maks {int(s1_enroll)})",
                0, int(s1_enroll) if s1_enroll > 0 else 1,
                min(5, int(s1_enroll)), key="s1_app"
            )
            s1_grade = st.number_input("Rata-rata Nilai Sem 1 (0–20)",
                                        0.0, 20.0, 12.0, key="s1_grade")
        with fp2:
            s2_app = st.slider(
                f"Matkul Lulus Sem 2  (maks {int(s2_enroll)})",
                0, int(s2_enroll) if s2_enroll > 0 else 1,
                min(5, int(s2_enroll)), key="s2_app"
            )
            s2_grade = st.number_input("Rata-rata Nilai Sem 2 (0–20)",
                                        0.0, 20.0, 12.0, key="s2_grade")
        st.markdown("")
        submitted = st.form_submit_button("Analisis Risiko", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Result ────────────────────────────────────────────────────────────────
    if submitted:
        s1_enroll_val = st.session_state.get("s1_enroll", s1_enroll)
        s2_enroll_val = st.session_state.get("s2_enroll", s2_enroll)

        user_data = {
            'Course': course_options[selected_course],
            'Age_at_enrollment': age,
            'Admission_grade': adm_grade,
            'Tuition_fees_up_to_date': tuition,
            'Scholarship_holder': scholarship,
            'Curricular_units_1st_sem_enrolled': s1_enroll_val,
            'Curricular_units_1st_sem_approved': s1_app,
            'Curricular_units_1st_sem_grade': s1_grade,
            'Curricular_units_2nd_sem_enrolled': s2_enroll_val,
            'Curricular_units_2nd_sem_approved': s2_app,
            'Curricular_units_2nd_sem_grade': s2_grade,
        }
        final_input = defaults.copy()
        final_input.update(user_data)
        df_input = pd.DataFrame([final_input])[cols]

        prob       = model.predict_proba(df_input)[0][1]
        prediction = 1 if prob >= best_threshold else 0

        st.divider()
        is_dropout = prediction == 1

        # Color palette
        if is_dropout:
            accent, bg, border = "#dc2626", "#fff5f5", "#fecaca"
            label = "Risiko Dropout Terdeteksi"
            prob_display = prob * 100
            sub = f"Probabilitas dropout: {prob*100:.1f}%"
        else:
            accent, bg, border = "#16a34a", "#f0fdf4", "#bbf7d0"
            label = "Risiko Rendah — Potensi Lulus"
            prob_display = (1 - prob) * 100
            sub = f"Probabilitas graduate: {(1-prob)*100:.1f}%"

        # ── Result panel ──────────────────────────────────────────────────────
        rcol1, rcol2 = st.columns([1, 1])

        with rcol1:
            st.markdown(
                f'<div class="result-panel" style="background:{bg};border-color:{border}">'
                f'<div class="result-title" style="color:{accent}">{label}</div>'
                f'<div class="result-prob" style="color:{accent}">{prob_display:.0f}%</div>'
                f'<div class="result-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Breakdown metric bars (clean, no chart overhead)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:.7rem;font-weight:600;letter-spacing:.08em;'
                        'text-transform:uppercase;color:#94a3b8;margin-bottom:.6rem">'
                        'Indikator Risiko</div>', unsafe_allow_html=True)

            # Compute individual risk scores
            fin_risk  = 80 if tuition == 0 else 15
            fin_risk  = min(100, fin_risk + (30 if scholarship == 0 else 0))

            s1_rate   = s1_app / max(s1_enroll_val, 1)
            s2_rate   = s2_app / max(s2_enroll_val, 1)
            acad_risk = int(min(100, max(5,
                (1 - s1_rate) * 40 + (1 - s2_rate) * 60 +
                max(0, 12 - s1_grade) * 2.5 + max(0, 12 - s2_grade) * 4
            )))

            age_risk  = int(min(100, max(5, max(0, age - 25) * 3 + max(0, 18 - age) * 5)))

            for bar_label, val, color in [
                ("Akademik",  acad_risk, "#f43f5e" if acad_risk > 60 else "#f59e0b" if acad_risk > 35 else "#22c55e"),
                ("Finansial", fin_risk,  "#f43f5e" if fin_risk  > 60 else "#f59e0b" if fin_risk  > 35 else "#22c55e"),
                ("Demografi", age_risk,  "#f43f5e" if age_risk  > 60 else "#f59e0b" if age_risk  > 35 else "#22c55e"),
            ]:
                st.markdown(
                    f'<div style="margin-bottom:.6rem">'
                    f'<div style="display:flex;justify-content:space-between;'
                    f'font-size:.82rem;margin-bottom:.25rem">'
                    f'<span style="color:#374151">{bar_label}</span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:.8rem;color:{color}">{val}</span>'
                    f'</div>'
                    f'<div style="height:5px;background:#f1f5f9;border-radius:99px;overflow:hidden">'
                    f'<div style="height:100%;width:{val}%;background:{color};'
                    f'border-radius:99px;transition:width .4s ease"></div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

        with rcol2:
            # Gauge — minimal and clean
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(prob * 100, 1),
                number={"font": {"size": 48, "color": accent, "family": "DM Mono"},
                        "suffix": "%"},
                title={"text": "Probabilitas Dropout",
                       "font": {"size": 12, "color": "#94a3b8"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 0.5,
                             "tickcolor": "#e2e8f0", "tickfont": {"size": 10}},
                    "bar": {"color": accent, "thickness": 0.35},
                    "bgcolor": "#f8fafc",
                    "borderwidth": 1, "bordercolor": "#e2e8f0",
                    "steps": [
                        {"range": [0, best_threshold * 100], "color": "#f0fdf4"},
                        {"range": [best_threshold * 100, 100], "color": "#fff5f5"},
                    ],
                    "threshold": {
                        "line": {"color": "#64748b", "width": 1.5, "dash": "dot"} if False else {"color": "#64748b", "width": 1.5},
                        "thickness": 0.8,
                        "value": best_threshold * 100,
                    },
                }
            ))
            fig_g.update_layout(
                height=260,
                paper_bgcolor="rgba(0,0,0,0)",
                font_family="Inter",
                margin=dict(t=32, b=8, l=20, r=20),
            )
            st.plotly_chart(fig_g, use_container_width=True)

            # Context metrics
            m1, m2 = st.columns(2)
            m1.metric("Matkul Lulus Sem 1", f"{s1_app}/{int(s1_enroll_val)}",
                       delta=f"{s1_rate*100:.0f}%",
                       delta_color="normal")
            m2.metric("Matkul Lulus Sem 2", f"{s2_app}/{int(s2_enroll_val)}",
                       delta=f"{s2_rate*100:.0f}%",
                       delta_color="normal")

        # ── Recommendations (only if dropout) ─────────────────────────────────
        if is_dropout:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:.7rem;font-weight:600;letter-spacing:.08em;'
                'text-transform:uppercase;color:#94a3b8;margin-bottom:.6rem">'
                'Rekomendasi Tindakan</div>',
                unsafe_allow_html=True
            )

            recs = []
            if tuition == 0:
                recs.append(("#dc2626", "Konsultasi Keuangan",
                              "Jadwalkan pertemuan dengan bagian keuangan untuk opsi cicilan atau beasiswa darurat."))
            if scholarship == 0 and tuition == 0:
                recs.append(("#ea580c", "Intervensi Finansial Prioritas",
                              "Kombinasi tidak ada beasiswa dan SPP bermasalah meningkatkan risiko secara signifikan."))
            if s2_app < s1_app:
                recs.append(("#d97706", "Penurunan Akademik",
                              f"Matkul lulus turun dari {s1_app} (Sem 1) menjadi {s2_app} (Sem 2). Rekomendasikan pertemuan dengan Dosen Wali."))
            if s2_enroll_val > 0 and (s2_app / s2_enroll_val) < 0.5:
                recs.append(("#7c3aed", "Completion Rate Rendah",
                              f"Hanya {s2_app} dari {int(s2_enroll_val)} matkul lulus di Sem 2. Pertimbangkan program remedial."))
            if s2_grade < 10:
                recs.append(("#0891b2", "Nilai Di Bawah Standar",
                              f"Rata-rata nilai Sem 2 adalah {s2_grade:.1f}. Evaluasi beban studi dan metode pembelajaran."))
            if not recs:
                recs.append(("#64748b", "Pemantauan Berkala",
                              "Tidak ada faktor risiko spesifik teridentifikasi. Lanjutkan pemantauan pada semester berikutnya."))

            for color, title, desc in recs:
                st.markdown(
                    f'<div class="rec-item">'
                    f'<div class="rec-dot" style="background:{color}"></div>'
                    f'<div><div class="rec-title" style="color:{color}">{title}</div>'
                    f'<div class="rec-desc">{desc}</div></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="margin-top:.75rem;padding:.9rem 1.1rem;background:#f0fdf4;'
                'border:1px solid #bbf7d0;border-radius:10px;font-size:.875rem;color:#166534">'
                'Mahasiswa ini tidak menunjukkan tanda-tanda risiko dropout berdasarkan data saat ini. '
                'Tetap pantau perkembangan akademik di semester berikutnya.'
                '</div>',
                unsafe_allow_html=True
            )