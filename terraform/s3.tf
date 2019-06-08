resource "aws_s3_bucket" "bucket" {
  bucket = "slowhacker-site"
  acl    = "public-read"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
              "s3:GetObject"
          ],
          "Resource": [
              "arn:aws:s3:::slowhacker-site/*"
          ]
      }
  ]
}
EOF

  website {
    index_document = "index.html"
  }

  tags = {
    Name = "slowerhacker hosting bucket"
    Env  = "prod"
  }
}
