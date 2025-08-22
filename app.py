import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="COVID-19 Global Analytics Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .sidebar-info {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and preprocess COVID-19 data from Our World in Data"""
    try:
        url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
        df = pd.read_csv(url)

        # Basic preprocessing
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(['country', 'date'])

        # Fill missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


@st.cache_data
def calculate_global_stats(df):
    """Calculate global statistics"""
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    total_cases = latest_data['total_cases'].sum()
    total_deaths = latest_data['total_deaths'].sum()
    total_vaccinations = latest_data['total_vaccinations'].sum()

    # Calculate daily changes
    prev_date = latest_date - timedelta(days=1)
    prev_data = df[df['date'] == prev_date]

    new_cases = latest_data['new_cases'].sum()
    new_deaths = latest_data['new_deaths'].sum()

    return {
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'total_vaccinations': total_vaccinations,
        'new_cases': new_cases,
        'new_deaths': new_deaths,
        'latest_date': latest_date
    }


def create_global_trend_chart(df):
    """Create global trend chart"""
    global_daily = df.groupby('date').agg({
        'new_cases': 'sum',
        'new_deaths': 'sum',
        'total_cases': 'sum',
        'total_deaths': 'sum'
    }).reset_index()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily New Cases', 'Daily Deaths', 'Cumulative Cases', 'Cumulative Deaths'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Daily new cases
    fig.add_trace(
        go.Scatter(x=global_daily['date'], y=global_daily['new_cases'],
                   mode='lines', name='New Cases', line=dict(color='#ff7f0e')),
        row=1, col=1
    )

    # Daily deaths
    fig.add_trace(
        go.Scatter(x=global_daily['date'], y=global_daily['new_deaths'],
                   mode='lines', name='New Deaths', line=dict(color='#d62728')),
        row=1, col=2
    )

    # Cumulative cases
    fig.add_trace(
        go.Scatter(x=global_daily['date'], y=global_daily['total_cases'],
                   mode='lines', name='Total Cases', line=dict(color='#1f77b4')),
        row=2, col=1
    )

    # Cumulative deaths
    fig.add_trace(
        go.Scatter(x=global_daily['date'], y=global_daily['total_deaths'],
                   mode='lines', name='Total Deaths', line=dict(color='#ff0000')),
        row=2, col=2
    )

    fig.update_layout(height=600, showlegend=False, title_text="Global COVID-19 Trends")
    return fig


def create_country_comparison_chart(df, countries, metric):
    """Create country comparison chart"""
    country_data = df[df['country'].isin(countries)]

    fig = px.line(
        country_data,
        x='date',
        y=metric,
        color='country',
        title=f'{metric.replace("_", " ").title()} by Country',
        labels={'date': 'Date', metric: metric.replace("_", " ").title()}
    )

    fig.update_layout(height=500)
    return fig


def create_top_countries_chart(df, metric, top_n=15):
    """Create top countries chart"""
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    top_countries = latest_data.nlargest(top_n, metric)[['country', metric]]

    fig = px.bar(
        top_countries,
        x=metric,
        y='country',
        orientation='h',
        title=f'Top {top_n} Countries by {metric.replace("_", " ").title()}',
        labels={'country': 'Country', metric: metric.replace("_", " ").title()}
    )

    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    return fig


def create_vaccination_chart(df):
    """Create vaccination progress chart"""
    # Filter countries with significant vaccination data
    vacc_data = df[df['total_vaccinations'] > 0].copy()

    if vacc_data.empty:
        return None

    # Get latest vaccination data
    latest_date = vacc_data['date'].max()
    latest_vacc = vacc_data[vacc_data['date'] == latest_date]

    # Top 20 countries by vaccination
    top_vacc = latest_vacc.nlargest(20, 'total_vaccinations')

    fig = px.bar(
        top_vacc,
        x='total_vaccinations',
        y='country',
        orientation='h',
        title='Top 20 Countries by Total Vaccinations',
        labels={'total_vaccinations': 'Total Vaccinations', 'country': 'Country'}
    )

    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    return fig


