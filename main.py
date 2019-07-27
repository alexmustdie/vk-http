from vk_http import VkHttp

bot = VkHttp('login', 'password')
chat_id = bot.create_chat(user_ids=[187552130], title='test')
bot.add_group_to_chat(chat_id=chat_id, group_id=151378510)
