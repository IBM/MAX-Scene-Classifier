import pytest
import requests


def test_response():
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
