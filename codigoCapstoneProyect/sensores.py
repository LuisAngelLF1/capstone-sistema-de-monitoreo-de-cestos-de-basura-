import RPi.GPIO as GPIO#se importa la libreria para manejar los pines de la raspberry
import time #libreria para funcionalidaes relacionadas al tiempo
from datetime import datetime
import paho.mqtt.client
import dht11

GPIO.setmode(GPIO.BCM) #se establece el modo BCM de los pines raspberry
GPIO_TRIGGER = 23 #trigger del sensor hcr04
GPIO_ECHO    = 24 #echo del sensor hcr04

GPIO.setup(GPIO_TRIGGER,GPIO.OUT) #establece el pin trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN) #establece el pin echo como entrada
GPIO.output(GPIO_TRIGGER, False) #pin de salida trigger inicialmente apagado
GPIO.setwarnings(False)

instance = dht11.DHT11(pin = 4)

#MQTT
def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
client = paho.mqtt.client.Client(client_id='sensorDistancia', clean_session=False)
client.connect(host='localhost', port=1883)

sFileStamp = time.strftime('%Y %m %d %H')#formato año mes dia hora
sFileName = '\out' + sFileStamp + '.txt' #se concatena el formato con la extension .txt
f=open(sFileName, 'a') #manejador archivo, open(file, mode) 'a'-append abre el archivo para añadir, crea archivo si no existe
f.write('TimeStamp,Value' + '\n') #se escribe en el archivo
print ("Inicia la toma de datos") #impresion en consola

try: #manejo de excepciones
	while True: #inicio bucle while
		print ("acerque el objeto para medir la distancia") #impresion por consola
		GPIO.output(GPIO_TRIGGER,True) #la salida trigger encendido
		time.sleep(0.00001) # espera de 10 micros 0.00001s 
		GPIO.output(GPIO_TRIGGER,False) #salida trigger apagado
		start = time.time() #se inicia un tiempo
		while GPIO.input(GPIO_ECHO)==0: #mientras el echo apagado
			start = time.time() #registro de inicio de tiempo
		while GPIO.input(GPIO_ECHO)==1:# mientras echo encendido
			stop = time.time()# registro alto de tiempo
		elapsed = stop-start #resta para saber lapso de tiempo
		distance = (elapsed * 34300)/2 #formula para saber la distancia basado en el tiempo
		sTimeStamp = time.strftime('%Y/%m/%d %H:%M:%S') #formato año mes dia hora minuto segundo

		f.write(sTimeStamp + ', D:' + str(distance) + '\n') #se escribe en el archivo formato, cadena de la distancia
		print (sTimeStamp + ', D: ' + str(distance)) #se muestra en consola
		
		#Lectura del sensor DTH11
		result = instance.read()
		if result.is_valid():
			f.write(sTimeStamp + ', T:' + str(result.temperature) + 'C\n') #se escribe en el archivo formato, cadena de la distancia
			print (sTimeStamp + ', T: ' + str(result.temperature)+ 'C') #se muestra en consola

			f.write(sTimeStamp + ', H:' + str(result.humidity) + '\n') #se escribe en el archivo formato, cadena de la distancia
			print (sTimeStamp + ', H: ' + str(result.humidity)) #se muestra en consola
			
		
		else:
			print("Error: %d" % result.error_code)
		
		
		#MQTT
		client.publish('samsung/codigoiot/casa/cesto',distance)#se publica la distancia en mqtt
		#comando para suscribirse en consola
		#mosquitto_sub -h localhost -t samsung/codigoiot/casa/cesto -q 2 -i miCliente
		#comando para publicar en consola
		#mosquitto_sub -h localhost -t samsung/codigoiot/casa/cesto -q 2 -i otroCliente
		time.sleep(1) #espera de 1s
		sTmpFileStamp = time.strftime('%Y %m %d %H') #formato auxiliar año mes dia hora
		if sTmpFileStamp != sFileStamp: #si el primer formato es distinto e este auxiliar (diferente hora)
			f.close() #cierra el archivo
			sFileName = '\out' + sTmpFileStamp + '.txt'
			f=open(sFileName, 'a') #manejador para archivo

			sFileStamp = sTmpFileStamp #actualiza sFileStamp
			print ("creando el archivo")#impresion en consola

except KeyboardInterrupt: #excepcion
	print ('\n' + 'termina la captura de datos.' + '\n')#indica fin de captura
	f.close() #cierra el archivo
	GPIO.cleanup() #limpia los pines