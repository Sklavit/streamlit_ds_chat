
https://www.coiled.io/

Absolutely fascinating service and library which manage cloud for python computations.

```
Code locally, run at scale
Coiled creates ephemeral VMs that match your local environment exactly, spinning up clones in about a minute, copying ...

Your code
Your software libraries
Your working files
Your cloud credentials (securely)
```

Works with AWS, GCloud, Azure, etc.
Runs Dask and pure Python.


# How to install Coiled

Just register on `coiled.io` and follow instructions. Everything is very simple and works great.

The only pitfall: all you installs should probably come from single distribution system.
If you use conda, you should install everything with `conda install`.
If you use `pip`, you should install all packages with `pip install`.


```bash
pip3 install coiled "dask[complete]"
coiled login
```

> Authentication successful 🎉
> Credentials have been saved at /home/s-nechuiviter/.config/dask/coiled.yaml

Use `coiled setup gcp` once to set up connection to GCP.

Coiled requires that all modules should be `conda` compatible, at least if start from conda environment.
Or use pip/venv everywhere.

# pip and venv

To create new virtual environment:

```bash
python -m venv ./env
```

Activate:

```bash
source .venv/bin/activate
```

Check

```bash
which python
```

Deactivate

```bash
deactivate
```

Prepare pip

```bash
python3 -m pip install --upgrade pip
```



What we need?

```
[//]: # (for streamlit)
pip3 install streamlit

[//]: # (For Google vertex AI)
pip3 install --upgrade google-cloud-aiplatform numpy"<=2.0"
```
[//]: # (sudo snap install google-cloud-cli --classic)  For google account access

# Results

https://docs.coiled.io/user_guide/functions.html
`executor_1.py` successfully executes already existing code, but will not reload it.

https://docs.coiled.io/user_guide/cli-jobs.html
Single file can be executed from terminal with `coiled run python file_name.py`. Stdout --> stdout.

## Notebooks

### Files
The --sync flag will optionally synchronize the files you have locally to the cloud machine, and copy any changes made on the cloud machine back to your local hard drive.

This gives you the experience of just working on your local file system.

To do this, you will need to install mutagen, which is available on brew :

brew install mutagen-io/mutagen/mutagen
And then use the --sync flag.

coiled notebook start --sync
Then you will get live synchronization between the remote server (/scratch/synced) and your local machine. This allows you to edit files on either machine and have the edits quickly show up on the other.

Files larger than 1 GiB are not synced. If you would like to work in an entire directory that isn’t synced, you can create one in another directory, for example at /scratch/not_synced/




