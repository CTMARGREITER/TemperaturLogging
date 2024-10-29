import serial

import signal
import csv
from datetime import datetime

from typing import List



terminate = False                            
def signal_handling(signum, frame):           
    global terminate                         
    terminate = True

# Expected messages in this format:
# Once per second per device
#" 37.1\n\r" == 7 bytes
def read_temperature_from_device(ser : serial.Serial) -> float:
    # Try to read one line of data that ends with the \n\r characters
    line = ser.read_until(b'\n\r').decode("utf-8")
    
    if len(line) < 7: # If the line is empty, return None
        return None
    
    line = line.strip() # Remove the \n\r characters from the line
    temperature = float(line)
    return temperature

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handling) 

    CSV_HEADER = ["Timestamp", "Temp6", "Temp5", "Temp4", "Temp3", "Temp2", "Temp1"]

    # Open the serial port and connect to device COM11 with the given parameters
    # For some reason the switch with COM port 15
    com_ports = ["COM11", "COM12", "COM13", "COM14", "COM15", "COM16"]
    bytesizes = [serial.SEVENBITS, serial.SEVENBITS, serial.SEVENBITS, serial.SEVENBITS, serial.EIGHTBITS, serial.SEVENBITS]

    serial_devices: List[serial.Serial] = []
    for com_port, bytesize in zip(com_ports, bytesizes):
        ser = serial.Serial(
            com_port,
            baudrate=1200,
            bytesize=bytesize,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1.0
        )
        serial_devices.append(ser)

    # Creat a CSV file and write the header
    with open("./data/temp_data.csv", "a", encoding="UTF8", newline="") as f:
        csv_file = csv.writer(f, delimiter=";")
        csv_file.writerow(CSV_HEADER)

        # Continously read the temperature from the device and write it to the CSV file
        while True:
            temperatures = []
            for ser in serial_devices:
                temperature = read_temperature_from_device(ser)
                temperatures.append(temperature)

            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not None in temperatures:
                temp_string = map(str, temperatures)
                row = [timestamp_str, *temp_string]

                csv_file.writerow(row)
                print(row)

            if terminate:
                print("Intercepted CTRL+C, closing the program...")
                break

    # Close the serial port
    print("Closing the serial ports...")
    for ser in serial_devices:
        ser.close()