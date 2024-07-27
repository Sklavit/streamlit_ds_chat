import coiled
from dask.distributed import Client

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
    client.upload_file("test_func.py")

    # Step 3: Verify the file upload
    def check_file(filename):
        import os

        return os.path.exists(filename)

    print(client.run(check_file, "test_func.py"))  # Should print True on all workers

    # Step 4: Use the uploaded module in a distributed task
    def use_uploaded_module():
        import test_func

        return test_func.estimate_pi_simple(100_000)

    result = client.run(use_uploaded_module)
    print(result)  # Should print "Hello, world!" from all workers
