import os
import boto3
from tabulate import tabulate

# The Bedrock API Key.
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "<Your bedrock API key>"

def list_inference_profiles(region):
    """
    List inference profiles for the specified AWS region
    """
    # Create Bedrock client (not bedrock-runtime)
    client = boto3.client(
        service_name="bedrock",
        region_name=region
    )

    # Get list of inference profiles
    response = client.list_inference_profiles()

    # Format data for table
    table_data = []
    for profile in response.get('inferenceProfileSummaries', []):
        table_data.append([
            profile.get('inferenceProfileName', 'N/A'),
            profile.get('inferenceProfileId', 'N/A'),
            profile.get('inferenceProfileArn', 'N/A')
        ])

    # Create table with tabulate in Markdown format
    headers = ["Name", "Profile ID", "ARN"]
    md_table = tabulate(table_data, headers=headers, tablefmt="pipe")

    return md_table

if __name__ == "__main__":
    # Default region - can be changed via command line argument
    region = "eu-west-1"

    # Allow region to be specified as command line argument
    import sys
    if len(sys.argv) > 1:
        region = sys.argv[1]

    print(f"Listing Bedrock inference profiles for region: {region}")

    try:
        table = list_inference_profiles(region)
        print("\nMarkdown Formatted Table:")
        print(table)
    except Exception as e:
        print(f"Error: {str(e)}")
