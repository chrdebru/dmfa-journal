import time
import numpy as np
import os
import tqdm
import matplotlib.pyplot as plt

NB_RUNS = 100

def line_plot(x, ys):
    plt.rcParams.update({'font.size': 18})
    plt.plot(x, ys[:,0], label = "0% error rate")
    plt.plot(x, ys[:,1], label = "50% error rate")
    plt.plot(x, ys[:,2], label = "100% error rate")
    plt.legend()
    plt.show()

NbNaturalPersonsArray = [10, 50, 100, 500, 1000, 5000, 10000]
ErrorRateArray = [0, 0.5, 1]
ShapesFileArray = ["shapes_child_distinct.ttl", "shapes_parent.ttl"]

for shapefile in ShapesFileArray:
    shape_times = np.zeros((len(NbNaturalPersonsArray), len(ErrorRateArray)))
    for x, nb in enumerate(NbNaturalPersonsArray):
        for z, errorRate in enumerate(ErrorRateArray):
            datafilename = "./data/data_" + str(nb) + "_ER-" + str(errorRate) + ".ttl"
            times = np.ndarray(NB_RUNS)
            for i in tqdm.tqdm(range(NB_RUNS)):
                start = time.time()
                os.system('cmd /c "shaclvalidate.bat -datafile {} -shapesfile {} > NUL"'.format(datafilename, shapefile))
                end = time.time()
                times[i] = (end - start)
            

            shape_times[x, z] = np.mean(times)
    line_plot(NbNaturalPersonsArray, shape_times)
