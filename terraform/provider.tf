provider "aws" {
  region = "us-west-2"
}

terraform {
  backend "s3" {
    bucket = "mcordell-terraform"
    key    = "slowhacker"
    region = "us-west-2"
  }
}
