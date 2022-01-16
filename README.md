# Private Tracker Pushover Notifications
Sends Pushover notifications for various user events on private trackers.

Currently works with GGn and RED.

# Run Command
```
docker run --rm \
--name tracker-pushover \
-e GGN_PUSH_TOKEN=<GGn Pushover App Token> \
-e GGN_API_TOKEN=<GGn API Token> \
-e RED_PUSH_TOKEN=<RED Pushover App Token> \
-e RED_API_TOKEN=<RED API Token> \
-e PUSHOVER_USER=<Pushover User Token> \
bancas/tracker-pushover
```

# GitHub
https://github.com/Bancas/tracker-pushover
