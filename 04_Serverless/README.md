# Getting Started

In this challenge you will set up a fully serverless web app hosted on AWS. The app should allow authenticated users to: 

1. Upload image files 
2. Receive a notification when an image thumbnail is created
2. View a gallery of image thumbnails

**Note** - The focus here is on getting everything working end to end in the cloud, but this project can be extended for image manipulation (like meme generators) or image classification using machine learning. The uploaded file doesn't even have to be limited to images.

## Tech Stack

The following technology stack will be used to build the application: 

1. Frontend - React served from S3 + Cloudfront
2. Backend - Python on Lambda + API Gateway + Cloudfront
3. Database - DynamoDB
4. Auth - Cognito

## Tooling

The following tools will be used to manage the AWS resources:

1. AWS CLI for uploading the frontent to S3
2. Chalice for managing the endpoints
3. Terraform for all other AWS resources

## Challenge Breakdown

This challenge is broken down into parts that sequentially build on the solution parts before it.