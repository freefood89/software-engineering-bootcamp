# 01A - Working with boto3

In this step you will use `boto3` to programmatically call AWS APIs. The first will upload images to S3 and the other will trigger every time a message is queued onto SQS.

## Parts

- `boto3` is a python SDK for interacting with AWS APIs

## Creating a boto client

`boto3` is architected in a way such that a separate clients are created for each service. This can be done by calling `session.client` with the service name. This function will use your default AWS credentials stored at `~/.aws/credentials`.

```python
import boto3

s3 = boto3.resource('s3')
```

However, for this challenge, you will need to create a client from a session so that the profile configured with the correct AWS IAM User can be specified:

```python
import boto3

session = boto3.Session(profile_name='thumbnail-service')
s3_client = session.client('s3')
```

## Using boto with S3

The client can be used to do anything you can do on the AWS console ([S3 client docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#id243)).

Listing buckets:

```python
response = s3_client.list_buckets()

for bucket in response['Buckets']:
	print(bucket['Name'])
```

Uploading a file:

```python
filename = 'lolcats.thumbnail.jpg'
bucket_name = 'gg-thumbnail-project'
key = f'thumbnails/{filename}'

response = s3_client.upload_file(filename, bucket_name, key)
```

Look through the docs to see what else you can do.

## Using boto with SQS

Similarly, boto can be used to interact with SQS ([SQS client docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html)):

```python
sqs= session.client('sqs')
response = sqs.list_queue()
for queue in response['QueueUrls']:
	print(queue)
```

Retrieving messages from your queue is quite easy:

```python
sqs = session.client('sqs')
response = sqs.receive_message(
	QueueUrl='<thumbnail_queue_url>',
)

for message in response.get('Messages', []):
	print(message)
```


## Understanding SQS

Before moving onto the challenge, there are a few key factors important to working with SQS.

### Message Lifecycle

Event driven systems typically have multiple workers listening on an event bus for messages at a time. By having redundant workers, timely processing of messages can be ensured even when the worker programs crash or freeze. With multiple workers how do you make sure that the same message doesn't get processed more than once? When a worker program crashes, how do you ensure that another worker will handle the message? SQS has mechanisms designed with these scenarios in mind.

When a message is received from SQS it becomes invisible for a timeout duration. If the timeout expires before the message is deleted the message gets put back on the queue. A worker program can therefore delete the message after the message has been processed. If the program crashes before the message is processed and deleted the queue will automatically enqueue the message after the timeout.

You might have seen that in the example above, that a message is received only during the first execution of the program. Subsequent executions should print no messages until the timeout duration has passed.

Read the [guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-basic-architecture.html) for more information.

### Pricing and Long polling

AWS SQS is priced using a pay-per-use model, meaning your account will get charged based on how many times the SQS APIs - including _receive messages_ - are called ([reference](https://aws.amazon.com/sqs/pricing/)). For this reason, AWS enabled HTTP long polling on the SQS urls.

In regular polling a client program periodically makes requests to a server with the expectation of receiving an instant response (with a short timeout). In HTTP this can be expensive because it may mean creating and destroying a connection every request even when the server returns blank responses (e.g. when there are no queued messages). Instead, with long polling enabled, the server will delay responding and keep the connection alive until there is content or if the timeout duration is reached.

## Challenge

Using the template code in `main.py` write a program that creates thumbnails of images from `s3://<bucket_name>/images/` automatically when it is uploaded and upload them to `s3://<bucket_name>/thumbnails`. Use long polling to wait on messages from SQS using `sqs.receive_messages` with `WaitTimeSeconds`. When the thumbnail is generated and uploaded make sure to delete the message from the queue so it does not get processed again. It is highly recommended that you set `MaxNumberOfMessages=1`.

Try to understand the new concepts sprinkled throughout the template.