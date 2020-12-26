import os, time, asyncio
import subprocess

class CryptoFarmController:

    def __init__(self):

        self.video_settings = self.VideoCardSettings()
        self.miner = self.Miner()


    class VideoCardSettings:

        def __init__(self):

            self._initial_settings = '3070-1.bat
            self._secondary_settings = '3070.bat'

        #Функция устонавливает настройки карты через бат файлы с интервалом в 3 минуты
        async def video_card_settings(self):
            
            print(f'initializing  {self._initial_settings}................')
            # os.system(self._initial_settings)

            await asyncio.sleep(10)
            
            print(f'initializing  {self._secondary_settings}................')
            # os.system(self._secondary_settings)

            return True


    class Miner:

        def __init__(self):

            self._mining_file = '!ETH-ethermine.bat'

        #Функция инициализирует файл для запуска фермы, и следит за логами
        @staticmethod
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
                    if 'Hashrate' in output:
                        line = output.split(' ')
                        hash_rate = line[3]
                        if float(hash_rate) < 200:
                            process.terminate()
                            return None


            rc = process.poll()
            return rc



class Controller(CryptoFarmController):

    def __init__(self):

        CryptoFarmController.__init__(self)
        self.loop = None


    def stop_loop(self, future):

        print(future.result())
        self.loop.stop()
        self.loop = None

  
    def main(self, test = True):
        print('initializing')
        # бат файл с инициализацией крипто фермы
        if test:
            mining_file = 'ping ya.ru -t' #temp command
        else:
            mining_file = self.miner._mining_file

        self.loop = asyncio.get_event_loop()

        set_settings = self.loop.create_task(self.video_settings.video_card_settings())
        _start_mining = self.loop.create_task(self.miner.start_mining(mining_file))

        _start_mining.add_done_callback(self.stop_loop)
        
        self.loop.run_forever()


    

if __name__ == '__main__':

    controller = Controller()

    while True:

        if controller.loop is None:

            controller.main()

        else:
            time.sleep(5)
