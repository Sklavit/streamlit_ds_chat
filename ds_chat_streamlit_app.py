import streamlit as st
import importlib

from dask.distributed import Client

import pandas as pd
from rich.pretty import pprint

from vertex_ai_codegen import (
    start_code_generator_chat,
    GENERATION_CONFIG,
    SAFETY_SETTINGS,
)

st.title("DS chat with Google Vertex AI")

########################################################################################################################
# Initialization

# init chat model

if "vertex_ai_model" not in st.session_state:
    st.session_state["vertex_ai_model"] = "gemini-1.5-flash-001"

if "code_get_chat" not in st.session_state:
    chat = start_code_generator_chat(
        st.secrets["gcs_connections"], model_name=st.session_state["vertex_ai_model"]
    )
    st.session_state.code_get_chat = chat
else:
    chat = st.session_state.code_get_chat

# Create or connect to a Coiled cluster
with st.spinner("Creating or connecting to a Coiled cluster"):
    if "cluster" not in st.session_state:
        import coiled

        cluster = coiled.Cluster(
            name="my-cluster", n_workers=1, idle_timeout="20 minutes"
        )
        # n_workers – Number of workers in this cluster.
        # Can either be an integer for a static number of workers,
        # or a list specifying the lower and upper bounds for adaptively scaling up/ down workers
        # depending on the amount of work submitted.
        # Defaults to n_workers=[4, 20] which adaptively scales between 4 and 20 workers.
        client = Client(cluster)
        st.session_state.cluster = cluster
        st.session_state.client = client
    else:
        cluster = st.session_state.cluster
        client = st.session_state.client

########################################################################################################################
# Helpful sidebar

with st.sidebar:
    "[View the source code](https://github.com/Sklavit/pet_project/tree/20240629_ds_chat/apps/streamlit_ds_chat)"

########################################################################################################################
# Get data to analyze

# upload some dataset to analyze
uploaded_file = st.file_uploader("Upload a dataset to be analyzed", type=["csv"])

# NOTE this upload ALWAYS reload the page, which is a bit of dangerous
# TODO it is better to add buttons: 'reset and use new file', 'do all operations with new file'
# TODO it looks like cool functionality to replay analysis for other data

if not uploaded_file:
    st.error("Upload dataset to work with")
    st.stop()
else:
    # if uploaded_file:  # and question:  # and anthropic_api_key:
    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe)

    ####################################################################################################################
    # Chat logic goes here

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display all session history
    for message in st.session_state.messages:
        # set custom avatars for system messages (they are not saved in the history)
        kwargs = {}
        match message["role"]:
            case "error":
                kwargs["avatar"] = "🛑"
            case "info":
                kwargs["avatar"] = "📝"

        with st.chat_message(message["role"], **kwargs):
            st.write(message["content"])

    if prompt := st.chat_input("What do you what to ask about given dataset?"):
        # save user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

        # render user prompt in chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # processing of the assistant response
        with st.chat_message("assistant"):
            # step 1. code generation
            with st.spinner(
                "Waiting for the whole generated code "
                "(streaming not working with Streamlit and this beta version of vertexAI)..."
            ):
                # TODO componentize this direct usage of chat.send_message
                api_response = chat.send_message(
                    prompt,
                    generation_config=GENERATION_CONFIG,
                    safety_settings=SAFETY_SETTINGS,
                    stream=False,
                )
                response = api_response.candidates[0].content.parts[0]._raw_part.text

            st.markdown(response)
            print("A")
            st.session_state.messages.append({"role": "assistant", "content": response})

        print("B")

        response = response.strip()

        # This response should be in the form of code
        if not (response.startswith("```python") and response.endswith("```")):
            st.error("AI response is not a code!")
            pprint(response)
            print("C")
            st.rerun()

        print("D")
        with st.chat_message("assistant"):
            st.info("So, this is code")

        # so, the response IS code. Save it to tmp file
        # TODO using only one and the same file is not safe in multiuser environment
        file = "task.py"
        with open(file, "w") as file:
            file.write(response[10:-3])

        msg = "Generated code was saved to the file"
        st.info(msg)

        # Now we should run remote execution
        with st.spinner("Waiting for remote code execution..."):
            # Step 2: Upload the module file to all workers
            # TODO using the same file is unsafe, especially for multiple users working at the same time
            file_name = "task.py"
            try:
                client.upload_file(file_name)
            except Exception as e:
                st.error(e)
                st.write(e)
                st.write(client)
                st.write(client.status)

                if client.status == "closed":
                    client.restart()

            # Use the uploaded module in a distributed task
            def use_uploaded_module():
                try:
                    module = importlib.import_module(file_name[:-3])
                    print(f"Successfully imported {file_name}")
                except ImportError as e:
                    print(f"Error importing {file_name}: {e}")
                    return None

                return module.run({"df_table": dataframe})

            execution_results = client.run(use_uploaded_module)
            # get the result from the first executor TODO there is a dict at all?
            result = next(iter(execution_results.values()))

        with st.chat_message("assistant"):
            # st.info(result)
            print("vertexAI response:")
            pprint(result)
            answer = result.get("results")
            st.write(answer)

            # save results in the history, so they will ba available for chatbot later
            st.session_state.messages.append({"role": "assistant", "content": answer})
            api_response = chat.send_message(
                f"Below is the result of the execution of your code, from the last response. "
                f"So, the response to question <q>{prompt}</q> is <response>{answer}</response>.",
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
                stream=False,
            )
            response = api_response.candidates[0].content.parts[0]._raw_part.text
            st.divider()
            st.markdown(response)
            st.divider()

            # Let's show some charts
            chart = result.get("chart")
            if chart:
                st.write("Chart is here")
                kwargs = chart.get("kwargs", {})

                st.write(answer)

                st.markdown(f'*{chart.get("title")}*')
                match chart["chart_type"]:
                    case "bar_chart":
                        st.bar_chart(
                            chart["source"],
                            x=chart.get("x"),
                            y=chart.get("y"),
                            x_label=kwargs.get("x_label"),
                            y_label=kwargs.get("y_label"),
                        )
                    case "line_chart":
                        st.line_chart(
                            chart["source"],
                            x=chart.get("x"),
                            y=chart.get("y"),
                            x_label=kwargs.get("x_label"),
                            y_label=kwargs.get("y_label"),
                        )
                    case "scatter_chart":
                        st.scatter_chart(
                            chart["source"],
                            x=chart.get("x"),
                            y=chart.get("y"),
                            x_label=kwargs.get("x_label"),
                            y_label=kwargs.get("y_label"),
                        )
