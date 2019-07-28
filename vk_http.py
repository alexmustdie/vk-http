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

	def create_chat(self, user_ids, title):
		return self._create_chat_by_hash(user_ids, title, self._get_write_hash())

	def _get_create_chat_html(self):
		return self.session.get('https://vk.com/im?act=create')

	def _get_write_hash(self):
		return re.search(r'(?:"writeHash":")(.*?)(?:")', self._get_create_chat_html().text).group(1)

	def _create_chat_by_hash(self, user_ids, title, hash):
		result = self.session.post(
			'https://vk.com/al_im.php',
			data = {
				'al': 1,
				'im_v': 2,
				'hash': hash,
				'act': 'a_multi_start',
				'peers': ','.join(str(x) for x in user_ids),
				'title': title
			}
		).text
		return re.search(r'(?:"peerId":)(\d+)', result).group(1)

	def add_group_to_chat(self, chat_id, group_id):
		return self._invite_by_hash(chat_id, group_id, self._get_inviting_hash(group_id))

	def _get_inviting_html(self, group_id):
		return self.session.post(
			'https://vk.com/al_groups.php',
			data = {
				'al': 1,
				'act': 'a_search_chats_box',
				'group_id': group_id
			}
		)

	def _get_inviting_hash(self, group_id):
		return json.loads(re.sub(r'.*\n.*\n.*json>', '', self._get_inviting_html(group_id).text)).get('add_hash')

	def _invite_by_hash(self, chat_id, group_id, hash):
		return self.session.post(
			'https://vk.com/al_im.php',
			data = {
				'act': 'a_add_bots_to_chat',
				'al': 1,
				'add_hash': hash,
				'bot_id': -group_id,
				'peer_ids': chat_id
			}
		).text

	def toggle_admin(self, chat_id, group_id):

		chat_page = self.session.get('https://vk.com/im?sel=c%d' % (int(chat_id) - 2000000000)).text
		hash = re.search(r'(?:dialog&hash=)(.*?)(?:&)', chat_page).group(1)

		self.session.post(
			'https://vk.com/al_im.php',
			data = {
				'al': 1,
				'im_v': 2,
				'hash': hash,
				'act': 'a_toggle_admin',
				'is_admin': 1,
				'chat': chat_id,
				'mid': -group_id
			}
		)
