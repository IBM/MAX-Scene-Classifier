#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from maxfw.model import MAXModelWrapper

import torch
from torch.autograd import Variable as V
from torchvision import transforms as trn
from torch.nn import functional as F

import io
from PIL import Image
import logging

logger = logging.getLogger()

from config import MODEL_ID, MODEL_LICENSE, API_TITLE,\
    MODEL_INPUT_IMG_SIZE, DEFAULT_MODEL_PATH, DEFAULT_MODEL_FILE

def read_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
    except Exception as e:
        logger.warn(str(e))
        from flask import abort
        abort(400, "The provided input is not a valid image (PNG or JPG required).")

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
    

class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': MODEL_ID,
        'name': API_TITLE,
        'description': 'Pytorch ResNet18 model trained on Places365 dataset',
        'license': '{}'.format(MODEL_LICENSE),
        'type': 'Image Classification',
        'source': 'https://developer.ibm.com/exchanges/models/all/{}/'.format(MODEL_ID)
    }

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

    def _pre_process(self, x):
        return preprocess_image(x, MODEL_INPUT_IMG_SIZE)

    def _post_process(self, x):
        probs, idx = x.sort(0, True)
        return post_process_result(probs, idx, self.classes)

    def _predict(self, x):
        logit = self.model.forward(x)
        probs = F.softmax(logit, 1).data.squeeze()
        return probs


        