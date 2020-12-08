import random
from termcolor import cprint

from smart_m3.m3_kp_api import *
from time import sleep

kp = m3_kp_api()

def client(agentname, color):
    class KP_Handler_Client:
        handler_subscription_client = 0
        minnum = 0
        maxnum = 100
        last_guess = 0

        def __init__(self, kp=None):
            self.kp = kp

        def handle(self, added, remove):
            sleep(0.3)

            for data in added:
                if str(data[1]) == "game_status":
                    if str(data[2]) == "ready":
                        self.last_guess = random.randint(self.minnum, self.maxnum)
                        cprint('Начальное предположение. Предполагаю число {}'.format(self.last_guess), color)
                        kp.load_rdf_insert(Triple(URI(agentname), URI('last_guess'), Literal(self.last_guess)))

                if str(data[1]) == "last_guess_result":
                    kp.load_rdf_remove(Triple(URI(agentname), URI('last_guess_result'), None))
                    if str(data[2]) == "less":
                        cprint('Получен ответ: меньше', color)
                        self.maxnum = self.last_guess - 1
                        self.last_guess = random.randint(self.minnum, self.maxnum)
                        cprint('Предполагаю число {}'.format(self.last_guess), color)
                        kp.load_rdf_insert(Triple(URI(agentname), URI('last_guess'), Literal(self.last_guess)))
                    elif str(data[2]) == "more":
                        cprint('Получен ответ: больше', color)
                        self.minnum = self.last_guess + 1
                        self.last_guess = random.randint(self.minnum, self.maxnum)
                        cprint('Предполагаю число {}'.format(self.last_guess), color)
                        kp.load_rdf_insert(Triple(URI(agentname), URI('last_guess'), Literal(self.last_guess)))
                    elif str(data[2]) == "guessed":
                        cprint('Угадано! Число {}'.format(self.last_guess), color)
                        # Корректно выйти из системы.
                        kp.load_unsubscribe(self.handler_subscription_client)
                        # Как в примере не получится использовать os._exit(0), так что бросим исключение
                        raise Exception("All done!")

    handler_client = KP_Handler_Client(kp)
    handler_subscription_client = kp.load_subscribe_RDF(Triple(URI(agentname), None, None),
                                                        handler_client)
    #передадим handler_client чтобы можно было остановить подписку после успешного угадывания
    handler_client.handler_subscription_client = handler_subscription_client
    # сообщаем о готовности
    kp.load_rdf_insert(Triple(URI(agentname), URI('game_status'), Literal('waiting')))
    cprint('!!!--{} запущен с цветом {}--!!!'.format(agentname, color), color)

class prog_closer:
    countOfDone = 0
    def incr(self):
        self.countOfDone += 1

    def finish(self):
        kp.clean_sib()
        kp.leave()
        print('All finished!')

myProg = prog_closer()

def uncaughtExceptionHandler(err):
    if str(err.exc_value) == "All done!":
        print("Agent exited")
        myProg.incr()
    else:
        raise
    # Количество агентов, которое надо ждать
    if myProg.countOfDone == 2:
        myProg.finish()



threading.excepthook = uncaughtExceptionHandler

client('agent1', 'red')
sleep(0.3)
client('agent2', 'green')
