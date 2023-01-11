
from concurrent import futures
import time 

import grpc
import image_pb2
import image_pb2_grpc
from utils import load_NLImage,save_image, nlimage_to_pil,pil_to_NLImage, compute_mean_image

class NLImageServiceServicer(image_pb2_grpc.NLImageServiceServicer):
    def RotateImage(self, request, context):
        print("Request to rotate image")
        rotation_degree = request.rotation * 90
        
        pil_img = nlimage_to_pil(request.image.data, request.image.width, request.image.height, request.image.color)
        save_image(pil_img,'./pre_rot_server.png')
        rotated_pil = pil_img.rotate(angle=rotation_degree)
        save_image(rotated_pil,'./post_rot_server.png')
        rotated_nlimage = pil_to_NLImage(rotated_pil)
        # return rotated_nlimage
        return rotated_nlimage
    
    def MeanFilter(self, request, context):
        print("Request to compute mean image")
        mean_nlimage = compute_mean_image(request.data, request.width, request.height, request.color)
        return mean_nlimage


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageServiceServicer(),server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()





