"""
Author : Diplav
utility function used in client.py and server.py 
"""

from PIL import Image, ImageChops, ImageFilter
import image_pb2
import numpy as np

def is_grayscale(img):
    """
    Check if image is monochrome (1 channel or 3 identical channels)
    Arguments:
        - img (PIL.Image) :       Image to check for 
    Returns:
        - Bool :                  True if rgb image

    """
    if img.mode == "RGB":
        rgb = img.split()
        if ImageChops.difference(rgb[0],rgb[1]).getextrema()[1]!=0: 
            return False
        if ImageChops.difference(rgb[0],rgb[2]).getextrema()[1]!=0: 
            return False
    return True

def pil_to_NLImage(img):
    """
    Converts PIL Image to NLImage
    Arguments:
        - img (PIL.Image) :       Image to convert to NLImage
    Returns:
        - img_NLImage (NLImage) :       Converted NLImage
    """
    w, h = img.size
    color = not is_grayscale(img)
    # constraint the size to some max dimension 
    img_val = []
    if color:
        img_rgb = list(img.getdata())
        for pixel in img_rgb:
            for rgb_val in pixel:
                img_val.append(rgb_val)

    else:
        img_grey = img.convert("L")
        for row in range(0, img.height):
            for col in range(0, img.width):
                img_val.append(img_grey.getpixel((col, row)))
    
    img_NLImage = image_pb2.NLImage(color=color,data=bytes(img_val),width= img.width,height = img.height)
    return img_NLImage

def load_NLImage(file):
    """
    Load NLImage from file
    Arguments:
        - file (str) :            File location for Image
    Returns:
        - img (NLImage) :       Converted NLImage
    """
    img = Image.open(file).convert('RGB')
    # save_image(img,"./init_check.png")
    return pil_to_NLImage(img)

def save_image(image, outfile):
    """
    Save an PIL.Image object into a file.
    Arguments:
        - image (PIL.Image) :       Image object to save
        - outfile (str) :           File to save the image to 
    Returns:
        None
    """
    image.save(outfile)
def compute_mean_array(np_img):
    output = np.zeros(np_img.shape,dtype=np.uint8)
    for x in range(np_img.shape[0]):
        for y in range(np_img.shape[1]):
            x_min = max(x-1,0)
            x_max = min(x+1,np_img.shape[0]-1)+1
            y_min = max(y-1,0)
            y_max = min(y+1,np_img.shape[1]-1)+1
            patch = np_img[x_min:x_max,y_min:y_max]
            output[x,y] = patch.sum(axis=(0,1)) / (patch.shape[0] * patch.shape[1])
            # output[x,y] = np_img[x_min:x_max,y_min:y_max].mean(axis=(0, 1))
    return output

# def compute_mean_image(image_data,image_width, image_height, image_color):
#     pil_img = nlimage_to_pil(image_data,image_width, image_height, image_color)
#     np_img = np.asarray(pil_img)
#     # print("Shape of image = :",np_img.shape)
#     np_mean_img = compute_mean_array(np_img)
#     # print("Shape of mean image = :",np_mean_img.shape)
#     nil_mean_image = pil_to_NLImage(Image.fromarray(np_mean_img))
#     return nil_mean_image

def compute_mean_image(image_data,image_width, image_height, image_color):
    """
    Compute Mean NLImage
    Arguments:
        - image_data (Byte) :       Image byte date
        - image_width (int) :       Image Width
        - image_height (int) :      Image Height
        - image_color (bool) :      Is rgb or not
    Returns:
        - nil_mean_image (NLImage) :       Mean Image
    """
    pil_img = nlimage_to_pil(image_data,image_width, image_height, image_color)
    blur_pil = pil_img.filter(ImageFilter.BoxBlur(1))
    nil_mean_image = pil_to_NLImage(blur_pil)
    return nil_mean_image


def nlimage_to_pil(image_data,image_width, image_height, image_color):
    """
    Converts NLImage to PIL Image.
    Arguments:
        - image_data (Byte) :       Image byte date
        - image_width (int) :       Image Width
        - image_height (int) :      Image Height
        - image_color (bool) :      Is rgb or not
    Returns:
        - img (PIL.Image) :       Image object to save
    """
    if not image_color:
        img = Image.frombytes(mode="L", size=(image_width, image_height), data=image_data)
    else:
        img = Image.frombytes(mode="RGB", size=(image_width, image_height), data=image_data)
    return img

