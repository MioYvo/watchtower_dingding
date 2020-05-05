# coding=utf-8
# __author__ = 'Mio'

from os import getenv
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOLoop

GOTIFY_HTTP_SCHEMA = getenv("GOTIFY_HTTP_SCHEMA", "http")
GOTIFY_HOST = getenv("GOTIFY_HOST")
assert GOTIFY_HOST
GOTIFY_PORT = int(getenv("GOTIFY_PORT", 80))
GOTIFY_USER = getenv("GOTIFY_USER", "admin")
GOTIFY_PASS = getenv("GOTIFY_PASS", "admin")
GOTIFY_HTTP_URL = f"{GOTIFY_HTTP_SCHEMA}://{GOTIFY_HOST}:{GOTIFY_PORT}"
GOTIFY_WS_URL = f"ws://{GOTIFY_HOST}:{GOTIFY_PORT}"

DINGTALK_ROBOT_TOKEN = getenv("DINGTALK_ROBOT_TOKEN")
DINGTALK_ROBOT_KEYWORD = getenv("DINGTALK_ROBOT_KEYWORD")
assert DINGTALK_ROBOT_TOKEN
assert DINGTALK_ROBOT_KEYWORD

loop: AsyncIOLoop = IOLoop.current()
async_loop = loop.asyncio_loop
