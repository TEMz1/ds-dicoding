import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="TEMZ1 · E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLORS ────────────────────────────────────────────────────────────────────
C_bg      = '#0b0f1a'
C_surf    = '#0f1523'
C_surf2   = '#131928'
C_border  = '#1e2740'
C_border2 = '#243050'
C_text    = '#e8eaf0'
C_text2   = '#8896b3'
C_text3   = '#4a5568'
C_blue    = '#4fc3f7'
C_blue2   = '#38bdf8'
C_teal    = '#2dd4bf'
C_green   = '#34d399'
C_purple  = '#a78bfa'
C_pink    = '#f472b6'
C_orange  = '#fb923c'
C_yellow  = '#fbbf24'

PALETTE = [C_blue, C_purple, C_pink, C_green, C_orange,
           C_yellow, '#60a5fa', '#e879f9', C_teal, '#4ade80']

# ── CSS (unchanged) ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#0b0f1a; color:#e8eaf0; }

[data-testid="stSidebar"] { background:#0f1523 !important; border-right:1px solid #1e2740; }
[data-testid="stSidebar"] * { color:#c8cfe0 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,[data-testid="stSidebar"] h4 { color:#e8eaf0 !important; }

.topbar {
    display:flex; align-items:center; gap:0.65rem;
    padding:0.45rem 0 0.55rem;
    border-bottom:1px solid #1e2740; margin-bottom:0.85rem;
}
.topbar-logo {
    font-family:'Syne',sans-serif; font-weight:800; font-size:1.1rem;
    background:linear-gradient(135deg,#4fc3f7,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:-0.02em; white-space:nowrap;
}
.topbar-sep { width:1px; height:16px; background:#1e2740; flex-shrink:0; }
.topbar-meta { font-size:0.75rem; color:#4a5568; white-space:nowrap; }
.topbar-spacer { flex:1; }
.topbar-badge {
    background:#1e2740; color:#8896b3;
    border-radius:20px; padding:0.15rem 0.6rem;
    font-size:0.67rem; font-weight:500; letter-spacing:0.04em; white-space:nowrap;
}
.topbar-badge.blue  { background:#0c2340; color:#4fc3f7; }
.topbar-badge.green { background:#0a2318; color:#34d399; }

.kpi-card {
    background:linear-gradient(145deg,#131928,#0f1523);
    border:1px solid #1e2740; border-radius:14px;
    padding:0.9rem 1rem 0.75rem; position:relative; overflow:hidden;
}
.kpi-card::after {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    border-radius:14px 14px 0 0;
}
.kpi-blue::after   { background:linear-gradient(90deg,#4fc3f7,#38bdf8); }
.kpi-purple::after { background:linear-gradient(90deg,#a78bfa,#8b5cf6); }
.kpi-pink::after   { background:linear-gradient(90deg,#f472b6,#ec4899); }
.kpi-green::after  { background:linear-gradient(90deg,#34d399,#10b981); }
.kpi-orange::after { background:linear-gradient(90deg,#fb923c,#f97316); }
.kpi-teal::after   { background:linear-gradient(90deg,#2dd4bf,#14b8a6); }

.kpi-label {
    font-size:0.63rem; font-weight:500; text-transform:uppercase;
    letter-spacing:0.09em; color:#4a5568; margin-bottom:0.25rem;
}
.kpi-value {
    font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:700;
    color:#e8eaf0; line-height:1; margin-bottom:0.15rem;
}
.kpi-sub { font-size:0.67rem; color:#4a5568; }

.sec-header {
    font-family:'Syne',sans-serif; font-size:0.82rem; font-weight:700;
    color:#c8d6f0; text-transform:uppercase; letter-spacing:0.07em;
    margin-bottom:0.65rem; padding-bottom:0.45rem; border-bottom:1px solid #1e2740;
}

.insight {
    background:linear-gradient(135deg,#131928,#0f1d2e);
    border:1px solid #1e3a5f; border-left:3px solid #4fc3f7;
    border-radius:8px; padding:0.65rem 0.9rem;
    font-size:0.8rem; color:#8eaacc; line-height:1.6; margin-top:0.65rem;
}
.insight strong { color:#4fc3f7; }

.stTabs [data-baseweb="tab-list"] {
    background:#0f1523; border-radius:10px; padding:3px; gap:2px;
    border:1px solid #1e2740;
}
.stTabs [data-baseweb="tab"] {
    background:transparent; color:#6b7a99 !important;
    border-radius:7px; font-size:0.8rem; font-weight:500; padding:0.32rem 0.85rem;
}
.stTabs [aria-selected="true"] {
    background:#1e2740 !important; color:#c8d6f0 !important; font-weight:600 !important;
}

label, .stSelectbox label, .stMultiSelect label,
.stSlider label, .stRadio label {
    color:#8896b3 !important; font-size:0.77rem !important; font-weight:500 !important;
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background:#131928 !important; border-color:#1e2740 !important; color:#c8d6f0 !important;
}
hr { border-color:#1e2740 !important; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#0b0f1a; }
::-webkit-scrollbar-thumb { background:#1e2740; border-radius:4px; }
[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }

</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Mengambil path folder tempat file dashboard.py 
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "main_data.csv")
    
    try:
        # Load langsung dari folder yang sama
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Gagal load data lokal: {e}")
        st.info(f"Pastikan file main_data.csv ada di folder: {base_dir}")
        return pd.DataFrame() 
    
    # --- Sisanya tetap sama seperti sebelumnya ---
    for col in ['order_purchase_timestamp','order_delivered_customer_date',
                'order_estimated_delivery_date','order_delivered_carrier_date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    df['purchase_month_str'] = df['order_purchase_timestamp'].dt.strftime('%b %Y')
    df['purchase_month_key'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')
    df['purchase_quarter']   = df['order_purchase_timestamp'].dt.to_period('Q').astype(str)
    
    if 'total_revenue' not in df.columns:
        df['total_revenue'] = df['price'] + df['freight_value']
    if 'shipping_days' not in df.columns:
        df['shipping_days'] = (df['order_delivered_customer_date'] - df['order_delivered_carrier_date']).dt.days
    if 'delay_days' not in df.columns:
        df['delay_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
    
    return df

df_raw = load_data()

# ── LABEL MAPS (English) ──────────────────────────────────────────────────────
PAY_LABELS = {
    'credit_card': 'Credit Card',
    'boleto':      'Boleto',
    'voucher':     'Voucher',
    'debit_card':  'Debit Card',
    'not_defined': 'Not Defined',
}

STATE_NAMES = {
    'SP':'São Paulo','RJ':'Rio de Janeiro','MG':'Minas Gerais','RS':'Rio Grande do Sul',
    'PR':'Paraná','SC':'Santa Catarina','BA':'Bahia','GO':'Goiás','DF':'Federal District',
    'ES':'Espírito Santo','PE':'Pernambuco','CE':'Ceará','MT':'Mato Grosso',
    'MS':'Mato Grosso do Sul','PA':'Pará','MA':'Maranhão','RN':'Rio Grande do Norte',
    'PB':'Paraíba','AM':'Amazonas','AL':'Alagoas','PI':'Piauí','SE':'Sergipe',
    'RO':'Rondônia','TO':'Tocantins','AC':'Acre','AP':'Amapá','RR':'Roraima',
}

CAT_LABELS = {
    'bed_bath_table': 'Bed Bath & Table',
    'health_beauty': 'Health & Beauty',
    'sports_leisure': 'Sports & Leisure',
    'furniture_decor': 'Furniture & Decor',
    'computers_accessories': 'Computers & Accessories',
    'housewares': 'Housewares',
    'watches_gifts': 'Watches & Gifts',
    'telephony': 'Telephony',
    'garden_tools': 'Garden Tools',
    'baby': 'Baby Products',
    'electronics': 'Electronics',
    'toys': 'Toys',
    'cool_stuff': 'Cool Stuff',
    'perfumery': 'Perfumery',
    'auto': 'Automotive',
    'stationery': 'Stationery',
    'fashion_bags_accessories': 'Fashion Bags & Accessories',
    'food_drink': 'Food & Drinks',
    'office_furniture': 'Office Furniture',
    'consoles_games': 'Consoles & Games',
    'pet_shop': 'Pet Shop',
    'construction_tools_lights': 'Construction Tools & Lights',
    'agro_industry_and_commerce': 'Agro Industry',
    'air_conditioning': 'Air Conditioning',
    'art': 'Art',
    'books_general_interest': 'General Interest Books',
    'books_imported': 'Imported Books',
    'books_technical': 'Technical Books',
    'christmas_supplies': 'Christmas Supplies',
    'cine_photo': 'Photography & Cinema',
    'computers': 'Computers',
    'costumes_accessories': 'Costumes & Accessories',
    'diapers_and_hygiene': 'Diapers & Hygiene',
    'drinks': 'Drinks',
    'dvds_blu_ray': 'DVDs & Blu-Ray',
    'fashion_childrens_clothes': "Children's Clothing",
    'fashion_male_clothing': "Men's Clothing",
    'fashion_female_clothing': "Women's Clothing",
    'fashion_shoes': 'Shoes',
    'fashion_sport': 'Sportswear',
    'fashion_underwear_beach': 'Underwear & Beachwear',
    'fixed_telephony': 'Landline Telephony',
    'flowers': 'Flowers & Plants',
    'food': 'Food',
    'furniture_bedroom': 'Bedroom Furniture',
    'furniture_living_room': 'Living Room Furniture',
    'furniture_mattress_and_upholstery': 'Mattresses & Upholstery',
    'home_appliances': 'Large Home Appliances',
    'home_appliances_2': 'Home Appliances 2',
    'home_comfort': 'Home Comfort',
    'home_comfort_2': 'Home Comfort 2',
    'home_construction': 'Construction Materials',
    'industry_commerce_and_business': 'Industry & Business',
    'instruments': 'Musical Instruments',
    'kitchen_dining_laundry_garden_furniture': 'Kitchen & Dining',
    'la_cuisine': 'Cookware',
    'luggage_accessories': 'Luggage & Accessories',
    'market_place': 'Marketplace',
    'music': 'Music',
    'musical_instruments': 'Musical Instruments',
    'office_stationary': 'Office Stationery',
    'party_supplies': 'Party Supplies',
    'pc_gamer': 'Gaming PCs',
    'portrait_and_frames': 'Portraits & Frames',
    'security_and_services': 'Security & Services',
    'signaling_and_security': 'Signaling & Security',
    'small_appliances': 'Small Appliances',
    'small_appliances_home_oven_and_coffee': 'Ovens & Coffee Makers',
    'sports_fitness': 'Fitness & Sports',
    'tablets_printing_image': 'Tablets & Printing',
    'Uncategorized': 'Uncategorized',
    'uncategorized': 'Uncategorized',
}

def friendly_cat(name):
    return CAT_LABELS.get(str(name), str(name).replace('_',' ').title())

def friendly_pay(name):
    return PAY_LABELS.get(str(name), str(name).replace('_',' ').title())

def friendly_state(code):
    return f"{code} – {STATE_NAMES.get(code, code)}"

# ── CHART DEFAULTS ────────────────────────────────────────────────────────────
CT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color=C_text2, size=11),
    margin=dict(l=8, r=8, t=36, b=8),
    colorway=PALETTE,
)
AX = dict(gridcolor='#1a2035', linecolor=C_border, tickcolor=C_border, zerolinecolor='#1a2035')

def cscale(lo, hi): return [[0, lo], [1, hi]]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1rem; border-bottom:1px solid #1e2740; margin-bottom:0.9rem;'>
        <div style='font-family:Syne; font-weight:800; font-size:1.15rem;
             background:linear-gradient(135deg,#4fc3f7,#a78bfa);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🛒 TEMZ1
        </div>
        <div style='font-size:0.68rem; color:#4a5568; margin-top:2px;'>
            E-Commerce Analytics Dashboard · 2016–2018
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 🗓 Date Range")
    min_date = df_raw['order_purchase_timestamp'].min().date()
    max_date = df_raw['order_purchase_timestamp'].max().date()
    date_start = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    date_end   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date)

    st.markdown("##### 🗺 State")
    all_states = sorted(df_raw['customer_state'].dropna().unique())
    state_opts = {friendly_state(s): s for s in all_states}
    sel_state_labels = st.multiselect("Filter States", list(state_opts.keys()), placeholder="All States")
    selected_states = [state_opts[l] for l in sel_state_labels]

    st.markdown("##### 🏷 Product Category")
    all_cats = sorted(df_raw['product_category_name_english'].dropna().unique())
    cat_opts = {friendly_cat(c): c for c in all_cats}
    sel_cat_labels = st.multiselect("Filter Categories", list(cat_opts.keys()), placeholder="All Categories")
    selected_cats = [cat_opts[l] for l in sel_cat_labels]

    st.markdown("##### 💳 Payment Method")
    pay_types = sorted(df_raw['payment_type'].dropna().unique())
    pay_opts = {friendly_pay(p): p for p in pay_types}
    sel_pay_labels = st.multiselect("Filter Payment Methods", list(pay_opts.keys()), placeholder="All Methods")
    selected_pay = [pay_opts[l] for l in sel_pay_labels]

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
df = df[(df['order_purchase_timestamp'].dt.date >= date_start) &
        (df['order_purchase_timestamp'].dt.date <= date_end)]
if selected_states: df = df[df['customer_state'].isin(selected_states)]
if selected_cats:   df = df[df['product_category_name_english'].isin(selected_cats)]
if selected_pay:    df = df[df['payment_type'].isin(selected_pay)]

df['category_name']   = df['product_category_name_english'].apply(friendly_cat)
df['payment_method']  = df['payment_type'].apply(friendly_pay)
df['state_name']      = df['customer_state'].apply(friendly_state)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='topbar'>
    <span class='topbar-logo'>🛒 TEMZ1</span>
    <span class='topbar-sep'></span>
    <span class='topbar-meta'>E-Commerce Analytics Dashboard</span>
    <span class='topbar-spacer'></span>
    <span class='topbar-badge'>🇧🇷 Brazil</span>
    <span class='topbar-badge blue'>E-commerce Platform</span>
    <span class='topbar-badge green'>{len(df):,} orders</span>
</div>
""", unsafe_allow_html=True)

# ── KPI ───────────────────────────────────────────────────────────────────────
total_revenue   = df['total_revenue'].sum()
total_orders    = df['order_id'].nunique()
avg_order_val   = df.groupby('order_id')['total_revenue'].sum().mean() if total_orders else 0
total_customers = df['customer_unique_id'].nunique()
avg_review      = df['review_score'].mean() if len(df) else 0
on_time_pct     = (df['delay_days'] <= 0).mean() * 100 if len(df) else 0

def kpi(label, value, sub, color):
    return f"""<div class='kpi-card kpi-{color}'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>"""

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.markdown(kpi("Total Revenue",     f"${total_revenue/1e6:.2f}M", "price + freight",         "blue"),   unsafe_allow_html=True)
with c2: st.markdown(kpi("Total Orders",      f"{total_orders:,}",         "unique orders",           "purple"), unsafe_allow_html=True)
with c3: st.markdown(kpi("AOV",               f"${avg_order_val:.0f}",      "average order value",     "pink"),   unsafe_allow_html=True)
with c4: st.markdown(kpi("Total Customers",   f"{total_customers:,}",      "unique customers",        "green"),  unsafe_allow_html=True)
with c5: st.markdown(kpi("Avg Rating",        f"{avg_review:.2f} ★",       "out of 5",                "orange"), unsafe_allow_html=True)
with c6: st.markdown(kpi("On-Time Delivery",  f"{on_time_pct:.1f}%",       "delivered on / before ETA","teal"),   unsafe_allow_html=True)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Revenue & Trends",
    "🏷 Products",
    "🗺 Geography",
    "👥 Customer Segmentation",
    "⭐ Reviews & Delivery",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – REVENUE & TRENDS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<p class='sec-header'>Revenue & Order Trends</p>", unsafe_allow_html=True)

    monthly = df.groupby(['purchase_month_key','purchase_month_str']).agg(
        order_count=('order_id','nunique'),
        total_revenue=('total_revenue','sum')
    ).reset_index().sort_values('purchase_month_key')

    col_a, col_b = st.columns([3, 1])
    with col_a:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly['purchase_month_str'], y=monthly['total_revenue'],
            name='Revenue', marker_color=C_blue, opacity=0.75,
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>',
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly['purchase_month_str'], y=monthly['order_count'],
            name='Order Count', line=dict(color=C_pink, width=2.5),
            mode='lines+markers', marker=dict(size=5),
            hovertemplate='<b>%{x}</b><br>Orders: %{y:,}<extra></extra>',
        ), secondary_y=True)
        fig.update_layout(title='Monthly Revenue & Order Count', **CT, height=300)
        fig.update_xaxes(**AX, tickangle=45)
        fig.update_yaxes(title_text="Revenue ($)", secondary_y=False, **AX)
        fig.update_yaxes(title_text="Order Count", secondary_y=True, gridcolor='rgba(0,0,0,0)', showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        quarterly = df.groupby('purchase_quarter')['total_revenue'].sum().reset_index().sort_values('purchase_quarter')
        quarterly.columns = ['Quarter', 'total']
        fig2 = px.bar(quarterly, x='Quarter', y='total',
                      title='Revenue by Quarter',
                      color='total', color_continuous_scale=cscale('#1e2740', C_blue),
                      labels={'total':'Revenue ($)', 'Quarter':'Period'})
        fig2.update_traces(hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>')
        fig2.update_layout(**CT, height=300, showlegend=False, coloraxis_showscale=False)
        fig2.update_xaxes(**AX, tickangle=45, title=None)
        fig2.update_yaxes(**AX, title=None)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        pay_s = df.groupby('payment_method')['total_revenue'].sum().reset_index()
        pay_s.columns = ['Payment Method', 'Revenue']
        fig3 = px.pie(pay_s, values='Revenue', names='Payment Method',
                      title='Revenue Share by Payment Method',
                      color_discrete_sequence=PALETTE, hole=0.55)
        fig3.update_traces(
            textposition='outside', textinfo='percent+label', textfont_size=11,
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>',
        )
        fig3.update_layout(**CT, height=310)
        fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', yanchor='bottom', y=-0.28))
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        if 'payment_installments' in df.columns:
            inst = df[df['payment_type']=='credit_card']['payment_installments'].value_counts().reset_index()
            inst.columns = ['Installments (months)', 'Transaction Count']
            inst = inst[inst['Installments (months)'] <= 12].sort_values('Installments (months)')
            fig4 = px.bar(inst, x='Installments (months)', y='Transaction Count',
                          title='Credit Card Installment Distribution',
                          color='Transaction Count',
                          color_continuous_scale=cscale('#1e2740', C_purple))
            fig4.update_traces(hovertemplate='<b>%{x} months</b><br>Transactions: %{y:,}<extra></extra>')
            fig4.update_layout(**CT, height=310, showlegend=False, coloraxis_showscale=False)
            fig4.update_xaxes(**AX, title='Number of Installments', dtick=1)
            fig4.update_yaxes(**AX, title='Transaction Count')
        else:
            pv = df.groupby('payment_method')['payment_value'].sum().reset_index()
            pv.columns = ['Payment Method', 'Total Value']
            fig4 = px.bar(pv.sort_values('Total Value'), x='Total Value', y='Payment Method',
                          orientation='h', title='Total Transaction Value by Payment Method',
                          color='Total Value', color_continuous_scale=cscale('#1e2740', C_purple))
            fig4.update_traces(hovertemplate='<b>%{y}</b><br>Total: $%{x:,.0f}<extra></extra>')
            fig4.update_layout(**CT, height=310, showlegend=False, coloraxis_showscale=False)
            fig4.update_xaxes(**AX, title='Total Value ($)')
            fig4.update_yaxes(**AX, title=None)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""<div class='insight'>
        💡 <strong>Insight:</strong> Revenue and order volume grew significantly throughout 2017–2018.
        A sharp spike in <strong>November 2017</strong> is likely driven by Black Friday promotions.
        Credit cards dominate payments, reflecting strong preference for installment options.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – PRODUCTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<p class='sec-header'>Product & Category Performance</p>", unsafe_allow_html=True)

    cat_s = df.groupby('category_name').agg(
        items_sold=('order_item_id','count'),
        total_revenue=('total_revenue','sum'),
        avg_price=('price','mean'),
        avg_rating=('review_score','mean')
    ).reset_index().sort_values('items_sold', ascending=False)

    top_n = st.slider("Show top N categories?", 5, 20, 10, key='cat_n')

    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(cat_s.head(top_n).sort_values('items_sold'),
                     x='items_sold', y='category_name', orientation='h',
                     title=f'🏆 Top {top_n} Best-Selling Categories',
                     color='items_sold', color_continuous_scale=cscale('#1e2a3a', C_blue),
                     labels={'items_sold':'Items Sold','category_name':'Category'})
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Sold: %{x:,} items<extra></extra>')
        fig.update_layout(**CT, height=420, showlegend=False, coloraxis_showscale=False)
        fig.update_xaxes(**AX, title='Items Sold')
        fig.update_yaxes(**AX, title=None)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.bar(cat_s.tail(top_n).sort_values('items_sold', ascending=False),
                      x='items_sold', y='category_name', orientation='h',
                      title=f'⚠️ Bottom {top_n} Least-Sold Categories',
                      color='items_sold', color_continuous_scale=cscale('#2a1e40', C_purple),
                      labels={'items_sold':'Items Sold','category_name':'Category'})
        fig2.update_traces(hovertemplate='<b>%{y}</b><br>Sold: %{x:,} items<extra></extra>')
        fig2.update_layout(**CT, height=420, showlegend=False, coloraxis_showscale=False)
        fig2.update_xaxes(**AX, title='Items Sold')
        fig2.update_yaxes(**AX, title=None)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns([3, 2])
    with col_c:
        fig3 = px.scatter(cat_s.head(20),
                          x='items_sold', y='total_revenue',
                          size='avg_price', color='avg_rating',
                          hover_name='category_name',
                          custom_data=['avg_price','avg_rating'],
                          title='Revenue vs Sales Volume',
                          color_continuous_scale='plasma', size_max=40,
                          labels={
                              'items_sold':'Items Sold',
                              'total_revenue':'Total Revenue ($)',
                              'avg_price':'Avg Price',
                              'avg_rating':'Avg Rating',
                          })
        fig3.update_traces(
            hovertemplate=(
                '<b>%{hovertext}</b><br>'
                'Sold: %{x:,} items<br>'
                'Revenue: $%{y:,.0f}<br>'
                'Avg price: $%{customdata[0]:.0f}<br>'
                'Avg rating: %{customdata[1]:.2f} ★'
                '<extra></extra>'
            )
        )
        fig3.update_layout(**CT, height=360,
                           coloraxis_colorbar=dict(title=dict(text='Avg Rating',
                                                              font=dict(color=C_text2)),
                                                   tickfont=dict(color=C_text2)))
        fig3.update_xaxes(**AX, title='Items Sold')
        fig3.update_yaxes(**AX, title='Total Revenue ($)')
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        top8 = cat_s.sort_values('total_revenue', ascending=False).head(8)
        fig4 = px.pie(top8, values='total_revenue', names='category_name',
                      title='Revenue Share – Top 8 Categories',
                      color_discrete_sequence=PALETTE, hole=0.5)
        fig4.update_traces(
            textposition='inside', textinfo='percent', textfont_size=10,
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>',
        )
        fig4.update_layout(**CT, height=360, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<p class='sec-header' style='margin-top:0.4rem'>Category Detail Table</p>", unsafe_allow_html=True)
    disp = cat_s.head(20).copy()
    disp['total_revenue'] = disp['total_revenue'].map('${:,.0f}'.format)
    disp['avg_price']     = disp['avg_price'].map('${:.2f}'.format)
    disp['avg_rating']    = disp['avg_rating'].map('{:.2f} ★'.format)
    disp.columns = ['Category','Items Sold','Total Revenue','Avg Price','Avg Rating']
    st.dataframe(disp, use_container_width=True, hide_index=True)

    st.markdown("""<div class='insight'>
        💡 <strong>Insight:</strong> <strong>Bed Bath & Table</strong> consistently leads in sales volume across regions.
        Categories with high ratings but low volume present clear opportunities for targeted promotion campaigns.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – GEOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<p class='sec-header'>Geographic Distribution</p>", unsafe_allow_html=True)

    STATE_COORDS = {
        'AC':(-9.02,-70.81),'AL':(-9.57,-36.78),'AM':(-3.42,-65.86),
        'AP':( 1.41,-51.77),'BA':(-12.58,-41.70),'CE':(-5.50,-39.32),
        'DF':(-15.80,-47.86),'ES':(-19.18,-40.31),'GO':(-15.83,-49.84),
        'MA':(-5.42,-45.44),'MG':(-18.51,-44.56),'MS':(-20.77,-54.79),
        'MT':(-12.68,-56.92),'PA':(-3.42,-52.23),'PB':(-7.24,-36.78),
        'PE':(-8.81,-36.95),'PI':(-7.72,-42.73),'PR':(-25.25,-52.02),
        'RJ':(-22.91,-43.17),'RN':(-5.81,-36.20),'RO':(-11.51,-63.58),
        'RR':( 1.99,-61.33),'RS':(-30.03,-51.22),'SC':(-27.24,-50.22),
        'SE':(-10.57,-37.39),'SP':(-23.55,-46.63),'TO':(-10.18,-48.30),
    }

    state_s = df.groupby('customer_state').agg(
        order_count=('order_id','nunique'),
        total_revenue=('total_revenue','sum'),
        customer_count=('customer_unique_id','nunique'),
        avg_rating=('review_score','mean'),
        avg_shipping_days=('shipping_days','mean')
    ).reset_index().sort_values('total_revenue', ascending=False)

    state_s['State'] = state_s['customer_state'].apply(friendly_state)
    state_s['lat'] = state_s['customer_state'].map(lambda s: STATE_COORDS.get(s,(None,None))[0])
    state_s['lon'] = state_s['customer_state'].map(lambda s: STATE_COORDS.get(s,(None,None))[1])
    state_map = state_s.dropna(subset=['lat','lon'])

    metric_choice = st.radio(
        "Select metric to display on map:",
        ['total_revenue','order_count','customer_count','avg_rating'],
        horizontal=True,
        format_func=lambda x: {
            'total_revenue': '💰 Total Revenue',
            'order_count':   '📦 Order Count',
            'customer_count':'👥 Customer Count',
            'avg_rating':    '⭐ Average Rating'
        }[x]
    )

    MSCALE = {
        'total_revenue': cscale('#0c2340', C_blue),
        'order_count':   cscale('#1a0a2e', C_purple),
        'customer_count':cscale('#0a2318', C_green),
        'avg_rating':    cscale('#2a1500', C_orange),
    }
    MLABEL = {
        'total_revenue': 'Total Revenue ($)',
        'order_count':   'Order Count',
        'customer_count':'Customer Count',
        'avg_rating':    'Average Rating'
    }
    MHOVER = {
        'total_revenue': lambda r: f"${r:,.0f}",
        'order_count':   lambda r: f"{r:,} orders",
        'customer_count':lambda r: f"{r:,} customers",
        'avg_rating':    lambda r: f"{r:.2f} ★",
    }

    col_a, col_b = st.columns([3, 2])
    with col_a:
        fig_map = px.scatter_geo(
            state_map, lat='lat', lon='lon',
            size=metric_choice, color=metric_choice,
            hover_name='State',
            hover_data={
                metric_choice: ':,.0f' if metric_choice != 'avg_rating' else ':.2f',
                'lat': False, 'lon': False,
                'customer_state': False,
            },
            color_continuous_scale=MSCALE[metric_choice],
            size_max=55,
            title=f'Brazil Map – {MLABEL[metric_choice]} by State',
            scope='south america',
            fitbounds='locations',
            labels={metric_choice: MLABEL[metric_choice]}
        )
        fig_map.update_geos(
            showcountries=True, countrycolor=C_border2,
            showcoastlines=True, coastlinecolor=C_border2,
            showland=True, landcolor='#131928',
            showocean=True, oceancolor='#0b1220',
            showlakes=True, lakecolor='#0b1220',
            showsubunits=True, subunitcolor=C_border,
            projection_type='mercator',
        )
        fig_map.update_layout(**CT, height=440,
                              geo=dict(bgcolor='rgba(0,0,0,0)'),
                              coloraxis_colorbar=dict(
                                  title=dict(text=MLABEL[metric_choice], font=dict(color=C_text2)),
                                  len=0.55, thickness=11, tickfont=dict(color=C_text2)
                              ))
        st.plotly_chart(fig_map, use_container_width=True)

    with col_b:
        top10 = state_s.head(10).sort_values(metric_choice)
        fig2 = px.bar(top10, x=metric_choice, y='State', orientation='h',
                      title=f'Top 10 States – {MLABEL[metric_choice]}',
                      color=metric_choice, color_continuous_scale=MSCALE[metric_choice],
                      labels={metric_choice: MLABEL[metric_choice], 'State': 'State'})
        fig2.update_traces(
            hovertemplate='<b>%{y}</b><br>' + MLABEL[metric_choice] + ': %{x:,.0f}<extra></extra>'
        )
        fig2.update_layout(**CT, height=440, showlegend=False, coloraxis_showscale=False)
        fig2.update_xaxes(**AX, title=MLABEL[metric_choice])
        fig2.update_yaxes(**AX, title=None)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<p class='sec-header'>Revenue Heatmap: State × Category</p>", unsafe_allow_html=True)
    top8_s = state_s['customer_state'].head(8).tolist()
    sc = df[df['customer_state'].isin(top8_s)].groupby(
        ['customer_state','category_name'])['total_revenue'].sum().reset_index()
    top12c = sc.groupby('category_name')['total_revenue'].sum()\
               .sort_values(ascending=False).head(12).index.tolist()
    pivot = sc[sc['category_name'].isin(top12c)].pivot_table(
        index='customer_state', columns='category_name',
        values='total_revenue', aggfunc='sum', fill_value=0)
    pivot.index = [friendly_state(s) for s in pivot.index]

    fig3 = px.imshow(pivot, color_continuous_scale=cscale('#0c1a2e', C_blue),
                     title='Revenue Heatmap: Top 8 States × Top 12 Categories',
                     aspect='auto',
                     labels=dict(color='Revenue ($)', x='Category', y='State'))
    fig3.update_traces(hovertemplate='<b>%{y}</b> · %{x}<br>Revenue: $%{z:,.0f}<extra></extra>')
    fig3.update_layout(**CT, height=300)
    fig3.update_xaxes(**AX, tickangle=30, title=None)
    fig3.update_yaxes(**AX, title=None)
    st.plotly_chart(fig3, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        ship_s = df.groupby('customer_state')['shipping_days'].mean().reset_index()
        ship_s['State'] = ship_s['customer_state'].apply(friendly_state)
        ship_s.columns = ['customer_state','Avg Shipping Days','State']
        fig4 = px.bar(ship_s.sort_values('Avg Shipping Days').head(10),
                      x='Avg Shipping Days', y='State', orientation='h',
                      title='Fastest Shipping (avg days)',
                      color='Avg Shipping Days',
                      color_continuous_scale=cscale('#0a2318', C_green))
        fig4.update_traces(hovertemplate='<b>%{y}</b><br>Avg shipping: %{x:.1f} days<extra></extra>')
        fig4.update_layout(**CT, height=290, showlegend=False, coloraxis_showscale=False)
        fig4.update_xaxes(**AX, title='Average Shipping Days')
        fig4.update_yaxes(**AX, title=None)
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        fig5 = px.bar(ship_s.sort_values('Avg Shipping Days', ascending=False).head(10),
                      x='Avg Shipping Days', y='State', orientation='h',
                      title='Slowest Shipping (avg days)',
                      color='Avg Shipping Days',
                      color_continuous_scale=cscale('#2a1500', C_orange))
        fig5.update_traces(hovertemplate='<b>%{y}</b><br>Avg shipping: %{x:.1f} days<extra></extra>')
        fig5.update_layout(**CT, height=290, showlegend=False, coloraxis_showscale=False)
        fig5.update_xaxes(**AX, title='Average Shipping Days')
        fig5.update_yaxes(**AX, title=None)
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""<div class='insight'>
        💡 <strong>Insight:</strong> <strong>São Paulo (SP)</strong> dominates across all metrics.
        Southeast region (SP, RJ, MG) accounts for the majority of transactions.
        Optimizing warehouses and logistics in SP could significantly reduce costs and speed up delivery to most customers.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 – CUSTOMER SEGMENTATION (RFM)
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<p class='sec-header'>Customer Segmentation (RFM)</p>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.78rem; color:#8896b3; margin-bottom:0.8rem; line-height:1.6;'>
        RFM analysis segments customers based on three dimensions:
        <strong style='color:#4fc3f7'>Recency</strong> (how recently they purchased),
        <strong style='color:#a78bfa'>Frequency</strong> (how often they purchase), and
        <strong style='color:#34d399'>Monetary</strong> (how much they spend).
    </div>""", unsafe_allow_html=True)

    @st.cache_data
    def compute_rfm(data):
        rfm = data.groupby('customer_unique_id', as_index=False).agg(
            last_purchase=('order_purchase_timestamp','max'),
            frequency=('order_id','nunique'),
            monetary=('total_revenue','sum')
        )
        ref = data['order_purchase_timestamp'].max()
        rfm['days_since_purchase'] = (ref - rfm['last_purchase']).dt.days
        rfm.drop('last_purchase', axis=1, inplace=True)

        def rseg(d):
            if d<=7:    return '≤ 1 Week'
            elif d<=30:  return '≤ 1 Month'
            elif d<=180: return '≤ 6 Months'
            elif d<=360: return '≤ 1 Year'
            else:        return '> 1 Year'
        rfm['recency_range'] = rfm['days_since_purchase'].apply(rseg)

        rfm['R'] = pd.cut(rfm['days_since_purchase'], bins=5, labels=[5,4,3,2,1]).astype(int)
        rfm['F'] = pd.cut(rfm['frequency'].clip(upper=rfm['frequency'].quantile(0.99)),
                          bins=5, labels=[1,2,3,4,5]).astype(int)
        rfm['M'] = pd.cut(rfm['monetary'].clip(upper=rfm['monetary'].quantile(0.99)),
                          bins=5, labels=[1,2,3,4,5]).astype(int)

        def seg(row):
            r,f = row['R'], row['F']
            if r>=4 and f>=4:   return 'Champions'
            elif r>=3 and f>=3: return 'Loyal Customers'
            elif r>=4 and f<2:  return 'New Customers'
            elif r<2 and f>=3:  return 'At Risk'
            elif r<2 and f<2:   return 'Inactive'
            else:                return 'Potential'
        rfm['Segment'] = rfm.apply(seg, axis=1)
        return rfm

    rfm_df = compute_rfm(df)

    seg_counts  = rfm_df['Segment'].value_counts()
    seg_col_map = {
        'Champions':'green', 'Loyal Customers':'blue', 'New Customers':'teal',
        'Potential':'orange', 'At Risk':'pink', 'Inactive':'purple'
    }
    seg_desc = {
        'Champions':       'Frequent, high-value, recently active',
        'Loyal Customers': 'Regular purchasers with good spend',
        'New Customers':   'Recently acquired – need nurturing',
        'Potential':       'Have potential but inconsistent',
        'At Risk':         'Previously active, now fading',
        'Inactive':        'Long time no purchase',
    }
    seg_icon = {
        'Champions':'🏆','Loyal Customers':'💎','New Customers':'🌱',
        'Potential':'⚡','At Risk':'⚠️','Inactive':'😴'
    }
    scols = st.columns(len(seg_counts))
    for i,(seg,cnt) in enumerate(seg_counts.items()):
        with scols[i]:
            st.markdown(kpi(
                f"{seg_icon.get(seg,'')} {seg}",
                f"{cnt:,}",
                seg_desc.get(seg,'customers'),
                seg_col_map.get(seg,'blue')
            ), unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    order_range = ['≤ 1 Week','≤ 1 Month','≤ 6 Months','≤ 1 Year','> 1 Year']

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        rd = rfm_df['recency_range'].value_counts().reindex(order_range, fill_value=0).reset_index()
        rd.columns = ['Last Purchase','Customer Count']
        fig = px.bar(rd, x='Last Purchase', y='Customer Count',
                     title='Distribution by Time Since Last Purchase',
                     color='Customer Count',
                     color_continuous_scale=cscale('#1e2740', C_blue))
        fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y:,} customers<extra></extra>')
        fig.update_layout(**CT, height=270, showlegend=False, coloraxis_showscale=False)
        fig.update_xaxes(**AX, title=None, categoryorder='array', categoryarray=order_range)
        fig.update_yaxes(**AX, title='Customer Count')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        t5f = rfm_df.sort_values('frequency', ascending=False).head(5).copy()
        t5f['Rank'] = [f'#{i+1}' for i in range(5)]
        fig2 = px.bar(t5f, x='Rank', y='frequency',
                      title='Top 5 Most Frequent Buyers',
                      color='frequency',
                      color_continuous_scale=cscale('#2a1e40', C_purple),
                      labels={'frequency':'Number of Orders'})
        fig2.update_traces(hovertemplate='<b>Rank %{x}</b><br>Purchased %{y}x<extra></extra>')
        fig2.update_layout(**CT, height=270, showlegend=False, coloraxis_showscale=False)
        fig2.update_xaxes(**AX, title='Rank')
        fig2.update_yaxes(**AX, title='Order Count')
        st.plotly_chart(fig2, use_container_width=True)

    with col_c:
        t5m = rfm_df.sort_values('monetary', ascending=False).head(5).copy()
        t5m['Rank'] = [f'#{i+1}' for i in range(5)]
        fig3 = px.bar(t5m, x='Rank', y='monetary',
                      title='Top 5 Highest Spenders',
                      color='monetary',
                      color_continuous_scale=cscale('#0a2318', C_green),
                      labels={'monetary':'Total Spend ($)'})
        fig3.update_traces(hovertemplate='<b>Rank %{x}</b><br>Total spend: $%{y:,.0f}<extra></extra>')
        fig3.update_layout(**CT, height=270, showlegend=False, coloraxis_showscale=False)
        fig3.update_xaxes(**AX, title='Rank')
        fig3.update_yaxes(**AX, title='Total Spend ($)')
        st.plotly_chart(fig3, use_container_width=True)

    col_d, col_e = st.columns([2, 1])
    with col_d:
        fig4 = px.scatter(rfm_df.sample(min(3000,len(rfm_df))),
                          x='days_since_purchase', y='monetary',
                          color='Segment', size='frequency',
                          custom_data=['frequency'],
                          title='Customer Map: Days Since Last Purchase vs Total Spend',
                          color_discrete_sequence=PALETTE, size_max=18, opacity=0.65,
                          labels={
                              'days_since_purchase':'Days Since Last Purchase',
                              'monetary':'Total Spend ($)',
                              'frequency':'Frequency',
                              'Segment':'Customer Segment',
                          })
        fig4.update_traces(
            hovertemplate=(
                '<b>Segment: %{fullData.name}</b><br>'
                'Last purchase: %{x} days ago<br>'
                'Total spend: $%{y:,.0f}<br>'
                'Frequency: %{customdata[0]} orders'
                '<extra></extra>'
            )
        )
        fig4.update_layout(**CT, height=350)
        fig4.update_xaxes(**AX, title='Days Since Last Purchase')
        fig4.update_yaxes(**AX, title='Total Spend ($)')
        st.plotly_chart(fig4, use_container_width=True)

    with col_e:
        seg_rev = rfm_df.groupby('Segment')['monetary'].sum().reset_index()\
            .sort_values('monetary', ascending=False)
        fig5 = px.pie(seg_rev, values='monetary', names='Segment',
                      title='Revenue Share by Customer Segment',
                      color_discrete_sequence=PALETTE, hole=0.5)
        fig5.update_traces(
            textposition='inside', textinfo='percent+label', textfont_size=10,
            hovertemplate='<b>%{label}</b><br>Total spend: $%{value:,.0f}<br>Share: %{percent}<extra></extra>',
        )
        fig5.update_layout(**CT, height=350, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""<div class='insight'>
        💡 <strong>Insight:</strong> A large portion of customers fall into the <strong>Inactive</strong> segment
        (no purchase in over a year) — the platform heavily relies on new customer acquisition.
        High-value one-time buyers should be targeted with loyalty programs to encourage repeat purchases.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 – REVIEWS & DELIVERY
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<p class='sec-header'>Customer Reviews & Delivery Performance</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        rd2 = df['review_score'].value_counts().sort_index().reset_index()
        rd2.columns = ['Stars','Review Count']
        rd2['Percentage'] = rd2['Review Count'] / rd2['Review Count'].sum() * 100
        rd2['label_stars'] = rd2['Stars'].map({1:'1 ★',2:'2 ★★',3:'3 ★★★',4:'4 ★★★★',5:'5 ★★★★★'})
        fig = px.bar(rd2, x='Stars', y='Review Count',
                     title='Review Score Distribution',
                     color='Stars',
                     color_discrete_sequence=['#f87171','#fb923c','#fbbf24','#34d399','#4fc3f7'],
                     text='Percentage',
                     labels={'Stars':'Rating','Review Count':'Number of Reviews'})
        fig.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside',
            hovertemplate='<b>%{x} Stars</b><br>%{y:,} reviews (%{text:.1f}%)<extra></extra>',
        )
        fig.update_layout(**CT, height=290, showlegend=False)
        fig.update_xaxes(**AX, title='Rating', dtick=1,
                         ticktext=['1 ★','2 ★★','3 ★★★','4 ★★★★','5 ★★★★★'],
                         tickvals=[1,2,3,4,5])
        fig.update_yaxes(**AX, title='Review Count')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        delay_c = df['delay_days'].dropna().clip(-30, 60)
        fig2 = px.histogram(delay_c, nbins=50,
                            title='Delivery Delay Distribution',
                            color_discrete_sequence=[C_purple],
                            labels={'value':'Delay (days)','count':'Order Count'})
        fig2.add_vline(x=0, line_dash='dash', line_color=C_pink,
                       annotation_text='On Time', annotation_position='top right',
                       annotation_font_color=C_pink)
        fig2.update_traces(
            hovertemplate='Delay %{x} days: %{y:,} orders<extra></extra>'
        )
        fig2.update_layout(**CT, height=290, showlegend=False)
        fig2.update_xaxes(**AX, title='Days (negative = early)')
        fig2.update_yaxes(**AX, title='Order Count')
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        mr = df.groupby(['purchase_month_key','purchase_month_str']).agg(
            avg_rating=('review_score','mean'),
            review_count=('review_score','count')
        ).reset_index().sort_values('purchase_month_key')

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Scatter(
            x=mr['purchase_month_str'], y=mr['avg_rating'],
            name='Avg Rating', line=dict(color=C_yellow, width=2.5),
            mode='lines+markers',
            hovertemplate='<b>%{x}</b><br>Avg: %{y:.2f} ★<extra></extra>',
        ), secondary_y=False)
        fig3.add_trace(go.Bar(
            x=mr['purchase_month_str'], y=mr['review_count'],
            name='Review Count', marker_color=C_blue, opacity=0.35,
            hovertemplate='<b>%{x}</b><br>Reviews: %{y:,}<extra></extra>',
        ), secondary_y=True)
        fig3.update_layout(title='Monthly Review Trend', **CT, height=290)
        fig3.update_xaxes(**AX, tickangle=45)
        fig3.update_yaxes(title_text='Avg Rating', secondary_y=False, **AX)
        fig3.update_yaxes(title_text='Review Count', secondary_y=True,
                          gridcolor='rgba(0,0,0,0)', showgrid=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        cr = df.groupby('category_name').agg(
            avg_rating=('review_score','mean'),
            review_count=('review_score','count')
        ).reset_index()
        cr = cr[cr['review_count'] >= 100].sort_values('avg_rating', ascending=False).head(12)
        fig4 = px.bar(cr.sort_values('avg_rating'),
                      x='avg_rating', y='category_name', orientation='h',
                      title='Average Rating by Category (min. 100 reviews)',
                      color='avg_rating',
                      color_continuous_scale=cscale('#2a1500', C_yellow),
                      labels={'avg_rating':'Average Rating','category_name':'Category'})
        fig4.update_traces(
            hovertemplate='<b>%{y}</b><br>Avg: %{x:.2f} ★<extra></extra>'
        )
        fig4.update_layout(**CT, height=360, showlegend=False, coloraxis_showscale=False)
        fig4.update_xaxes(**AX, title='Average Rating', range=[3.5, 5])
        fig4.update_yaxes(**AX, title=None)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<p class='sec-header' style='margin-top:0.2rem'>Delivery Performance</p>", unsafe_allow_html=True)
    col_e, col_f = st.columns(2)
    with col_e:
        sc2 = df[(df['shipping_days'] >= 0) & (df['shipping_days'] <= 60)]['shipping_days']
        fig5 = px.histogram(sc2, nbins=40,
                            title='Shipping Duration Distribution (0–60 days)',
                            color_discrete_sequence=[C_teal],
                            labels={'value':'Shipping Days','count':'Order Count'})
        fig5.update_traces(hovertemplate='%{x} days: %{y:,} orders<extra></extra>')
        fig5.update_layout(**CT, height=270, showlegend=False)
        fig5.update_xaxes(**AX, title='Shipping Duration (days)')
        fig5.update_yaxes(**AX, title='Order Count')
        st.plotly_chart(fig5, use_container_width=True)

    with col_f:
        cor2 = df[['shipping_days','review_score']].dropna()
        cor2 = cor2[(cor2['shipping_days'] >= 0) & (cor2['shipping_days'] <= 60)]
        cor2['bucket'] = pd.cut(cor2['shipping_days'],
                                bins=[0,3,7,14,21,30,60],
                                labels=['0–3 days','4–7 days','8–14 days','15–21 days','22–30 days','31–60 days'])
        br = cor2.groupby('bucket', observed=True)['review_score'].mean().reset_index()
        br.columns = ['Shipping Duration','Avg Rating']
        fig6 = px.line(br, x='Shipping Duration', y='Avg Rating',
                       title='Impact of Shipping Time on Review Rating',
                       markers=True,
                       labels={'Shipping Duration':'Shipping Duration','Avg Rating':'Average Rating'})
        fig6.update_traces(
            line_color=C_blue, marker_color=C_teal, marker_size=9, line_width=2.5,
            hovertemplate='<b>%{x}</b><br>Avg: %{y:.2f} ★<extra></extra>',
        )
        fig6.update_layout(**CT, height=270)
        fig6.update_xaxes(**AX, title='Shipping Duration')
        fig6.update_yaxes(**AX, title='Average Rating', range=[1, 5])
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""<div class='insight'>
        💡 <strong>Insight:</strong> Longer shipping times strongly correlate with lower review ratings.
        Deliveries within <strong>3 days</strong> achieve the highest average scores.
        Investment in strategic logistics hubs is highly recommended to improve delivery speed.
    </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#2d3a52; font-size:0.68rem;
     border-top:1px solid #1a2035; margin-top:1.2rem; padding-top:0.8rem;'>
    TEMZ1 · Built with Streamlit & Plotly · Brazilian E-Commerce Dataset 2016–2018
</div>
""", unsafe_allow_html=True)