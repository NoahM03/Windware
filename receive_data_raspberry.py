import serial         # Importerer pyserial-biblioteket til seriel kommunikation med Arduino
import time           # Bruges til at vente efter Arduino reset
import csv            # Bruges til at skrive til en CSV-fil
from datetime import datetime  # Bruges til at tilføje tidsstempel til hver måling

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
            
            
    print("Starter modtagelse af data...")  # Besked når programmet starter.

    # Uendelig løkke – lytter hele tiden på den serielle port(fra Arduino)
    while True:
        if ser.in_waiting > 0:  # Tjekker om der er data klar i den serielle buffer
            line = ser.readline().decode('utf-8').strip()  # Læser én linje og dekoder den til tekst
            data = parse_data(line)  # Parser tekstlinjen til dictionary

            if data:  # Hvis parsing lykkedes
                print(f"Vindretning: {data['WIND_DIR']} grader, "
                      f"Vindhastighed: {data['WIND_SPEED']} m/s, "
                      f"Effekt: {data['POWER']} W, "
                      f"Retningsændring: {data['WIND_DIR_CHANGE']} grader")  # Udskriver data læsbart

                # Opretter et timestamp for målingen
                timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # henter den aktuelle dato og klokkeslæt
                # og formaterer det til en læsbar tekst efter skabelon f.eks. "08-05-2025 xx:xx:xx"

                # Åbner CSV-filen igen og gemmer/tilføjer én ny række med måledata i CSV-filen med tidsstempel
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
        data = {}  # Opretter tom dictionary til at gemme data
        parts = line.split(',')  # Splitter linjen op ved komma
        for part in parts:
            key, value = part.split(':')  # Splitter hver del i nøgle og værdi adskilt af kolon
            data[key.strip()] = float(value.strip())  # Fjerner mellemrum og konverterer til float
        return data  # Returnerer den færdige dictionary
    except Exception as e:
        print(f"Parse error: {e}")  # Viser fejl hvis noget går galt
        return None


run_reciever()
