resource "aws_dynamodb_table" "smmry-storage" {
    name = "slowhacker-smmry-storage"
    billing_mode = "PAY_PRE_REQUEST"
    
    hash_key = "url"
    range_key = "url"

    attribute {
        name = "url"
        type = "S"
    }

    tags = {
        name = "dynamodb-slowhacker-smmry-storage"
    }
}