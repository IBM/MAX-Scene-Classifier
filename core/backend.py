import torch
from torch.autograd import Variable as V
from torchvision import transforms as trn
from torch.nn import functional as F

import io
from PIL import Image
import logging

logger = logging.getLogger()

from config import MODEL_INPUT_IMG_SIZE, DEFAULT_MODEL_PATH, DEFAULT_MODEL_FILE

def read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    return image

def preprocess_image(image, target):
    # load the image transformer
    centre_crop = trn.Compose([
            trn.Resize(target),
            trn.CenterCrop(224),
            trn.ToTensor(),
            trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return V(centre_crop(image).unsqueeze(0), volatile=True)

def post_process_result(probs, idxs, classes, topk=5):
    results = []
    for i in range(0, topk):
        result = (idxs[i], classes[idxs[i]], probs[i])
        results.append(result)
    return results
    

class ModelWrapper(object):
    """Model wrapper for PyTorch models"""
    def __init__(self, path=DEFAULT_MODEL_PATH, model_file=DEFAULT_MODEL_FILE):
        logger.info('Loading model from: {}...'.format(path))
        model_path = '{}/{}'.format(path, model_file)
        self.model = torch.load(model_path, map_location=lambda storage, loc: storage) # cpu only for now ...
        logger.info('Loaded model')
        self._load_assets(path)

    def _load_assets(self, path):
        file_name = '{}/categories_places365.txt'.format(path)
        classes = list()
        with open(file_name) as class_file:
            for line in class_file:
                classes.append(line.strip().split(' ')[0][3:])
        self.classes = tuple(classes)

    def predict(self, x):
        x = preprocess_image(x, MODEL_INPUT_IMG_SIZE)
        logit = self.model.forward(x)
        h_x = F.softmax(logit, 1).data.squeeze()
        probs, idx = h_x.sort(0, True)
        return post_process_result(probs, idx, self.classes)


        