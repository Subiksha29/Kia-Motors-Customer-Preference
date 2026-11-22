import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency
from pathlib import Path

st.set_page_config(page_title="Kia Motors Consumer Study", page_icon="🚗", layout="wide")

ROOT = Path(__file__).parent
freq_path = ROOT / "data" / "frequency_data.csv"
cross_path = ROOT / "data" / "satisfaction_crosstabs.csv"

st.title("Kia Motors – Consumer Preference Study")
st.caption("Coimbatore District | Project dashboard based on the supplied project report")

freq = pd.read_csv(freq_path)
cross = pd.read_csv(cross_path)

st.info(
    "This dashboard uses grouped respondent counts transcribed from the report. "
    "It does not contain individual respondent records. Percentages are displayed as reported in the document."
)

total_respondents = 180
c1, c2, c3 = st.columns(3)
c1.metric("Reported sample size", total_respondents)
c2.metric("Frequency categories", len(freq))
c3.metric("Satisfaction cross-tab rows", len(cross))

tab1, tab2, tab3 = st.tabs(["Frequency analysis", "Satisfaction analysis", "About the project"])

with tab1:
    st.subheader("Percentage / frequency analysis")
    variables = sorted(freq["variable"].dropna().unique().tolist())
    selected = st.selectbox("Choose a survey factor", variables)
    view = freq[freq["variable"] == selected].copy()
    view["reported_percentage"] = pd.to_numeric(view["reported_percentage"], errors="coerce")
    left, right = st.columns([1, 1])
    with left:
        st.dataframe(
            view[["category", "respondents", "reported_percentage"]]
            .rename(columns={"category": "Category", "respondents": "Respondents",
                             "reported_percentage": "Reported percentage (%)"}),
            use_container_width=True, hide_index=True
        )
    with right:
        fig = px.bar(view, x="category", y="respondents",
                     title=f"Respondents by {selected}", text="respondents")
        fig.update_layout(xaxis_title="", yaxis_title="Number of respondents")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Level of satisfaction by socio-economic factor")
    variables = sorted(cross["variable"].dropna().unique().tolist())
    selected = st.selectbox("Choose a factor for cross-tabulation", variables, key="cross_variable")
    view = cross[cross["variable"] == selected].copy()
    observed = view[["high", "moderate", "low"]].astype(int)
    st.dataframe(
        view[["category", "high", "moderate", "low"]]
        .rename(columns={"category": "Category", "high": "High", "moderate": "Moderate", "low": "Low"}),
        use_container_width=True, hide_index=True
    )
    fig = px.bar(view, x="category", y=["high", "moderate", "low"],
                 barmode="group", title=f"Satisfaction levels by {selected}",
                 labels={"value": "Respondents", "category": selected, "variable": "Satisfaction"})
    st.plotly_chart(fig, use_container_width=True)

    if len(observed) >= 2 and observed.to_numpy().sum() > 0:
        chi2, p_value, dof, expected = chi2_contingency(observed.to_numpy())
        a, b, c = st.columns(3)
        a.metric("Chi-square statistic", f"{chi2:.3f}")
        b.metric("Degrees of freedom", int(dof))
        c.metric("P-value", f"{p_value:.4f}")
        st.caption(
            "Interpretation at 5% significance: " +
            ("Evidence of an association (p < 0.05)." if p_value < 0.05
             else "No statistically significant association detected (p ≥ 0.05).")
        )
        st.caption("The test is calculated from the displayed grouped counts. Review expected cell frequencies before using the result in a formal report.")
    else:
        st.warning("Not enough categories to calculate the Chi-square test.")

with tab3:
    st.subheader("Project details")
    st.markdown("""
    **Project title:** A Study on Consumer Preference Towards Kia Motors with Special Reference to Coimbatore District

    **Study design:** Descriptive study  
    **Study area:** Coimbatore District  
    **Sample size:** 180 respondents  
    **Period stated in report:** January 2025 to March 2025  
    **Statistical methods stated in report:** Percentage Analysis and Chi-square Test

    **Objectives**
    - Identify the mode of car purchase by consumers.
    - Study factors influencing consumers when choosing cars.
    - Assess customers' opinions on Kia Motors' brand performance.
    - Test association with selected socio-economic variables.

    **Data note:** The source document contains aggregate tables, not respondent-level records.
    Some source tables contain inconsistent totals or percentages. The app preserves the extracted
    table values and calculates tests only from the displayed satisfaction cross-tab counts.
    """)
    st.download_button("Download frequency data (CSV)", freq.to_csv(index=False).encode("utf-8"),
                       "frequency_data.csv", "text/csv")
    st.download_button("Download satisfaction cross-tabs (CSV)", cross.to_csv(index=False).encode("utf-8"),
                       "satisfaction_crosstabs.csv", "text/csv")

st.divider()
st.caption("Educational project prototype. Verify source-table values before submitting statistical conclusions.")
