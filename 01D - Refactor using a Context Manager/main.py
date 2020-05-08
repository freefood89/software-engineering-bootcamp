import boto3
import os
from io import BytesIO
from PIL import Image

from SQSQueue import SQSQueue, SQSMessage

BUCKET_NAME = '<bucket_name>'
OUTPUT_FOLDER = 'thumbnails'
QUEUE_URL = '<queue_url>'

session = boto3.Session(profile_name='thumbnail-service')
s3 = session.client('s3')
sqs = session.client('sqs')


def create_thumbnail(input_stream, size=(128, 128)):
	# TODO - Replace with solution from previous steps


def create_thumbnail_key(key):
	# TODO - Replace with solution from previous steps

def main():
	sqs_queue = SQSQueue(QUEUE_URL, session=session)
	print('Waiting for Messages...')
	
	while True:
		try:
			with sqs_queue.get() as message:
				# TODO - Insert thumbnail logic from previous step
		except Exception as e:
			# TODO - Implement Error Handling
			pass

if __name__ == '__main__':
	main()