import logging
import json
import rethinkdb as r

from api.errors import ApiBadRequest





async def create_asset_entry(conn, asset_entry):
    result = await r.table('asset1').insert(auth_entry).run(conn)
    
    if result.get('errors') > 0 and \
       "Duplicate primary key `file_hash`" in result.get('first_error'):
        raise ApiBadRequest("A file with that filehash already exists")


async def fetch_info_by_filehash(conn, file_hash):
    try:
        result=[]
        # entry = await r.db("main_db").table('auth1').get(email).run(conn)
        cursor = await r.table("asset1").filter(r.row["file_hash"] == file_hash).run(conn)
        # cursor = await r.table("auth1").run(conn)
        while (await cursor.fetch_next()):
            # print(cursor.fetch_next())
            item = await cursor.next()
            result.append(item)

                    
    except Exception as e:
        return None
    
    return result