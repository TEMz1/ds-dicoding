import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path


# ── Mappings ─────────────────────────────────────────────────────────────────
COURSE_MAP = {
    33:   'Biofuel Production Tech.',
    171:  'Animation & Multimedia',
    8014: 'Social Service (Eve.)',
    9003: 'Agronomy',
    9070: 'Communication Design',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Nursing',
    9556: 'Oral Hygiene',
    9670: 'Advertising & Marketing',
    9773: 'Journalism & Comm.',
    9853: 'Basic Education',
    9991: 'Management (Eve.)',
}
GENDER_MAP  = {1: 'Laki-laki', 0: 'Perempuan'}
ATTEND_MAP  = {1: 'Pagi', 0: 'Malam'}
SCHOLAR_MAP = {1: 'Penerima', 0: 'Non-penerima'}
TUITION_MAP = {1: 'Lancar', 0: 'Tunggakan'}
DEBTOR_MAP  = {1: 'Debtor', 0: 'Non-debtor'}

STATUS_COLORS = {
    'Dropout':  '#f43f5e',
    'Enrolled': '#f59e0b',
    'Graduate': '#22c55e',
}

PLOTLY_BASE = dict(
    font_family="Inter",
    font_size=12,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    # margin=dict(t=48, b=16, l=8, r=8),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.04,
        xanchor="left", x=0,
        font_size=11,
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
    ),
)

CSS = """
<style>
.kpi-wrap {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.1rem 1.25rem 0.9rem;
    position: relative;
    overflow: hidden;
}
.kpi-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
    border-radius: 12px 0 0 12px;
}
.kpi-label { font-size: 0.7rem; font-weight: 600; letter-spacing: .08em;
             text-transform: uppercase; color: #94a3b8; margin-bottom: .35rem; }
.kpi-value { font-size: 1.85rem; font-weight: 700; line-height: 1.1;
             color: var(--accent); }
.kpi-sub   { font-size: 0.78rem; color: #94a3b8; margin-top: .25rem; }

.chart-wrap {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.3rem 0.5rem;
    margin-bottom: 0.5rem;
}
.sec-label {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: #94a3b8; margin: 1.25rem 0 .6rem;
}
.legend-strip {
    display: flex; gap: 1rem; align-items: center;
    font-size: .8rem; font-weight: 500;
    margin-bottom: .5rem;
}
.legend-dot {
    width: 10px; height: 10px;
    border-radius: 50%; display: inline-block; margin-right: 5px;
}

</style>
"""

ROOT = Path(__file__).parent.parent

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(ROOT / "dataset" / "data.csv", sep=';')
    mask = ~(
        (df['Curricular_units_1st_sem_enrolled'] == 0) &
        (df['Curricular_units_2nd_sem_enrolled'] == 0) &
        (df['Status'] == 'Graduate')
    )
    df = df[mask].copy()
    df['Course_name']  = df['Course'].map(COURSE_MAP).fillna(df['Course'].astype(str))
    df['Gender_name']  = df['Gender'].map(GENDER_MAP)
    df['Attend_name']  = df['Daytime_evening_attendance'].map(ATTEND_MAP)
    df['Scholar_name'] = df['Scholarship_holder'].map(SCHOLAR_MAP)
    df['Tuition_name'] = df['Tuition_fees_up_to_date'].map(TUITION_MAP)
    df['Debtor_name']  = df['Debtor'].map(DEBTOR_MAP)
    return df


# ── Chart builders ────────────────────────────────────────────────────────────
def fig_donut(df):
    counts = df['Status'].value_counts().reset_index()
    counts.columns = ['Status', 'n']
    fig = px.pie(
        counts, names='Status', values='n',
        hole=0.60,
        color='Status', color_discrete_map=STATUS_COLORS,
    )
    fig.update_traces(
        textposition='outside', textinfo='percent+label',
        textfont_size=11, pull=[0.02]*len(counts),
        showlegend=False,
    )
    fig.update_layout(**PLOTLY_BASE, height=300,
                      title=dict(text="Distribusi Status", font_size=13),
                      )
    return fig


def fig_course(df):
    grp = (df.groupby(['Course_name', 'Status'])
           .size().reset_index(name='n'))
    tot = grp.groupby('Course_name')['n'].transform('sum')
    grp['pct'] = grp['n'] / tot * 100

    order = (grp[grp['Status'] == 'Dropout']
             .sort_values('pct')['Course_name'].tolist())

    fig = px.bar(
        grp, y='Course_name', x='pct',
        color='Status', barmode='stack',
        color_discrete_map=STATUS_COLORS,
        category_orders={'Course_name': order, 'Status': ['Dropout', 'Enrolled', 'Graduate']},
        labels={'Course_name': '', 'pct': '% Mahasiswa'},
        text_auto='.0f',
    )
    fig.update_traces(textposition='inside', textfont_size=10, showlegend=False)
    fig.update_layout(
        **PLOTLY_BASE,
        height=480,
        title=dict(text="Komposisi Status per Program Studi", font_size=13),
        xaxis=dict(title='% Mahasiswa', ticksuffix='%', gridcolor='#f1f5f9'),
        yaxis=dict(title=''),
    
    )
    return fig


