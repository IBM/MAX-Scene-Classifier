FROM continuumio/miniconda3

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/pytorch/places365
ARG model_file=whole_resnet18_places365_python36.pth

WORKDIR /workspace
RUN mkdir assets
RUN wget -nv ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}

RUN conda install -y pytorch-cpu torchvision -c pytorch
RUN conda install -y ipython
RUN pip install flask-restplus

COPY . /workspace

EXPOSE 5000

CMD python app.py