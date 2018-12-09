import web3
import web3.eth
import web3.personal
import web3.miner
import web3.utils
import web3.manager
from web3 import Web3
import web3.contract
import time


class Estate:
    f1 = open('Store.abi', 'r')
    abi = f1.readline()
    f1.close()
    f1 = open('Store.bin', 'r')
    bin = f1.readline()
    f1.close()
    w3 = None
    contract_address = web3.Web3.toChecksumAddress("0x58a85dffa33250bebde9eb97b23302407f9195b1")
    user_address = None
    passfrase = None
    ws = None
    admin = web3.Web3.toChecksumAddress('0x2F9Ef54732FDCc38331451F866a344333e82d9D2')

    def __init__(self):
        # self.w3 = Web3(web3.HTTPProvider('http://127.0.0.1:8545'))
        self.w3 = Web3(web3.HTTPProvider('http://192.168.1.120:8545'))
        self.ws = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.abi,
        )

    # РАБОТАЕТ
    def auth(self, login, password):
        try:
            self.user_address = web3.Web3.toChecksumAddress(str(login))
        except Exception:
            log = False
        else:
            self.passfrase = str(password)
            log = self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
        print("Address: ", self.user_address)
        return log

    # РАБОТАЕТ
    def get_balance(self):
        balance = web3.Web3.fromWei(self.w3.eth.getBalance(self.user_address), 'ether')
        balance = str(balance)
        return balance

    # РАБОТАЕТ
    def create_estate(self, owner, info, squaere, useful):
        if self.user_address == self.admin:
            owner = web3.Web3.toChecksumAddress(str(owner))
            info = str(info)
            squaere = int(squaere)
            useful = int(useful)
            self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
            self.w3.miner.start(1)
            tx = self.ws.functions.create_estate(owner, info, squaere, useful).transact()
            self.w3.eth.waitForTransactionReceipt(tx)
            self.w3.miner.stop()

    # РАБОТАЕТ
    def get_estates_number(self):
        try:
            number = self.ws.functions.get_estates_number().call()
        except Exception:
            number = False
        return number

    # РАБОТАЕТ
    def get_estates(self):
        '''
        реестр
        :return:
        '''
        list_of_estates = []
        number = self.get_estates_number()
        if number:
            for id in range(number):
                answer = self.ws.functions.get_estates(id).call()
                for i in range(len(answer)):
                    answer[i] = str(answer[i])
                status = self.ws.functions.get_estates_statuses(id).call()
                for i in status:
                    if i:
                        answer.append('да')
                    else:
                        answer.append('нет')
                list_of_estates.append(answer)
        return list_of_estates

    # РАБОТАЕТ
    def get_estate_by_id(self, estate_id):
        try:
            answer = self.ws.functions.get_estates(estate_id).call()
        except Exception:
            answer = False
        return answer

    # РАБОТАЕТ
    def my_estates(self):
        list_of_estates = []
        number = self.get_estates_number()
        if number:
            for id in range(number):
                answer = self.ws.functions.get_estates(id).call()
                if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                    answer.pop(1)
                    for i in range(len(answer)):
                        answer[i] = str(answer[i])
                    status = self.ws.functions.get_estates_statuses(id).call()
                    for i in status:
                        if i:
                            answer.append("да")
                        else:
                            answer.append("нет")
                    list_of_estates.append(answer)
        return list_of_estates

    # РАБОТАЕТ
    def can_present(self):
        list_of_present = []
        number = self.get_estates_number()
        if number:
            for id in range(number):
                status = self.ws.functions.get_estates_statuses(id).call()
                if (not status[0]) and (not status[1]) and (not status[2]):
                    answer = self.ws.functions.get_estates(id).call()
                    if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                        answer.pop(1)
                        for j in range(len(answer)):
                            answer[j] = str(answer[j])
                        list_of_present.append(answer)
        return list_of_present

    # РАБОТАЕТ
    def create_present(self, estate_id, address_to, deadline):
        '''
        :param estate_id: номер собственности в реестре
        :param address_to:
        :param deadline: количество дней (срок истечения заказа)
        :return:
        '''
        estate_id = int(estate_id)
        status = self.ws.functions.get_estates_statuses(estate_id).call()
        if (not status[0]) and (not status[1]) and (not status[2]):
            answer = self.ws.functions.get_estates(estate_id).call()
            print(answer)
            if self.user_address == web3.Web3.toChecksumAddress(answer[1]):
                address_to = web3.Web3.toChecksumAddress(str(address_to))
                deadline = int(deadline) * 86400
                self.w3.personal.unlockAccount(self.user_address, self.passfrase)
                self.w3.eth.defaultAccount = self.user_address
                self.w3.miner.start(1)
                tx = self.ws.functions.create_present(estate_id, address_to, deadline).transact()
                self.w3.eth.waitForTransactionReceipt(tx)
                self.w3.miner.stop()

    # РАБОТАЕТ
    def get_presents_number(self):
        try:
            number = self.ws.functions.get_presents_number().call()
        except Exception:
            number =False
        return number

    # РАБОТАЕТ
    def get_present_by_id(self, present_id):
        try:
            number = self.ws.functions.get_presents(present_id).call()
        except Exception:
            number = False
        return number

    # РАБОТАЕТ
    def my_present(self):
        list_of_estates = []
        number = self.get_presents_number()
        if number:
            for id in range(number):
                present = self.get_present_by_id(id)
                if web3.Web3.toChecksumAddress(present[2]) == self.user_address:
                    # удаляем адрес получателя
                    present.pop(2)
                    # время
                    present[2] = time.ctime(int(present[2]))
                    # индекс собстевнности
                    estate_id = int(present[0])
                    estate = self.get_estate_by_id(estate_id)
                    for i in range(len(present)):
                        present[i] = str(present[i])
                    # физический адрес
                    present.insert(2, str(estate[2]))
                    # общая площадь
                    present.insert(3, str(estate[3]))
                    # полезная площадь
                    present.insert(4, str(estate[4]))
                    list_of_estates.append(present)
        return list_of_estates

    # РАБОТАЕТ
    def i_presented(self):
        '''
        Какую недвижимость я дарю
        '''
        list_of_estates = []
        number = self.get_presents_number()
        if number:
            for id in range(number):
                present = self.get_present_by_id(id)
                if web3.Web3.toChecksumAddress(present[1]) == self.user_address:
                    # удаляем адрес отправителя
                    present.pop(1)
                    # время
                    present[2] = time.ctime(int(present[2]))
                    # индекс собстевнности
                    estate_id = int(present[0])
                    estate = self.get_estate_by_id(estate_id)
                    for i in range(len(present)):
                        present[i] = str(present[i])
                    # физический адрес
                    present.insert(2, str(estate[2]))
                    # общая площадь
                    present.insert(3, str(estate[3]))
                    # полезная площадь
                    present.insert(4, str(estate[4]))
                    list_of_estates.append(present)
        return list_of_estates

    # РАБОТАЕТ
    def confirm_present(self, estate_id):
        '''
        Тот кому дарят, принимает подарок
        :param estate_id: индекс элемента в списке струтур Present
        '''
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.confirm_present(estate_id).transact({'gas': 900000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def cancel_present(self, estate_id):
        '''
        Тот кто дарит, отменяет свой подарок
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.cancel_present(estate_id).transact({'gas': 900000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()


    # КУПЛЯ - ПРОДАЖА


    # РАБОТАЕТ
    def can_sale(self):
        list_of_sale = []
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        estates_number = self.get_estates_number()
        # print(estates_number)
        for id in range(estates_number):
            status = self.ws.functions.get_estates_statuses(id).call()
            # print(status)
            if (not status[0]) and (not status[1]) and (not status[2]):
                answer = self.ws.functions.get_estates(id).call()
                if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                    answer.pop(1)
                    for j in range(len(answer)):
                        answer[j] = str(answer[j])
                    list_of_sale.append(answer)
        return list_of_sale

    # РАБОТАЕТ
    def get_sales_number(self):
        try:
            number = self.ws.functions.get_sales_number().call()
            return number
        except Exception:
            return False

    # РАБОТАЕТ
    def get_sale_by_id(self, sale_id):
        try:
            number = self.ws.functions.get_sales(sale_id).call()
            return number
        except Exception:
            return False

    # РАБОТАЕТ
    def my_sales(self):
        list_of_sales = []
        number = self.get_sales_number()
        if number:
            for id in range(number):
                answer = self.ws.functions.get_sales(id).call()
                if answer[1] != '0x0000000000000000000000000000000000000000':
                    if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                        new_answer = []
                        estate = self.get_estate_by_id(answer[0])
                        # estate_id
                        new_answer.append(str(answer[0]))
                        # Адрес
                        new_answer.append(str(estate[2]))
                        # Общая площадь
                        new_answer.append(str(estate[3]))
                        # Полезная площадь
                        new_answer.append(str(estate[4]))
                        # Цена
                        new_answer.append(str(answer[2]))
                        # Дедлайн
                        deadline = time.ctime(int(answer[4]))
                        new_answer.append(str(deadline))
                        list_of_sales.append(new_answer)
        return list_of_sales

    # РАБОТАЕТ
    def who_want_to_buy(self):
        list_of_sales = []
        number = self.get_sales_number()
        for id in range(number):
            answer = self.ws.functions.get_sales(id).call()
            if answer[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                    for i in range(len(answer[5])):
                        if answer[5][i] != '0x0000000000000000000000000000000000000000':
                            estate = self.get_estate_by_id(int(answer[0]))
                            # estate_id
                            new_answer = []
                            new_answer.append(str(answer[0]))
                            # физический адрес
                            new_answer.append(str(estate[2]))
                            # общая площадь
                            new_answer.append(str(estate[3]))
                            # полезная площадь
                            new_answer.append(str(estate[4]))
                            # цена, установленная продавцом
                            new_answer.append(str(answer[2]))
                            # время окончания срока действия предложения о продаже
                            new_answer.append(str(answer[4]))
                            # добавить кто предложил
                            new_answer.append(str(answer[5][i]))
                            # добавить сколько предложили
                            new_answer.append(str(answer[6][i]))
                            list_of_sales.append(new_answer)
        return list_of_sales

    # РАБОТАЕТ
    def choose_to_buy(self):
        '''
        Список продающихся домов
        :return:
        '''
        list_of_sales = []
        number = self.get_sales_number()
        for id in range(number):
            answer = self.ws.functions.get_sales(id).call()
            if answer[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(answer[1]) != self.user_address:
                    new_answer = []
                    # Поменять индекс
                    estate = self.get_estate_by_id(answer[0])
                    # estate_id
                    new_answer.append(str(answer[0]))
                    # физический адрес
                    new_answer.append(str(estate[2]))
                    # общая площадь
                    new_answer.append(str(estate[3]))
                    # полезная площадь
                    new_answer.append(str(estate[4]))
                    # цена
                    new_answer.append(str(answer[2]))
                    # дедлайн
                    answer[4] = time.ctime(int(answer[4]))
                    new_answer.append(str(answer[4]))
                    list_of_sales.append(new_answer)
        return list_of_sales

    # РАБОТАЕТ
    def i_have_payed(self):
        '''
        За что я заплатил
        :return:
        '''
        list_of_sales = []
        number = self.get_sales_number()
        for id in range(number):
            answer = self.ws.functions.get_sales(id).call()
            if answer[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(answer[1]) != self.user_address:
                    for i in range(len(answer[5])):
                        if answer[5][i] == self.user_address:
                            new_answer = []
                            estate = self.get_estate_by_id(int(answer[0]))
                            # estate_id
                            new_answer = []
                            new_answer.append(str(answer[0]))
                            # физический адрес
                            new_answer.append(str(estate[2]))
                            # общая площадь
                            new_answer.append(str(estate[3]))
                            # полезная площадь
                            new_answer.append(str(estate[4]))
                            # цена, установленная продавцом
                            new_answer.append(str(answer[2]))
                            # дедлайн
                            new_answer.append(str(answer[4]))
                            # добавить кто предложил
                            new_answer.append(str(answer[5][i]))
                            # добавить сколько предложили
                            new_answer.append(str(answer[6][i]))
                            list_of_sales.append(new_answer)
        return list_of_sales

    # КНОПКА
    # РАБОТАЕТ
    def create_sale(self, estate_id, price, deadline):
        '''
        :param estate_id:
        :param price: продавец указывает цену недвижимости в эфире
        :param deadline: срок окончания продажи в днях
        :return:
        '''
        estate_id = int(estate_id)
        price = int(price)
        deadline = int(deadline) * 86400
        answer = self.ws.functions.get_estates(estate_id).call()
        print(answer)
        if self.user_address == web3.Web3.toChecksumAddress(answer[1]):
            self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
            self.w3.miner.start(1)
            tx = self.ws.functions.create_sale(estate_id, price, deadline).transact({'gas': 900000})
            self.w3.eth.waitForTransactionReceipt(tx)
            self.w3.miner.stop()

    # РАБОТАЕТ
    def check_to_buy(self, estate_id, price):
        '''
        Покупатель выбирает недвижимость, которую он хочет купить
        :param estate_id: индекс собственности
        :param price: цена в эфире
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.check_to_buy(estate_id).transact({'to': self.contract_address, 'from': self.user_address, 'value': Web3.toWei(price, 'wei'), 'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def cancel_sale(self, estate_id):
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.cancel_sale(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def cancel_to_buy(self, estate_id):
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.cancel_to_buy(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def confirm_sale(self, estate_id, customer):
        estate_id = int(estate_id)
        customer = Web3.toChecksumAddress(str(customer))
        number = self.get_sales_number()
        for i in range(number):
            sale_id = i
            sale = self.get_sale_by_id(sale_id)
            if sale[1] != '0x0000000000000000000000000000000000000000' and sale[0] == estate_id:
                for j in range(len(sale[5])):
                    cus = Web3.toChecksumAddress(sale[5][j])
                    if cus == customer:
                        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
                        self.w3.eth.defaultAccount = self.user_address
                        self.w3.miner.start(1)
                        tx = self.ws.functions.confirm_sale(estate_id, j).transact({'gas': 9000000})
                        self.w3.eth.waitForTransactionReceipt(tx)
                        self.w3.miner.stop()



    # ЗАЛОГИ

    # РАБОТАЕТ
    def get_pledges_number(self):
        number = self.ws.functions.get_pledges_number().call()
        return number

    # РАБОТАЕТ
    def get_pledge_by_id(self, pledges_id):
        try:
            number = self.ws.functions.get_pledges(pledges_id).call()
        except Exception:
            number = False
        return number

    # РАБОТАЕТ
    def can_pledge(self):
        '''
        Взять под залог / Таблица 1 / Моя собственность
        :return:
        '''
        list_of_pledge = []
        estates_number = self.get_estates_number()
        for id in range(estates_number):
            status = self.ws.functions.get_estates_statuses(id).call()
            if (not status[0]) and (not status[1]) and (not status[2]):
                answer = self.ws.functions.get_estates(id).call()
                if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                    answer.pop(1)
                    for j in range(len(answer)):
                        answer[j] = str(answer[j])
                    list_of_pledge.append(answer)
        return list_of_pledge

    # КНОПКА
    # РАБОТАЕТ
    def create_pledge(self, estate_id, price, time):
        '''
        Взять под залог / Кнопка 1 / Заложить
        :param estate_id:
        :param price:
        :param time:
        :return:
        '''
        estate_id = int(estate_id)
        time = int(time) * 86400
        answer = self.get_estate_by_id(estate_id)
        print(answer)
        if self.user_address == web3.Web3.toChecksumAddress(answer[1]):
            self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
            self.w3.miner.start(1)
            tx = self.ws.functions.create_pledge(estate_id, price, time).transact({'gas': 9000000})
            self.w3.eth.waitForTransactionReceipt(tx)
            self.w3.miner.stop()

    # РАБОТАЕТ
    def my_pledges(self):
        '''
        Взять под залог / Таблица 2 / Мои залоги
        :return:
        '''
        list_of_pledges = []
        new_answer = []
        number = self.get_pledges_number()
        for id in range(number):
            pladge = self.get_pledge_by_id(id)
            if not pladge:
                continue
            if web3.Web3.toChecksumAddress(pladge[1]) == self.user_address:
                estate = self.get_estate_by_id(int(pladge[0]))
                # estate_id
                new_answer.append(str(estate[0]))
                # Физический адрес
                new_answer.append(str(estate[2]))
                # Общая площадь
                new_answer.append(str(estate[3]))
                # Полезная площадь
                new_answer.append(str(estate[4]))
                # Сумма залога
                new_answer.append(str(pladge[3]))
                # За сколько выдаст залог
                new_answer.append(str(int(pladge[4]/86400)))
                list_of_pledges.append(new_answer)
        return list_of_pledges

    # КНОПКА
    # РАБОТАЕТ
    def cancel_pledge(self, estate_id):
        '''
        Выдать под залог / кнопка 2 / отменить
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.cancel_pledge(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def pledges_when_i_find_money(self):
        '''
        Выдать под залог / Таблица 3 / Получить залоги
        :return:
        '''
        list_of_pledges = []
        number = self.get_pledges_number()
        for id in range(number):
            answer = self.ws.functions.get_pledges(id).call()
            if answer[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(answer[1]) == self.user_address:
                    if answer[2] != web3.Web3.toChecksumAddress('0x0000000000000000000000000000000000000000'):
                        estate = self.get_estate_by_id(answer[0])
                        new_answer = []
                        new_answer.append(str(answer[0]))
                        new_answer.append(str(estate[2]))
                        new_answer.append(str(estate[3]))
                        new_answer.append(str(estate[4]))
                        new_answer.append(str(answer[2]))
                        new_answer.append(str(answer[3]))
                        new_answer.append(str(int(answer[4]/86400)))
                        list_of_pledges.append(new_answer)
        return list_of_pledges

    # КНОПКА
    # РАБОТАЕТ
    def confirm_pledge(self, estate_id):
        '''
        Взять под залог / кнопка 3 / Принять
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.confirm_pledge(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # КНОПКА
    # РАБОТАЕТ
    def refuse_pledge(self, estate_id):
        '''
        Взять под залог / кнопка 4 / отказать
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.refuse_pledge(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def pledges_when_i_get_money(self):
        '''
        Выдать под залог / Таблица 3 / Выданные мне залоги
        :return:
        '''
        list_of_pledges = []
        number = self.get_pledges_number()
        for id in range(number):
            pledge = self.ws.functions.get_pledges(id).call()
            if pledge[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(pledge[1]) == self.user_address:
                    if pledge[2] != web3.Web3.toChecksumAddress('0x0000000000000000000000000000000000000000'):
                        if pledge[5]:
                            new_answer = []
                            estate = self.get_estate_by_id(pledge[0])
                            new_answer.append(str(pledge[0]))
                            new_answer.append(str(estate[2]))
                            new_answer.append(str(estate[3]))
                            new_answer.append(str(estate[4]))
                            new_answer.append(str(pledge[2]))
                            new_answer.append(str(pledge[3]))
                            new_answer.append(time.ctime(int(pledge[5])))
                            list_of_pledges.append(new_answer)
        return list_of_pledges

    # КНОПКА
    # РАБОТАЕТ
    def finish_pledge(self, estate_id):
        '''
        Взять под залог / кнопка 5 / вернуть
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        pledge_id = self.ws.functions.get_pledgeID_by_estateID(estate_id).call()
        print(pledge_id)
        pledge_id = int(pledge_id)
        pledge = self.get_pledge_by_id(pledge_id)
        if pledge:
            price = pledge[3]
            self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
            self.w3.miner.start(1)
            tx = self.ws.functions.finish_pledge(estate_id).transact({'gas': 9000000, 'value': price})
            self.w3.eth.waitForTransactionReceipt(tx)
            self.w3.miner.stop()

    # РАБОТАЕТ
    def choose_pledge(self):
        '''
        Выдать залог / Таблица1 / Выберите, чтобы выдать залог"
        :return:
        '''
        list_of_pledges = []
        number = self.get_pledges_number()
        for id in range(number):
            pladge = self.ws.functions.get_pledges(id).call()
            if pladge[1] != '0x0000000000000000000000000000000000000000':
                new_answer = []
                estate = self.get_estate_by_id(int(pladge[0]))
                # estate_id
                new_answer.append(str(estate[0]))
                # Кто выдает под залог
                new_answer.append(str(pladge[1]))
                # Физический адрес
                new_answer.append(str(estate[2]))
                # Общая площадь
                new_answer.append(str(estate[3]))
                # Полезная площадь
                new_answer.append(str(estate[4]))
                # Сумма залога
                new_answer.append(str(pladge[3]))
                # Срок
                new_answer.append(str(int(pladge[4] / 86400)))
                list_of_pledges.append(new_answer)
        return list_of_pledges

    # КНОПКА
    # РАБОТАЕТ
    def check_to_pledge(self, estate_id):
        '''
        Выдать залог / Кнопка 1 / Выдать
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        pledge_id = self.ws.functions.get_pledgeID_by_estateID(estate_id).call()
        pledge_id = int(pledge_id)
        pledge = self.get_pledge_by_id(pledge_id)
        if pledge:
            price = pledge[3]
            self.w3.personal.unlockAccount(self.user_address, self.passfrase)
            self.w3.eth.defaultAccount = self.user_address
            self.w3.miner.start(1)
            tx = self.ws.functions.check_to_pledge(estate_id).transact({'gas': 9000000, 'value':price})
            self.w3.eth.waitForTransactionReceipt(tx)
            self.w3.miner.stop()

    # РАБОТАЕТ
    def choose_to_cancel_pledge(self):
        '''
        Выдать залог / Таблица 2 / Предложенные мной залоги
        :return:
        '''
        list_of_pledges = []
        number = self.get_pledges_number()
        for id in range(number):
            answer = self.ws.functions.get_pledges(id).call()
            if answer[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(answer[2]) == self.user_address:
                    estate = self.get_estate_by_id(answer[0])
                    new_answer = []
                    new_answer.append(str(answer[0]))
                    new_answer.append(str(answer[1]))
                    new_answer.append(str(estate[2]))
                    new_answer.append(str(estate[3]))
                    new_answer.append(str(estate[4]))
                    new_answer.append(str(answer[3]))
                    new_answer.append(str(int(answer[4]/86400)))

                    list_of_pledges.append(new_answer)
        return list_of_pledges

    # КНОПКА
    # РАБОТАЕТ
    def cancel_to_pledge(self, estate_id):
        '''
        Выдать залог / кнопка 2 / Отменить
        :param estate_id:
        :return:
        '''
        estate_id = int(estate_id)
        self.w3.personal.unlockAccount(self.user_address, self.passfrase)
        self.w3.eth.defaultAccount = self.user_address
        self.w3.miner.start(1)
        tx = self.ws.functions.cancel_to_pledge(estate_id).transact({'gas': 9000000})
        self.w3.eth.waitForTransactionReceipt(tx)
        self.w3.miner.stop()

    # РАБОТАЕТ
    def pledges_im_waiting_for(self):
        '''
        Выдать залог / Таблица 3 / Выданные мною залоги
        :return:
        '''
        list_of_pledges = []
        number = self.get_pledges_number()
        for id in range(number):
            pledge = self.ws.functions.get_pledges(id).call()
            if pledge[1] != '0x0000000000000000000000000000000000000000':
                if web3.Web3.toChecksumAddress(pledge[1]) == self.user_address:
                    if pledge[2] != web3.Web3.toChecksumAddress('0x0000000000000000000000000000000000000000'):
                        if pledge[5]:
                            new_answer = []
                            estate = self.get_estate_by_id(pledge[0])
                            new_answer.append(str(pledge[0]))
                            new_answer.append(str(estate[2]))
                            new_answer.append(str(estate[3]))
                            new_answer.append(str(estate[4]))
                            new_answer.append(str(pledge[1]))
                            new_answer.append(str(pledge[3]))
                            new_answer.append(time.ctime(int(pledge[5])))
                            list_of_pledges.append(new_answer)
        return list_of_pledges
