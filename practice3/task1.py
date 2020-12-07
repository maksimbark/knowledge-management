import random
import os

from smart_m3.m3_kp_api import *
from threading import Timer
from time import sleep

kp = m3_kp_api()

# Задание 1.1 Проверка insert / query / update / remove
print('\n!----Task 1.1----!\n')
# Вставить несколько RDF-троек при помощи Insert.
insert_list = [
        Triple(URI('maksimbark'), URI('has_temperature'), Literal(36.6)),
        Triple(URI('ivan'), URI('has_temperature'), Literal(37.3)),
        Triple(URI('andrew'), URI('has_temperature'), Literal(38.1)),
        Triple(URI('viktor'), URI('has_temperature'), Literal(38.1)),
    ]
kp.load_rdf_insert(insert_list)

# Проверить их вставку при помощи операции Query
# использовать как строгое условие, когда определена вся тройка
# так и условия с wildcard’ом - т.е. тройка с определенным паттерном)
kp.load_query_rdf(Triple(URI('viktor'), URI('has_temperature'), Literal('38.1')))
print('Found: {}'.format(kp.result_rdf_query))

kp.load_query_rdf(Triple(None, None, Literal(38.1)))
print('Temp 38.1 found: {}'.format(kp.result_rdf_query))

# Изменить существующие тройки при помощи команды Update.

kp.load_query_rdf(Triple(URI('viktor'), URI('has_temperature'), None))
if len(kp.result_rdf_query) > 0:
    kp.load_rdf_update([Triple(URI('viktor'), URI('has_temperature'), Literal(36.6))], kp.result_rdf_query)

# Проверим изменение
kp.load_query_rdf(Triple(None, None, Literal(36.6)))
print('Temp 36.6 found: {}'.format(kp.result_rdf_query))

# Удалить данные при помощи команды Remove
kp.load_rdf_remove(Triple(None, None, None))

# Проверим отсутствие данные
kp.load_query_rdf(Triple(None, None, None))
print('Found: {}'.format(kp.result_rdf_query))

# Задание 1.2 Проверка работы подписок
print('\n!----Task 1.2----!\n')
# Разработать интеллектуального агента, который через равные
# промежутки времени записывает RDF-тройку вида: [URI(‘Agent_X’), URI(‘has_item’), Literal(число)]

def insert_cats():
    kp.load_rdf_insert(Triple (URI('Agent_X'), URI('has_cats'), Literal(random.randint(0,30))))

for i in range(50):
    Timer(1.0*i, insert_cats).start()

# Подписаться на изменение хранилища и удостовериться, что подписка работает.
class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        # in case if you want to react on added/removed data - just use self.kp.your_function(....) here
        print('added', added)

handler = KP_Handler(kp)
handler_subscription = kp.load_subscribe_RDF(Triple(None, None, None), handler)
# Посмотрим вывод 5 секунд
sleep(5)
# Корректно выйти из системы.
kp.load_unsubscribe(handler_subscription)

# Добавить второго агента, который “слушает” изменения в хранилище и удаляет все тройки,
# в которых субъект - это четное число

class KP_Handler_2:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        if len(added) > 0:
            print('added', added)

        for data in added:
            value = 1
            try:
                value = int(str(data[2]))
            except ValueError:
                value = 1

            if value % 2 == 0:
                print('!!! --- triplet with even subject {} will be removed --- !!!'.format(value))
                kp.load_rdf_remove(Triple(data[0], data[1], data[2]))
                # Необходимо удостовериться в правильности удалении данных
                kp.load_query_rdf(Triple(None, None, None))
                print('Current status: {}\n'.format(kp.result_rdf_query))
                break

handler = KP_Handler_2(kp)
handler_subscription = kp.load_subscribe_RDF(Triple(None, None, None), handler)

# Очистим данные: удалим все старые значения
kp.clean_sib()
print('!!! Started second handler !!!')
# Посмотрим вывод 15 секунд
sleep(15)

kp.load_query_rdf(Triple(None, None, None))
print('Final status: {}\n'.format(kp.result_rdf_query))

# Корректно выйти из системы.
kp.load_unsubscribe(handler_subscription)
kp.clean_sib()
kp.leave()
raise os._exit(0)
