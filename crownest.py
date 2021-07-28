import requests
import json
import requests
from discord import Webhook, RequestsWebhookAdapter
import yaml


class Crownest:
    """
    Crow's nest!
    just go to yaml file fill it up and run.
    will do gui or something else later
    """

    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as fp:
            conf = yaml.safe_load(fp)
            self.conf = conf
        print(self.conf)

        if (line_token := conf['setting'].get('line_token')) is not None:
            self.line_token = line_token
            self.line_alert = True

        if (discord_hook := conf['setting'].get('discord_hook')) is not None:
            self.discord_hook = discord_hook
            self.discord_alert = True

        self.notify_new_collection = conf.get('notify_new_collection')
        self.notify_new_NFT = conf.get('notify_new_NFT')
        self.notify_new_offer = conf.get('notify_new_offer')
        self.notify_new_transaction = conf.get('notify_new_transaction')
        self.notify_early_alert = conf.get('notify_early_alert')

        self.wallet_list = conf['track'].get('wallet', [])
        self.collection_list = conf['track'].get('collection', [])
        self.nfts_list = conf['track'].get('nfts', [])

        self.wallet_history = {}
        self.asset_history = {}
        self.key_time = []

    def add_target_wallet(self, wallet_address):
        self.wallet_list.append(wallet_address)

    def add_tract_collection(self, collection):
        self.collection_list.append(collection)

    def add_tract_NFTs(self, nft_id):
        self.nfts_list.append(nft_id)

    def run(self):

        for wallet_address in self.wallet_list:
            cols = self.get_collection(wallet_address)
            for col in cols:
                col_data = self.extract_collection_data(col)
                pass # todo: do something

        for collection in self.collection_list:
            nfts = self.get_asset_collection(collection)
            for nft in nfts:
                nft_data = self.extract_nft_data(nft)
                pass  # todo: do something

        for nft_id in self.nfts_list:
            nfts = self.get_asset_collection(nft_id)
            for nft in nfts:
                nft_data = self.extract_nft_data(nft)
                pass  # todo: do something

        self.backup()

    def backup(self):
        # todo implement
        pass

    def discord_hook(self, message):
        webhook = Webhook.from_url(self.discord_hook, adapter=RequestsWebhookAdapter())
        webhook.send(message)

    def line_hook(self, message):
        url = 'https://notify-api.line.me/api/notify'
        token = self.line_token
        headers = {
            'content-type':
                'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + token
        }
        r = requests.post(url, headers=headers, data={'message': message})

    @staticmethod
    def extract_collection_data(data):
        pass

    @staticmethod
    def extract_nft_data(data):
        pass

    @staticmethod
    def get_collection(owner):
        tmp = json.loads(
            requests.get(f'https://api.opensea.io/api/v1/collections?offset=0&limit=300&asset_owner={owner}').text)
        return tmp

    @staticmethod
    def get_asset_collection(collection):
        tmp = json.loads(
            requests.get(
                f'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=50&collection={collection}').text)
        return tmp['assets']

    @staticmethod
    def get_asset_id(id):
        tmp = json.loads(
            requests.get(
                f'https://api.opensea.io/api/v1/assets?token_ids={id}').text)
        return tmp['assets']


crownest = Crownest('sample_conf.yaml')
crownest.run()
