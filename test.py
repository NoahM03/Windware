test_data = [
"WIND_DIR:45,WIND_SPEED:3.2,POWER:50,WIND_DIR_CHANGE:2",
"WIND_DIR:45,WIND_SPEED:3.2,POWER:50,WIND_DIR_CHANGE:2",
"WIND_DIR:45,WIND_SPEED:3.2,POWER:50,WIND_DIR_CHANGE:2",
"WIND_DIR:45,WIND_SPEED:3.2,POWER:50,WIND_DIR_CHANGE:2",
"WIND_DIR:45,WIND_SPEED:3.2,POWER:50,WIND_DIR_CHANGE:2",
"WIND_DIR:47,WIND_SPEED:3.4,POWER:52,WIND_DIR_CHANGE:2",
"WIND_DIR:50,WIND_SPEED:4.1,POWER:60,WIND_DIR_CHANGE:3",
"WIND_DIR:55,WIND_SPEED:4.5,POWER:68,WIND_DIR_CHANGE:5",
"WIND_DIR:60,WIND_SPEED:4.8,POWER:70,WIND_DIR_CHANGE:5",
"WIND_DIR:65,WIND_SPEED:5.0,POWER:74,WIND_DIR_CHANGE:5",
"WIND_DIR:70,WIND_SPEED:5.2,POWER:80,WIND_DIR_CHANGE:5",
"WIND_DIR:75,WIND_SPEED:5.5,POWER:85,WIND_DIR_CHANGE:5",
"WIND_DIR:80,WIND_SPEED:5.8,POWER:90,WIND_DIR_CHANGE:5",
"WIND_DIR:85,WIND_SPEED:1.0,POWER:95,WIND_DIR_CHANGE:5"


]

def parse_data(line):
    try:
        data = {}                                # Tom dictionary til at gemme data
        parts = line.split(',')                  # Splitter linje op ved komma
        for part in parts:
            key, value = part.split(':')         # Splitter hvert element op ved kolon
            data[key.strip()] = float(value.strip())  # Fjerner mellemrum og konverter til float
        return data                              # Returnér det færdige dictionary
    except Exception as e:
        print(f"Parse error: {e}")               # Viser fejl hvis noget går galt
        return None

for line in test_data:
    data = parse_data(line)

pre_Wind_speed_data = []
pre_Wind_direction_data = []

# Sortere data

def sort_data(data):
    pre_Wind_speed_data.append(data["WIND_SPEED"])
    pre_Wind_direction_data.append(data["WIND_DIR"])

# Prøv med test data
for line in test_data:
    data = parse_data(line)
    if data:
        sort_data(data)

print(pre_Wind_speed_data)

