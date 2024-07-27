import time

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # To read file as string:
    string_data = stringio.readline()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)

    # from stqdm import stqdm
    # dataframe = pd.concat([chunk for chunk in stqdm(pd.read_csv(uploaded_file, chunksize=1000), desc='Loading data')])

    st.write(dataframe)

    with st.sidebar:
        with st.echo():
            st.write("This code will be printed to the sidebar.")

        with st.spinner("Loading..."):
            time.sleep(5)
        st.success("Done!")
