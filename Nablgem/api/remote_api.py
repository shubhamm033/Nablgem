import aiohttp
import asyncio
from api import errors
import json

async def registration(request):

    async with aiohttp.ClientSession() as session:
        
        try:
            
            data ={'email': request.json["email"], "phone_number": request.json["phone_number"],
                    'adhaar': request.json["adhaar"],'pancard': request.json["pancard"],
                    'first_name': request.json["first_name"], 'last_name': request.json['last_name'],\
                    'user_type': request.json["user_type"]}
            # print(data)
            async with session.post("http://52.66.22.183/registration",json=data) as response:
                # print(response)
                data1 = await response.read()
                data1= data1.decode("utf-8")
                # print(data1)
            async with session.post("http://52.66.22.183/getkeys",json=data) as response:
                data2 = await response.read()
                data2 = data2.decode("utf-8")
                # print(data2)
        

        except Exception as e:
            # raise ApiInternalError("Registration api is not working, Please fix it Dude")
            return {"sucess":False,"error":str(e)}

        data1 = json.loads(data1)
        data2 =json.loads(data2)
        password = data1["data"]["password"]
        user_id = data1["data"]["user_id"]
        secrets = data2["data"]["secrets"]
        # print(secrets)
    

    return user_id,password, secrets

                    
                    
async def get_child_key(mnemonic,child_key_index):

    async with aiohttp.ClientSession() as session:
        
        try:    
            
            data ={"mnemonic":mnemonic,"child_key_index": child_key_index}
            
            async with session.post("http://52.66.22.183/child_mnemonic_keys",json=data) as response:
                data3 = await response.read()        
                data3 = data3.decode("utf-8")
                
        
        except Exception as e:
                return {"sucess":False,"error":str(e)}

    data3 = json.loads(data3)
    # print(data3)
    private_hex_key = data3["data"]["child_private_key"]
    public_hex_key =data3["data"]["child_public_key"]
        
    return private_hex_key,public_hex_key
        