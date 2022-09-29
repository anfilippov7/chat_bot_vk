import requests
from pprint import pprint

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {
           'user_ids': self.id,
           'fields' : 'sex, bdate, city'
       }
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def users_photos(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {
           # 'owner_id': "-" + self.id,
           'owner_id': self.id,
           'album_id' : 'profile',
           'rev' : 0,
           'extended' : 1,
           'photo_sizes' : 1
       }
       response = requests.get(url, params={**self.params, **params})
       return response.json()


   def get_list_photos(self, dict_photos, qty_photos):

       list_photos = []
       list_likes = []
       list_likes_max = []
       for item in range(qty_photos):
           like = int(dict_photos[item]['likes']['count'])
           list_likes.append(like)
       list_likes.sort()
       list_likes_max.append(list_likes[-1])
       list_likes_max.append(list_likes[-2])
       list_likes_max.append(list_likes[-3])

       like_3 = []
       for item in range(qty_photos):
         like = int(dict_photos[item]['likes']['count'])
         if like in list_likes_max and like not in like_3:
             file_name = str(dict_photos[item]['likes']['count']) + "_" + str(dict_photos[item]['date']) + ".jpg"
             type = dict_photos[item]['sizes'][-1]['type']
             url_photo = dict_photos[item]['sizes'][-1]['url']
             dict_photo = {}
             dict_photo["file_name"] = file_name
             dict_photo["size"] = type
             dict_photo["url"] = url_photo
             list_photos.append(dict_photo)
             like_3.append(like)
             print(f"Даем название фотографии {item + 1}")

       return list(list_photos)
