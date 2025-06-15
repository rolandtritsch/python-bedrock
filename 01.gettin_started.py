"""Main module for my AWS Bedrock playground"""

import json

import boto3 as aws

bedrock = aws.client(service_name="bedrock")
bedrock_runtime = aws.client(service_name="bedrock-runtime")


def list_models():
    models = bedrock.list_foundation_models()
    return models


def get_model(model: str):
    model = bedrock.get_foundation_model(modelIdentifier=model)
    return model["modelDetails"]


def get_titan_question(ask):
    return {
        "modelId": "amazon.titan-text-lite-v1",
        "ask": {
            "inputText": ask,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0.0,
                "topP": 1.0,
            },
        },
    }


def get_mistral_question(ask):
    return {
        "modelId": "mistral.mistral-7b-instruct-v0:2",
        "ask": {
            "prompt": ask,
            "max_tokens": 4096,
            "temperature": 0.0,
            "top_p": 1.0,
            "top_k": 50,
        },
    }


def answer(question):
    response = bedrock_runtime.invoke_model(
        body=json.dumps(question["ask"]),
        modelId=question["modelId"],
        accept="application/json",
        contentType="application/json",
    )
    answer = json.loads(response.get("body").read())
    return answer


def main():
    models = list_models()
    print(json.dumps(models, default=str))

    print("\n---\n")

    model = get_model("amazon.titan-text-lite-v1")
    print(json.dumps(model, default=str))

    print("\n---\n")

    titan_question = get_titan_question("Give me a random planet from the solar system.")
    titan_answer = answer(titan_question)
    print(json.dumps(titan_answer, default=str))

    print("\n---\n")

    mistral_question = get_mistral_question("Give me a random planet from the solar system.")
    mistral_answer = answer(mistral_question)
    print(json.dumps(mistral_answer, default=str))


if __name__ == "__main__":
    main()
