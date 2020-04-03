# 01A - Working with boto3

In this step you will design an API and write an OpenAPI specification for it.

## Parts

- `OpenAPI` is a standard for writing specifications for APIs [[docs](http://spec.openapis.org/oas/v3.0.3)]
- `boto3`


## Example

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

## Challenge

Write specifications for the following API endpoints:

- `POST /images` takes a filename and returns a presigned url for uploading an image to S3
- `GET /thumbnails` returns presigned URLs for all images in thumbnails folder