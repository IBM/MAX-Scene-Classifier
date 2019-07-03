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

# Application settings

# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'MAX Scene Classifier'
API_DESC = 'Classify images according to the place/location labels in the Places365 data set.'
API_VERSION = '1.2.0'
MODEL_ID = API_TITLE.lower().replace(' ', '-')

# default model
MODEL_NAME = 'resnet18_places365'
DEFAULT_MODEL_PATH = 'assets'
DEFAULT_MODEL_FILE = 'whole_resnet18_places365_python36.pth'
# for image models, may not be required
MODEL_INPUT_IMG_SIZE = (256, 256)
MODEL_LICENSE = 'CC BY'
