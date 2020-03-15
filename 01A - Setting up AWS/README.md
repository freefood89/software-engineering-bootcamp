[DRAFT]

# 01A - Setting up AWS

In this step you will set up your own AWS account and cloud resources necessary for automating thumbnail generation. For this step, please read over all of the instructions first before proceeding.

## Account Setup

1. Create a new AWS account. This may take a while.
2. Secure your root account with MFA such as Google Authenticator.
3. Create a user with both programmatic access and AWS management console access. This will be how you will log in and access AWS. During this process you will also create a group with permissions. You can simply use the policy `PowerUserAccess`, which is an AWS managed policy that bundles permissions for pretty much everything except Administratice permissions. Finally, you will be presented with the access key for this user. Click 'Download CSV' to get credentials. Do not share or lose this file!
4. Log out of Root Account and Log in using the new credentials you have just created.

## Configuring Resources

Before you start, set the region in the top right of the console to 'N. Virginia' to set the AWS region to `us-east-1`. Alternatively, you can just go to the following address: [https://console.aws.amazon.com/console/home?region=us-east-1](https://console.aws.amazon.com/console/home?region=us-east-1). We will be working exclusively in this region to avoid confusion. For more on AWS regions read their documentation ([docs](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)).

### IAM Service Account

Note: This step will require you to log back into the root account.

1. Create an IAM User named `thumbnail-service` with only programmatic access.
2. Add the following permissions directly to the User:
   - AmazonSQSFullAccess
   - AmazonS3FullAccess
3. Save the credentials file

### S3 Bucket

Create an S3 bucket with a unique bucket name. This is where all of your images and thumbnails will be stored. The bucket can be created with the default settings. Note that this means:

 - Bucket is located in US East
 - Versioning is disabled
 - Access logging is disabled
 - Objects are not encrypted
 - Metrics are not collected
 - Public Access is Denied

Once the bucket is created, create a folder called `images` and another called `thumbnails`. The URLs for those folders are `s3://<bucket_name>/images` and `s3://<bucket_name>/thumbnails` respectively.

### SQS Queue

1. Navigate to SQS (Simple Queue Service) and click Create New Queue
2. Name it `thumbnail-uploads` select Standard Queue and click Quick Create
3. Configure the queue with the following policy document. Make sure to use your bucket name.

```json
{
  "Version": "2012-10-17",
  "Id": "example-ID",
  "Statement": [
    {
      "Sid": "example-statement-ID",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:SendMessage",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:<bucket_name>"
        }
      }
    }
  ]
}
```

4. Configure your S3 bucket to emit events to your new queue:
   - Select your S3 bucket from the console and navigate to properties tab. Scroll all the way down to Events and create a new notification
   - Select "All object create events"
   - Set prefix to "image/"
   - Set Send To to SQS
   - Select your queue from dropdown
5. Your queue should now receive events every time a new file is uploaded to `s3://bucket_name/images`. You can inspect the message in the queue by right clicking your queue from the console and selecting View Messages then Start Polling.

## Install AWS CLI

Install the AWS command line interface ([instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)). This is a very handy tool to interact with AWS' API. It's often used for debugging and automation.

Configure AWS CLI. You will need to configure the CLI to use your credentials for both your power user and `thumbnail-service` user:

```
$ aws configure --profile power-user
AWS Access Key ID [None]: <access_key_id_for_power_user>
AWS Secret Access Key [None]: <secret_key_for_power_user>
Default region name [None]: us-east-1
Default output format [None]: 
```

```
$ aws configure --profile thumbnail-service`
AWS Access Key ID [None]: <access_key_id_for_thumbnail_service>
AWS Secret Access Key [None]: <secret_key_for_thumbnail_service>
Default region name [None]: us-east-1
Default output format [None]: 
```

Let's confirm that the profiles are set up properly. The `thumbnail-service` profile should have access to perform any action against S3 and SQS as configured. The following commands should list the resources you created in the previous steps:

```
$ aws s3 ls --profile thumbnail-service
$ aws sqs list-queues --profile thumbnail-service
```

It should not have access to anything else:

```
$ aws sns list-subscriptions --profile thumbnail-service
An error occurred (AuthorizationError) when calling the ListSubscriptions operation: User: arn:aws:iam::0000000000:user/thumbnail-service is not authorized to perform: SNS:ListSubscriptions on resource: arn:aws:sns:us-east-1:0000000000:*
```

The `power-user` profile should be able to do all three and more:

```
$ aws s3 ls --profile power-user
$ aws sqs list-queues --profile power-user
$ aws sns list-subscriptions --profile power-user
```


