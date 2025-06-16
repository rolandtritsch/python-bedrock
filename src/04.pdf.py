"""This is a simple chat application that will allow users to chat with some PDF files."""

import logging
import os
import sys

import boto3 as aws
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_aws.llms import BedrockLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

bedrock = aws.client(service_name="bedrock")
bedrock_runtime = aws.client(service_name="bedrock-runtime")
model = BedrockLLM(model_id="amazon.titan-text-express-v1", client=bedrock_runtime)
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_runtime)

logging.basicConfig(level=logging.INFO)


def get_chunks(pdf_files, n):
    chunks = []
    for pdf_file in pdf_files[:n]:
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=80)
        texts = text_splitter.split_documents(documents)
        chunks.extend(texts)

    return chunks


def get_context(question, retriever):
    results = retriever.invoke(question)

    context = []
    for result in results:
        context.append(result.page_content)

    return context


def get_response(question, context):
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that answers questions about PDF files. Answer the questions using this context: {context}",  # noqa: E501
            ),
            ("user", "{question}"),
        ]
    )

    chain = template | model

    response = chain.invoke({"question": question, "context": context})

    return response


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Chat about PDF files")
    parser.add_argument("directory", type=str, help="the directory containing the PDF files")
    args = parser.parse_args()

    pdf_files = []
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    logging.debug(f"Found {len(pdf_files)} pdf files in the directory")
    logging.debug(f"PDF files: {pdf_files}")

    chunks = get_chunks(pdf_files, 20)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 30})

    logging.info(f"Added {len(chunks)} chunks to the vectorstore")

    question = "What is are these PDF docs about?"
    context = get_context(question, retriever)

    logging.debug(f"Context: {context}")

    response = get_response(question, context)

    print(response)

    sys.exit(0)


if __name__ == "__main__":
    main()
