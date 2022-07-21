from picarx import Picarx
import websockets
import asyncio

px = Picarx()

async def listen():
    #connect to server
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url) as ws:
        while True:
            #receiving data for processing
            msg = await ws.recv()
            data = list(map(int,msg.split(' ')))
            distance = float(data[3])
            gm_val_list = data[:-1]
            print(gm_val_list)
            
            rep_dist = ''
            #data processing
            if distance < 10:
                rep_dist = 'stop'
            line_state = px.get_line_status(gm_val_list)
            rep = line_state + ' '+rep_dist

            #sending response
            await ws.send(rep)
asyncio.get_event_loop().run_until_complete(listen())

