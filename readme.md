Title
feat: add Streamlit app for DS chat with Google Vertex AI and Coiled integration

Overview
Introduced a new Streamlit application for data science chat functionality using Google Vertex AI.
Added multiple supporting scripts and modules for handling various functionalities such as code generation, cloud execution, and data visualization.
Integrated Coiled for distributed computing and remote code execution.
Provided detailed documentation and examples for setting up the environment, using the application, and testing different components.


# Setting up a local development environment

Before we can actually start building Streamlit apps, we will first have to set up a development environment.

Let's start by installing and setting up a conda environment.

## **Install conda**
- Install `conda` by going to https://docs.conda.io/en/latest/miniconda.html and choose your operating system (Windows, Mac or Linux). 
- Download and run the installer to install `conda`.

## **Create a new conda environment**
Now that you have conda installed, let's create a conda environment for managing all the Python library dependencies.

To create a new environment with Python 3.9, enter the following:
```bash
conda create -n stenv python=3.9
```
where `create -n stenv` will create a conda environment named `stenv` and `python=3.9` will setup the conda environment with Python version 3.9.

or

```bash
conda create -p ./env python=3.9
```
for local environment at `./env`


## **Activate the conda environment**

To use a conda environment that we had just created that is named `stenv`, enter the following into the command line:

```bash
conda activate stenv
```

## **Install the Streamlit library**

It's now time to install the `streamlit` library:
```bash
conda install streamlit
// or
pip install streamlit
```


## Other dependencies

### For HuggingFace transformers
pip install transformers
conda install pytorch

### For Google vertex AI
pip install google-cloud-aiplatform   // --upgrade ?
sudo snap install google-cloud-cli --classic
pip3 install black
conda install numpy"<=2.0"


### Installing Ruff
Ruff is available as ruff on PyPI:

```
pip install ruff
```

Once installed, you can run Ruff from the command line:

```bash
ruff check   # Lint all files in the current directory.
ruff format  # Format all files in the current directory.
```

### Bokeh visualization

pip install bokeh -- already installed?
