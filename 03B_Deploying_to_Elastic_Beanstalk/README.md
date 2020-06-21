# 03B - Deploying to AWS Elastic Beanstalk Part 1

In this step you will modify and deploy the thumbnail generation service to AWS using Elastic Beanstalk. Elastic Beanstalk is a platform service in AWS that it helps simplify infrastructure for developers. Using this platform, developers can focus on developing their application, rather than having to implement and maintain all of the infrastructure from the ground up,

Of the two application types supported by Elastic Beanstalk (web server and worker) the challenge in this step will focus on the worker tier.

### Elastic Beanstalk Worker Tier

The worker tier is designed to process messages from SQS queues and thus is well suited for the thumbnail service. A daemon process called `sqsd` will be deployed alongside your application and will handle listening for messages from SQS for you. The message will then be sent to your application via an HTTP POST request.

## Parts

- `eb cli` - Elastic Beanstalk dedicated CLI tool

## Challenge

Deploy the thumbnail service in a python worker tier environment. The worker should subscribe to your existing SQS queue that's already configured to receive messages from S3. Starter code has been provided in `application.py`.

### Step 1 - Queue

Make sure that your S3 bucket and SQS queue are working so that when you upload a file to `s3://<bucket_name>/images` a message is put on the SQS queue.

### Step 2 - IAM Instance Profile

Up until now, the application has been using credentials belonging to an IAM User. 

In this step, you will need to create a new IAM Role named `thumbnail-worker` which your worker environment instances will assume through an Instance Profile to interact with S3. The IAM policies associated with this role will mostly be the same and should contain the folloing managed policies:

- `AmazonS3FullAccess`
- `AWSElasticBeanstalkWorkerTier`

As mentioned earlier ElasticBeanstalk configures all of the infrastructure components, as such it requires permission to interact with various AWS services it enables. It is recommended that you take note of the permissions attached to `AWSElasticBeanstalkWorkerTier`.

### Step 3 - Deploy the Starter Code

Initialize your ElasticBeanstalk application named `thumbnail-service`:

`eb init --region us-east-1 --platform "Python 3.7" thumbnail-service`

in a folder named `.ebextensions` create a file named `options.config` with the following contents:

```yaml
option_settings:
  - namespace: aws:elasticbeanstalk:sqsd
    option_name: WorkerQueueURL
    value: <your_sqs_queue_url>
```

Then create your `thumbnail-worker-dev` ElasticBeanstalk environment:

`eb create -t worker -i t3.micro -ip "thumbnail-worker" thumbnail-worker-dev`

The instance profile is configured in the CLI as opposed to the SQS URL due to precedence reasons [read more](https://stackoverflow.com/questions/30669483/assign-role-to-instance-in-ebextensions).

### Step 4 - Test the Starter Code

Test your deployed starter code by uploading a file to `s3://<your_bucket>/images` and viewing your application logs. The command `eb logs thumbnail-worker-dev` will download and open your logs. Look for the section `/var/log/web.stdout.log` to find logs from the starter code. 

You should see that the logged SQS Message body looks different from when you get the message directly using `boto3`. This is because the `sqsd` daemon running in your worker will perform the appropriate SQS operations depending on your application's HTTP response. There's no need for you to handle it manually.

### Step 5 - Implement

Using the starter code and logged SQS Message body modify the code to generate thumbnails as you have previously done. In this step do not worry about the database aspect of the code. If a file `gg.png` is uploaded simply store its thumbnail as `gg.thumbnail.png` in the appropriate folder.