# encoding: utf-8

from server import coinsecd_client


async def get_network():
    """
    Get some global coinsec network information
    """
    resp = await coinsecd_client.request("getBlockDagInfoRequest")
    return resp["getBlockDagInfoResponse"]
