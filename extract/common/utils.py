import asyncio
import json
import os

import requests
from urllib.parse import urlparse

import s3fs

s3 = s3fs.S3FileSystem()


class CamaraSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        })

    async def get(self, url, **kwargs):
        response = await asyncio.to_thread(self.session.get, url, **kwargs)
        return json.loads(response.content)


def create_dirs(dir_path):
    match urlparse(dir_path).scheme:
        case 'file' | '':
            os.makedirs(dir_path, exist_ok=True)
        case 's3':
            s3.makedirs(dir_path, exist_ok=True)
        case scheme:
            raise NotImplemented(f"Protocol not supported for dir creation: {scheme}")
