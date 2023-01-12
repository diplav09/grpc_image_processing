# gRPC Image Processing Server

This Grpc python server provides two microservice 
##### 1. Image Rotate Request
        Rotates the input image in multiple of 90 degree based on input argument.
##### 2. Mean Filter
        Computes and return the mean image for given input image.



### 1. File contents

    1. server.py   -- contains code for Server to interact with client 
    2. client.py   -- contains code for Client to connect to server and make request and recieve response.
    3. utils.py    -- contains image processing utility function used in server.py and client.py
    4. setup.py    -- executable for setting up the system
    5. build.py    -- to generate image_pb2_grpc.py and image_pb2.py files


### 2. Setup

    This setup applies for fresh Ubuntu 18.04 or Mac OS
    - Download and save the the folder at desired location
    - Python3           : ```sudo apt-get update```;```sudo apt-get install python3```
    - Pip3              : ```sudo python3 -m pip install pip```; ```python3 -m pip install --upgrade pip```
    - requirements.txt  : ```python3 -m pip install -r requirements.txt```

Setup can be installed by using following executable
```bash
./setup
```

### 3. Build
To generate image_pb2_grpc.py and image_pb2.py run following executable
```bash
./build
```

### 4. Instruction
</br>

#### 4.1 Server 
To start the server run following command
```bash
`./server --port <...> --host <...>`
```
Parameters and their default values:

>```port```: **```50051```** &nbsp; - &nbsp; port number to connect to <br/>
>```host```: **```localhost```** &nbsp; - &nbsp; host to connect to <br/>
</br>

#### 4.2 Client
For client run following command
```bash
`./client --port <...> --host <...> --input <...> --output <...> --rotate <...> --mean`
```
Parameters and their default values:

>```port```: **```50051```** &nbsp; - &nbsp; port number to connect to <br/>
>```host```: **```localhost```** &nbsp; - &nbsp; host to connect to <br/>
>```input```: **```Required Parameter```** &nbsp; - &nbsp; input file path <br/>
>```output```: **```Required Parameter```** &nbsp; - &nbsp; output folder path <br/>
>```rotate```: **```NONE```** &nbsp; - &nbsp; Rotation enum representing rotation degree  <br/>
>```mean```: **```optional```** &nbsp; - &nbsp; specifies that the mean filter should be
run on the input image  <br/>
</br>

### 5. Concerns

Both the microservices deals with image data and uses Unary RPCs where the client sends 
a single request to the server and gets a single response back, just like a normal function call. 
1. This limits the amount of data that can be transferred and thus limit the operation speed.
2. Unary RPCs can be useful for smaller payloads, but for images, where data is frequently greater 
than the normal payload, we actually require partial upload of data due to latency concerns or network problems, 
and so basic unary requests to upload images on a backend framework are unreliable. 

### 6. Improvement 
1. Streaming RPC can be a alternative way which can be used as it allow larger data like image
to be transfer in smaller bits called chunk. Chunk supports partial uploads and lets us monitor 
upload progress in case we ever decide to bring this functionality to the frontend clients. 
Additionally, chunks also consumes less memory for every request sent. 
