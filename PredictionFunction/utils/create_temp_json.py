import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import logging

# Retrieve the connection string and container name from environment variables
storage_account_link = os.environ.get("AzureWebJobsStorage", None)
storage_account_location = os.environ.get("storage_name", None)
import random

# Initial JSON data
initial_json = {
    "Los Tacos": {
        "Oslo Storo": 0,
        "Oslo City": 0,
        "Oslo Torggata": 0,
        "Karl Johan": 0,
        "Fredrikstad": 0,
        "Oslo Lokka": 0,
        "Stavanger": 0,
        "Bergen": 0,
        "Oslo Steen_Strom": 0,
        "Oslo Smestad": 0,
        "Sandnes": 0,
        "Trondheim": 0,
    },
    "Fisketorget": {"Restaurant": 0, "Fisketorget Utsalg": 0},
    # "Burgerheim": {"Åsane Storsenter": 0},
}


def fetch_or_initialize_json():
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(
            storage_account_link
        )

        # Create the container client
        container_client = blob_service_client.get_container_client(
            storage_account_location
        )

        # Define the blob name (filename in the container)
        blob_name = "execution_counts.json"

        # Create the blob client
        blob_client = container_client.get_blob_client(blob_name)

        try:
            # Attempt to read the blob content
            blob_data = blob_client.download_blob().readall()
            data = json.loads(blob_data)
            logging.info(f"Fetched existing JSON from blob: {blob_name}")
        except Exception as e:
            # If the blob does not exist, use the initial JSON data
            if "BlobNotFound" in str(e):
                data = initial_json
                logging.info(f"Blob not found. Initializing with initial JSON data.")
            else:
                raise

    except Exception as e:
        logging.info(f"Error fetching or initializing JSON: {e}")
        data = initial_json

    return data


def update_execution_count(data, company, restaurant):
    if company in data:
        if restaurant in data[company]:
            data[company][restaurant] += 1
        else:
            data[company][restaurant] = 1
    else:
        logging.info(f"Error: {company} does not exist in data.")
    return data


def save_json_file(data):
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(
            storage_account_link
        )

        # Create the container client
        container_client = blob_service_client.get_container_client(
            storage_account_location
        )

        # Create the container if it does not exist
        try:
            container_client.create_container()
        except Exception as e:
            # Handle the error if the container already exists
            if "ContainerAlreadyExists" not in str(e):
                raise

        # Convert the dictionary to a JSON string
        data_json = json.dumps(data, indent=4)

        # Define the blob name (filename in the container)
        blob_name = "execution_counts.json"

        # Create the blob client
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the JSON file
        blob_client.upload_blob(data_json, overwrite=True)

        logging.info(f"File {blob_name} uploaded successfully.")

    except Exception as e:
        logging.info(f"Error: {e}")


# Fetch or initialize the JSON data
def select_minimum_restaurant(data):
    min_count = float("inf")
    for company in data.values():
        for count in company.values():
            if count < min_count:
                min_count = count

    candidates = []
    for company, restaurants in data.items():
        for restaurant, count in restaurants.items():
            if count == min_count:
                candidates.append((company, restaurant))

    # Select one restaurant randomly from the candidates
    company, restaurant = random.choice(candidates)
    return company, restaurant
