FROM jinaai/jina:2.0.0rc6 as base
# install git
RUN apt-get -y update && apt-get install -y git
# setup the workspace
COPY . /workspace
WORKDIR /workspace
# install the third-party requirements
RUN pip install -r requirements.txt
RUN python -c "import clip;clip.load('ViT-B/32', 'cpu', True)"
# for testing the image
FROM base
RUN pip install -r tests/requirements.txt
RUN pytest -s -vv
FROM base
ENTRYPOINT ["jina", "pod", "--uses", "config.yml"]