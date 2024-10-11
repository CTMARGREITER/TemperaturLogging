import serial

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

    # Open the serial port and connect to device COM11 with the given parameters
    com_ports = ["COM11", "COM12", "COM13", "COM14"]
    serial_devices = []

    for com_port in com_ports:
        ser = serial.Serial(com_port,
                            baudrate=1200,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1.0)
        serial_devices.append(ser)
    
    csv_file = open("./data/temp_data.csv", "a")

    while True:

        temperatures = []
        for ser in serial_devices:
            temperature = read_temperature_from_device(ser)
            temperatures.append(temperature)

        if not None in temperatures:
            csv_file.write("; ".join(map(str, temperatures)) + "\n")
            print(temperatures)
        else:
            print(f"Error reading data for one of the devices: {temperatures}")
           
    csv_file.close()
    for ser in serial_devices:
        ser.close()