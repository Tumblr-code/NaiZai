from telethon import events
from .. import jdbot, chat_id, user
import re
import requests
import asyncio

@user.on(events.NewMessage(pattern=r'^(jx)$', outgoing=True))
async def jcmd(event):
    reply = await event.get_reply_message()
    if reply:
        msg_text = reply.text

        url = 'http://150.230.4.231:3500/api/JComExchange'
        payload = {'data':reply}
        data = requests.post(url,data=payload).json()

        code = data['code']
        if code == '0':
            data = data["data"]
            msg = f'【活动信息🏛】: {data["title"]}\n【口令发起人🐶】：{data["userName"]}\n【活动链接🔗】: {data["jumpUrl"]}'
            await user.send_message(event.chat_id,msg)