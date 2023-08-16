from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient,BlobServiceClient

storage_account_key = "t+YV6VRqvmrnVPmzGSTRZf62074W0V7yHEiuJ26Q3KjiGDU/hMUX4Ewa9r2Ci3bDVQbRlQmY4zsw+AStXbt30Q=="
storage_account_name = "fotafwstorage"
connection_string = "DefaultEndpointsProtocol=https;AccountName=fotafwstorage;AccountKey=t+YV6VRqvmrnVPmzGSTRZf62074W0V7yHEiuJ26Q3KjiGDU/hMUX4Ewa9r2Ci3bDVQbRlQmY4zsw+AStXbt30Q==;EndpointSuffix=core.windows.net"
container_name = "fwstore"


def list_blobs(): 
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container=container_name) 
    blob_list = container_client.list_blobs()
    print('file',blob_list)
    file_list= []
    for blob in blob_list:
        file_list.append(blob.name)
    return file_list

print(list_blobs())