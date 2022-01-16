import requests
import json
import http.client
import urllib
import os

ggnPushToken = os.environ.get('GGN_PUSH_TOKEN')
ggnAPIToken = os.environ.get('GGN_API_TOKEN')
redPushToken = os.environ.get('RED_PUSH_TOKEN')
redAPIToken = os.environ.get('RED_API_TOKEN')
pushoverUser = os.environ.get('PUSHOVER_USER')

def ggnAPI():

    # Free Leech Push
    ploads = {'x-api-key':ggnAPIToken}
    response = requests.get("https://gazellegames.net/api.php?request=items&type=users_buffs",headers=ploads)
    todos = json.loads(response.text)
    download = todos['response']['Download']

    if(download == 0):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": ggnPushToken,
                "user": pushoverUser,
                "message": "GGn Free Leech!",
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

    # Unread Messages Push
    ploads = {'x-api-key':ggnAPIToken}
    response = requests.get("https://gazellegames.net/api.php?request=inbox",headers=ploads)
    todos = json.loads(response.text)
    messages = todos['response']['messages']

    for message in messages:
        unread = message['unread']
        if(unread == True):
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urllib.parse.urlencode({
                    "token": ggnPushToken,
                    "user": pushoverUser,
                    "message": message['subject'],
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

    # User Stats JSON
    ploads = {'x-api-key':ggnAPIToken}
    response = requests.get("https://gazellegames.net/api.php?request=quick_user",headers=ploads)
    todos = json.loads(response.text)
    userstats = todos['response']['userstats']
    with open('ggnstats.json', 'w') as outfile:
        json.dump(userstats, outfile)

def redAPI():

    # Unread Messages Push
    ploads = {'Authorization':redAPIToken}
    response = requests.get("https://redacted.ch/ajax.php?action=inbox",headers=ploads)
    todos = json.loads(response.text)
    messages = todos['response']['messages']
    
    for message in messages:
        unread = message['unread']
        if(unread == True):
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urllib.parse.urlencode({
                    "token": redPushToken,
                    "user": pushoverUser,
                    "message": message['subject'],
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

    # New Invite Thread Push
    ploads = {'Authorization':redAPIToken}
    response = requests.get("https://redacted.ch/ajax.php?action=forum&type=viewforum&forumid=35",headers=ploads)
    todos = json.loads(response.text)
    threads = todos['response']['threads']

    for thread in threads:
        read = thread['read']
        locked = thread['locked']

        if(read == False and locked == True):
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urllib.parse.urlencode({
                    "token": redPushToken,
                    "user": pushoverUser,
                    "subject": "New Official Invite Thread",
                    "message": thread['title'],
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

if __name__ == "__main__":
    ggnAPI()
    redAPI()
