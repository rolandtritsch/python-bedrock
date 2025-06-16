"""A similarity calculator that takes two text files and returns the similarity between them."""

import json
import os
import sys

import boto3 as aws
import numpy as np

bedrock = aws.client(service_name="bedrock")
bedrock_runtime = aws.client(service_name="bedrock-runtime")


def get_model(model: str):
    model = bedrock.get_foundation_model(modelIdentifier=model)
    return model["modelDetails"]


model = get_model("amazon.titan-embed-text-v2:0")


def get_embedding(text: str):
    response = bedrock_runtime.invoke_model(
        body=json.dumps({"inputText": text}),
        modelId=model["modelId"],
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Calculate the similarity between two text files")
    parser.add_argument("file1", type=str, help="the first file")
    parser.add_argument("file2", type=str, help="the second file")
    args = parser.parse_args()

    for file in [args.file1, args.file2]:
        if not os.path.isfile(file):
            print(f"{file} is not a file")
            sys.exit(1)
        if os.path.splitext(file)[1] not in [".txt", ".csv"]:
            print(f"{file} is not a text file")
            sys.exit(1)

    with open(args.file1, "r") as file:
        text1 = file.read()
    with open(args.file2, "r") as file:
        text2 = file.read()

    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)

    similarity = np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )
    print(similarity)

    sys.exit(0)


if __name__ == "__main__":
    main()
