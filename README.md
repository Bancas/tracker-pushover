# Private Tracker Pushover Notifications
Sends Pushover notifications for various events on private torrent trackers.

## Current use cases:
GGn: 
    - Sitewide Free Leech Notification
    - Unread Message Notification
    - Downloads User Stats JSON
RED: 
    - Unread Message Notification
    - New Unread Official Invite Thread Notification

## Configuration
Replace the API tokens in tracker-pushover.py before running.
```
ggnPushToken = "<GGn Pushover App Token>"
ggnAPIToken = "<GGn API Token>"
redPushToken = "<RED Pushover App Token>"
redAPIToken = "<RED API Token>"
pushoverUser = "<Pushover User Token>"
```

## Run Command
```
python3 tracker-pushover.py
```
