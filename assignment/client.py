"""
Author : Diplav
Client to connect to server.
"""

import image_pb2_grpc
import image_pb2
from utils import load_NLImage,save_image, nlimage_to_pil
import time 
import grpc
import argparse
from enum import Enum
import os

class Rotate(Enum):
    NONE = 0
    NINETY_DEG = 1
    ONE_EIGHTY_DEG = 2
    TWO_SEVENTY_DEG = 3

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return Rotate[s]
        except KeyError:
            raise ValueError()

def run(args):
    host = args.host
    server_port = args.port
    
    with grpc.insecure_channel('{}:{}'.format(host, server_port)) as channel:
        stub = image_pb2_grpc.NLImageServiceStub(channel)
        print("Make unary call")
        file = args.input
        output_folder = args.output
        file_name = file.split('/')[-1]
        img = load_NLImage(file)
        print("Is color image = ",img.color)
        print("rotate = ",args.rotate.value)
        reply = stub.RotateImage(image_pb2.NLImageRotateRequest(rotation=args.rotate.value,image=img))
        print("Mean Computed = ",args.mean)
        if args.mean:
            reply = stub.MeanFilter(reply)
        pil_img = nlimage_to_pil(reply.data, reply.width, reply.height, reply.color)
        out_file = "processed_" + file_name
        save_image(pil_img, os.path.join(output_folder,out_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help="input file path")
    parser.add_argument('--output', type=str, required=True,help="output folder path")
    parser.add_argument('--rotate', type=Rotate.from_string, choices=list(Rotate),default="NONE")
    parser.add_argument('--mean', action='store_true')
    parser.add_argument('--host',type=str,default='localhost')
    parser.add_argument('--port',type=str,default='50051')
    args = parser.parse_args()
    run(args)