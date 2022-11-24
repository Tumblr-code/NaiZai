# 引入库文件，基于telethon
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import jdbot, chat_id,logger
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
from .login import user
import time,re,requests,asyncio,random
from urllib.parse import unquote
##监听通用转发
@user.on(events.NewMessage(chats=频道id,pattern=r'[\s\S]*关键词'))  #改频道id 关键词
async def gua(event):
    try:
        # 获取全文
        gua_text = event.raw_text
        logger.info(gua_text)
        # 随机沉睡
        await asyncio.sleep(random.randint(30,60))  ##随机延迟60秒
        msg = await user.send_message(群组id,event.message)  #群组输出 改
        # msg1 = await user.send_message(-xxxxxxx,f'{variable}') # xxxxx自己修改想多输出的群组或者频道id
        await asyncio.sleep(30) ##自动撤回
        await msg.delete()
    except Exception as e:
        logger.info(f'错误：\n{e}')
