# coding=utf-8
# __author__ = 'Mio'
import json
import logging
from urllib.parse import urljoin
from asyncio import sleep

from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

import dingtalk
from settings import GOTIFY_HTTP_URL, GOTIFY_WS_URL, GOTIFY_USER, GOTIFY_PASS, loop

STREAM_MSG = urljoin(GOTIFY_WS_URL, "stream")
MSG_ID = urljoin(GOTIFY_HTTP_URL, "/message") + "/{msg_id}"


async def delete_msg(msg_id):
    d_ = MSG_ID.format(msg_id=msg_id)
    logging.info(d_)
    req = HTTPRequest(url=d_, method="DELETE",
                      auth_mode='basic',
                      auth_username=GOTIFY_USER, auth_password=GOTIFY_PASS)
    try:
        await AsyncHTTPClient().fetch(req)
    except Exception as e:
        logging.error(e)


async def conn_gotify():
    logging.info(STREAM_MSG)
    req = HTTPRequest(url=STREAM_MSG,
                      auth_mode='basic',
                      auth_username=GOTIFY_USER, auth_password=GOTIFY_PASS)
    try:
        conn = await websocket_connect(req)
    except Exception as e:
        logging.error(e)
        loop.stop()
        return
    while True:
        msg: str = await conn.read_message()
        if msg is None:
            break

        try:
            msg: dict = json.loads(msg)
        except Exception as e:
            pass
        else:
            await dingtalk.send_markdown(title=msg['title'], text=msg['message'])
            await delete_msg(msg['id'])
        await sleep(1)
