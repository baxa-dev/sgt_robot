import json
# from django.conf import settings
from asgiref.sync import sync_to_async
from config import settings


@sync_to_async
class Data:
    def __init__(self, user_id, path):
        self.user_id = user_id
        self.filepath = settings.BASE_DIR/'bot_client/data.json'
        self.path = path

    @property
    def data_load(self):
        with open(self.filepath) as file:
            return json.load(file)

    def write_json(self, basket):
        with open(self.filepath, 'w+') as file:
            json.dump(basket, file, ensure_ascii=False)

    def create_path(self):
        basket = self.data_load
        data = {"path": {"user_id": self.user_id, "product_path": self.path}}
        if len(basket) < 1:
            basket.append(data)
            self.write_json(basket=basket)
            return data
        else:
            for i in range(len(basket)):
                if basket[i].get("path").get("user_id") == self.user_id:
                    if self.path.split(sep='/')[-2] == "catalog":
                        print(self.path)
                        basket[i]['path']['product_path'] = self.path
                        self.write_json(basket=basket)
                    else:
                        print(self.path)
                        basket[i]['path']['product_path'] = basket[i]['path']['product_path'] + self.path
                        self.write_json(basket=basket)
                    return basket[i]
                elif i == len(basket)-1:
                    basket.append(data)
                    self.write_json(basket=basket)
                    return data

    def get_path(self):
        basket = self.data_load
        print(type(basket), basket)
        for i in basket:
            print(len(basket), basket)
            print(i.get("path").get('user_id'))
            if i.get("path").get('user_id') == self.user_id:
                print("I entered to condition")
                print(type(i["path"]['product_path']), i["path"]['product_path'])
                return i["path"]['product_path']

    def delete(self):
        basket = self.data_load
        for i in range(len(basket)):
            if basket[i].get("path").get('user_id') == self.user_id:
                basket[i]['path']['product_path'] = basket[i]['path']['product_path'].replace(basket[i]['path']['product_path'].split(sep='/')[-2], "")
                basket[i]['path']['product_path'] = basket[i]['path']['product_path'][:-1]
                self.write_json(basket=basket)
                break

