import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Ecommerce Analytics", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Clean & Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Soft background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean metric cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: left;
        margin-bottom: 24px;
    }
    .metric-title {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 800;
        white-space: nowrap;
        display: inline-block;
    }
    .metric-icon {
        float: right;
        font-size: 2rem;
        background: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    
    /* Fix multiselect tags */
    span[data-baseweb="tag"] {
        background-color: #e2e8f0 !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
    }
    span[data-baseweb="tag"] span[role="button"] {
        color: #64748b !important;
        background-color: transparent !important;
    }
    span[data-baseweb="tag"] span[role="button"]:hover {
        color: #ef4444 !important;
    }
    
    /* Titles alignment */
    h1, h2, h3 {
        text-align: left;
        color: #1e293b !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Format numbers helper
def format_num(num):
    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.1f}K"
    else:
        return f"${num:.0f}"

# 3. Load Data
@st.cache_data
def load_data():
    path = r"F:\archive (3)\Ecommerce_Sales_Data_2024_2025.csv"
    try:
        df = pd.read_csv(path)
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Month_Year'] = df['Order Date'].dt.to_period('M').astype(str)
        df['Year'] = df['Order Date'].dt.year
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 4. Sidebar
    st.sidebar.markdown("## ⚙️ Report Settings")
    st.sidebar.markdown("---")
    
    year_filter = st.sidebar.multiselect("Year:", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
    region_filter = st.sidebar.multiselect("Region:", options=df["Region"].unique(), default=df["Region"].unique())
    category_filter = st.sidebar.multiselect("Category:", options=df["Category"].unique(), default=df["Category"].unique())
    
    df_selection = df.query("Year in @year_filter & Region in @region_filter & Category in @category_filter")

    # 5. Header
    st.markdown("<h1 style='margin-bottom: 30px;'>📊 E-Commerce Sales Analytics</h1>", unsafe_allow_html=True)
    
    if not df_selection.empty:
        # 6. Metrics
        s_total = df_selection["Sales"].sum()
        p_total = df_selection["Profit"].sum()
        o_total = df_selection["Order ID"].nunique()
        d_avg = df_selection["Discount"].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-title">Total Sales</div>
            <div class="metric-value">{format_num(s_total)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col2.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-title">Total Profit</div>
            <div class="metric-value">{format_num(p_total)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col3.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📦</div>
            <div class="metric-title">Total Orders</div>
            <div class="metric-value">{o_total:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col4.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏷️</div>
            <div class="metric-title">Avg Discount</div>
            <div class="metric-value">{d_avg:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 7. Charts
        c1, c2 = st.columns(2)
        
        with c1: 
            m_sales = df_selection.groupby('Month_Year')['Sales'].sum().reset_index().sort_values('Month_Year')
            fig_line = px.line(m_sales, x='Month_Year', y='Sales', 
                               title='📈 Monthly Sales Trend', 
                               markers=True,
                               line_shape='spline')
            fig_line.update_traces(line=dict(color='#2563eb', width=4), marker=dict(size=8, color='#1e40af'))
            fig_line.update_layout(xaxis_title="", yaxis_title="Sales ($)", 
                                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family="Inter", size=14, color="#475569"),
                                   title_font=dict(size=20, color="#0f172a", family="Inter"),
                                   xaxis=dict(tickangle=45, showgrid=False),
                                   yaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
                                   height=400, margin=dict(l=0, r=0, t=50, b=0))
            st.plotly_chart(fig_line, use_container_width=True)
            
        with c2: 
            cat_p = df_selection.groupby('Category')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True)
            fig_bar = px.bar(cat_p, x='Profit', y='Category', orientation='h',
                             title='💰 Profit by Category', 
                             color='Profit', color_continuous_scale='Blues')
            fig_bar.update_layout(xaxis_title="Profit ($)", yaxis_title="",
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family="Inter", size=14, color="#475569"),
                                  title_font=dict(size=20, color="#0f172a", family="Inter"),
                                  coloraxis_showscale=False,
                                  xaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
                                  height=400, margin=dict(l=0, r=0, t=50, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        
        with c3: 
            reg_sales = df_selection.groupby('Region')['Sales'].sum().reset_index()
            fig_pie = px.pie(reg_sales, values='Sales', names='Region', hole=0.5,
                             title='🌍 Sales by Region',
                             color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#6366f1', '#8b5cf6'])
            fig_pie.update_layout(font=dict(family="Inter", size=15, color="#475569"),
                                  title_font=dict(size=20, color="#0f172a", family="Inter"),
                                  height=400, margin=dict(l=0, r=0, t=50, b=0))
            fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c4: 
            sub_sales = df_selection.groupby('Sub-Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(5)
            fig_bar2 = px.bar(sub_sales, x='Sub-Category', y='Sales',
                             title='🔥 Top 5 Sub-Categories', 
                             color='Sales', color_continuous_scale='Teal')
            fig_bar2.update_layout(xaxis_title="", yaxis_title="Sales ($)",
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family="Inter", size=14, color="#475569"),
                                  title_font=dict(size=20, color="#0f172a", family="Inter"),
                                  coloraxis_showscale=False,
                                  yaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
                                  height=400, margin=dict(l=0, r=0, t=50, b=0))
            st.plotly_chart(fig_bar2, use_container_width=True)
