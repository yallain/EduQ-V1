
import csv
import time
import serial
import datetime

# Prog de savegarde et de colelcte des données dans un fichier CSV  en provenance du FPGA via la liaison Serie
# Date : 14 09 2023

# Prog de collecte des données en provenance du FPGA via la liaison Serie
# Date : 14 09 2023
# Permet de récuprer les 10 registres dans le bon ordre avec un tripplet de valeur pour chaque registre 
# Registre 0 0 -> décimal
# registre 0 1 -> binaire
# registre 0 3 -> hexa
# registre 1 0 //etc

nombre_registres = 10
# Header binaire à rechercher
header_to_find = 12345678 # ancienne valeur 2576980377 # Valeur du Header en décimal - 10011001100110011001100110011001

registres= []

# Configuration de la liaison série
baud_rate = 19200
stop_bits = 1
start_bits = 1
parity = serial.PARITY_NONE
serial_port = "COM4"
# Création de l'objet de liaison série
ser = serial.Serial(serial_port, baud_rate, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

# Fonction pour obtenir un horodatage au format ISO 8601
def get_timestamp():
    now = datetime.datetime.now()
    return now.isoformat()

def lire_registres(ser, nombre_registres):
    registres = []
    for _ in range(nombre_registres):
        donnees = ser.read(4)  # Lire 4 octets (32 bits)
        
        # Inverser les octets dans les données
        donnees_inversees = donnees[::-1]
        
        registre_decimal = int.from_bytes(donnees_inversees, byteorder='big', signed=False)
        registre_binaire = bin(registre_decimal)[2:].zfill(32)
        registre_hexa = hex(registre_decimal)[2:].zfill(8)
        registres.append((registre_decimal, registre_binaire, registre_hexa))
        print(f"Registre décimal: {registre_decimal}, binaire: {registre_binaire}, hexadécimal: 0x{registre_hexa}")
    return registres



with open('data.csv', 'w') as csv_file:
    fieldnames = ["TimeStamp","NbrPulseA", "NbrPulseB", "NbrPulseC", "NbrPulseD", "NbrCoincidencePulseAB", "NbrCoincidencePulseAC", "NbrCoincidencePulseDB", "NbrCoincidencePulseDC", "NbrCoincidencePulseABC"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    # Lire les 10 registres
    registres = lire_registres(ser, 10)
    
    # Vérifier si le registre n°1 contient la valeur 12345678 
    # BUG dans la liason serie ou de décodage en python . Une valeur apparait de temps en temps dans les coincdences. 16777216 16777216. Donc pour contourner, si elle est présente
    # j'enleve le registre
    if registres[0][2] == '12345678': 
        print("Les 10 registres : ", registres) 
        print("!!!! Header en position 1 Trouvé !!!!! ")
        with open('data.csv', 'a') as csv_file1:
            csv_writer = csv.DictWriter(csv_file1, fieldnames=fieldnames)
            info = {
            "TimeStamp" : get_timestamp(),
            "NbrPulseA": registres[1][0], 
            "NbrPulseB": registres[2][0],
            "NbrPulseC": registres[3][0],
            "NbrPulseD": registres[4][0],
            "NbrCoincidencePulseAB": registres[5][0],
            "NbrCoincidencePulseAC": registres[6][0],
            "NbrCoincidencePulseDB": registres[7][0],
            "NbrCoincidencePulseDC": registres[8][0],
            "NbrCoincidencePulseABC": registres[9][0]        
            }

            csv_writer.writerow(info)
            print(registres[0])
            print(info)
            registres.clear()
    else:
        print("Le registre n°1 ne contient pas la valeur attendue.")
        # Réinitialiser tous les registres à zéro
        registres = [0] * 10
    
    # Relancer une acquisition de données depuis la liaison série
    ser.flushInput()  # Vider le tampon d'entrée
    #time.sleep(0.3)