# 02A - Designing a Web API

In this step you will design an API and write an OpenAPI specification for it.

An API (Application Programming Interface) is a layer of software between an Application and an underlying system. This layer is often designed to provide specific ways in which the underlying system is to be utilized. It is common for APIs to evolve as Application developers request features and bugs are discovered. When releasing updates, API developers must use caution to not make changes in a way that breaks existing Applications that depend on it. 


## Parts

- `OpenAPI` is a standard for writing specifications for APIs [[docs](http://spec.openapis.org/oas/v3.0.3)]
- `boto3`


## Example

Paste the following to [Online Swagger Editor](https://editor.swagger.io/)

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
      summary: Gets profile of current user
      operationId: getProfile
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

The example above is a specification for a Web API for getting a user's profile in which calling `GET /users/me` should return `{ "id": "some_id" }`. If there is an error it will return something like the following:

```
{
	"code": 500,
	"message": "Could not connect to database"
}
```

## Challenge

1. Write specifications for the following API endpoint:

  - `POST /images` takes a filename and returns a url for uploading an image to S3

2. Generate a javascript client sdk with [OpenApi Generator](https://openapi-generator.tech/) and inspect contents.
