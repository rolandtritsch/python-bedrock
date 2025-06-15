"""A very simple chat app (that keeps the context/history of the conversation)"""

import json

import boto3 as aws

prompt_prefix = "User: "

bedrock = aws.client(service_name="bedrock")
bedrock_runtime = aws.client(service_name="bedrock-runtime")


def get_model(model: str):
    model = bedrock.get_foundation_model(modelIdentifier=model)
    return model["modelDetails"]


model = get_model("amazon.titan-text-express-v1")


def get_request(prompt):
    if model["modelId"] == "amazon.titan-text-express-v1":
        return {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0.0,
                "topP": 1.0,
            },
        }
    else:
        raise Exception("Unknown model")


def get_response(request):
    response = bedrock_runtime.invoke_model(
        body=json.dumps(request),
        modelId=model["modelId"],
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    if model["modelId"] == "amazon.titan-text-express-v1":
        return response_body.get("results")[0].get("outputText").strip()
    else:
        raise Exception("Unknown model")


def get_history(history):
    return "\n".join(history)


def main():
    print("Bot: A chat, we should have (use '/quit' to quit)!")
    history = []
    while True:
        prompt = input(prompt_prefix)
        if prompt.lower() == "/quit":
            break
        elif prompt.lower() == "/clear":
            history = []
            continue
        elif prompt.lower() == "/history":
            print(get_history(history))
            continue
        elif prompt.lower() == "/help":
            print("Available commands:\n")
            print("/quit: Quit the chat")
            print("/clear: Clear the chat history")
            print("/history: Print the chat history")
            print("/help: Print this help message")
            continue
        else:
            history.append(prompt_prefix + prompt)
            request = get_request(get_history(history))
            response = get_response(request)
            history.append(response)
            print(response)


if __name__ == "__main__":
    main()
