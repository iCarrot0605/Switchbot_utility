import requests
import json
from switchbot.switchbot import Switchbot

class SwitchbotWebhook(Switchbot):
    def __init__(self):
        super().__init__()

    """Switchbot Webhook action"""
    def setup_webhook(self, url):
        """Setup Webhook"""
        header = self.gen_sign()
        # token, secret = self.read_token()
        # header = {"Content-type": "application/json"}
        # header['Authorization'] = token
        body = {"action": "setupWebhook",
                "deviceList": "ALL"}
        body['url'] = url
        posturl = 'https://api.switch-bot.com/v1.1/webhook/setupWebhook'
        response = requests.post(posturl, headers=header, data=json.dumps(body))
        return response.text

    def query_url(self):
        """Get webhook configuration"""
        header = self.gen_sign()
        body = {"action": "queryUrl"}
        posturl = 'https://api.switch-bot.com/v1.1/webhook/queryWebhook'
        response = requests.post(posturl, headers=header, data=json.dumps(body))
        return response.text
    
    def query_details(self, url):
        """Get webhook detail configurations"""
        header = self.gen_sign()
        body = {"action": "queryDetails"}
        body['urls'] = url
        posturl = 'https://api.switch-bot.com/v1.1/webhook/queryWebhook'
        response = requests.post(posturl, headers=header, data=json.dumps(body))
        return response.text

    def update_webhook(self, url):
        """Update webhook url"""
        header = self.gen_sign()
        body = {"action": "updateWebhook"}
        body['urls'] = url
        posturl = 'https://api.switch-bot.com/v1.1/webhook/queryWebhook'
        response = requests.post(posturl, headers=header, data=json.dumps(body))
        return response.text
    
    def delete_webhook(self, url):
        """Delete webhook"""
        header = self.gen_sign()
        body = {"action": "deleteWebhook"}
        body['url'] = url
        posturl = 'https://api.switch-bot.com/v1.1/webhook/deleteWebhook'
        response = requests.post(posturl, headers=header, data=json.dumps(body))
        return response.text