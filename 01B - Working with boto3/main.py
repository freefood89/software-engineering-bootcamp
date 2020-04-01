import boto3
import json
import os
from io import BytesIO
from PIL import Image
from urllib.parse import unquote_plus

BUCKET_NAME = '<bucket_name>'
OUTPUT_FOLDER = 'thumbnails'
QUEUE_URL = '<queue_url>'

session = boto3.Session(profile_name='thumbnail-service')
s3 = session.client('s3')
sqs = session.client('sqs')

class S3Message:
	'''
	This class encapsulates logic and data so that receiving messages and processing images can be handled separately. This is sometimes referred to as a Data Transfer Object (DTO).

	'''

	def __init__(self, _id, key, receipt_handle):
		'''
		The constructor for S3Message.
		'''
		self._id = _id
		self.key = key
		self.receipt_handle = receipt_handle
		print(key)

	@classmethod
	def parse(cls, message):
		'''
		This class method parses the raw message from SQS in JSON form and returns an instance of S3Message.

		Needs to be Implemented
		'''
		_id = message['MessageId']
		body = json.loads(message['Body'])

		# IMPLEMENT

		return cls(_id, key, receipt_handle)


def gen_messages_from_response(response):
	'''
	This function parses a response from AWS ReceiveMessages and returns a generator that yields one message at a time for each message in the response.
	'''

	raw_messages = response.get('Messages', [])
	for raw_message in raw_messages:
		yield S3Message.parse(raw_message)


def create_thumbnail(input_stream, size=(128, 128)):
	'''
	This function creates a thumbnail of an image. It expects bytes and returns bytes.
	'''

	output_stream = BytesIO()
	image = Image.open(BytesIO(input_stream))
	image.thumbnail(size)
	image.save(output_stream, "JPEG")
	output_stream.seek(0)
	return output_stream


def create_thumbnail_key(key):
	'''
	This function creates the S3 key for the thumbnail to be uploaded to S3 based on the key of the original image.
	'''

	# EXAMPLE - feel free to use this or create your own
	# path, filename = os.path.split(key)
	# file, ext = os.path.splitext(filename)
	# return os.path.join(OUTPUT_FOLDER, file + '.thumbnail' + ext)


def main():
	print('Waiting for Messages...')
	
	while True:
		response = sqs.receive_message(
			# IMPLEMENT
		)

		messages = gen_messages_from_response(response)
		for message in messages:
			try:
				get_object_response = s3.get_object(
					# IMPLEMENT
				)

				print(f'Creating Thumbnail for {message._id}')
				stream = get_object_response['Body'].read()
				thumbnail_stream = create_thumbnail(stream)

				print(f'Uploading Thumbnail for {message._id}')
				thumbnail_key = create_thumbnail_key(message.key)
				s3.put_object(
					# IMPLEMENT
				)

				print(f'Deleting Message {message._id}')
				sqs.delete_message(
					# IMPLEMENT
				)

			except Exception as e:
				'''
				IMPLEMENT - this should be updated to only catch exceptions that are expected and print appropriate error messages. It is meant to prevent SQS messages from being deleted if the image was not properly processed. Make sure to look for all failure scenarios, including those caused by boto3.

				For example, if a failure occurs the error should be printed and the message should be left in the queue for later processing. This way the image can be kept in the queue and processed later when the code is updated to fix the bug.
				'''
				raise e



if __name__ == '__main__':
	main()