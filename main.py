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
    ser = serial.Serial("COM11", baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5)
    csv_file = open("data/temp_data.csv", "a")

    while True:
        temperature = read_temperature_from_device(ser)

        # Print the temperature value
        if temperature is not None:
            csv_file.write(f"{temperature}\n")
            print(temperature)

    csv_file.close()
    ser.close()