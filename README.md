# AWS Bedrock Document Intelligence Platform

An AI-powered document processing application built with Amazon Bedrock, Amazon S3, DynamoDB and Python Flask.

## Overview

This project analyses uploaded documents using Amazon Bedrock foundation models.

Users can upload PDF documents, which are stored in Amazon S3, processed by AI agents, and saved in DynamoDB for later review.

## Architecture

User
|
↓
Flask Web Application
|
↓
Amazon S3
|
↓
Document Processing Pipeline
|
↓
Amazon Bedrock
|
↓
Amazon DynamoDB


## Features

- PDF document upload
- S3 document storage
- AI document classification
- Invoice processing workflow
- Contract review workflow
- General document analysis
- Document history
- AI-powered document questions
- Document comparison


## AWS Services Used

- Amazon Bedrock
- Amazon S3
- Amazon DynamoDB
- AWS SDK for Python (Boto3)


## Technologies

- Python
- Flask
- HTML/CSS
- Boto3
- Amazon Nova Lite


## Project Structure

agent/
│
├── main.py
├── agent.py
├── bedrock_agent.py
├── s3_manager.py
├── database.py
├── document_classifier.py
├── invoice_processor.py
├── contract_reviewer.py
└── templates/



## Future Improvements

- Amazon Cognito authentication
- Bedrock Knowledge Base integration
- Vector search / RAG
- Production deployment
- User document permissions


## Author

GitHub: jazblue



