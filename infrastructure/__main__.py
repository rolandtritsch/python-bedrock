"""The AWS Bedrock Playground Resources"""

import pulumi
import pulumi_aws as aws

bucket = aws.s3.BucketV2('aws-bedrock-playground-bucket')

roland_user = aws.iam.get_user(user_name='roland')

bedrock_policy = aws.iam.Policy('bedrock-foundation-model-policy',
    name='BedrockFoundationModelAccess',
    description='Policy for accessing AWS Bedrock foundation models',
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                    "bedrock:ListFoundationModels",
                    "bedrock:GetFoundationModel"
                ],
                "Resource": "*"
            }
        ]
    }"""
)

roland_policy_attachment = aws.iam.UserPolicyAttachment('roland-bedrock-policy-attachment',
    user=roland_user.user_name,
    policy_arn=bedrock_policy.arn
)

pulumi.export('bucket_name', bucket.id)
pulumi.export('bedrock_policy_arn', bedrock_policy.arn)
