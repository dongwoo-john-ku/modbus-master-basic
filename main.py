from pymodbus.client.sync import ModbusTcpClient
import time

IP_ADDRESS = 'localhost' #IP Address of FEN20-4IOL
SERVER_PORT = 502 # Modbus/TCP default Port
START_ADDR = 0
LENGTH = 10

def modbustcp_client(host, port):
    c = ModbusTcpClient(host, port)
    return c

if __name__ == "__main__":
    while True:
        c = modbustcp_client(host=IP_ADDRESS, port=SERVER_PORT)
        try:
            readDataList = c.read_input_registers(START_ADDR,LENGTH).registers[START_ADDR:LENGTH]
        except:
            print('Not Connected')
        else:
            print('Connected')
            print(readDataList)
            c.close()
            time.sleep(1)



