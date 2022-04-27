from longthanhapi import driveapi

json_file_path = 'D:\API\code_secret_client.json'
api_name = 'drive'
api_version = 'v3'
scope = 'https://www.googleapis.com/auth/drive'

# Create service for gg drive api using.
services_var = driveapi(json_file_path, api_name, api_version, scope)
service = services_var.service_api()

# Create number folder with gg drive api.
number_folder = services_var.create_num_folder(service, 2,'hungdung')
print(number_folder)

# Create alone folder.
alone_folder = services_var.create_folder(service, 'huu trien')
print(alone_folder) 

# Create folder in folder parrents
folder_name = ['huu trien']
folder_in_parents = services_var.create_folder_in_folder(service, 1, alone_folder, folder_name)

# Upload image to gg drive
image_upload = services_var.upload_image('D:/API/background.png', service, 'anhnen.jpg', alone_folder)

# Get token access
token_access = services_var.token_access_get()
print(token_access)

# Check folder exist
check_code = services_var.check_exist_folder('huu trien', token_access)


