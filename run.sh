#!/bin/bash

#python ./src/process_log.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json
python ./src/process_log.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json  1  15 
## Optional pass D and T to the code default is D = 1, T = 10 
