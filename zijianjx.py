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

jds = "xxxx"   # 接口自建,自行替换
exchange_match = r'[\s\S]*([$%￥@！(#!][a-zA-Z0-9]{6,20}[$%￥@！)#!]|[㬌京亰倞兢婛景椋猄竞竟競竸綡鲸鶁][\u4e00-\u9fa5]{14,16}[东倲冻凍埬岽崠崬東栋棟涷菄諌鯟鶇]|(?:(?:[2-9]{2}[斤包袋箱]){1}[\u4e00-\u9fa5]{2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|(?:[\u4e00-\u9fa5]{4}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|(?:[\u4e00-\u9fa5]{4}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}){3}|[\u4e00-\u9fa5]{16}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[\u4e00-\u9fa5]{14}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[\u4e00-\u9fa5]{6}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[0-9A-Za-zα-ωА-Яа-яÀ-ž]{3}[\u4e00-\u9fa5]{2}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1}|(?:[\u2602-\u27be\U0001f400-\U0001f6fa]{1}[0-9A-Za-zα-ωА-Яа-яÀ-ž]{2}[\u4e00-\u9fa5]{2}){2}[\u2602-\u27be\U0001f400-\U0001f6fa]{1})'

@jdbot.on(events.NewMessage(pattern=exchange_match))
async def bot_jx(event):
    try:
        # 获取口令
        replytext=event.message.text       
    except ValueError:
        return await jdbot.send_message(event.chat_id, "获取回复信息失败")
    try:
        headers = {'content-type':'application/x-www-form-urlencoded;charset=utf-8;'}
        res = requests.post(url=jds,headers=headers,data={"key": replytext})
        data = res.json()

        data = data["data"]
        title = data["title"]
        jump_url = data["jumpUrl"]
        activateId = re.findall("activityId=(.*?)&", data['jumpUrl'])
        lz = re.findall("(.*?)/wxTeam", data['jumpUrl'])
        wdz = re.findall("(.*?)/microDz", data['jumpUrl'])
        actId = re.findall("actId=(.*?)&", data['jumpUrl'])
        code = re.findall("code=(.*?)&", data['jumpUrl'])
        active = re.findall("active/(.*?)/", data['jumpUrl'])
        asid = re.findall("asid=(.*)", data['jumpUrl'])
        shopid = re.findall("venderId=(.*)&", data['jumpUrl'])
        ## 热爱寻宝助力&组队
        ##inviteId = re.findall("inviteId=(.*)&mpin", data['jumpUrl']) ##组队码
        ##inviteId_1 = re.findall("inviteId=(.*)&mpin", data['jumpUrl'])  ##助力码
        ##inviteId_2 = re.findall("inviteId=(.*)&mpin", data['jumpUrl'])  ##膨胀码
        result = f'【活动名称】: {data["title"]}\n【分享来自】: [京东快递](https://t.me/kuaidiyuanJD)\n【活动链接】: [跳转浏览器]({data["jumpUrl"]})\n【快捷跳转】: [跳转到京东](http://www.lolkda.top/?url={data["jumpUrl"]})'

        ## 正常脚本
        if re.findall("https://cjhydz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: CJ组队瓜分\n【活动变量】:`export jd_cjhy_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: CJ组队瓜分\n【活动变量】:`export jd_cjhy_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ组队瓜分\n【活动变量】:`export jd_zdjr_activityId="{activateId[0]}"`\n`export jd_zdjr_activityUrl="{lz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ组队瓜分\n【活动变量】:`export jd_zdjr_activityId="{activateId[0]}"`\n`export jd_zdjr_activityUrl="{lz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index", data['jumpUrl']):
            msg = f'【脚本类型】: KR微定制瓜分\n【活动变量】:`export jd_wdz_activityId="{activateId[0]}"`\n`export jd_wdz_activityUrl="{wdz[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxgame/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ店铺游戏\n【活动变量】:`export jd_wxgame_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxShareActivity", data['jumpUrl']):
            msg = f'【脚本类型】: KR分享有礼\n【活动变量】:`export jd_wxShareActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjd.com/wxShareActivity/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR分享有礼\n【活动变量】:`export jd_wxShareActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxSecond/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR读秒拼手速\n【活动变量】:`export jd_wxSecond_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkjdz-isv.isvjd.com/wxSecond/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR读秒拼手速\n【活动变量】:`export jd_wxSecond_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://jinggengjcq-isv.isvjcloud.com/jdbeverage/pages", data['jumpUrl']):
            msg = f'【脚本类型】: KR大牌联合开卡\n【活动变量】:`export DPLHTY="{actId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCollectCard/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR集卡抽奖\n【活动变量】:`export jd_wxCollectCard_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/drawCenter/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ刮刮乐抽奖\n【活动变量】:`export jd_drawCenter_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjd.com/drawCenter/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ刮刮乐抽奖\n【活动变量】:`export jd_drawCenter_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxFansInterActionActivity/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 粉丝互动\n【活动变量】:`export jd_wxFansInterActionActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://prodev.m.jd.com/mall/active", data['jumpUrl']):
            msg = f'【脚本类型】: 邀好友赢大礼\n【活动变量】:`export yhyactivityId="{active[0]}"`\n`export yhyauthorCode="{code[0]}"`\n`export jd_inv_authorCode="{code[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ关注抽奖\n【活动变量】:`export jd_wxShopFollowActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxUnPackingActivity/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 让福袋飞\n【活动变量】:`export jd_wxUnPackingActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCartKoi/cartkoi/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 购物车锦鲤\n【活动变量】:`export jd_wxCartKoi_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://happy.m.jd.com/babelDiy", data['jumpUrl']):
            msg = f'【脚本类型】: 锦鲤红包\n【活动变量】:\n锦鲤红包助力id=`{asid[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxInviteActivity/openCard/invitee", data['jumpUrl']):
            msg = f'【脚本类型】: 入会开卡领取礼包\n【活动变量】:`export VENDER_ID="{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxBuildActivity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ盖楼有礼\n【活动变量】:`export jd_wxBuildActivity_activityId="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回' ##新增

        elif re.findall("https://lzkj-isv.isvjd.com/wxCollectionActivity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ加购有礼\n【活动变量】:`export jd_wxCollectionActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxCollectionActivity", data['jumpUrl']):
            msg = f'【脚本类型】: CJ加购有礼\n【活动变量】:`export jd_wxCollectionActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxKnowledgeActivity", data['jumpUrl']):
            msg = f'【脚本类型】: CJ知识超人\n【活动变量】:`export jd_wxKnowledgeActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxKnowledgeActivity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ知识超人\n【活动变量】:`export jd_wxKnowledgeActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        
        elif re.findall("https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts", data['jumpUrl']):
            msg = f'【脚本类型】: CJ店铺生日和等级礼包\n【活动变量】:`export jd_wxMcLevelAndBirthGifts_activityId="{activateId[0]}"`\n`export jd_wxMcLevelAndBirthGifts_activityUrl="https://cjhydz-isv.isvjcloud.com"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxShopFollowActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  关注店铺\n【活动变量】:`export jd_wxShopFollowActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  关注店铺\n【活动变量】:`export jd_wxShopFollowActivity_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopGift", data['jumpUrl']):
            msg = f'【脚本类型】:  店铺礼包特效\n【活动变量】:`export jd_wxShopGift_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxShopGift", data['jumpUrl']):
            msg = f'【脚本类型】:  店铺礼包特效\n【活动变量】:`export jd_wxShopGift_activityUrl="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/lzclient", data['jumpUrl']):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n【活动变量】:`export LUCK_DRAW_URL="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxDrawActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n【活动变量】:`export LUCK_DRAW_URL="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wxDrawActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  店铺抽奖 · 超级无线\n【活动变量】:`export LUCK_DRAW_URL="{data["jumpUrl"]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/sevenDay", data['jumpUrl']):
            msg = f'【脚本类型】:  超级无线店铺签到\n【活动变量】:`export LZKJ_SEVENDAY="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/signActivity2", data['jumpUrl']):
            msg = f'【脚本类型】:  超级无线店铺签到\n【活动变量】:`export LZKJ_SIGN="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/sevenDay/signActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  超级无线店铺签到\n【活动变量】:`export CJHY_SEVENDAY="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/signActivity", data['jumpUrl']):
            msg = f'【脚本类型】:  超级无线店铺签到\n【活动变量】:`export CJHY_SIGN="{activateId[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view", data['jumpUrl']):
            msg = f'【脚本类型】:  完善信息有礼\n【活动变量】:`export jd_completeInfoActivity_activityId="{activateId[0]}"`\n`export jd_completeInfoActivity_activityUrl="https://cjhydz-isv.isvjcloud.com"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        ## 开卡解析
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 活动开卡\n【活动变量】:`export jd_joinCommonId="{activateId[0]}&{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/aug/brandUnion/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 活动开卡\n【活动变量】:`export jd_joinCommonId="{activateId[0]}&{shopid[0]}"`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'

        elif re.findall("https://hdb-isv.isvjcloud.com", data['jumpUrl']):
            msg = f'【脚本类型】: 大牌联合\n【活动地址】:{data["jumpUrl"]}\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        ## 穿行寻宝
        ##elif re.findall("快加入我的队伍，躺赢赚红包~", data['title']):
            msg = f'【脚本类型】: 穿行寻宝组队\n【活动变量】:穿行寻宝组队码\n`{inviteId[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        ##elif re.findall("快快点击，助我瓜分20亿红包吧！", data['title']):
            msg = f'【脚本类型】: 穿行寻宝助力\n【活动变量】:穿行寻宝助力码\n`{inviteId_1[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
        ##elif re.findall("帮我点一点，膨胀红包就差你的助力啦~", data['title']):
            msg = f'【脚本类型】: 穿行寻宝膨胀\n【活动变量】:穿行寻宝膨胀码\n`{inviteId_2[0]}`\n[摸鱼🫧🐟无处不在](https://t.me/TumblrCN)\n消息将于60秒后撤回'
            
        else:
            msg = "【未适配变量】"
        if "脚本类型" in msg:
            msg_text = await jdbot.send_message(event.chat_id,result+"\n"+msg)
            await asyncio.sleep(60)
            await jdbot.delete_messages(event.chat_id,msg_text)
            await event.delete()


    except:
        msg = await jdbot.send_message(event.chat_id, f"呀呼，解析出错！\n请小八嘎重试几次")
        await asyncio.sleep(3)
        await msg.delete()