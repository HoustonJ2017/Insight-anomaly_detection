""" InsightDataScience Coding Challenge / Anomaly detection
1. Create a Anomaly_detec() class 
2. Define D and T for this process
3. Read the batch_log using the function in  Anomaly_detec() class : anomaly.read_batch(batch)
4. Initialize and update all the attributes in the network based on batch_log :  anomaly.init_ave_sd_all()
5. Read stream data and update the attributes of the network accordingly : anomaly.read_flag_stream(stream)
6. Write the flagged anomalies into the target file : anomaly.write_anomaly(flag)
Note : Timestamp doesn't have enough resolution, add an order attributes to represent
order 
"""
import json
from anomaly_detec import *
## Run time test modules
import timeit
import sys

#print(sys.argv)


batch = sys.argv[1]
stream = sys.argv[2]  #"../log_input/stream_log.json"
flag = sys.argv[3]    #"../log_output/flagged_purchases.json"
try :
    D = int(sys.argv[4])
except :
    D = 1
try : 
    T = int(sys.argv[5])
except :
    T = 10

#batch = "../log_input/batch_log.json"
#stream = "../log_input/stream_log.json"              
#flag = "../log_output/flagged_purchases.json"

anomaly = Anomaly_detec()

## Tune the degree of friend (D) and no. of latest purchases in the neighbor 
## network (T)

## Caution the run time increase significantly with D
## D = 2 is ~ 70 times slower than D = 1
## D = 3 is ~ 20 times slower than D = 2
anomaly.D = D
anomaly.T = T
print("The degree of neighbor is " + str(D)) 
print("The number of latest purchase is " +str(T))
## Read intial datasets from batch 
start = timeit.default_timer()
anomaly.read_batch(batch)
stop = timeit.default_timer()
print("Reading batch log takes %f secs "%(stop-start))

## For one vertex: 
## search the neighbors of degree d and update the average and sd
start = timeit.default_timer()
print(anomaly.init_ave_sd_id("2"))
stop = timeit.default_timer()
print("Initializing one id takes %f secs"%(stop-start))


## Initialized the whole network : Search neighbors of degree d and update
## ave and sd for all vertices in the network
start = timeit.default_timer()
anomaly.init_ave_sd_all()
stop = timeit.default_timer()
print("Initializing all ids takes %f secs"%(stop-start))


## Test read stream log and update the network and flag the large purchases
anomaly.flag_dyn = [False,flag]
start = timeit.default_timer()
anomaly.read_flag_stream(stream)
stop = timeit.default_timer()
print("Read update and flag for all events takes %f secs"%(stop-start))
anomaly.write_anomaly(flag)
