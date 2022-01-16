FROM python:slim

WORKDIR /usr/src/app/

RUN pip install requests

ENV GGN_PUSH_TOKEN = **None** \
	GGN_API_TOKEN = **None** \
	RED_PUSH_TOKEN = **None** \
	RED_API_TOKEN = **None** \
	PUSHOVER_USER = **None**

COPY . .

CMD [ "python", "./tracker-pushover.py" ]