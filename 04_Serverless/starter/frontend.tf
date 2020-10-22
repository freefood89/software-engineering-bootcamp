provider "aws" {
  region = "us-east-1"
  profile = "freefood89" # AWS_PROFILE for credentials
}

resource "aws_s3_bucket" "imagely_frontend" {
  bucket = "imagely-frontend" # pick your own bucket name!
  acl    = "private"

  tags = {
    Name = "imagely"
  }
}

data "aws_iam_policy_document" "imagely_frontend" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.imagely_frontend.arn}/*"]

    principals {
      type        = "AWS"
      # IMPLEMENT
      # identifiers = [aws_cloudfront_origin_access_identity.imagely_oai.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "imagely_frontend" {
  bucket = aws_s3_bucket.imagely_frontend.id
  policy = data.aws_iam_policy_document.s3_policy.json
}