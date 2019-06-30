resource "aws_route53_record" "slowhacker-main" {
  zone_id = "Z3JOBMR6NA6MPY"
  name    = "slowhacker.com"
  type    = "A"

  alias {
    name                   = "${aws_s3_bucket.bucket.website_domain}"
    zone_id                = "${aws_s3_bucket.bucket.hosted_zone_id}"
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "slowhacker-dev" {
  zone_id = "Z3JOBMR6NA6MPY"
  name    = "dev.slowhacker.com"
  type    = "A"

  alias {
    name                   = "${aws_s3_bucket.bucket-dev.website_domain}"
    zone_id                = "${aws_s3_bucket.bucket-dev.hosted_zone_id}"
    evaluate_target_health = true
  }
}
