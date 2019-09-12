import json
import pyrebase
import re
import requests
import random

try:
    from urllib.parse import urlencode, quote
except:
    from urllib import urlencode, quote

from pymitter import EventEmitter

class PyrebaseDatabase(object):
    def __init__(self):
        with open('./data/pyrebase_config.json') as f:
            self.config = json.load(f)
        with open('./data/database_paths_config.json') as f:
            self.paths_config = json.load(f)

        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
        self.token = self.auth.create_custom_token("pjchardt")
        self.auth_user()
        self.node_root = self.paths_config['node_root']
        self.node_path = "{0}/{1}".format(self.paths_config['node_root'], self.paths_config['node'])

    def auth_user(self):
        try:
            self.user = self.auth.sign_in_with_custom_token(self.token)
        except requests.exceptions.ConnectionError as conn_err:
            print("failed to auth user, trying again")
            self.auth_user()

    def reauth_user(self, image_path, image_data):
        self.user = self.auth.refresh(self.user['refreshToken'])
        self.send_image(image_path, image_data)

    def get_indexes(self):
        return self.db.child(self.node_root).child(self.paths_config['index']).get().val(), self.db.child(self.node_root).child(self.paths_config['max_index']).get().val()

    def download_image(self, content_path): #we should pass in the node we are using, i.e. camera_node_<x>
        index, url = self.get_url()
        if url is None:
            #we should remove this node as it is invalid, but then we have an issue with a 'hole' in the class
            print ("{0}{1}".format("Url was none at index: ", index))
            return False, None
        result = self.get_image(url, content_path)
        if result is False:
            return False, None
        return True, url

    def get_url(self):
        total_url_index = self.db.child(self.paths_config['content_image']).child("total_url_index").get().val()
        #Note: As coded we randomly grab an image, should we change to walk through images? If so, do we randomly pick a plac eto start? or save our last spot to a file?
        index = random.randint(0,total_url_index)
        random_url = "{0}{1}".format("url_", index)
        url = self.db.child(self.paths_config['content_image']).child(random_url).get().val()
        return index, url

    def get_image(self, url, content_path):
        print ("{0}{1}".format("downloading image from url: ", url))
        image = requests.get(url)
        if image is not None:
            with open(content_path, 'wb') as f:
                f.write(image.content)
            return True
        else:
            print ("failed to download image. will try again")
            return False

    def push_data(self, image_path, image_data):
        index, max_index = self.get_indexes()
        storage_path = "{0}{1}.jpg".format(self.paths_config['storage_path'], index)
        try:
            result = self.storage.child(storage_path).put(image_path, self.user['idToken'])
        except requests.exceptions.HTTPError:
            print("storage put failed with HTTPError, calling reauth_user to try and resolve")
            reauth_user(image_path, image_data)

        #get url for downloading image
        firebase_url = "https://firebasestorage.googleapis.com/v0/b/"
        storage_bucket = self.config["storageBucket"]
        token = result['downloadTokens']
        url = "{0}{1}/o/{2}?alt=media&token={3}".format(firebase_url, storage_bucket, quote(storage_path, safe=''), token)
        print ("Image sent. url = " + url)

        self.db.child(self.node_path).child(index).update({"url" : url});
        self.db.child(self.node_path).child(index).update({"image_data" : image_data})
        index = (index + 1) % max_index
        self.db.child(self.node_root).update({self.paths_config['index'] : index })
