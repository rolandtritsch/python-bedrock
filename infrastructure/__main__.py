"""The AWS Bedrock Playground Resources"""

import pulumi
import pulumi_aws as aws

bucket = aws.s3.BucketV2('aws-bedrock-playground-bucket')

pulumi.export('bucket_name', bucket.id)
