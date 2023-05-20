import time
import numpy as np
import os
import tqdm
import matplotlib.pyplot as plt

NB_RUNS = 100

def line_plot(x, ys):
    plt.rcParams.update({'font.size': 18})
    plt.plot(x, ys[:,0], label = "child")
    plt.plot(x, ys[:,1], label = "parent")
    plt.legend()
    plt.xlabel("Number of natural persons")
    plt.ylabel("Validation time (s)")
    plt.show()

NbNaturalPersonsArray = [1000, 2000, 3000, 4000, 5000]
ShapesFileArray = ["shapes_child_distinct.ttl", "shapes_parent.ttl"]

shape_times = np.zeros([len(NbNaturalPersonsArray), len(ShapesFileArray), 2])
for shapeIdx, shapefile in enumerate(ShapesFileArray):
    for x, nb in enumerate(NbNaturalPersonsArray):
        datafilename = "./data/data_" + str(nb) + "_ER-0.ttl"
        times = np.ndarray(NB_RUNS)
        for i in tqdm.tqdm(range(NB_RUNS)):
            start = time.time()
            os.system('cmd /c "shaclvalidate.bat -datafile {} -shapesfile {} > NUL"'.format(datafilename, shapefile))
            end = time.time()
            times[i] = (end - start)
        shape_times[x, shapeIdx, 0] = np.mean(times)
        shape_times[x, shapeIdx, 1] = np.std(times)

line_plot(NbNaturalPersonsArray, shape_times[:,:,0])
print(shape_times)