#Programa que genera medidas de humedad en el suelo
import RPi.GPIO as GPIO
import time


#set our gpio numbering to bcm
GPIO.setmode(GPIO.BCM)
#Definir el pin GPIO  a usar, en este caso el 21
channel=21
#POner el in GPIO como input
GPIO.setup(channel, GPIO.IN)
#Funcion para obtener el valor del pin digital
def medirHumedad():
    valor=GPIO.input(21)
    if valor == 0:
        print("Humedo")#nivel bajo indica presencia de agua
    else:
        print("Seco")

print("Sensor de humedad en tierra")
#Ciclo infinito para medir la humedad cada 2 segundos
while True:
    medirHumedad()
    time.sleep(1)