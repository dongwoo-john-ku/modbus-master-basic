from pymodbus.client.sync import ModbusTcpClient

IP_ADDRESS = '192.168.1.100'
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

def close(c):
    c.close()
    print("Modbus/TCP Connection is Closed\n")
