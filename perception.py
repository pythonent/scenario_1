from dis import Instruction

from cv2 import line
from picarx import Picarx
import websockets
import asyncio
import math

px = Picarx()
px_power = 1

#opening server
port = 7890
print("Server listening on port: "+str(port))

async def echo(websocket, path):
    try:
        while(True):
            #data gathering and sending operation
                line_percept = px.get_grayscale_data()
                msg = ' '.join(str(val) for val in line_percept)
                ultrasonic_percept = math.floor(px.ultrasonic.read())
                print(ultrasonic_percept)
                msg += ' '+str(ultrasonic_percept)

                await websocket.send(msg)

            #receiving instructions
                rep = await websocket.recv()
                instructions = rep.split(' ')
                 
                ultrasonic_instruction = instructions[1]
                line_instruction = instructions[0] 

                if ultrasonic_instruction == 'stop':
                    px.stop()
                else:
                    if line_instruction == 'forward':
                        print(1)
                        px.forward(px_power) 
                    elif line_instruction == 'left':
                        px.set_dir_servo_angle(12)
                        px.forward(px_power) 

                    elif line_instruction == 'right':
                        px.set_dir_servo_angle(-12)   
                    else:
                        px.set_dir_servo_angle(0)
                        px.stop()

    except websocket.exceptions.ConnectionClosed as e:
        print('not receiving')
    finally:
        px.stop()
            

start_server = websockets.serve(echo,"127.0.0.1",port)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()