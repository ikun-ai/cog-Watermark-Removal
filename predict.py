from cog import BasePredictor, Input, Path
from PIL import Image
import cv2
import numpy as np
from preprocess_image import preprocess_image
import tensorflow as tf
import neuralgym as ng
from inpaint_model import InpaintCAModel
import os
import shutil


def process_image(inputimage, model, output_file='/tmp/output.png', watermark_type='istock', checkpoint_dir='model/'):
    FLAGS = ng.Config('inpaint.yml')

    image = Image.open(inputimage)
    input_image = preprocess_image(image, watermark_type)
    tf.reset_default_graph()

    sess_config = tf.compat.v1.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    if (input_image.shape != (0,)):
        with tf.compat.v1.Session(config=sess_config) as sess:
            input_image = tf.compat.v1.constant(input_image, dtype=tf.float32)
            output_tensor = model.build_server_graph(FLAGS, input_image)
            output_tensor = (output_tensor + 1.) * 127.5
            output_tensor = tf.compat.v1.reverse(output_tensor, [-1])
            output_tensor = tf.compat.v1.saturate_cast(output_tensor, tf.uint8)
            # load pretrained model
            vars_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
            assign_ops = []
            for var in vars_list:
                vname = var.name
                from_name = vname
                var_value = tf.contrib.framework.load_variable(
                    checkpoint_dir, from_name)
                assign_ops.append(tf.compat.v1.assign(var, var_value))
            sess.run(assign_ops)
            print('Model loaded.')
            result = sess.run(output_tensor)
            cv2.imwrite(output_file, cv2.cvtColor(
                result[0][:, :, ::-1], cv2.COLOR_BGR2RGB))
            print('image saved to {}'.format(output_file))
    return output_file  # return the path to the output file

def get_image(path):
    shutil.copyfile(path, "/tmp/image.png")
    return "/tmp/image.png"


class Predictor(BasePredictor):
    def setup(self):
        self.model = InpaintCAModel() 

    def predict(self, image: Path = Input(description="Input image with watermark", default=None)) -> Path:
        image_path = get_image(image)
        output_file_path = process_image(image_path, self.model)
        return Path(output_file_path)  # return a Path object
