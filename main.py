"""Main module for my AWS Bedrock playground"""

import boto3 as aws
import json

bedrock = aws.client("bedrock")

def list_models():
    models = bedrock.list_foundation_models()
    return models

def get_model(model: str):
    model = bedrock.get_foundation_model(modelIdentifier=model)
    return model["modelDetails"]


def main():
    models = list_models()
    print(json.dumps(models, default=str))

    print('\n---\n')
    
    model = get_model('amazon.titan-text-lite-v1')
    print(json.dumps(model, default=str))


if __name__ == "__main__":
    main()
