FROM python:alpine

COPY * /watchtower_dingding/

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r /watchtower_dingding/requirements.txt

WORKDIR /watchtower_dingding
ENTRYPOINT ["python", "-u", "run.py"]