def fig_age(df):
    fig = px.box(
        df, x='Status', y='Age_at_enrollment',
        color='Status', color_discrete_map=STATUS_COLORS,
        points='outliers',
        labels={'Age_at_enrollment': 'Usia', 'Status': ''},
    )
    fig.update_traces(showlegend=False)
    fig.update_layout(
        **PLOTLY_BASE, height=300,
        title=dict(text="Distribusi Usia saat Mendaftar", font_size=13),
        yaxis=dict(gridcolor='#f1f5f9'),
        # margin=dict(t=36, b=8, l=8, r=8),
    )
    return fig


def _pct_bar(df, group_col, title, fig, row, col, show_legend=False):
    tmp = df.groupby([group_col, 'Status']).size().reset_index(name='n')
    tot = tmp.groupby(group_col)['n'].transform('sum')
    tmp['pct'] = (tmp['n'] / tot * 100).round(1)
    for status, color in STATUS_COLORS.items():
        d = tmp[tmp['Status'] == status]
        fig.add_trace(go.Bar(
            x=d[group_col], y=d['pct'],
            name=status, marker_color=color,
            showlegend=show_legend,
            text=d['pct'].astype(str) + '%',
            textposition='inside', textfont_size=10,
        ), row=row, col=col)


def fig_gender_attend(df):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Gender", "Waktu Kuliah"),
                        horizontal_spacing=0.12)
    _pct_bar(df, 'Gender_name', 'Gender', fig, 1, 1, show_legend=False)
    _pct_bar(df, 'Attend_name', 'Waktu Kuliah', fig, 1, 2, show_legend=False)
    fig.update_layout(
        **PLOTLY_BASE, height=300, barmode='stack',
        title=dict(text="Komposisi Status — Gender & Waktu Kuliah", font_size=13),
        yaxis_title='%', yaxis2_title='%',
        yaxis=dict(gridcolor='#f1f5f9', ticksuffix='%'),
        yaxis2=dict(gridcolor='#f1f5f9', ticksuffix='%'),
        # margin=dict(t=40, b=8, l=8, r=8),
    )
    return fig


def fig_financial(df):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Status SPP", "Status Beasiswa"),
                        horizontal_spacing=0.12)
    _pct_bar(df, 'Tuition_name', 'SPP', fig, 1, 1)
    _pct_bar(df, 'Scholar_name', 'Beasiswa', fig, 1, 2)
    fig.update_layout(
        **PLOTLY_BASE, height=300, barmode='stack',
        title=dict(text="Komposisi Status — Faktor Finansial", font_size=13),
        yaxis_title='%', yaxis2_title='%',
        yaxis=dict(gridcolor='#f1f5f9', ticksuffix='%'),
        yaxis2=dict(gridcolor='#f1f5f9', ticksuffix='%'),
        # margin=dict(t=40, b=8, l=8, r=8),
        showlegend=False,
    )
    return fig


def fig_scatter_grades(df):
    sample = df.sample(min(2000, len(df)), random_state=42)
    fig = px.scatter(
        sample,
        x='Curricular_units_1st_sem_grade',
        y='Curricular_units_2nd_sem_grade',
        color='Status', color_discrete_map=STATUS_COLORS,
        opacity=0.45,
        labels={
            'Curricular_units_1st_sem_grade': 'Nilai Sem 1 (0–20)',
            'Curricular_units_2nd_sem_grade': 'Nilai Sem 2 (0–20)',
        },
    )
    fig.update_traces(showlegend=False, marker_size=5)
    fig.update_layout(
        **PLOTLY_BASE, height=320,
        title=dict(text="Nilai Semester 1 vs Semester 2", font_size=13),
        xaxis=dict(gridcolor='#f1f5f9'),
        yaxis=dict(gridcolor='#f1f5f9'),
        # margin=dict(t=36, b=8, l=8, r=8),
    )
    return fig


def fig_approved(df):
    tmp = (df.groupby('Status')[
               ['Curricular_units_1st_sem_approved',
                'Curricular_units_2nd_sem_approved']
           ].mean().reset_index()
           .melt(id_vars='Status', var_name='Semester', value_name='Avg'))
    tmp['Semester'] = tmp['Semester'].map({
        'Curricular_units_1st_sem_approved': 'Sem 1',
        'Curricular_units_2nd_sem_approved': 'Sem 2',
    })
    fig = px.bar(
        tmp, x='Semester', y='Avg', color='Status',
        barmode='group',
        color_discrete_map=STATUS_COLORS,
        text_auto='.1f',
        labels={'Avg': 'Rata-rata Matkul Lulus', 'Semester': ''},
    )
    fig.update_traces(showlegend=False, textposition='outside', textfont_size=10)
    fig.update_layout(
        **PLOTLY_BASE, height=300,
        title=dict(text="Rata-rata Matkul Lulus per Semester", font_size=13),
        yaxis=dict(gridcolor='#f1f5f9'),
        
    )
    return fig


