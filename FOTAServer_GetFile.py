from azure.storage.blob import BlobServiceClient
from azure.iot.device import IoTHubDeviceClient
import time

# ket noi toi iot hub
CONNECTION_STRING = "HostName=FotaWebserver.azure-devices.net;DeviceId=raspberry4;SharedAccessKey=bsmqCOwvRpNENe4O5Z4wubiz80TM9jxZhRlCsK1bsRs="

# Kết nối tới Azure Storage Account
connection_string = "DefaultEndpointsProtocol=https;AccountName=fotafwstorage;AccountKey=t+YV6VRqvmrnVPmzGSTRZf62074W0V7yHEiuJ26Q3KjiGDU/hMUX4Ewa9r2Ci3bDVQbRlQmY4zsw+AStXbt30Q==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Tên container cần kiểm tra
container_name = "fwstore"
# Lưu trữ danh sách tên file trước đó


# Biến đánh dấu lần đầu chạy

# Lấy danh sách tên file trong container
def get_file_names():
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()
    file_names = [blob.name for blob in blobs]
    return file_names
def load_file_name():
    saved_file_name = []
    saved_file_name = get_file_names()
    return saved_file_name
    
def get_file_from_cloud(previous_files):


    # Kiểm tra sự thay đổi trong container và tải xuống file khi yêu cầu
    download_file_status = "NOK"
    # Lấy danh sách tên file hiện tại
    current_files = get_file_names()

    # Kiểm tra sự thay đổi nếu không phải lần đầu chạy
    
    added_files = [file for file in current_files if file not in previous_files]
    
    # In ra thông báo nếu có sự thay đổi
    if added_files:
        print("Đã phát hiện sự thay đổi trong container")
        print("Các file mới được thêm:")
        for file in added_files:
            print(file)
            # Hỏi người dùng có muốn tải xuống file hay không
            user_input = input("Bạn có muốn tải xuống file này? (y/n): ")
            if user_input.lower() == 'y':
                # Tải xuống file
                container_client = blob_service_client.get_container_client(container_name)
                blob_client = container_client.get_blob_client(file)
                with open(file, "wb") as f:
                    f.write(blob_client.download_blob().read())
                print("File đã được tải xuống thành công!")
                device_client= IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
                device_client.connect()
                message= "Da download firmware moi thanh cong"
                download_file_status = "OK"
                device_client.send_message(message)
                device_client.disconnect()
    else:
        print("No change on files")
    # Lưu trữ danh sách tên file hiện tại để so sánh trong lần kiểm tra tiếp theo
    previous_files = current_files
    return previous_files, download_file_status


   