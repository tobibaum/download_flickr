import os
import requests
from gdata.photos.service import PhotosService
from oauth2client.file import Storage
from googleapiclient.discovery import build


cred_file = 'tobi_credentials.secret'
storage = Storage(cred_file)

if not os.path.exists(cred_file):
    from oauth2client.client import flow_from_clientsecrets
    flow = flow_from_clientsecrets('client_secrets.json',
                                   scope='https://www.googleapis.com/auth/photoslibrary.appendonly',
                                   #scope='https://www.googleapis.com/auth/photoslibrary',
                                   redirect_uri='http://localhost:8080/google_callback')
    url = flow.step1_get_authorize_url()
    print 'visit:'
    print url
    from IPython import embed; embed(); raise
    creds = flow.step2_exchange(code=code)
    storage.put(creds)

def upload(creds, filename):
    f = open(filename, 'rb').read();

    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    headers = {
        'Authorization': "Bearer " + creds.access_token,
        'Content-Type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': filename,
        'X-Goog-Upload-Protocol': "raw",
    }

    r = requests.post(url, data=f, headers=headers)
    print '\nUpload token: %s' % r.content
    return r.content

creds = storage.get()
service = build('photoslibrary', 'v1', credentials=creds)
#albums = service.albums().list().execute()
#album_id = filter(lambda x: x['title']=='flickr upload', albums['albums'])[0]['id']
album_id = 'AJeFRi1D0GKydfCXvz-DXNUg8dw9jx4FdWhsDovuvChABhj_PV8uVwcIxxOfzuMQJ_NeNYgftQXI'

upload_token = upload(creds, 'puppy.jpg')

from IPython import embed; embed(); raise
upload_dict = 
service.mediaItems().batchCreate(body=dict(
        #albumId=album_id,
        newMediaItems=[
            {"simpleMediaItem": {"uploadToken": upload_token}}]
    )).execute()

from IPython import embed; embed(); raise
