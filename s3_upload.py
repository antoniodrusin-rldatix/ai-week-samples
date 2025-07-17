#!/usr/bin/env python3
import json
import boto3
import argparse
import os
import uuid
import base64
from botocore.exceptions import ClientError

## After uploading to the s3 bucket, you can create a Knowledge Base in Amazon Bedrock using the AWS console or CLI.

def load_regulatory_standards(file_path):
    """
    Load the regulatory standards from a JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            standards_data = json.load(file)
        return standards_data
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        return None

def create_standard_document(standard, chapter, regulation):
    """
    Create a document for a single standard, including all parent information and elements.
    """
    # Create the document with all attributes embedded
    document = {
        "id": str(uuid.uuid4()),
        "regulation": {
            "name": regulation["name"],
            "entity": regulation["entity"]
        },
        "chapter": {
            "name": chapter["name"],
            "title": chapter["title"],
            "overview": chapter.get("overview", ""),
            "about": chapter.get("about", ""),
            "outline": chapter.get("outline", "")
        },
        "standard": {
            "name": standard["name"],
            "title": standard.get("title", ""),
            "code": standard.get("code", ""),
            "description": standard["description"],
            "rationale": standard.get("rationale", ""),
            "introduction": standard.get("introduction", "")
        },
        "elements": standard["elements"]
    }

    # Create a human-readable content string for potential future use
    content = f"""
Regulation: {regulation['name']}
Entity: {regulation['entity']}
Chapter: {chapter['name']}
Chapter Title: {chapter['title']}

Standard: {standard['name']}
Description: {standard['description']}

Elements:
"""
    for element in standard["elements"]:
        content += f"{element['name']} ({element['short_name']}): {element['description']}\n"

    # Add overview, about, and outline from chapter
    if chapter.get("overview"):
        content += f"\nChapter Overview:\n{chapter['overview']}\n"
    if chapter.get("about"):
        content += f"\nAbout the Chapter:\n{chapter['about']}\n"
    if chapter.get("outline"):
        content += f"\nChapter Outline:\n{chapter['outline']}\n"

    # Store the formatted content as well
    document["formatted_content"] = content

    return document

def create_s3_bucket(bucket_name, region=None):
    """
    Create an S3 bucket if it doesn't exist

    :param bucket_name: Name of the bucket to create
    :param region: AWS region to create bucket in, e.g., 'us-east-1'
    :return: True if bucket exists or was created, False otherwise
    """
    try:
        s3_client = boto3.client('s3', region_name=region)

        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} already exists")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket does not exist, create it
                if region is None:
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration=location
                    )
                print(f"Bucket {bucket_name} created successfully")
                return True
            else:
                print(f"Error checking bucket: {e}")
                return False
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return False

def upload_to_s3(documents, bucket_name, prefix="regulatory_standards/", region=None):
    """
    Upload documents to an S3 bucket as formatted text files

    :param documents: List of document objects to upload
    :param bucket_name: Name of the S3 bucket
    :param prefix: Prefix (folder) to use for uploaded files
    :param region: AWS region for the S3 bucket
    :return: True if upload was successful, False otherwise
    """
    try:
        # First, ensure the bucket exists
        if not create_s3_bucket(bucket_name, region):
            return False

        # Initialize S3 client
        s3_client = boto3.client('s3', region_name=region)

        # Track upload statistics
        successful_uploads = 0
        failed_uploads = 0

        # Upload each document
        for document in documents:
            try:
                # Create a unique filename for each document
                doc_id = document["id"]
                filename = f"{prefix}{document['regulation']['name']}/{document['chapter']['name']}/{doc_id}.txt"

                # Create a formatted text document
                formatted_text = format_document_as_text(document)


                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=filename,
                    Body=formatted_text,
                    ContentType='text/plain'
                )
                successful_uploads += 1

                # Print progress every 10 documents
                if successful_uploads % 10 == 0:
                    print(f"Uploaded {successful_uploads} documents so far...")

            except Exception as e:
                print(f"Failed to upload document {document.get('id', 'unknown')}: {str(e)}")
                failed_uploads += 1

        print(f"Upload completed. Total: {len(documents)}, Successful: {successful_uploads}, Failed: {failed_uploads}")
        return True

    except Exception as e:
        print(f"Error during S3 upload process: {str(e)}")
        return False

def format_document_as_text(document):
    """
    Format a document object as a well-structured text document

    :param document: The document object containing all regulatory standard data
    :return: A formatted text string
    """
    # Extract components for easier reference
    regulation = document["regulation"]
    chapter = document["chapter"]
    standard = document["standard"]
    elements = document["elements"]

    # Build the formatted text
    text = f"""REGULATORY STANDARD DOCUMENT
Document ID: {document["id"]}

---------- REGULATION ----------
Name: {regulation["name"]}
Regulatory Entity: {regulation["entity"]}

---------- CHAPTER ----------
Name: {chapter["name"]}
Title: {chapter["title"]}
"""

    # Add optional chapter content if available
    if chapter["overview"]:
        text += f"\nOVERVIEW:\n{chapter['overview']}\n"

    if chapter["about"]:
        text += f"\nABOUT:\n{chapter['about']}\n"

    if chapter["outline"]:
        text += f"\nOUTLINE:\n{chapter['outline']}\n"

    # Add standard information
    text += f"""
---------- STANDARD ----------
Name: {standard["name"]}
"""

    if standard["title"]:
        text += f"Title: {standard['title']}\n"

    if standard["code"]:
        text += f"Code: {standard['code']}\n"

    text += f"Description: {standard['description']}\n"

    if standard["rationale"]:
        text += f"\nRATIONALE:\n{standard['rationale']}\n"

    if standard["introduction"]:
        text += f"\nINTRODUCTION:\n{standard['introduction']}\n"

    # Add elements
    text += "\n---------- ELEMENTS ----------\n"

    for i, element in enumerate(elements, 1):
        text += f"{i}. {element['name']} ({element['short_name']})\n"
        text += f"   {element['description']}\n\n"

    text += "---------- END OF DOCUMENT ----------"

    return text

def main():
    parser = argparse.ArgumentParser(description="Upload regulatory standards to Amazon S3.")
    parser.add_argument("--file", default="data\\regulatory_standards_usa.json", help="Path to the regulatory standards JSON file")
    parser.add_argument("--bucket", default="rldatix-ai-week-usa-regulatory-standards", help="S3 bucket name")
    parser.add_argument("--prefix", default="regulatory_standards/", help="S3 prefix (folder) for uploads")
    parser.add_argument("--region", default="us-east-2", help="AWS region")

    args = parser.parse_args()

    # Load the regulatory standards
    data = load_regulatory_standards(args.file)
    if not data:
        return

    all_documents = []

    # Process each regulation
    for regulation in data:
        print(f"Processing regulation: {regulation['name']}")

        # Process each chapter
        for chapter in regulation["chapters"]:
            # Process each standard
            for standard in chapter["standards"]:
                # Create a document for this standard
                document = create_standard_document(standard, chapter, regulation)
                all_documents.append(document)

    print(f"Prepared {len(all_documents)} documents for upload.")

    # Upload to S3
    if all_documents:
        print(f"Uploading documents to S3 bucket: {args.bucket}")
        upload_to_s3(all_documents, args.bucket, args.prefix, args.region)

if __name__ == "__main__":
    main()
