# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2022/04/09 21:27
# @author  : xiaomi
# @desc    :tg机器人上传代码到git
# 依赖：
#pip install gitpython
#pip install retrying
#pip install pysocks
#
from git import Repo
#from turtle import update
import requests
import time,os, json,logging
from retrying import retry
requests.packages.urllib3.disable_warnings()


#botToken
botToken="5746829332:AAH7NVxSQP-uTiVdUno92KfMSFSDlOmMHI8"
#要监听的群组id
listem_id= -1001676996661
#代理地址  
proxies={
    #不需要代理禁用这两行
    #'http': "http://127.0.0.1:7890",
    #'https': "http://127.0.0.1:7890"
}
#基本设置，可以替代注释里的配置项
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)   #创建logger对象
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("bot.log")   #创建handler对象，保存文件
handler.setLevel(logging.INFO)
log_format = '[%(levelname)s TIME:%(asctime)s] %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

updateId = None
s = requests.session()
s.keep_alive = False

def getUpdates(offset):
    global updateId
    if (offset):
        url = "https://api.telegram.org/bot"+botToken+"/getUpdates?offset="+str(offset)
    else:
        url = "https://api.telegram.org/bot"+botToken+"/getUpdates"
    response = requests.request("GET", url, data=None, headers=None,proxies=proxies,verify=False)
    resultStr = response.text
    result = json.loads(resultStr)
    if (result["ok"]==True):
        messages = result["result"]
        for message in messages:
            if(("message" in message)==False):
                updateId = message["update_id"]+1
                break
            chat_id = message["message"]["chat"]["id"]
            if (message["message"]["chat"]["id"]==listem_id):
                if("document" in message["message"]):
                    file_name = message["message"]["document"]["file_name"]
                    downFile(message["message"]["document"]["file_id"],file_name,chat_id)
                else:
                    if("text" in message["message"]):
                        text = message["message"]["text"]
                        logger.info(message["message"]["chat"]["title"]+"("+str(message["message"]["chat"]["id"])+")消息："+text)
                        if("删除 " in text):
                            fileName = text.replace("删除 ","")
                            sendMsg(chat_id,"开始删除: "+fileName)
                            try:
                                os.unlink(fileName)
                            except:
                                sendMsg(chat_id,"本地文件不存在")
                            if(pushFile()):
                                sendMsg(chat_id,fileName+"没水了，已停止并删除!")
                            else:
                                sendMsg(chat_id,fileName+"删除失败,网络异常")
                updateId = message["update_id"]+1


def downFile(fileId,file_name,chat_id):
    sendMsg(chat_id,"又有开卡了,爽歪歪,上传服务器中:"+file_name)
    fileIdUrl = "https://api.telegram.org/bot"+botToken+"/getFile?file_id="+fileId
    response = requests.request("GET", fileIdUrl, data=None, headers=None,proxies=proxies,verify=False)
    resultStr = response.text
    result = json.loads(resultStr)
    if (result["ok"]==True):
        filePath = result["result"]["file_path"]
        filePathUrl = "https://api.telegram.org/file/bot"+botToken+"/"+filePath
        down_res = requests.request("GET", filePathUrl, data=None, headers=None,proxies=proxies,verify=False)
        with open(file_name,"wb") as code:
            b = code.write(down_res.content)
            logger.info(b)

        logger.info("文件准备完成:"+file_name)
        pushResult = pushFile()
        if(pushResult):
            sendMsg(chat_id,file_name+"文件已准备好，已开启并发模式!")
            return
        sendMsg(chat_id,file_name+"上传失败,网络异常")

def pushFile():
    dirfile = os.path.abspath('') # code的文件位置，我默认将其存放在根目录下
    repo = Repo(dirfile)
    g = repo.git
    g.pull()
    g.add("--all")
    try:
        g.commit("-m auto update")
    except:
        logger.info("没有任何改变,无须更新")
        return True

    try:
        push(g)
        return True
    except:
        logger.info("上传失败")
        return False

@retry()
def push(git):
    logger.info("git push")
    git.push()

def sendMsg(chat_id,text):
    url = "https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(chat_id)+"&text="+text
    response = requests.request("GET", url, data=None, headers=None,proxies=proxies,verify=False)
    resultStr = response.text
if __name__ == '__main__':
    logger.info('启动成功，开始监听群消息')
    while True:
        try:
            getUpdates(updateId)
        except:
            logger.info("网络异常")
        time.sleep(3)
