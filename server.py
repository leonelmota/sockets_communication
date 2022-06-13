import socket
import sys
import random
from typing import List

sensors_in_equipments = {'01': [], '02': [], '03': [], '04': []}
valid_sensors = ['01', '02', '03', '04']
valid_equipments = ['01', '02', '03', '04']
number_of_sensors = 0
MAX_SENSORS = 15

def get_random_numbers_str(size : int) -> List[str]:
    return [f"{(random.randint(0, 1000) / 100.0):.2f}" for i in range(size)]


def process_msg(msg : str) -> str:
    msg_split = msg.split(' ')
    print(msg_split)
    equipment = msg_split[-1]
    global number_of_sensors
    
    if msg_split[:2] == ['add', 'sensor']:
        if equipment not in valid_equipments:
            return "invalid equipment"

        sensors = msg_split[2:-2]

        for sensor in sensors:
            if sensor not in valid_sensors:
                return "invalid sensor"
        
        installed_sensors = [s for s in sensors if s in sensors_in_equipments[equipment]]
        if len(installed_sensors):
            return_msg = f"sensor {' '.join(installed_sensors)} already exists in {equipment}"
        else:
            for sensor in list(set(sensors)):
                sensors_in_equipments[equipment].append(sensor)
                number_of_sensors+=1
            return_msg = f"sensor {' '.join(sensors)} added"
        if number_of_sensors > 15:
            return_msg = "limit exceeded"
        return return_msg

    elif msg_split[:2] == ['remove', 'sensor']:
        if equipment not in valid_equipments:
            return "invalid equipment"
        sensor = msg_split[2]
        if sensor in sensors_in_equipments[equipment]:
            sensors_in_equipments[equipment].remove(sensor)
            number_of_sensors -= 1
            return f"sensor {sensor} removed"
        else:
            return f"sensor {sensor} does not exist in {equipment}"
        
    elif msg_split[:3] == ['list', 'sensors', 'in']:
        if equipment not in valid_equipments:
            return "invalid equipment"
        if len(sensors_in_equipments[equipment]) == 0:
            return "none"
        else:
            return_msg = "" 
            for sensor in sensors_in_equipments[equipment]:
                return_msg += sensor + " "
            return return_msg.strip()
    
    elif msg_split[0] == 'read' and msg_split[-2] == 'in':
        if equipment not in valid_equipments:
            return "invalid equipment"
        sensors = msg_split[1: -2]
        not_installed_sensors = [s for s in sensors if s not in sensors_in_equipments[equipment]]
        
        if len(not_installed_sensors):
            not_installed_sensors_str = ' '.join(not_installed_sensors)
            return_msg = f"sensor(s) {not_installed_sensors_str} not installed"
        else:
            rand_numbers = get_random_numbers_str(len(sensors))
            return_msg = ' '.join(rand_numbers)
        return return_msg

    else:
        return ''
    

if __name__ == '__main__':
    IP_VERSION = sys.argv[1]
    PORT = int(sys.argv[2])

    AF = socket.AF_INET if IP_VERSION == 'v4' else socket.AF_INET6

    running_server = True
    
    with socket.socket(AF, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))

        while running_server:      
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(500)
                    msg = data.decode()
                    if msg == "kill":
                        running_server = False
                        break
                    else:
                        return_msg = process_msg(msg)

                    if not return_msg:
                        break
                    print(msg)
                    print("return", return_msg)

                    conn.sendall(return_msg.encode())