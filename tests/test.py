import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'Model Asset Exchange Server'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'resnet18_places365-pytorch-places365'
    assert metadata['name'] == 'resnet18_places365 Pytorch Model'
    assert metadata['description'] == 'resnet18_places365 Pytorch model trained on Places365'
    assert metadata['license'] == 'CC BY'


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/bakery.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'

    assert response['predictions'][0]['label_id'] == '31'
    assert response['predictions'][0]['label'] == 'bakery/shop'
    assert response['predictions'][0]['probability'] > 0.7


if __name__ == '__main__':
    pytest.main([__file__])
