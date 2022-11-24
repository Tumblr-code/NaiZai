#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件  :   京东快递.py
@时间  :   2022/10/31 08:23:34
@作者  :   各位不知名大佬们和一名摸鱼小弟
@说明  :   基于Jbot机器人自动解析插件,仅供学习
@接口  :   本API解析接口自建,自建接口的不要外泄,自己偷用,有自建接口的自行替换API
@版本  :   v3
更新日志
2022/10/29 01:30:17 修复解析出错
2022/10/30 11:30:23 修复无法撤回问题
2022/10/31 08:23:34 补充相关域名解析
'''
# here put the import lib
# 引入库文件，基于telethon
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
# from .login import user
import time,re,requests,asyncio

jds = "http://api.nolanstore.top/JComExchange"   # 接口自建,自行替换
exchange_match = r'[\s\S]*([$%￥@！(#!][a-zA-Z0-9]{6,20}[$%￥@！)#!]|[㬌京亰倞兢婛景椋猄竞竟競竸綡鲸鶁][\u4e00-\u9fa5]{14,16}[东倲冻凍埬岽崠崬東栋棟涷菄諌鯟鶇]|(?:(?:[2-9]{2}[斤包袋箱]){1}[\u4e00-\u9fa5]{2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|(?:[\u4e00-\u9fa5]{4}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|(?:[\u4e00-\u9fa5]{4}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|[\u4e00-\u9fa5]{16}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[\u4e00-\u9fa5]{14}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[\u4e00-\u9fa5]{6}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[0-9A-Za-zα-ωА-Яа-яÀ-ž]{3}[\u4e00-\u9fa5]{2}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[0-9A-Za-zα-ωА-Яа-яÀ-ž]{2}[\u4e00-\u9fa5]{2}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1})'

@jdbot.on(events.NewMessage(pattern=exchange_match))
async def bot_jx(event):
    try:
        # 获取口令
        replytext=event.message.text 
    except ValueError:
        return await jdbot.send_message(event.chat_id, "获取回复信息失败")
    try:
        body = {
                "code": replytext,
            }      
        headers = {"Content-Type": "application/json"}
        res = requests.post(url=jds,headers=headers,json=body)
        data = res.json()

        data = data["data"]
        title = data["title"]
        jumpUrl = data["jumpUrl"]
        img = data["img"]

        activateId = re.findall("activityId=(.*?)&", jumpUrl)
        lz = re.findall("(.*?)/wxTeam", jumpUrl)
        wdz = re.findall("(.*?)/microDz", jumpUrl)
        actId = re.findall("actId=(.*?)&", jumpUrl)
        code = re.findall("code=(.*?)&", jumpUrl)
        active = re.findall("active/(.*?)/", jumpUrl)
        asid = re.findall("asid=(.*)", jumpUrl)
        shopid = re.findall("venderId=(.*)&", jumpUrl)
        activateId1 = re.findall("(.*?)&", jumpUrl)
        ## 热爱寻宝助力&组队
        ##inviteId = re.findall("inviteId=(.*)&mpin", jumpUrl) ##组队码
        ##inviteId_1 = re.findall("inviteId=(.*)&mpin", jumpUrl)  ##助力码
        ##inviteId_2 = re.findall("inviteId=(.*)&mpin", jumpUrl)  ##膨胀码
        ##大赢家助力码
        ##activeId = re.findall("&activeId=(.*?)&", jumpUrl)
        msg1 = f'【活动名称】: {title}\n【分享来自】: [京东快递](https://t.me/kuaidiyuanJD)\n【活动链接】: [跳转浏览器]({jumpUrl})\n【快捷跳转】: [跳转到京东](http://www.lolkda.top/?url={jumpUrl})'
        
        ## 正常脚本
        if re.findall("https://cjhydz-isv.isvjcloud.com/wxTeam/activity", jumpUrl):
            msg = f'【脚本类型】: CJ组队瓜分\n`export jd_cjhy_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxTeam/activity", jumpUrl):
            msg = f'【脚本类型】: CJ组队瓜分\n`export jd_cjhy_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxTeam/activity", jumpUrl):
            msg = f'【脚本类型】: LZ组队瓜分\n`export jd_zdjr_activityId="{activateId[0]}"`\n`export jd_zdjr_activityUrl="{lz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxTeam/activity", jumpUrl):
            msg = f'【脚本类型】: LZ组队瓜分\n`export jd_zdjr_activityId="{activateId[0]}"`\n`export jd_zdjr_activityUrl="{lz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index", jumpUrl):
            msg = f'【脚本类型】: KR微定制瓜分\n`export jd_wdz_activityId="{activateId[0]}"`\n`export jd_wdz_activityUrl="{wdz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxgame/activity", jumpUrl):
            msg = f'【脚本类型】: LZ店铺游戏\n`export jd_wxgame_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxShareActivity", jumpUrl):
            msg = f'【脚本类型】: KR分享有礼\n`export jd_wxShareActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjd.com/wxShareActivity/activity", jumpUrl):
            msg = f'【脚本类型】: KR分享有礼\n`export jd_wxShareActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxSecond/activity", jumpUrl):
            msg = f'【脚本类型】: KR读秒拼手速\n`export jd_wxSecond_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjd.com/wxSecond/activity", jumpUrl):
            msg = f'【脚本类型】: KR读秒拼手速\n`export jd_wxSecond_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://jinggengjcq-isv.isvjcloud.com/jdbeverage/pages", jumpUrl):
            msg = f'【脚本类型】: KR大牌联合开卡\n`export DPLHTY="{actId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCollectCard/activity", jumpUrl):
            msg = f'【脚本类型】: KR集卡抽奖\n`export jd_wxCollectCard_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/drawCenter/activity", jumpUrl):
            msg = f'【脚本类型】: LZ刮刮乐抽奖\n`export jd_drawCenter_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjd.com/drawCenter/activity", jumpUrl):
            msg = f'【脚本类型】: LZ刮刮乐抽奖\n`export jd_drawCenter_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxFansInterActionActivity/activity", jumpUrl):
            msg = f'【脚本类型】: 粉丝互动\n`export jd_wxFansInterActionActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://prodev.m.jd.com/mall/active", jumpUrl):
            msg = f'【脚本类型】: 邀好友赢大礼\n`export yhyactivityId="{active[0]}"`\n`export yhyauthorCode="{code[0]}"`\n`export jd_inv_authorCode="{code[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", jumpUrl):
            msg = f'【脚本类型】: LZ关注抽奖\n`export jd_wxShopFollowActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxUnPackingActivity/activity", jumpUrl):
            msg = f'【脚本类型】: 让福袋飞\n`export jd_wxUnPackingActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCartKoi/cartkoi/activity", jumpUrl):
            msg = f'【脚本类型】: 购物车锦鲤\n`export jd_wxCartKoi_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://happy.m.jd.com/babelDiy", jumpUrl):
            msg = f'【脚本类型】: 锦鲤红包\n\n锦鲤红包助力id=`{asid[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxInviteActivity/openCard/invitee", jumpUrl):
            msg = f'【脚本类型】: 入会开卡领取礼包\n`export VENDER_ID="{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxBuildActivity", jumpUrl):
            msg = f'【脚本类型】: LZ盖楼有礼\n`export jd_wxBuildActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回' ##新增

        elif re.findall("https://lzkj-isv.isvjd.com/wxCollectionActivity", jumpUrl):
            msg = f'【脚本类型】: LZ加购有礼\n`export jd_wxCollectionActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxCollectionActivity", jumpUrl):
            msg = f'【脚本类型】: CJ加购有礼\n`export jd_wxCollectionActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxKnowledgeActivity", jumpUrl):
            msg = f'【脚本类型】: CJ知识超人\n`export jd_wxKnowledgeActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxKnowledgeActivity", jumpUrl):
            msg = f'【脚本类型】: LZ知识超人\n`export jd_wxKnowledgeActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        
        elif re.findall("https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts", jumpUrl):
            msg = f'【脚本类型】: CJ店铺生日和等级礼包\n`export jd_wxMcLevelAndBirthGifts_activityId="{activateId[0]}"`\n`export jd_wxMcLevelAndBirthGifts_activityUrl="https://cjhydz-isv.isvjcloud.com"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxShopFollowActivity", jumpUrl):
            msg = f'【脚本类型】:  关注店铺\n`export jd_wxShopFollowActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", jumpUrl):
            msg = f'【脚本类型】:  关注店铺\n`export jd_wxShopFollowActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopGift", jumpUrl):
            msg = f'【脚本类型】:  店铺礼包特效\n`export jd_wxShopGift_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxShopGift", jumpUrl):
            msg = f'【脚本类型】:  店铺礼包特效\n`export jd_wxShopGift_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/lzclient", jumpUrl):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n`export LUCK_DRAW_URL="{activateId1[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxDrawActivity", jumpUrl):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n`export LUCK_DRAW_URL="{activateId1[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxDrawActivity", jumpUrl):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n`export LUCK_DRAW_URL="{activateId1[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/sevenDay", jumpUrl):
            msg = f'【脚本类型】:  超级无线店铺签到\n`export LZKJ_SEVENDAY="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/signActivity2", jumpUrl):
            msg = f'【脚本类型】:  超级无线店铺签到\n`export LZKJ_SIGN="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/sevenDay/signActivity", jumpUrl):
            msg = f'【脚本类型】:  超级无线店铺签到\n`export CJHY_SEVENDAY="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/signActivity", jumpUrl):
            msg = f'【脚本类型】:  超级无线店铺签到\n`export CJHY_SIGN="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view", jumpUrl):
            msg = f'【脚本类型】:  完善信息有礼\n`export jd_completeInfoActivity_activityId="{activateId[0]}"`\n`export jd_completeInfoActivity_activityUrl="https://cjhydz-isv.isvjcloud.com"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        ## 开卡解析
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity", jumpUrl):
            msg = f'【脚本类型】: 活动开卡\n`export jd_joinCommonId="{activateId[0]}&{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/aug/brandUnion/activity", jumpUrl):
            msg = f'【脚本类型】: 活动开卡\n`export jd_joinCommonId="{activateId[0]}&{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://hdb-isv.isvjcloud.com", jumpUrl):
            msg = f'【脚本类型】: 大牌联合\n【活动地址】:{data["jumpUrl"]}\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        ## 穿行寻宝
        ##elif re.findall("快加入我的队伍，躺赢赚红包~", data['title']):
            msg = f'【脚本类型】: 穿行寻宝组队\n穿行寻宝组队码\n`{inviteId[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        ##elif re.findall("快快点击，助我瓜分20亿红包吧！", data['title']):
            msg = f'【脚本类型】: 穿行寻宝助力\n穿行寻宝助力码\n`{inviteId_1[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        ##elif re.findall("帮我点一点，膨胀红包就差你的助力啦~", data['title']):
            msg = f'【脚本类型】: 穿行寻宝膨胀\n穿行寻宝膨胀码\n`{inviteId_2[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        ## 大赢家
        ##elif re.findall("我的小店开业大酬宾，帮我打卡涨人气！更有海量低价好物，新人享1分购噢！ ", data['title']):
            msg = f'【脚本类型】: 大赢家\n大赢家助力码\n`{activeId[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        ## 扭蛋
        elif re.findall("一起来玩超闪CP雀巢咖啡潮玩扭蛋机", data['title']):
            msg = f'【脚本类型】: 扭蛋机-手动玩游戏\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        else:
            msg = "【未适配变量】"
        if "脚本类型" in msg:
            msg_text = await jdbot.send_message(event.chat_id,msg1+"\n"+msg,file=f'{img}')
            await asyncio.sleep(60)
            await jdbot.delete_messages(event.chat_id,msg_text)
            await event.delete()


    except:
        msg = await jdbot.send_message(event.chat_id, f"呀呼，解析出错！\n请小八嘎重试几次")
        await asyncio.sleep(3)
        await msg.delete()