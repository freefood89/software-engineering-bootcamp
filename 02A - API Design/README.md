# 02A - Designing a Web API

In this step you will design a Web API for retrieving presigned URLs for uploading images by writing an OpenAPI specification for it.

An API (Application Programming Interface) is a layer of software between an Application and an underlying system. This layer is often designed to provide specific ways in which the underlying system is to be utilized. In this challenge the underlying system is your image upload and thumbnail generation microservice, which is presumably a part of some sort of Content Management System like Wordpress, Facebook, iStock, etc.

### A Note on Backwards Compatibility

It is common for APIs to evolve as Application developers request features and bugs are discovered. When releasing updates, API developers must use caution to not make changes in a way that breaks existing Applications that depend on it. Afterall, without the developers you have no customers.

## Parts

- `OpenAPI` is a standard for writing specifications for APIs [[docs](http://spec.openapis.org/oas/v3.0.3)]

## Example

Paste the following to [Online Swagger Editor](https://editor.swagger.io/). The online editor can be used to validate the specification YAML.

```
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Thumbnail Service API
  license:
    name: MIT
servers:
  - url: http://lolcats.gg
paths:
  /users/me:
    get:
      tags:
        - users
      summary: Gets profile of current user
      operationId: app.get_profile
      responses:
        '200':
          description: User Profile
          content:
            application/json:    
              schema:
                $ref: "#/components/schemas/User"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
components:
  schemas:
    User:
      type: object
      required:
        - id
      properties:
        id:
          type: string
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: integer
          format: int32
        message:
          type: string
```

The example above is a specification for a Web API for getting a user's profile in which calling `GET /users/me` should return a `User`, with a schema specified in `components`. 

If there is an error it will return something like the following:

```
{
	"code": 500,
	"message": "Could not connect to database"
}
```

## Challenge

Extend the OpenAPI specification above for an endpoint for retrieving a presigned URL. In order to create a presigned URL for uploading images [[boto docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url)] the API will need to get the image's file name and [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types).

For example, for a PNG image `lol.png`, the HTTP request will be the following:

`GET /images/upload_url?filename=lol.png&image%2Fpng`

The above HTTP request should return `{ "upload_url": "https://blah..." }` with a URL configured for a payload of MIME type of `image/png`.

Hint: In OpenAPI query parameters ([see docs](https://swagger.io/docs/specification/describing-parameters/)) can be specified using the following:

```
parameters:
  - in: query
    name: <key name>
    description: <description>
    schema:
      type: string
    required: true
```