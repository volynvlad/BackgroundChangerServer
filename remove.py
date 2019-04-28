from io import BytesIO

import numpy as np
from PIL import Image

import tensorflow as tf
import datetime

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        graph_def = tf.GraphDef.FromString(open("/home/vlad/flask-server/background_remover/" + tarball_path + "/frozen_inference_graph.pb", "rb").read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)
        """
        writer = tf.summary.FileWriter('.')
        writer.add_graph(graph_def)
        writer.flush()
        """

    def run(self, image):
        """Runs inference on a single image.

        Args:
        image: A PIL.Image object, raw input image.

        Returns:
        resized_image: RGB image resized from original input image.
        seg_map: Segmentation map of `resized_image`.
        """
        start = datetime.datetime.now()

        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        print(image)
        print(image.convert('RGB'))
        print(image.convert('RGB').resize(target_size, Image.ANTIALIAS))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
        feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]

        end = datetime.datetime.now()

        diff = end - start
        print("Time taken to evaluate segmentation is : " + str(diff))

        return resized_image, seg_map

def drawSegment(baseImg, matImg, outputFilePath):
    width, height = baseImg.size
    dummyImg = np.zeros([height, width, 4], dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            color = matImg[y,x]
            (r,g,b) = baseImg.getpixel((x,y))
            if color == 0:
                dummyImg[y,x,3] = 0
            else:
                dummyImg[y,x] = [r,g,b,255]
    img = Image.fromarray(dummyImg)
    img.save(outputFilePath)

def run_visualization(filepath, MODEL, outputFilePath):
    """Inferences DeepLab model and visualizes result."""
    try:
        print("Trying to open : " + filepath)
        jpeg_str = open(filepath, "rb").read()
        orignal_im = Image.open(BytesIO(jpeg_str))
    except IOError:
        print('Cannot retrieve image. Please check file: ' + filepath)
        return

    print('running deeplab on image %s...' % filepath)
    resized_im, seg_map = MODEL.run(orignal_im)

    # vis_segmentation(resized_im, seg_map)
    drawSegment(resized_im, seg_map, outputFilePath)

def run(name):
    inputFilePath = '/home/vlad/changer_server/pictures/received/'
    outputFilePath = '/home/vlad/changer_server/pictures/send/'
    modelType = 'mobile_net_model'

    MODEL = DeepLabModel(modelType)
    inputFilePath = inputFilePath + name
    name = name[:(len(name) - 4)] + '.png'
    outputFilePath = outputFilePath + name
    print("inputFilePath - " + inputFilePath)
    print("outputFilePath - " + outputFilePath)
    print('model loaded successfully : ' + modelType)
    run_visualization(inputFilePath, MODEL, outputFilePath)

