import image_pb2_grpc
import image_pb2
from utils import load_NLImage,save_image, nlimage_to_pil
import time 
import grpc
import argparse



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = image_pb2_grpc.NLImageServiceStub(channel)
        print("make unary call")
        file = './test.png'
        output_file = './mean.png'
        img = load_NLImage(file)
        print("color = ",img.color)
        # reply = stub.RotateImage(image_pb2.NLImageRotateRequest(rotation=1,image=img))
        reply = stub.MeanFilter(img)
        pil_img = nlimage_to_pil(reply.data, reply.width, reply.height, reply.color)
        save_image(pil_img, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)
    run()