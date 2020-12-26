import os, time, asyncio

import subprocess


#Функция устонавливает настройки карты через бат файлы с интервалом в 3 минуты
async def video_card_settings(setting_1, setting_2):
    
    print(f'initializing  {setting_1}................')
    # os.system(setting_1)

    await asyncio.sleep(10)
    
    print(f'initializing  {setting_2}................')
    # os.system(setting_2)

    return True


#Функция инициализирует файл для запуска фермы, и следит за логами
async def start_mining(mining_file):
    
    print(mining_file)
    process = subprocess.Popen(mining_file, stdout=subprocess.PIPE) 
    
    counter = 0

    while True:
        await asyncio.sleep(1)
        output = process.stdout.readline().decode('cp866')

        if output == '' and process.poll() is not None:
            break
        if output:

            print(output)
            # if 'Hashrate' in output:
            #     line = output.split(' ')
            #     hash_rate = line[3]
            #     if float(hash_rate) < 200:
            #         process.kill()
            #         run_command(video_settings_initial,mining_file,video_settings_final)

        if counter > 10:


            print('iter limit reached')
            process.terminate()
            print('stopping loop')
            return 'complete'
        
        counter += 1

    rc = process.poll()
    print(rc)
    return rc


def stop_loop(future):
    print(future.result())
    loop.stop()
    
def main():
    
    # бат файл с первыми с настройками видеокарты
    setting_1 = 'file_1'

    # бат файл с новыми с настройками видеокарты
    setting_2 = 'file_2'

    # бат файл с инициализацией крипто фермы
    mining_file = 'mining_file'

    mining_file = 'ping ya.ru -t' #temp command
    global loop 
    loop = asyncio.get_event_loop()


    set_settings = loop.create_task(video_card_settings(setting_1, setting_2))
    _start_mining = loop.create_task(start_mining(mining_file))

    _start_mining.add_done_callback(stop_loop)
    
    loop.run_forever()

    return True

    

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
main()


