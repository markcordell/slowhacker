resource "aws_s3_bucket" "bucket" {
  bucket = "slowhacker-site"

  tags = {
    Name = "slowerhacker hosting bucket"
    Env  = "prod"
  }
}
