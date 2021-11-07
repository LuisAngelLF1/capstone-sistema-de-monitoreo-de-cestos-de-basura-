import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)

sFileStamp = time.strftime('%Y%m%d%H')
sFileName = '\out' + sFileStamp + '.txt'
f=open(sFileName, 'a')
f.write('TimeStamp,Value' + '\n')
print ("Inicia la toma de datos")

try:
	while True:
		print ("acerque el objeto para medir la distancia")
		GPIO.output(GPIO_TRIGGER,True)
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER,False)
		start = time.time()
		while GPIO.input(GPIO_ECHO)==0:
			start = time.time()
		while GPIO.input(GPIO_ECHO)==1:
			stop = time.time()
		elapsed = stop-start
		distance = (elapsed * 34300)/2
		sTimeStamp = time.strftime('%Y%m%d%H%M%S')
		f.write(sTimeStamp + ',' + str(distance) + '\n')
		print (sTimeStamp + ' ' + str(distance))
		time.sleep(1)
		sTmpFileStamp = time.strftime('%Y%m%d%H')
		if sTmpFileStamp != sFileStamp:
		  	f.close
		   	sFileName = 'out/' + sTmpFileStamp + '.txt'
		   	f=open(sFileName, 'a')
		   	sFileStamp = sTmpFileStamp
			print ("creando el archivo")

except KeyboardInterrupt:
	print ('\n' + 'termina la captura de datos.' + '\n')
	f.close
	GPIO.cleanup()