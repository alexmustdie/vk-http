# vk-http

Мини-модуль, работающий с HTTP ВКонтакте и предназначенный для приглашения групп в беседы.

## Пример
```python
from vk_http import VkHttp
bot = VkHttp(login, password)
bot.add_group_to_chat(peer_id, group_id)
```
