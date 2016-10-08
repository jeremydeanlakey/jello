import requests
import json


class Client(object):
    def __init__(self, api_key, token):
        self._api_key = api_key
        self._token = token
    def boards(self):
        raise NotImplemented
    def board(self, board_id):
        return Board(self, board_id)
    def card(self, card_id):
        return Card(self, card_id)
    def list(self, list_id):
        return List(self, list_id)


class Board(object):
    def __init__(self, client, id):
        self._client = client
        self.id = id


class List(object):
    def __init__(self, client, id):
        self._client = client
        self.id = id
    def new_card(self, name='', desc='', pos='top'):
        data = {
            'name': name,
            'idList': self.id,
            'desc': desc,
            'pos': pos,
            'key': self._client._api_key,
            'token': self._client._token
        }
        resp = requests.post("https://trello.com/1/cards", params=data)
        card_data = json.loads(resp.text)
        card_id = card_data['id']
        return Card(self._client, card_id, card_data)


class Card(object):
    def __init__(self, client, card_id, data=None):
        self._client = client
        self.id = card_id
        if not data:
            key = client._api_key
            token = client._token
            resp = requests.get("https://trello.com/1/cards/{}?token={}&key={}".format(card_id, token, key))
            data = json.loads(resp.text)
        self._data = data
        self.name = data['name']
        self.desc = data['desc']
        self.idList = data['idList']
    def reload(self):
        raise NotImplemented
    def save(self):
        self._data['name'] = self.name
        self._data['desc'] = self.desc
        self._data['idList'] = self.idList
        data = self._data.copy()
        put_keys = ['name', 'desc', 'idMembers', 'idAttachmentCover', 'idList', 'idBoard', 'pos', 'due', 'subscribed'] #'closed', 
        for k in data.keys():
            if k not in put_keys:
                del data[k]
        data['key'] = self._client._api_key
        data['token'] = self._client._token
        resp = requests.put("https://trello.com/1/cards/{}".format(self.id), params=data)
        return resp


