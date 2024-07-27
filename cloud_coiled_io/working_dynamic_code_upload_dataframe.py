import coiled
from dask.distributed import Client


import numpy as np
import dask.dataframe as dd
import pandas as pd

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
cluster = coiled.Cluster(name="my-cluster", n_workers=1)
# n_workers – Number of workers in this cluster.
# Can either be an integer for a static number of workers,
# or a list specifying the lower and upper bounds for adaptively scaling up/ down workers
# depending on the amount of work submitted.
# Defaults to n_workers=[4, 20] which adaptively scales between 4 and 20 workers.
client = Client(cluster)

for i in range(10):
    input("go?")
    print("go")

    # Step 2: Upload the module file to all workers
    client.upload_file("func_df.py")

    # Step 3: Verify the file upload
    def check_file(filename):
        import os

        return os.path.exists(filename)

    print(client.run(check_file, "func_df.py"))  # Should print True on all workers

    # Step 4: Use the uploaded module in a distributed task
    def use_uploaded_module():
        import func_df

        return func_df.run(df)

    result = client.run(use_uploaded_module)
    print(type(result))
    print(result)
