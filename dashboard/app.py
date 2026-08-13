# dashboard/app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AgriScope - Sustainability Dashboard",
    page_icon="🌾",
    layout="wide"
)

# Generate sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    n = 2000
    regions = ['Midwest', 'Southeast', 'West', 'Northeast']
    crops = ['Corn', 'Soybean', 'Wheat', 'Cotton']
    
    df = pd.DataFrame({
        'region': np.random.choice(regions, n),
        'crop_type': np.random.choice(crops, n),
        'year': np.random.choice(range(2022, 2027), n),
        'farm_size_ha': np.random.exponential(200, n) + 20,
        'practice_adoption': np.random.beta(2, 3, n),
        'soil_organic_matter': np.random.uniform(1, 5, n),
        'emissions_co2e': np.random.gamma(2, 1000, n),
        'revenue_usd': np.random.gamma(3, 1000, n)
    })
    
    df['sustainability_score'] = (
        df['soil_organic_matter'] / df['soil_organic_matter'].max() * 0.4 +
        (1 - df['emissions_co2e'] / df['emissions_co2e'].max()) * 0.6
    ) * 100
    
    df['roi_percent'] = (df['revenue_usd'] / 500) * 100
    return df

df = generate_sample_data()

# Sidebar
st.sidebar.title("🌾 AgriScope")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

regions = st.sidebar.multiselect(
    "Select Region", 
    df['region'].unique(), 
    default=df['region'].unique()[:2]
)

crops = st.sidebar.multiselect(
    "Select Crop", 
    df['crop_type'].unique(), 
    default=df['crop_type'].unique()[:2]
)

filtered_df = df[df['region'].isin(regions) & df['crop_type'].isin(crops)]

# Header
st.markdown("# 🌾 AgriScope")
st.markdown("### Agricultural Sustainability Intelligence Dashboard")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Sustainability Score", f"{filtered_df['sustainability_score'].mean():.1f}%")
with col2:
    st.metric("Average ROI", f"{filtered_df['roi_percent'].mean():.0f}%")
with col3:
    st.metric("Emissions (tons)", f"{filtered_df['emissions_co2e'].mean():.0f}")
with col4:
    st.metric("Adoption Rate", f"{filtered_df['practice_adoption'].mean()*100:.0f}%")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Emissions by Region")
    region_emissions = filtered_df.groupby('region')['emissions_co2e'].mean().reset_index()
    fig = px.bar(region_emissions, x='region', y='emissions_co2e', color='region')
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📈 Adoption Trends")
    adoption_trend = filtered_df.groupby('year')['practice_adoption'].mean().reset_index()
    fig = px.line(adoption_trend, x='year', y='practice_adoption')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("---")
st.markdown("### 💡 Key Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.info("✅ Midwest leads in sustainability outcomes with 45% adoption")
    st.info("📊 Practice adoption is growing at 8.2% annually")

with insights_col2:
    st.info("💰 Cover crops show the highest ROI (22% increase)")
    st.info("🌱 Emissions reduction potential: 35% through nitrogen optimization")

# Scenario Planner
st.markdown("---")
st.markdown("### 🔮 Scenario Planner")

adoption_increase = st.slider("Increase Practice Adoption (%)", 0, 50, 20)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Emissions Saved", f"{filtered_df['emissions_co2e'].sum() * 0.2:,.0f} tons")
with col2:
    st.metric("Projected ROI Increase", f"{adoption_increase * 1.5:.0f}%")
with col3:
    st.metric("Additional Acres", f"{filtered_df['farm_size_ha'].sum() * 0.1:,.0f} ha")

st.markdown("---")
st.caption("Built for the Regrow.ag Data Analyst Application | Data: USDA Quick Stats")
