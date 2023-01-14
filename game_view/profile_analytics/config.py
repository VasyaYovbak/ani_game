import os

from datetime import datetime, timezone

from azure.cosmos import CosmosClient, PartitionKey


endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")


client = CosmosClient(url=endpoint, credential=key)

database = client.create_database_if_not_exists(id="AniGame")

partition_key_path = PartitionKey(path="/id")

container = database.create_container_if_not_exists(
    id="ProfileAnalytics", partition_key=partition_key_path, offer_throughput=400
)

# Getting UTC +0 date
time_now = datetime.now(timezone.utc)

date_now = time_now.date()
