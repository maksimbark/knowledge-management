## Угадай число

import random

from smart_m3.m3_kp_api import *

kp = m3_kp_api(PrintDebug=True)

class KP_Handler_Server:
    _numbers_for_guess = dict()
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        if len(added) > 0:
            print('added', added)

        for data in added:
            # Инициализируем игру
            if str(data[2]) == "waiting" and str(data[1]) == "game_status":
                kp.load_query_rdf(Triple(data[0], data[1], data[2]))
                if len(kp.result_rdf_query) > 0:
                    self._numbers_for_guess[str(data[0])] = random.randint(0, 100)
                    print('Загадано число {} для {}'.format(self._numbers_for_guess[str(data[0])], str(data[0])))
                    kp.load_rdf_update([Triple(data[0], data[1], Literal('ready'))], kp.result_rdf_query)

            if str(data[1]) == "last_guess":
                value = 1
                try:
                    value = int(str(data[2]))
                    agent = str(data[0])
                    if self._numbers_for_guess[agent] > value:
                        kp.load_rdf_insert(Triple(data[0], URI("last_guess_result"), Literal('more')))
                    elif self._numbers_for_guess[agent] < value:
                        kp.load_rdf_insert(Triple(data[0], URI("last_guess_result"), Literal('less')))
                    else:
                        kp.load_rdf_insert(Triple(data[0], URI("last_guess_result"), Literal('guessed')))

                except ValueError:
                    print('expected num, got {}'.format(str(data[2])))

#Запускаем сервер
handler_server = KP_Handler_Server(kp)
handler_subscription_server = kp.load_subscribe_RDF(Triple(None, None, None), handler_server)
print('!!!--Сервер запущен--!!!')
