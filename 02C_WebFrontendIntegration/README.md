# 02C - Web Frontend Integration

Now that the Presigned URL API is implemented, in this step you will generate a Javascript client library for it. The library will then be used by a browser based frontend to grab a presigned URL and upload directly to S3.

Whether a code generator is used to create a client library for an API is a decision impacted by the specific needs of a team. I personally dislike generated code, but it definitely has its uses. By being rigourous about the specification of the underlying service (API) we can instantly create a client interface in any language and publish versioned releases into package managers like PyPI, NPM, etc. This can be an accelerant for small teams or serve as a codified contract for teams interfacing at the technology stack level (e.g. frontend team and backend team), reducing the risk of miscommunication i.e. bugs. In the context of this challenge it's vastly reducing the time it takes to build out a system than can be tested end to end.

Note: It's highly recommended to at least scan through the code that's been generated. You should treat it as if it were your work product.

## Parts

- `connexion`
- `OpenAPI` is a standard for writing specifications for APIs [[docs](http://spec.openapis.org/oas/v3.0.3)]
- `openapi-generator` is a CLI that can generate client libraries for APIs using its OpenAPI specification file

## Generating your SDK

Once `openapi-generator` is installed (Java is required for this step) use it to generate the SDK code:

```
cd <folder with solution>
openapi-generator generate -i example.yaml -g javascript -o image-api
```

The command above generates the javascript project in a folder named `image-api`. The next step is to install dependencies and build your SDK:

```
cd image-api
npm install
npm run build
```

You should now find a `dist` folder with the transpiled module. This module can be imported from your javascript project, which in this case is the mock frontend that can be found in the starter folder for this challenge.

## Building the Frontend

With the client SDK the frontend code will now have to be built. In your solution folder you will find all the files necessary to build the frontend. First run `npm install` to install dependancies and especially `rollup` which is the build tool being used for this challenge. Run `npm run build` to build the frontend. Once built `app.py` will serve the frontend at [localhost:5000/](http://localhost:5000/) with static files being served from `localhost:5000/static/`.

Depending on how things are named in the OpenAPI specification the method names and client SDK structure may be different from what the frontend Javascript code expects. You may need to change things to get your app to work. Luckily, the generated SDK will also come with documentation to help you sort this out.

## Setup S3 Bucket

In order to allow the S3 bucket to receive new objects from `localhost:5000` it needs to be configured to accept cross origin requests (We are making requests from one origin at `localhost:5000` to another at `s3.amazonaws.com`). Navigate to your S3 bucket's permissions configuration view and update the CORS configuration with the following:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>http://localhost:5000</AllowedOrigin>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

Once the app is hosted with a non-local domain name it will need to be added with another `AllowedOrigin` tag.

## Challenge

Make the entire service work end to end. From the frontend you should be able to upload an image to S3, which will subsequently trigger an SQS message. The SQS message should trigger your local thumbnail worker code to generate a thumbnail for this image and upload it to the thumbnail folder in the bucket.