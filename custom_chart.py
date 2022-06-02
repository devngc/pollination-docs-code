"""A module showing how to create a custom chart in a Pollination app."""

import streamlit as st
from ladybug.epw import EPW
from ladybug.analysisperiod import AnalysisPeriod

st.set_page_config(
    page_title='Dry bulb temperature', layout='wide'
)


epw = EPW("./assets/sample.epw")
dbt = epw.dry_bulb_temperature


dbt_work_hours = dbt.filter_by_analysis_period(
    AnalysisPeriod(1, 1, 9, 12, 31, 17)).filter_by_conditional_statement('a>=18 and a<=24')
figure = dbt_work_hours.heat_map()


st.title("Dry bulb temperature")
st.plotly_chart(figure, use_container_width=True)
