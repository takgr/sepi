import tkinter as tk
from tkinter import font
import time
from pymodbus.client import ModbusTcpClient  # Correct import for the latest pymodbus

# Configuration for Modbus TCP
INVERTER_IP = '192.168.1.100'  # IP address of the inverter
MODBUS_PORT = 1502  # Modbus TCP port (1502 for SolarEdge)
REGISTER_POWER = 40101  # Modbus register address for current power

# Function to fetch solar production data from Modbus TCP
def fetch_current_production():
    try:
        # Create a Modbus TCP client
        client = ModbusTcpClient(INVERTER_IP, port=MODBUS_PORT)
        client.connect()

        # Read holding register (Modbus register 40101 for current power)
        # Note: Registers are 0-indexed in pymodbus, so subtract 1 from actual address
        response = client.read_holding_registers(REGISTER_POWER - 1, 1)

        if response.isError():
            print(f"Modbus Error: {response}")
            return None

        # The register value is in response.registers[0], scaled in watts
        current_power = response.registers[0]  # Typically, it's already in watts, no scaling needed

        client.close()
        return current_power
    except Exception as e:
        print(f"Exception occurred while reading Modbus: {e}")
        return None

# Function to update the display with the latest solar power data
def update_display():
    current_power = fetch_current_production()
    if current_power is not None:
        power_label.config(text=f"Solar: {current_power} W")
    else:
        power_label.config(text="Error fetching solar data")
    
    # Refresh the data every 60 seconds
    root.after(1000, update_display)

# Setup the main GUI window
root = tk.Tk()
root.title("SolarEdge Solar Production")
root.geometry("640x480")  # Raspberry Pi touchscreen resolution

# Set full screen mode
root.attributes("-fullscreen", True)

# Set the background color to black
root.configure(bg='black')

# Set a nice retro computer font
my_font = font.Font(family='Courier', size=36, weight='bold')

# Label to display current solar production
power_label = tk.Label(root, text="Fetching Solar Data...", font=my_font, fg='red', bg='black')
power_label.pack(pady=20)

# Update the display for the first time
update_display()

# Start the Tkinter main loop
root.mainloop()
