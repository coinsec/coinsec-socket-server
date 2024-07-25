# encoding: utf-8

from server import coinsecd_client


async def get_blockdag():
    """
    Get some global Coinsec BlockDAG information
    """
    resp = await coinsecd_client.request("getBlockDagInfoRequest")
    return resp["getBlockDagInfoResponse"]
