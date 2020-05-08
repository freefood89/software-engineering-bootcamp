import boto3
import json
from contextlib import contextmanager
from urllib.parse import unquote_plus


class SQSQueue:
	def __init__(self, queue_url, client=None, session=None):
		self.url = queue_url
		self.set_client(client=client, session=session)

	@contextmanager
	def get(self):
		'''
			This is Context Manager that provides setup and cleanup for handling SQS messages.
			
			Upon successfully executing the nested code block it will handle acknowledging the SQS message. 
		'''
		while True:
			# TODO - receive message
			if len(messages) == 1:
				message = SQSMessage.parse(messages[0])
				try:
					# TODO - Set the 'message' in the with statement 
				except Exception as e:
					# TODO - Propagate exception after logging why the message will not be deleted
				else:
					# TODO - If there were no exceptions delete message from queue
	
	@property
	def client(self):
		'''
			Property getter for queue.client.

			It returns a boto3 client provided by the user, otherwise it creates one with default credentials.
		'''
		if self._client:
			return self._client

		print('Using default boto3 client for SQS')
		return boto3.client('sqs')

	def set_client(self, client=None, session=None):
		'''
			Creates a boto3 client to interact with AWS APIs

			If a client is passed it's used as is.
			If a session is passed a client is created with it.
		'''
		if client:
			self._client = client
			return

		if session:
			self.session = session
			self._client = session.client('sqs')
			return	


class SQSMessage:
	def __init__(self, _id, key, receipt_handle):
		self._id = _id
		self.key = key
		self.receipt_handle = receipt_handle

	@classmethod
	def parse(cls, message):
		# TODO - use solution from previous step