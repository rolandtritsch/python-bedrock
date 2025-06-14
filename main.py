"""Main module for my AWS Bedrock playground"""

import boto3 as aws
import json


def list_models():
    bedrock = aws.client("bedrock")
    models = bedrock.list_foundation_models()
    return models


def main():
    models = list_models()
    print(json.dumps(models, default=str))


if __name__ == "__main__":
    main()
