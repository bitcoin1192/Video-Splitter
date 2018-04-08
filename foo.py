import random
import asyncio
import search

async def random_gen():
    name = await ''.join(random.choice('0123456789AaBbCcDdEeFf') for i in range(16))
    return name

async def testas():
    couint = 0
    state = True
    while state == True:#becareful infinite loop
        name = random_gen()
        if search.db_search(str(name)) is False:
            state = False
            search.db_insert(str(name))
        couint = couint + 1
        if couint > 10:#break loop incase of infinite loop
            return('maybe we are out of name')
    return('success')

