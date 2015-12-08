import requests
import time
import json

from collections import defaultdict

room_id = 10
count = 10000

def get_first():
	url = 'http://chat.stackoverflow.com/chats/{}/events?mode=Messages&msgCount={}'.format(room_id, count)
	r = requests.post(url, data = 'fkey=faffe0a7618d1e8293fc71c9c47e80e9')

	return r.json()


def get_events(last):
	url = 'http://chat.stackoverflow.com/chats/{}/events?mode=Messages&msgCount={}&before={}'.format(room_id, count, last)
	r = requests.post(url, data = 'fkey=faffe0a7618d1e8293fc71c9c47e80e9')

	return r.json()


current = get_first()
current_id = current['events'][0]['message_id']

reference_map = defaultdict(lambda : defaultdict(int))

while current_id > 20271010:
	print (current_id)
	for event in current['events']:
		if 'content' not in event: 
			continue
		message_text = event['content']

		if message_text[0] == '@':
			author = event['user_name']
			refers_to = message_text.split(' ')[0][1:]
			reference_map[author][refers_to] += 1

	time.sleep(1)
	current = get_events(current_id)
	current_id = current['events'][0]['message_id']

print (json.dumps(reference_map))