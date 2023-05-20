import time
import numpy as np
import tqdm
from SPARQLWrapper import SPARQLWrapper
import matplotlib.pyplot as plt


# -------------------------------------------- Queries --------------------------------------------
QUERY_DEFAULT = """   
    CONSTRUCT{
        ?s ?p ?o.
    }
    WHERE{
        <urn:ss:000-DmfAOriginal0> (<>|!<>)* ?s . 
        ?s ?p ?o . 
    }
"""


QUERY_NAMED = """
   CONSTRUCT{
        ?s ?p ?o.
    }
    FROM <urn:ss:000>
    WHERE{
        ?s ?p ?o . 
    }
"""

# -------------------------------------------- Code --------------------------------------------
# Make a box-plot from a series of response times
def box_plot_chart(names, serie):
    plt.rcParams.update({'font.size': 18})
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Response time (ms)")
    ax1.boxplot(
        x=serie,
        labels=names,
        widths=np.ones(len(names)) * 0.5
    )
    plt.show()


# Run a query for 'nb_runs' times on each endpoint and their respective query
# Report mean and stddev and show a box-plot of response times across endpoints
# Return response times where endpoint_times[i][j] is for endpoint i and run j
def benchmark_query(endpoints, names, queries, nb_runs = 50):
    assert nb_runs > 1 and len(endpoints) > 0 and len(endpoints) == len(queries)

    # Loop over endpoints
    endpoint_times = []
    for (endpoint, query) in zip(endpoints, queries):
        # Create wrapper
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)
        
        # Run nb_runs time query
        times = np.ndarray(nb_runs)
        for i in tqdm.tqdm(range(nb_runs)):
            start = time.time()
            _ = sparql.query()
            end = time.time()
            times[i] = (end - start) * 1000

        endpoint_times.append(times[1:])
        mean = np.mean(times)
        std = np.std(times)
        print(f"* Endpoint: {endpoint}")
        print(f"\tMean:  {mean:.5f} ms")
        print(f"\tStdev: {std:.5f} ms")
        
    # Make a box-plot
    box_plot_chart(names, endpoint_times)
    
    # Return response times
    return endpoint_times


if __name__ == '__main__':
    endpoints = ["http://localhost:3030/storageDefault/", "http://localhost:3030/storageNamed/"]
    queries = [QUERY_DEFAULT, QUERY_NAMED]
    names = ["Default", "Named"]
    print("Benchmarking ...")
    _ = benchmark_query(endpoints, names, queries, 100)
