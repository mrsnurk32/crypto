import time
import os

import threading
import subprocess


def run_command(video_settings_initial,mining_file,video_settings_final):
    
    print('starting new process')

    os.system(video_settings_initial)
    print('default video settings')
    
    time.sleep(3)
    
    print('start mining')
    process = subprocess.Popen(mining_file, stdout=subprocess.PIPE)

    time.sleep(180)
    
    print('setting new settings')
    os.system(video_settings_final)
    

    
    counter = 0
    while True:
        counter += 1
        time.sleep(1)
        output = process.stdout.readline().decode('cp866')
        if output == '' and process.poll() is not None:
            break
        if output:

            print(output)
            if 'Hashrate' in output:
                line = output.split(' ')
                hash_rate = line[3]
                if int(hash_rate) < 200:
                    process.kill()
                    run_command(video_settings_initial,mining_file,video_settings_final)
                    
    rc = process.poll()
    return rc


video_settings_initial = '3070-1.bat'
mining_file = '!ETH-ethermine.bat'
video_settings_final = '3070.bat'

run_command(video_settings_initial,mining_file,video_settings_final)