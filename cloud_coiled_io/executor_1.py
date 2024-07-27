import coiled

# from test_func import estimate_pi_simple
import test_func

cluster = coiled.Cluster(n_workers=2)  # Scale out to 100 machines
client = cluster.get_client()


for i in range(10):
    input("go?")
    print("go")

    # importlib.reload(test_func)   # reload doesn't send new code to cluster
    client.upload_file("test_func.py")

    futures = []
    for filename in range(100):  # Nested for loop
        future = client.submit(test_func.estimate_pi_simple, 100_000)
        futures.append(future)

    results = client.gather(futures)

    best = max(results)
    avg = sum(results) / len(results)
    print(f"{min(results)} : {avg} : {max(results)}")
