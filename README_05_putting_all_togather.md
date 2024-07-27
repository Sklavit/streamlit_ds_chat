# Step 5. Put all components together

Now I have code for:
- running Streamlit.app
- uploading sample dataset
- basic chat-like streamlit application
- generating code in response to the user request
- means for remote code execution
- preformatted params to draw charts with Bokeh
  (Bokeh exists for >10 years, Streamlit is quite young.  
  Probably, this is the reason why Gemini may generate Bokeh, but not Streamlit.chart code)

It is time now to put all components togather.

Example requests:
- Draw number of likes for people and fruits

conda create -p ./env12 -c conda-forge coiled python=3.12 "numpy<2.0.0" streamlit google-cloud-aiplatform dask


Known issues:
- Bokeh is not needed for workers but it is still provided.
- StreamlitAPIException: Streamlit only supports Bokeh version 2.4.3, but you have version 3.5.0 installed. Please run `pip install --force-reinstall --no-deps bokeh==2.4.3` to install the correct version.
- start of coiled cluster takes 1-2 minutes, but this will be the same for any cluster start on any tool
- hard to acquire good code from code generation; it usually works, but the return value is not exactly what was requested
  This complicates diagram generation on the client side.
- cluster disconnects and killed after set period of time, no reconnection implemented
- TODO needed some way to clear all interface