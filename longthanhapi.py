import pickle
import os
import requests
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

log_time = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

class driveapi:

    def __init__(self, PATHJSON, API, VER, SCOPE):
        self.__client_secret_file = PATHJSON
        self.__api_name = API
        self.__api_version = VER
        self.__scope = SCOPE
    
    def service_api(self):
        print(self.__scope)
        print(self.__client_secret_file, self.__api_name, self.__api_version, self.__scope)
        cred = None
        pickle_file = f'token_{self.__api_name}_{self.__api_version}.pickle'
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)
        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__client_secret_file, self.__scope)
                cred = flow.run_local_server()
            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
        try:
            service = build(self.__api_name, self.__api_version, credentials=cred)
            print(self.__api_name, 'service created successfully')
            print('{} | CREATED TOKEN PICKLE FILE'.format(log_time))
            return service
        except Exception as e:
            print('{} | Unable to connect.'.format(log_time))
            print(e)
            return None

    def create_num_folder(self, service_run, num, folder_name):
        ID = []
        for i in range(0, num):
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                }
            command_create_folder = service_run.files().create(body=file_metadata, fields='id').execute()
            print('{} | CREATED :) FOLDER ID {}: {}'.format(log_time, i, command_create_folder.get('id')))
            ID.append(command_create_folder.get('id'))
        return ID

    def create_folder(self, service_run, folder_name):
        ID = []
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            }
        command_create_folder = service_run.files().create(body=file_metadata, fields='id').execute()
        print('{} | CREATED :) FOLDER ID : {}'.format(log_time, command_create_folder.get('id')))
        ID.append(command_create_folder.get('id'))
        return ID

    def create_folder_in_folder(self, service, num_folder_parents, id_folder_parents, num_folder_name):
        ID = [] 
        for i in range(0, num_folder_parents): 
            for j in range(0, len(num_folder_name)):
                file_metadata = {
                    'name': num_folder_name[j],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [str(id_folder_parents[i])]
                    }
                command_create_folder = service.files().create(body=file_metadata, fields='id').execute()
                print('{} | CREATED :) {} FOLDER ID {}: {}'.format(log_time, num_folder_name[j] , j, command_create_folder.get('id')))
                ID.append(command_create_folder.get('id'))
        return ID

    def upload_image(self, service, name_image_format, path, id_parents): # upload for har and ppe. Just change id parrent folder. 
        file_metadata = {'name': name_image_format,
                        'parents': [str(id_parents)]
                        }
        media = MediaFileUpload(path, mimetype='image/jpeg')
        file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
        print('image id {}'.format(file.get('id')))
        ID = file.get('id')
        return ID

    def token_access_get(self):
        creds = None
        pickle_file = f'token_{self.__api_name}_{self.__api_version}.pickle'
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__client_secret_file, self.__scope)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        global service, access_token
        service = build('drive', 'v3', credentials=creds)
        access_token = creds.token
        print('{} | TOKEN ACCESS {}'.format(log_time, str(access_token)))
        return str(access_token)

    def check_exist_folder(self, folder_name, access_token):
        flag = 0
        url = 'https://www.googleapis.com/drive/v3/files'
        headers = {'Authorization': 'Bearer ' + access_token}
        query = {'q': "name='" + folder_name + "' and mimeType='application/vnd.google-apps.folder'"}
        response = requests.get(url, headers=headers, params=query)
        obj = response.json()
        if obj['files']:
            print('{} | CHECKED {} FOLDER EXISTING'.format(log_time, folder_name))
            flag = 1
        else:
            print('{} | CHECKED {} NOT EXISTING'.format(log_time, folder_name)) 
            flag = 0
        return flag
    


