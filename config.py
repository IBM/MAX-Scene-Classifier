# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'list'

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

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
    'description': '{} Pytorch model trained on Places365'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}
