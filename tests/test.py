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

import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Scene Classifier'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max-scene-classifier'
    assert metadata['name'] == 'MAX Scene Classifier'
    assert metadata['description'] == 'Pytorch ResNet18 model trained on Places365 dataset'
    assert metadata['license'] == 'CC BY'
    assert metadata['type'] == 'Image Classification'
    assert 'max-scene-classifier' in metadata['source']


def test_labels():
    
    model_endpoint = 'http://localhost:5000/model/labels'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    labels = r.json()

    assert labels['count'] == 365
    assert len(labels['labels']) == 365
    assert labels['labels'][0]['id'] == '0'
    assert labels['labels'][0]['name'] == 'airfield'
    assert labels['labels'][-1]['id'] == '364'
    assert labels['labels'][-1]['name'] == 'zen_garden'


def _check_predict(r):
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'

    assert response['predictions'][0]['label_id'] == '31'
    assert response['predictions'][0]['label'] == 'bakery/shop'
    assert response['predictions'][0]['probability'] > 0.7


def test_predict():

    model_endpoint = 'http://localhost:5000/model/predict'
    formats = ['jpg', 'png']
    file_path = 'tests/bakery.{}'

    for f in formats:
        p = file_path.format(f)
        with open(p, 'rb') as file:
            file_form = {'image': (p, file, 'image/{}'.format(f))}
            r = requests.post(url=model_endpoint, files=file_form)
        _check_predict(r)


def test_invalid_input():

    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'README.md'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400
    response = r.json()
    assert 'input is not a valid image' in response['message']

if __name__ == '__main__':
    pytest.main([__file__])
