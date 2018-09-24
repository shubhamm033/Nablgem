# from sawtooth_rest_api.protobuf import client_batch_submit_pb2
# from sawtooth_rest_api.protobuf import validator_pb2

from api.errors import ApiBadRequest
from api.errors import ApiInternalError
import time
import aiohttp
import asyncio
# from logging.clogging import logger

# async def send(conn, timeout, batches):
    # batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    # batch_request.batches.extend(batches)
    # await conn.send(
    #     validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
    #     batch_request.SerializeToString(),
    #     timeout)
async def send(data, request):
    """
    batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    batch_request.batches.extend(batches)
    await conn.send(
        validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
        batch_request.SerializeToString(),
        timeout)
    """
    headers = {'Content-Type': 'application/octet-stream'}
    
    # timeout = aiohttp.Timeout(request.app.config.TIMEOUT)
    # print(timeout)
    try:
        with aiohttp.Timeout(request.app.config.TIMEOUT):
            async with aiohttp.ClientSession() as session:
                async with session.post("http://127.0.0.1:8008/batches", data=data, headers=headers) as response:
                    # print(response)
                    data = await response.read()
                    print(data)
    except Exception as e:
        # logger.error("Blockchain rest-api is unreachable, Please fix it dude")
        raise ApiInternalError("Blockchain rest-api is unreachable, Please fix it dude")
    return data

async def wait_for_status(batch_id,wait, request):
    '''Wait until transaction status is not PENDING (COMMITTED or error).
       'wait' is time to wait for status, in seconds.
    '''
    headers = {'Content-Type': 'application/json'}
    # waited = 0
    # start_time = time.time()
    # wait = request.app.config.TIMEOUT
    # # timeout = aiohttp.ClientTimeout(total=request.app.config.TIMEOUT)
    # while waited < wait:
    try:
        with aiohttp.Timeout(request.app.config.TIMEOUT):
            async with aiohttp.ClientSession() as session:
                    async with session.get("http://127.0.0.1:8008/batch_statuses?id={}&wait={}".format(batch_id,wait), headers=headers) as response:
                        # print(response)
                        await asyncio.sleep(4)
                        data = await response.read()
                        print(data)
                        data = load_json(data)
        # print(data)
                        status = data['data'][0]['status']
        # print(status)
    except Exception as e:
        # logger.error("Error in wait for status")
        # logger.error(e)
        status = ""
        pass

        # waited = time.time() - start_time
        # logger.debug("Trying again, to check block status BLOCK-STATUS {status}")
    #     if status != 'PENDING':
    #         break
    # # if status == "COMMITTED":
    #     # logger.debug("Transaction successfully submittted")
    #     return True

    # elif status == "PENDING":
    #     # logger.error("Transaction submitted but timed out")
    #     raise ApiInternalError("Transaction submitted but timed out")
    # elif status == "UNKNOWN":
    #     # logger.error("Something went wrong. Try again later")
    #     raise ApiInternalError("Something went wrong. Try again later")
    # elif status == "INVALID":
    #     # logger.error("Transaction submitted to blockchain is invalid")
    #     raise ApiInternalError("Transaction submitted to blockchain is invalid")

    # else:
    #     # logger.error("Error in the transaction {%s}"%data['data'][0]['message'])
    #     raise ApiBadRequest("Error in the transaction {%s}"%data['data'][0]['message'])
    # return








# async def check_batch_status(conn, batch_id):
#     status_request = client_batch_submit_pb2.ClientBatchStatusRequest(
#         batch_ids=[batch_id], wait=True)
#     validator_response = await conn.send(
#         validator_pb2.Message.CLIENT_BATCH_STATUS_REQUEST,
#         status_request.SerializeToString())

#     status_response = client_batch_submit_pb2.ClientBatchStatusResponse()
#     status_response.ParseFromString(validator_response.content)
#     batch_status = status_response.batch_statuses[0].status
#     if batch_status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
#         invalid = status_response.batch_statuses[0].invalid_transactions[0]
#         raise ApiBadRequest(invalid.message)
#     elif batch_status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
#         raise ApiInternalError("Transaction submitted but timed out")
#     elif batch_status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
#         raise ApiInternalError("Something went wrong. Try again later")
