#!/usr/bin/env python3
import json
import boto3
import argparse
import os
import uuid
import base64

# Note, ensure your default AWS profile has the correct secret and key.
# The index is created with 4 attributes. I had to add those manually in the Kendra console.

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
    # Create the document with metadata from parent objects
    document = {
        "Regulation": regulation["name"],
        "RegulatoryEntity": regulation["entity"],
        "Chapter": chapter["name"],
        "ChapterTitle": chapter["title"],
        "StandardName": standard["name"],
        "StandardDescription": standard["description"]
    }

    # Add optional fields if they exist
    if "title" in standard and standard["title"]:
        document["StandardTitle"] = standard["title"]
    if "code" in standard and standard["code"]:
        document["StandardCode"] = standard["code"]
    if "rationale" in standard and standard["rationale"]:
        document["StandardRationale"] = standard["rationale"]
    if "introduction" in standard and standard["introduction"]:
        document["StandardIntroduction"] = standard["introduction"]

    # Format the elements
    elements_content = []
    for element in standard["elements"]:
        element_text = f"{element['name']} ({element['short_name']}): {element['description']}"
        elements_content.append(element_text)

    # Create content combining all relevant information
    content = f"""
Regulation: {regulation['name']}
Entity: {regulation['entity']}
Chapter: {chapter['name']}
Chapter Title: {chapter['title']}

Standard: {standard['name']}
Description: {standard['description']}

Elements:
{chr(10).join(elements_content)}
"""

    # Add overview, about, and outline from chapter
    if chapter.get("overview"):
        content += f"\nChapter Overview:\n{chapter['overview']}\n"
    if chapter.get("about"):
        content += f"\nAbout the Chapter:\n{chapter['about']}\n"
    if chapter.get("outline"):
        content += f"\nChapter Outline:\n{chapter['outline']}\n"

    # Convert content to bytes and encode as base64
    content_bytes = content.encode('utf-8')
    content_base64 = base64.b64encode(content_bytes)

    return {
        "Id": str(uuid.uuid4()),
        "Title": f"{regulation['name']} - {standard['name']}",
        "Blob": content,
        "ContentType": "PLAIN_TEXT",
        "Attributes": [
            {"Key": "regulatory_program", "Value": {"StringValue": regulation["name"]}},
            {"Key": "regulatory_entity", "Value": {"StringValue": regulation["entity"]}},
            {"Key": "regulatory_chapter", "Value": {"StringValue": chapter["name"]}},
            {"Key": "regulatory_standard", "Value": {"StringValue": standard["name"]}}
        ]
    }


def upload_to_kendra(documents, index_id, region="us-east-1"):
    """
    Upload documents to the specified Kendra index.
    """
    try:
        kendra_client = boto3.client('kendra', region_name=region)

        # Batch the documents into groups of 10 (Kendra's limit)
        batch_size = 10
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]

            response = kendra_client.batch_put_document(
                IndexId=index_id,
                Documents=batch
            )

            print(f"Uploaded batch {i//batch_size + 1} of {(len(documents) + batch_size - 1)//batch_size} batches.")
            failed_documents = response.get('FailedDocuments', [])
            if failed_documents:
                print(f"Failed to upload {len(failed_documents)} documents in this batch:")
                for failed_doc in failed_documents:
                    print(f"  - {failed_doc['Id']}: {failed_doc['ErrorMessage']}")

        print(f"Upload completed. Total documents: {len(documents)}")
        return True

    except Exception as e:
        print(f"Error uploading to Kendra: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Upload regulatory standards to Amazon Kendra.")
    parser.add_argument("--file", default="data\\regulatory_standards_usa.json", help="Path to the regulatory standards JSON file")
    parser.add_argument("--index-id", default="5d259b03-9d6b-47be-a08c-517bfbb3c7c5", help="Amazon Kendra index ID")
    parser.add_argument("--region", default="us-east-2", help="AWS region (default: us-east-2)")

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
            print(f"  Processing chapter: {chapter['name']}")

            # Process each standard
            for standard in chapter["standards"]:
                # Create a document for this standard
                document = create_standard_document(standard, chapter, regulation)
                all_documents.append(document)

    print(f"Prepared {len(all_documents)} documents for upload.")

    # Upload to Kendra
    if all_documents:
        print(f"Uploading documents to Kendra index: {args.index_id}")
        upload_to_kendra(all_documents, args.index_id, args.region)

if __name__ == "__main__":
    main()
