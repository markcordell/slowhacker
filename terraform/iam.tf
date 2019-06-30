resource "aws_iam_policy" "lambda_s3_policy" {
  name = "slowhacker-s3-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "slowhackerLambda",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:DeleteObject",
        "s3:GetBucketAcl",
        "s3:GetBucketCORS",
        "s3:GetBucketLocation",
        "s3:GetBucketLogging",
        "s3:GetBucketNotification",
        "s3:GetBucketPolicy",
        "s3:GetBucketWebsite",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:HeadBucket",
        "s3:ListBucket",
        "s3:ListBucketByTags",
        "s3:PutBucketAcl",
        "s3:PutBucketCORS",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::slowhacker-site/*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "slowhacker_lambda_role" {
  name = "slowhacker-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "slowhacker_lambda_s3" {
  name       = "slowhacker_lambda_s3_attachment"
  roles      = ["${aws_iam_role.slowhacker_lambda_role.name}"]
  policy_arn = "${aws_iam_policy.lambda_s3_policy.arn}"
}

resource "aws_iam_policy" "lambda_s3_policy_dev" {
  name = "slowhacker-s3-policy-dev"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "slowhackerLambda",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:DeleteObject",
        "s3:GetBucketAcl",
        "s3:GetBucketCORS",
        "s3:GetBucketLocation",
        "s3:GetBucketLogging",
        "s3:GetBucketNotification",
        "s3:GetBucketPolicy",
        "s3:GetBucketWebsite",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:HeadBucket",
        "s3:ListBucket",
        "s3:ListBucketByTags",
        "s3:PutBucketAcl",
        "s3:PutBucketCORS",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::slowhacker-site-dev/*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "slowhacker_lambda_role_dev" {
  name = "slowhacker-role-dev"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "slowhacker_lambda_s3_dev" {
  name       = "slowhacker_lambda_s3_attachment_dev"
  roles      = ["${aws_iam_role.slowhacker_lambda_role_dev.name}"]
  policy_arn = "${aws_iam_policy.lambda_s3_policy_dev.arn}"
}
