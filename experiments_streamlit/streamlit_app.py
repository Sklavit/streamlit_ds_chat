import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

# the application layout and title
st.set_page_config(
    layout="centered",
    page_title="DS agent chat",
    page_icon=":shark:",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "This app should work as AI Data Scientist, how answers questions about the given data."
    },
)

st.write("Hello world!")

st.header("st.button")

if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

"""
st.write allows writing text and arguments to the Streamlit app.

In addition to being able to display text, the following can also be displayed via the st.write() command:

Prints strings; works like st.markdown()
Displays a Python dict
Displays pandas DataFrame can be displayed as a table
Plots/graphs/figures from matplotlib, plotly, altair, graphviz, bokeh
And more (see st.write on API docs)
"""

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
st.write(df)

# Example 4

st.write("Below is a DataFrame:", df, "Above is a dataframe.")

# Example 5

df2 = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])
c = (
    alt.Chart(df2)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)
st.write(c)

# or
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)
