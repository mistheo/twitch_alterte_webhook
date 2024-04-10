import requests
import logging
from discord_webhook import DiscordWebhook
import time
import json
import sys

def load_config(filename='config.json'):
    with open(filename) as f:
        return json.load(f)

def get_stream_data(channel_name, token , client_id):
    url = f"https://api.twitch.tv/helix/streams?user_login={channel_name}"
    headers = {
        "Client-ID": client_id,
        "Authorization": ("Bearer "+ token)
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data['data']:
            return data['data'][0]
        return None
    
    except Exception as e:
        logging.error(f"Erreur twitch api pour la chaine {channel_name} : {str(e)}")
        return None

def send_discord_webhook(webhook_url, message):
    try:
        webhook = DiscordWebhook(url=webhook_url, content=message)
        response = webhook.execute()
        if response.status_code == 200:
            logging.info("Webhook envoyé avec succes.")
        else:
            logging.error(f"Echec de l'envoie du webhook. Code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending Discord webhook: {str(e)}")

def parse_message(msg,data):    
    msg = msg.replace("$~USER",data["user_name"])
    msg = msg.replace("$~PSEUDO",data["user_login"])
    msg = msg.replace("$~TITLE",data["title"])
    msg = msg.replace("$~GAME",data["game_name"])
    return msg

def main():
    try:
        print("sys.argv: ",sys.argv)
        
        if len(sys.argv) == 2:
            config = load_config(sys.argv[1])
        else :
            config = load_config()
        
        
        ch_name = config.get("channel_name")
        logging.basicConfig(filename=('logs/twitch_discord_' + ch_name + '.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        cli_id = config.get("client_id_twitch")
        token_oauth = config.get("token_oauth_twitch")
        webhook_url = config.get("discord_webhook_url")
        webhook_url_log = config.get("discord_webhook_url_for_log")
        raw_message = config.get("message")
        announced = False
        
        while True:
            stream_data = get_stream_data( ch_name, token_oauth , cli_id)
            print(stream_data)
            
            
            if stream_data and (announced == False):
                announced = True
                messageToSend = parse_message(raw_message,stream_data)
                send_discord_webhook(webhook_url, messageToSend)
                
                logging.info(f"Channel {ch_name} en Live. Discord Webhook envoyé. Annoncé: {announced}")
                send_discord_webhook(webhook_url_log,f"Channel {ch_name} en Live. Discord Webhook envoyé. Annoncé: {announced}")
            
            elif stream_data and announced == True: # 
                logging.info(f"Channel {ch_name} deja en Live. Annoncé: {announced}")
                send_discord_webhook(webhook_url_log,f"Channel {ch_name} deja en Live. Annoncé: {announced}")
            
            elif (not stream_data) and announced == True: # fin de live
                announced = False
            else:
                announced = False
                send_discord_webhook(webhook_url_log,f"Channel {ch_name} pas en live. {announced}")
            
            # Pause d'une minute avant de vérifier à nouveau
            time.sleep(60)
            
            
    except Exception as e:
        logging.error(f"une erreure est survenue: {str(e)}")
        send_discord_webhook(webhook_url_log,f"<@364802068894187531> une erreure est survenue: {str(e)}")

if __name__ == "__main__":
    main()
