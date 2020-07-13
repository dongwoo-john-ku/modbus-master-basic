from pymodbus.client.sync import ModbusTcpClient
import threading

IP_ADDRESS = '192.168.1.200'
SERVER_PORT = 502

def modbustcp_client(host = IP_ADDRESS, port = SERVER_PORT):
    c = ModbusTcpClient(host, port)
    return c

def connect(c):
    if c.connect():
        print("Modbus/TCP Connected\n")
        return True
    else:
        print("Modbus/TCP Connection is Not Connected\n")
        return False

def read_input_regs(c):
    if connect(c):
        print("Modbus/TCP Connected\n")
        print("Read Input Registers\n")
        readInputRegisters = c.read_input_registers(0,100)
        # print(readInputRegisters.registers[0:100], "\n")
        return readInputRegisters
    else:
        print("Modbus/TCP Connection is Not Connected\n")
        return None

def write_output_regs(c, value):
    if connect(c):
        print("Modbus/TCP Connected\n")
        print("Write Output Registers\n")
        c.write_registers(0x4400,value)
        # print(readInputRegisters.registers[0:100], "\n")
        return True
    else:
        print("Modbus/TCP Connection is Not Connected\n")
        return None

def close(c):
    c.close()
    print("Modbus/TCP Connection is Closed\n")

value = 0
def startTimer():
    global value
    timer = threading.Timer(5, startTimer)
    timer.start()
    c = modbustcp_client(host=IP_ADDRESS, port=SERVER_PORT)

    if value == 0 :
        value = 1
    else:
        value = 0
    write_output_regs(c, value)

if __name__ == "__main__":
    startTimer()

