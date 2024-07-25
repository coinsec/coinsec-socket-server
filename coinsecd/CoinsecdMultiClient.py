# encoding: utf-8
import asyncio

from coinsecd.CoinsecdClient import CoinsecdClient
# pipenv run python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/rpc.proto ./protos/messages.proto ./protos/p2p.proto
from coinsecd.CoinsecdThread import CoinsecdCommunicationError


class CoinsecdMultiClient(object):
    def __init__(self, hosts: list[str]):
        self.coinsecds = [CoinsecdClient(*h.split(":")) for h in hosts]

    def __get_coinsecd(self):
        for k in self.coinsecds:
            if k.is_utxo_indexed and k.is_synced:
                return k

    async def initialize_all(self):
        tasks = [asyncio.create_task(k.ping()) for k in self.coinsecds]

        for t in tasks:
            await t

    async def request(self, command, params=None, timeout=5):
        try:
            return await self.__get_coinsecd().request(command, params, timeout=timeout)
        except CoinsecdCommunicationError:
            await self.initialize_all()
            return await self.__get_coinsecd().request(command, params, timeout=timeout)

    async def notify(self, command, params, callback):
        return await self.__get_coinsecd().notify(command, params, callback)
