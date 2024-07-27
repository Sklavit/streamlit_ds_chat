import coiled
import importlib
import os.path
from dask.distributed import Client


import numpy as np
import dask.dataframe as dd
import pandas as pd
from rich.pretty import pprint

pdf = pd.DataFrame(
    {
        "A": np.random.rand(10000),
        "B": np.random.rand(10000),
        "C": np.random.rand(10000),
        "D": np.random.rand(10000),
    }
)
df = dd.from_pandas(pdf, npartitions=4)

print(f"Local result: {df.mean().compute()}")


# Step 1: Create or connect to a Coiled cluster
cluster = coiled.Cluster(name="my-cluster", n_workers=1, idle_timeout="20 minutes")
# n_workers – Number of workers in this cluster.
# Can either be an integer for a static number of workers,
# or a list specifying the lower and upper bounds for adaptively scaling up/ down workers
# depending on the amount of work submitted.
# Defaults to n_workers=[4, 20] which adaptively scales between 4 and 20 workers.
client = Client(cluster)

for i in range(10):
    file_name = input("file name?")
    print("go")

    if not file_name.endswith(".py"):
        raise Exception("not a file")

    if not os.path.exists(file_name):
        raise Exception(f"no file name: {file_name}")

    # Step 2: Upload the module file to all workers
    client.upload_file(file_name)

    # Step 3: Verify the file upload
    def check_file(filename):
        return os.path.exists(filename)

    print(client.run(check_file, file_name))  # Should print True on all workers

    # Step 4: Use the uploaded module in a distributed task
    def use_uploaded_module():
        try:
            module = importlib.import_module(file_name[:-3])
            print(f"Successfully imported {file_name}")
        except ImportError as e:
            print(f"Error importing {file_name}: {e}")
            return None

        return module.run(
            pdf
        )  # so, with proper function you can pass even Pandas Data Frames directly

    result = client.run(use_uploaded_module)
    print(type(result))
    pprint(result)
