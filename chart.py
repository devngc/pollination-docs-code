"""A module showing how to create a chart in a Pollination app."""

import streamlit as st
from ladybug.epw import EPW


st.set_page_config(
    page_title='Wind rose', layout='wide'
)


epw = EPW("./assets/sample.epw")
figure = epw.dry_bulb_temperature.heat_map()


st.title("Dry bulb temperature")
st.plotly_chart(figure, use_container_width=True)