def create_case_fatality_rate_chart(df):
    """Create case fatality rate chart"""
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date].copy()

    # Calculate case fatality rate
    latest_data = latest_data[latest_data['total_cases'] > 1000]  # Filter countries with >1000 cases
    latest_data['cfr'] = (latest_data['total_deaths'] / latest_data['total_cases']) * 100
    latest_data = latest_data.dropna(subset=['cfr'])

    # Top 20 countries by CFR
    top_cfr = latest_data.nlargest(20, 'cfr')

    fig = px.bar(
        top_cfr,
        x='cfr',
        y='country',
        orientation='h',
        title='Case Fatality Rate by Country (Countries with >1000 cases)',
        labels={'cfr': 'Case Fatality Rate (%)', 'country': 'Country'}
    )

    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    return fig


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">🦠 COVID-19 Global Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Load data
    with st.spinner('Loading COVID-19 data...'):
        df = load_data()

    if df is None:
        st.stop()

    # Sidebar
    st.sidebar.markdown('<div class="sidebar-info"><h3>📊 Dashboard Controls</h3></div>', unsafe_allow_html=True)

    # Date range selector
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - timedelta(days=90), max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter data by date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    else:
        df_filtered = df

    # Country selector for comparison
    countries = sorted(df['country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select Countries for Comparison",
        countries,
        default=['United States', 'India', 'Brazil', 'Russia', 'France'] if all(
            c in countries for c in ['United States', 'India', 'Brazil', 'Russia', 'France']) else countries[:5]
    )

    # Metric selector
    metrics = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
    selected_metric = st.sidebar.selectbox(
        "Select Metric for Country Comparison",
        metrics,
        format_func=lambda x: x.replace('_', ' ').title()
    )

    # Global Statistics
    st.markdown("## 📈 Global Statistics")

    global_stats = calculate_global_stats(df)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Cases",
            f"{global_stats['total_cases']:,.0f}",
            f"+{global_stats['new_cases']:,.0f}"
        )

    with col2:
        st.metric(
            "Total Deaths",
            f"{global_stats['total_deaths']:,.0f}",
            f"+{global_stats['new_deaths']:,.0f}"
        )

    with col3:
        if global_stats['total_vaccinations'] > 0:
            st.metric(
                "Total Vaccinations",
                f"{global_stats['total_vaccinations']:,.0f}"
            )
        else:
            st.metric("Total Vaccinations", "N/A")

    with col4:
        if global_stats['total_cases'] > 0:
            cfr = (global_stats['total_deaths'] / global_stats['total_cases']) * 100
            st.metric("Global CFR", f"{cfr:.2f}%")
        else:
            st.metric("Global CFR", "N/A")

    with col5:
        st.metric(
            "Last Updated",
            global_stats['latest_date'].strftime('%Y-%m-%d')
        )

    # Global Trends
    st.markdown("## 🌍 Global Trends")

    global_trend_fig = create_global_trend_chart(df_filtered)
    st.plotly_chart(global_trend_fig, use_container_width=True)

    # Country Comparison
    if selected_countries:
        st.markdown("## 🔄 Country Comparison")

        comparison_fig = create_country_comparison_chart(df_filtered, selected_countries, selected_metric)
        st.plotly_chart(comparison_fig, use_container_width=True)

    # Top Countries Analysis
    st.markdown("## 🏆 Top Countries Analysis")

    col1, col2 = st.columns(2)

    with col1:
        top_cases_fig = create_top_countries_chart(df, 'total_cases')
        st.plotly_chart(top_cases_fig, use_container_width=True)

    with col2:
        top_deaths_fig = create_top_countries_chart(df, 'total_deaths')
        st.plotly_chart(top_deaths_fig, use_container_width=True)

    # Vaccination Analysis
    vacc_fig = create_vaccination_chart(df)
    if vacc_fig:
        st.markdown("## 💉 Vaccination Progress")
        st.plotly_chart(vacc_fig, use_container_width=True)

    # Case Fatality Rate Analysis
    st.markdown("## ⚠️ Case Fatality Rate Analysis")
    cfr_fig = create_case_fatality_rate_chart(df)
    st.plotly_chart(cfr_fig, use_container_width=True)

    # Data Explorer
    with st.expander("🔍 Data Explorer"):
        st.markdown("### Raw Data Sample")
        st.dataframe(df.head(100))

        st.markdown("### Data Summary")
        st.write(f"**Total Countries:** {df['country'].nunique()}")
        st.write(f"**Date Range:** {df['date'].min().date()} to {df['date'].max().date()}")
        st.write(f"**Total Records:** {len(df):,}")

        # Download data
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Dataset",
            data=csv,
            file_name='covid19_data.csv',
            mime='text/csv'
        )


if __name__ == "__main__":
    main()