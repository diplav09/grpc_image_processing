# Grpc Image Processing Server

This Grpc python server provides two microservice 
##### 1. Image Rotate Request
        Rotates the input image in multiple of 90 degree based on input argument.
##### 2. Mean Filter
        Computes and return the mean image for given input image.



### 1. File contents

1. server.py   -- contains code for Server to interact with client 
2. client.py   -- contains code for Client to connect to server and make request and recieve response.
3. utils.py    -- contains image processing utility function used in server.py and client.py 


### 2. Setup

This setup applies for fresh Ubuntu 18.04 or Mac OS
- Download and save the the folder at desired location
- Python3           : sudo apt-get update; sudo apt-get install python3
- Pip3              : sudo python3 -m pip install pip; python3 -m pip install --upgrade pip
- requirements.txt  : python3 -m pip install -r requirements.txt





