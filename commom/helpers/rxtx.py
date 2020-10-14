# -*- coding: utf-8 -*-
import time
from threading import Thread
from serial import Serial


class RxTx(Serial):
    """
        Classe que implementa a leitura da porta serial (uart)
        * class      RxTx, Serial, Thread
        * requires   python 3.7
        * version    1.0.0
        * developer  Alcindo Schleder <alcindo.schleder@amcom.com.br>
    """

    flag_thread = True
    thread = None
    stop_threads = True
    result_data = []

    def __init__(self, serial_port: str, serial_baudrate: int = 9600, use_thread: bool = True):
        """
        Contrutor da classe
        @param serial_port: nome da porta serial (Linux: '/dev/śerial0' | win: 'COM2'
        @param serial_baudrate: Taxa de transmissão dos dados
        @param use_thread: Se a classe deve usar uma thread para criar o looping de leitura
        """
        if serial_port == '' or serial_port is None:
            raise Exception('A porta serial deve ser informada!')
        self.flag_thread = use_thread
        try:
            super(RxTx, self).__init__(port=serial_port, baudrate=serial_baudrate, timeout=1)
        except Exception as e:
            raise Exception(f'Erro ao conectar na porta Serial ({serial_port}) '
                            f'com baudrate em {serial_baudrate}!\n    Error: {e}')

    def handle_data(self, data) -> dict:
        """
        Função usada para decodificar a mensagem da porta serial
        @param data: string ou dict: Sendo uma string é uma mensagem que necessita ser trabalhada
                                     para separar os vários campos da string
                                     Sendo um dicionário é uma mensagem que tem os campos definidos
                                     a mensagem e o status da mensagem
        @return:
        """
        msg = ''
        if type(data) == str:
            msg = data.replace('/r', '')
            #TODO: split string here
            data = {"status": 200, "msg": msg}
        elif type(data) == dict:
            msg = data['msg']
        print(msg)
        return data

    def read_from_port(self, stop: bool = True) -> str:
        """
        Função para ler o buffer da porta serial
        @param stop: Se False Finaliza o looping
        @return: string
        """
        self.stop_threads = stop
        while True:
            data = self.readline().decode()
            if data != '':
                data = self.handle_data(data)
            if self.stop_threads:
                break
        self.result_data.apend(data)
        return data

    def start(self):
        """
        Função que inicia a leitura do buffer serial por thread
        Obs: para ler o buffer sem Thread deve usar a função da classe pai read(), readline() ou readlines().
             Porém se quiser pode chamar o looping de read_from_port(True) passando o parametro stop como True.
        @return: void
        """
        self.result_data = []
        if self.flag_thread:
            self.thread = Thread(target=self.read_from_port, args=(False, ))
        self.thread.start()

    def write(self, command: str, slot: int = 0) -> dict:
        """
        Sobreescreve a função write
        @param command: Comando a ser enviado para a porta serial
        @param port: Número do dispenser a ser comandado pelo arduino
        @return: void
        """
        self.result_data = []
        if command not in ['entregar', 'status']:
            data = self.handle_data({"status": "404", "msg": f"Comando {command} não existe!"})
            return data
        elif 0 > slot > 31:
            data = self.handle_data({"status": "403", "msg": f"Slot {slot} é inválida para o Comando {command}!"})
            return data
        # Chama a função write da classe pai
        super().write(f"{command}={slot}\n".encode('utf-8'))
        time.sleep(1)
        return {}

    def stop(self) -> list:
        """
        Função para parar a leitura da serial
        @return: void
        """
        if self.flag_thread and self.thread is not None:
            self.stop_threads = True
            self.thread.join()
        self.close()
        return self.result_data
