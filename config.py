# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'MAX Scene Classifier'
API_DESC = 'Classify images according to the place/location labels in the Places365 data set.'
API_VERSION = '1.0.0'

# default model
MODEL_NAME = 'resnet18_places365'
DEFAULT_MODEL_PATH = 'assets'
DEFAULT_MODEL_FILE = 'whole_resnet18_places365_python36.pth'
# for image models, may not be required
MODEL_INPUT_IMG_SIZE = (256, 256)
MODEL_LICENSE = 'CC BY'

MODEL_META_DATA = {
    'id': '{}-pytorch-places365'.format(MODEL_NAME.lower().replace(' ', '-')),
    'name': '{} Pytorch Model'.format(MODEL_NAME),
    'description': '{} Pytorch ResNet model trained on Places365'.format(MODEL_NAME),
    'license': '{}'.format(MODEL_LICENSE),
    'type': 'Image Classification',
    'source': 'https://developer.ibm.com/exchanges/models/all/max-scene-classifier/'
}
