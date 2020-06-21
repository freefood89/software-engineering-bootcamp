import logging
import json
import os
import boto3
import flask
from flask import request, Response
from io import BytesIO
from urllib.parse import unquote_plus
from PIL import Image

BUCKET_NAME = ''
OUTPUT_FOLDER = ''

# Create and configure the Flask app
app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)

session = boto3.Session(region_name='us-east-1')
s3 = session.client('s3')


class S3Message:
    def __init__(self, key):
        self.key = key

    @classmethod
    def parse(cls, message):
        # Implement
        return cls(key)


def create_thumbnail(input_stream, size=(128, 128)):
    output_stream = BytesIO()
    image = Image.open(BytesIO(input_stream))
    image.thumbnail(size)
    image.save(output_stream, image.format)
    output_stream.seek(0)
    return output_stream


def create_thumbnail_key(key):
    path, filename = os.path.split(key)
    file, ext = os.path.splitext(filename)
    return os.path.join(OUTPUT_FOLDER, file + '.thumbnail' + ext)


@app.route('/', methods=['POST'])
def process_message():
    app.logger.info(request.json)
    if not request.json:
        # Expect application/json request
        return Response("", status=415)

    # Implement

    return Response("", status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)