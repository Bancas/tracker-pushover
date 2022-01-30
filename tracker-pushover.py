import json
import typing
import http.client
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message

ggnPushToken = "<GGn Pushover App Token>"
ggnAPIToken = "<GGn API Token>"
redPushToken = "<RED Pushover App Token>"
redAPIToken = "<RED API Token>"
pushoverUser = "<Pushover User Token>"

class Response(typing.NamedTuple):
    body: str
    headers: Message
    status: int
    error_count: int = 0

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output

def requests(
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
    data_as_json: bool = True,
    error_count: int = 0,
) -> Response:
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body=str(e.reason),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response

def ggnAPI():

    # Free Leech Push
    ploads = {'x-api-key':ggnAPIToken}
    response = requests(url="https://gazellegames.net/api.php?request=items&type=users_buffs",headers=ploads)
    todos = json.loads(response.body)
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
    response = requests(url="https://gazellegames.net/api.php?request=inbox",headers=ploads)
    todos = json.loads(response.body)
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
    response = requests(url="https://gazellegames.net/api.php?request=quick_user",headers=ploads)
    todos = json.loads(response.body)
    userstats = todos['response']['userstats']
    with open('ggnstats.json', 'w') as outfile:
        json.dump(userstats, outfile)

def redAPI():

    # Unread Messages Push
    ploads = {'Authorization':redAPIToken}
    response = requests(url="https://redacted.ch/ajax.php?action=inbox",headers=ploads)
    todos = json.loads(response.body)
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
    response = requests(url="https://redacted.ch/ajax.php?action=forum&type=viewforum&forumid=35",headers=ploads)
    todos = json.loads(response.body)
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