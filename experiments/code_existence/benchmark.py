import time
import numpy as np
import os
import tqdm
import matplotlib.pyplot as plt

NB_RUNS = 100
ShapesFileArray = ["bound_version.ttl", "count_version.ttl"]

shape_times = np.zeros([len(ShapesFileArray),2])
for shapeIdx, shapefile in enumerate(ShapesFileArray):
    times = np.ndarray(NB_RUNS)
    for i in tqdm.tqdm(range(NB_RUNS)):
        start = time.time()
        os.system('cmd /c "shaclvalidate.bat -datafile data.ttl -shapesfile {} > NUL"'.format(shapefile))
        end = time.time()
        times[i] = (end - start)
    
    shape_times[shapeIdx,0] = np.mean(times)
    shape_times[shapeIdx,1] = np.std(times)

print(shape_times)
