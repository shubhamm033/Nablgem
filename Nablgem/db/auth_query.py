import logging
import json
import rethinkdb as r

from api.errors import ApiBadRequest


LOGGER = logging.getLogger(__name__)


async def create_auth_entry(conn, auth_entry):
    result = await r.table('auth1').insert(auth_entry).run(conn)
    
    if result.get('errors') > 0 and \
       "Duplicate primary key `email`" in result.get('first_error'):
        raise ApiBadRequest("A user with that email already exists")
    


async def remove_auth_entry(conn, email):
    await r.table('auth').get(email).delete().run(conn)


async def fetch_info_by_email(conn, user_id):
    try:
        result=[]
        # entry = await r.db("main_db").table('auth1').get(email).run(conn)
        cursor = await r.table("auth1").filter(r.row["user_id"] == user_id).run(conn)
        # cursor = await r.table("auth1").run(conn)
        while (await cursor.fetch_next()):
            # print(cursor.fetch_next())
            item = await cursor.next()
            result.append(item)

                    
    except Exception as e:
        return json.loads({"success":False,"error": str(e)})
    
    return result

async def update_auth_info(conn, email, public_key, update):
    result = await r.table('auth')\
        .get(email)\
        .do(lambda auth_info: r.expr(update.get('email')).branch(
            r.expr(r.table('auth').insert(auth_info.merge(update),
                                          return_changes=True)),
            r.table('auth').get(email).update(update, return_changes=True)))\
        .do(lambda auth_info: auth_info['errors'].gt(0).branch(
            auth_info,
            auth_info['changes'][0]['new_val'].pluck('email')))\
        .merge(_fetch_account_info(public_key))\
        .run(conn)
    if result.get('errors'):
        if "Duplicate primary key `email`" in result.get('first_error'):
            raise ApiBadRequest(
                "Bad Request: A user with that email already exists")
        else:
            raise ApiBadRequest(
                "Bad Request: {}".format(result.get('first_error')))
    if update.get('email'):
        await remove_auth_entry(conn, email)
    return result


def _fetch_account_info(public_key):
    return r.table('accounts')\
        .get_all(public_key, index='public_key')\
        .max('start_block_num')\
        .do(lambda account: account.merge(
            {'publicKey': account['public_key']}))\
        .do(lambda account: (account['label'] == "").branch(
            account.without('label'), account))\
        .do(lambda account: (account['description'] == "").branch(
            account.without('description'), account))\
        .without('public_key', 'delta_id',
                 'start_block_num', 'end_block_num')
