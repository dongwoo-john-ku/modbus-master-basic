from pymodbus.client.sync import ModbusTcpClient
import time

IP_ADDRESS = '192.168.1.110' #to be changed to proper IP Address of FEN20-4IOL
SERVER_PORT = 502 # Modbus/TCP default Port

def modbustcp_client(host, port):
    c = ModbusTcpClient(host, port)
    return c

if __name__ == "__main__":
    while True:
        c = modbustcp_client(host=IP_ADDRESS, port=SERVER_PORT)
        try:
            readDataList = c.read_input_registers(1,2).registers
        except:
            print('Not Connected')
        else:
            print('Connected')
            distanceData = [readDataList[0], readDataList[1]]
            distanceDataAfter = []

            distanceData[1] >>= 3
            distanceData[0] <<= 7
            distanceData[0] >>= 7
            distanceData[0] <<= 13
            data = (distanceData[0] + distanceData[1]) / 1000
            distanceDataAfter.append(data)

            print(distanceDataAfter)
            c.close()
            time.sleep(1)



