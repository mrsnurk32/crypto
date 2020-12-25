import time
import os

import threading
import subprocess
import asyncio


async def set_video_setting(video_settings_initial, video_settings_final):

    print('setting default video settings')
    os.system(video_settings_initial)

    await asyncio.sleep(180)

    print('setting new settings')
    os.system(video_settings_final)


async def start_mining(mining_file,video_settings_initial,video_settings_final):
    initial_settings = loop.create_task(set_video_setting(
        video_settings_initial, video_settings_final)
    )

    await asyncio.sleep(5)
    
    print('start mining')
    process = subprocess.Popen(mining_file, stdout=subprocess.PIPE) 
        
    while True:
        time.sleep(1)
        output = process.stdout.readline().decode('cp866')

        if output == '' and process.poll() is not None:
            break
        if output:

            print(output)
            if 'Hashrate' in output:
                line = output.split(' ')
                hash_rate = line[3]
                if float(hash_rate) < 200:
                    process.kill()
                    run_command(video_settings_initial,mining_file,video_settings_final)


    rc = process.poll()
    return rc


video_settings_initial = '3070-1.bat'
mining_file = '!ETH-ethermine.bat'
video_settings_final = '3070.bat'


if __name__ == '__main__':

    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        loop.run_until_complete(start_mining(mining_file,video_settings_initial,))
    except Exception as e:
        print(e)

    finally:
        loop.close()

