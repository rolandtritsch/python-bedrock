"""Main module for my AWS Bedrock playground"""

import boto3 as aws
import json

bedrock = aws.client(service_name="bedrock")
bedrock_runtime = aws.client(service_name="bedrock-runtime")

def list_models():
    models = bedrock.list_foundation_models()
    return models

def get_model(model: str):
    model = bedrock.get_foundation_model(modelIdentifier=model)
    return model["modelDetails"]


def answer_question(modelId, question):
    ask = json.dumps({
      "inputText": question,
      "textGenerationConfig": {
        "maxTokenCount": 4096,
        "stopSequences": [],
        "temperature": 0.0,
        "topP": 1.0,
        }
      })
    response = bedrock_runtime.invoke_model(
      body=ask,
      modelId=modelId,
      accept="application/json",
      contentType="application/json"
      )
    answer = json.loads(response.get('body').read())
    return answer


def main():
    models = list_models()
    print(json.dumps(models, default=str))

    print('\n---\n')
    
    model = get_model('amazon.titan-text-lite-v1')
    print(json.dumps(model, default=str))

    print('\n---\n')
    
    answer = answer_question(model['modelId'], 'Give me a random planet from the solar system.')
    print(json.dumps(answer, default=str))


if __name__ == "__main__":
    main()
