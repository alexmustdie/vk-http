
import re
import requests
import json

class VkHttp:
	def __init__(self, login, password):
		self.session = requests.Session()
		self._auth(login, password)

	def _auth(self, login, password):
		page = self.session.get('https://vk.com')

		action_url = re.search(
			r'https://login\.vk\.com/\?act=login&_origin=https://m\.vk\.com&ip_h=.*&lg_h=.*&role=pda&utf8=1',
			page.text
		).group()

		self.session.post(
			action_url,
			data = {'email': login, 'pass': password}
		)

	def add_group_to_chat(self, peer_id, group_id):
		return self._invite_by_hash(peer_id, group_id, self._get_inviting_hash(group_id))

	def _get_inviting_html(self, group_id):
		return self.session.post(
			'https://vk.com/al_groups.php',
			data = {
				'act': 'a_search_chats_box',
				'al': 1,
				'group_id': group_id
			}
		)

	def _get_inviting_hash(self, group_id):
		return json.loads(re.sub(r'.*\n.*\n.*json>', '', self._get_inviting_html(group_id).text)).get('add_hash')

	def _invite_by_hash(self, peer_id, group_id, hash):
		return self.session.post(
			'https://vk.com/al_im.php',
			data = {
				'act': 'a_add_bots_to_chat',
				'al': 1,
				'add_hash': hash,
				'bot_id': -group_id,
				'peer_ids': peer_id
			}
		).text