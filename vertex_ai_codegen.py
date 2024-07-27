import vertexai
import vertexai.preview.generative_models as generative_models
from google.oauth2.service_account import Credentials
from vertexai.generative_models import GenerativeModel, ChatSession

GENERATION_CONFIG = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def start_code_generator_chat(
    service_account_info, *, model_name="gemini-1.5-flash-001"
) -> ChatSession:
    """Create (?) connection to Vertex AI and initialize chat model for Code Generation task.

    Parameters
    ==========
    service_account_info : dict[str, str]
        The service account info in Google format.
    model_name : str
        The name of the Vertex AI model.

    Returns
    =======
    ChatSession
    """
    credentials = Credentials.from_service_account_info(service_account_info)
    vertexai.init(
        project="pivotal-cable-428219-c5",
        location="us-central1",
        credentials=credentials,
    )
    model = GenerativeModel(
        model_name,  # by default, it will be "gemini-1.5-flash-001",
        system_instruction=[
            "You are a data scientist manager."
            "You responsibility is to provide a plan of actions, which should be taken to answer the given question."
            "Each new question will be marked by tags: <q> and </q>."
            "If you don't have enough data to answer the question, respond: <not enough data/>"
            "Information about loaded data will be provided between tags <locals> and </locals> in JSON format."
            "You will be questioned with analytical questions about the data available in <locals>."
            "Write a full python module, which should contain only 1 function def run(data). "
            "The data parameter is expected to be a dictionary, with the same keys as <locals> and with corresponding values. "
            "The function should return the answer to the question in form of dictionary. "
            "Key `results` should include the answer represented in the most structured way: "
            "it should be a single number if possible, it may be list, or pandas.DataFrame. "
            "The function should not return the string unless it is directly requested by the user question. "
            "For example, the function may return string, if question was asked about something specific, like name of the person, "
            "who satisfy some conditions. For example: `<s>Who likes the most number of fruits?</s>`. "
            "Key `chart` should be `None` if no charts need, and be a dictionary if a chart is requested. "
            "This dictionary should contain the following keys: \n"
            "`chart_type`: One from list [`bar_chart`, `line_chart`, `scatter_chart`]\n"
            "`title`: the chart title\n"
            "`x`: Column name or key associated to the x-axis data. "
            "Should be `None` is the data index intended to be used for the x-axis values.\n"
            "`y`: Column name(s) or key(s) associated to the y-axis data. "
            "Should be `None`, if the data of all remaining columns intended to be used as data series."
            "Should be a Sequence of strings, if intended to draw several series on the same chart "
            "by melting wide-format table into a long-format table behind the scenes.\n"
            "`x_label`: The label for the x-axis. Should be `None` if intended to use the column name specified in `x`."
            "`y_label`: The label for the y-axis. Should be `None` if intended to use the column name specified in `y`."
            "`kwargs`: dict with kwargs for the corresponding Bokeh charting tool\n"
            "`source`: `pandas.DataFrame` with datapoints to be plotted.\n"
            "You should *not* write any code for chart plotting inside the python code, only return needed kwargs."
            "You must include explanations or any other important information into your answer in the form of code comments."
            "User may update the state of <locals> with messages starting with 'Update locals:'. You should update the state of <locals> respectively"
            "On message starting with '`locals' you should return the current state of <locals>.",
            "<locals>{" "df_table: {type: pandas.DataFrame}" "}</locals>",
        ],
    )
    chat = model.start_chat()
    return chat


"""
    _USER_ROLE = "user"
    _MODEL_ROLE = "model"
"""
