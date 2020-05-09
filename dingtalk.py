# coding=utf-8
# __author__ = 'Mio'
import json
import logging
from collections import namedtuple
from typing import List

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from settings import DINGTALK_ROBOT_TOKEN, DINGTALK_ROBOT_KEYWORD


async def _send(body: dict) -> None:
    req = HTTPRequest(
        url=DINGTALK_ROBOT_TOKEN,
        method="POST",
        headers={"Content-Type": "application/json"},
        body=json.dumps(body)
    )
    try:
        res = await AsyncHTTPClient().fetch(req)
    except Exception as e:
        logging.error(e)
    else:
        logging.info(f"{res.code} {body}")


async def send_text(content: str, atMobiles: List[str] = None, isAtAll: bool = None) -> None:
    data = {
        "msgtype": "text",
        "text": {
            "content": content + f"\n\r{DINGTALK_ROBOT_KEYWORD}"
        },
        "at": {
            "atMobiles": atMobiles if atMobiles else [],
            "isAtAll": bool(isAtAll) if not None else None
        }
    }
    await _send(body=data)


async def send_link(text, title, messageUrl, picUrl="") -> None:
    data = {
        "msgtype": "link",
        "link": {
            "text": text + f"\n\r{DINGTALK_ROBOT_KEYWORD}",
            "title": title,
            "picUrl": picUrl,
            "messageUrl": messageUrl
        }
    }
    await _send(data)


async def send_markdown(title: str, text: str, atMobiles: List[str] = None, isAtAll: bool = None) -> None:
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title + f"\n\r{DINGTALK_ROBOT_KEYWORD}",
            "text": text
        },
        "at": {
            "atMobiles": atMobiles if atMobiles else [],
            "isAtAll": bool(isAtAll) if not None else None
        }
    }
    await _send(data)


ActionCard = namedtuple("ActionCard", ["title", "url"])


async def send_action_card(title, text: str, btnOrientation: int = 0, *action_cards: ActionCard) -> None:
    if len(action_cards) == 1:
        data = {
            "actionCard": {
                "title": title + f"\n\r{DINGTALK_ROBOT_KEYWORD}",
                "text": text,
                "btnOrientation": str(btnOrientation),
                "singleTitle": action_cards[0].title,
                "singleURL": action_cards[0].url
            },
            "msgtype": "actionCard"
        }
    elif len(action_cards) <= 0:
        return
    else:
        data = {
            "actionCard": {
                "title": title + f"\n\r{DINGTALK_ROBOT_KEYWORD}",
                "text": text,
                "btnOrientation": str(btnOrientation),
                "btns": [dict(title=ac.title, actionURL=ac.url) for ac in action_cards]
            },
            "msgtype": "actionCard"
        }
    await _send(data)


FeedCard = namedtuple("FeedCard", field_names=["title", "msgUrl", "picUrl"])


async def send_feed_card(*feed_cards: FeedCard) -> None:
    if len(feed_cards) <= 0:
        return
    data = {
        "feedCard": {
            "links": [dict(title=fc.title + f"\n\r{DINGTALK_ROBOT_KEYWORD}", messageURL=fc.msgUrl, picURL=fc.picUrl) for fc in feed_cards]
        },
        "msgtype": "feedCard"
    }
    await _send(data)
