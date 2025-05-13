import serial         # Importerer pyserial-biblioteket til seriel kommunikation med Arduino
import time           # Bruges til at vente efter Arduino reset
import csv            # Bruges til at skrive til en CSV-fil
from datetime import datetime  # Bruges til at tilføje tidsstempel til hver måling
import threading
# test

# Denne funktion modtager data fra Arduino via seriel kommunikation og gemmer det i en CSV-fil.
def run_reciever():

    # Åben seriel port (skal muligvis tilpasses hvis nødvendigt, f.eks. port: /dev/ttyUSB0 i stedet for)
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Venter 2 sekunder for at give Arduino tid til at genstarte og blive klar

    # Navn på CSV-filen, hvor data gemmes
    csv_filename = "sensor_data.csv"

    # Åbner CSV-filen i append-mode(dvs. nye data bliver gemt/tilføjet i bunden af filen i stedet for at overskrive de eksisterende)
    # og newline='' sikrer at der ikke kommer tomme linjer mellem hver måling
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)  # opretter en CSV skriver-objekt(writer) som gør at man kan skrive data i korrekt CSV format.
        if file.tell() == 0:  # Tilføjer kolonneoverskrifter, hvis filen er tom(nyoprettet)
            writer.writerow(["timestamp", "WIND_DIR", "WIND_SPEED", "POWER", "WIND_DIR_CHANGE"])

     
    # first_line_skipped = False # Flag til at springe den første linje over

    # Vent et øjeblik for at sikre, at Arduino er klar
    time.sleep(1)

    # Tømseriel buffer for at sikre, at der ikke er gamle data
    ser.reset_input_buffer()
            
    print("Starter modtagelse af data...")  # Besked når programmet starter.

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()

            #if not fitst_line_skipped:
            #    print(f"Ignorere det første set af data: {line}")
            #    fitst_line_skipped = True
            #    continue

            # Ignorer tomme linjer
            if not line:
                continue

            # Debugging: Vis den rå linje fra Arduino
            print(f"Raw line: {line}")

            data = parse_data(line)

            if data:
                print(f"Vindretning: {data['WIND_DIR']} grader, "
                    f"Vindhastighed: {data['WIND_SPEED']} m/s, "
                    f"Effekt: {data['POWER']} W, "
                    f"Retningsændring: {data['WIND_DIR_CHANGE']} grader")

                timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        timestamp,
                        data['WIND_DIR'],
                        data['WIND_SPEED'],
                        data['POWER'],
                        data['WIND_DIR_CHANGE']
                    ])

# Funktion der parser en tekstlinje fra Arduino til en dictionary med key:value-par
# Dvs den analysere og omdanner tekstlinjen til data som python kan arbejde med.    
def parse_data(line):
    try:
        data = {}
        parts = line.split(',')
        for part in parts:
            if ':' not in part:
                raise ValueError(f"Mislykkedes data: {part}")
            key, value = part.split(':')
            data[key.strip()] = float(value.strip())
        return data
    except Exception as e:
        print(f"Parse error: {e}")
        return None




def start_receiver_thread():
    threading.Thread(target=run_reciever, daemon=True).start()


if __name__ == "__main__":
    run_reciever()  # Kald funktionen til at starte modtagelse af data