def fig_adm_grade(df):
    fig = px.histogram(
        df, x='Admission_grade', color='Status',
        color_discrete_map=STATUS_COLORS,
        nbins=40, barmode='overlay', opacity=0.65,
        labels={'Admission_grade': 'Admission Grade (0–200)', 'count': 'Jumlah'},
    )
    fig.update_traces(showlegend=False)
    fig.update_layout(
        **PLOTLY_BASE, height=300,
        title=dict(text="Distribusi Nilai Masuk per Status", font_size=13),
        xaxis=dict(gridcolor='#f1f5f9'),
        yaxis=dict(gridcolor='#f1f5f9', title='Jumlah'),
        
    )
    return fig


# ── Main ──────────────────────────────────────────────────────────────────────
def show():
    st.markdown(CSS, unsafe_allow_html=True)
    df = load_data()

    # ── Sidebar filters ───────────────────────────────────────────────────────
    st.sidebar.markdown(
        '<div style="font-size:0.72rem;font-weight:600;letter-spacing:.08em;'
        'text-transform:uppercase;color:#475569 !important;margin:.75rem 0 .5rem">'
        'Filter Data</div>',
        unsafe_allow_html=True
    )
    status_f  = st.sidebar.multiselect("Status", df['Status'].unique().tolist(),
                                        default=df['Status'].unique().tolist())
    gender_f  = st.sidebar.multiselect("Gender", df['Gender_name'].unique().tolist(),
                                        default=df['Gender_name'].unique().tolist())
    attend_f  = st.sidebar.multiselect("Waktu Kuliah", df['Attend_name'].unique().tolist(),
                                        default=df['Attend_name'].unique().tolist())
    scholar_f = st.sidebar.multiselect("Beasiswa", df['Scholar_name'].unique().tolist(),
                                        default=df['Scholar_name'].unique().tolist())

    dff = df[
        df['Status'].isin(status_f) &
        df['Gender_name'].isin(gender_f) &
        df['Attend_name'].isin(attend_f) &
        df['Scholar_name'].isin(scholar_f)
    ]

    if dff.empty:
        st.warning("Tidak ada data yang sesuai dengan filter.")
        return

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("### Dashboard Overview")
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            Menampilkan data <strong>{len(df):,}</strong> mahasiswa · 
            Jaya Jaya Institut
        </div>
        <div style="font-size: 15px;">
            <span style="color: #f43f5e; margin-right: 12px;">● Dropout</span>
            <span style="color: #f59e0b; margin-right: 12px;">● Enrolled</span>
            <span style="color: #22c55e;">● Graduate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Legend strip (satu kali di atas) ─────────────────────────────────────
    total    = len(dff)
    dropout  = (dff['Status'] == 'Dropout').sum()
    graduate = (dff['Status'] == 'Graduate').sum()
    enrolled = (dff['Status'] == 'Enrolled').sum()

    

    # ── KPI row ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "Total Mahasiswa", f"{total:,}",   "Dataset aktif", "#6366f1"),
        (k2, "Dropout",         f"{dropout:,}",  f"{dropout/total*100:.1f}% dari total", "#f43f5e"),
        (k3, "Graduate",        f"{graduate:,}", f"{graduate/total*100:.1f}% dari total", "#22c55e"),
        (k4, "Masih Enrolled",  f"{enrolled:,}", f"{enrolled/total*100:.1f}% dari total", "#f59e0b"),
    ]
    for col, label, val, sub, accent in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-wrap" style="--accent:{accent}">'
                f'<div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{val}</div>'
                f'<div class="kpi-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)


    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Profil Mahasiswa", "Performa Akademik", "Faktor Finansial"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_donut(dff), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_age(dff), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_course(dff), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_gender_attend(dff), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_scatter_grades(dff), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_approved(dff), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_adm_grade(dff), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_financial(dff), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Debtor
        tmp_d = dff.groupby(['Debtor_name', 'Status']).size().reset_index(name='n')
        tot_d = tmp_d.groupby('Debtor_name')['n'].transform('sum')
        tmp_d['pct'] = (tmp_d['n'] / tot_d * 100).round(1)
        fig_d = px.bar(
            tmp_d, x='Debtor_name', y='pct', color='Status',
            barmode='stack', color_discrete_map=STATUS_COLORS,
            text_auto='.0f',
            labels={'Debtor_name': '', 'pct': '%'},
        )
        fig_d.update_traces(showlegend=False, textposition='inside', textfont_size=10)
        fig_d.update_layout(
            **PLOTLY_BASE, height=300,
            title=dict(text="Komposisi Status — Status Debtor", font_size=13),
            yaxis=dict(gridcolor='#f1f5f9', ticksuffix='%'),
            
        )
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

