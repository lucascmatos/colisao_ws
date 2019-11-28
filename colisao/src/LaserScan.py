#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

from std_msgs .msg import Bool, Int32, Float32
from array import array

angMax=0
angMin=0
count=0
vet = []
global i
vet_ponts = []
ponto_colisao = LaserScan()

def callback(data):
   global ponto_colisao
   global vet
   vet = list(data.ranges) #Pega as distancias medidas do topico
   print len(data.ranges)
   for i in range(len(vet)): #Varre o vetor de pontos
        ponto_colisao = data

        if 0.03<vet[i]<1.0: #Checa se os pontos entao no meu range de colisao
            vet_ponts.append(vet[i])
              #ponto_colisao.ranges = vet[i]
              # d.write("%s\n" %vet[i])
               #print "Colisao"# se estiverem manda a mensagem de colisao
               #else:
               #       print "Nao vai bater"
        else :
            vet_ponts.append(data.range_min)

   ponto_colisao.ranges =  list(vet_ponts)
def deteccao_colisao():
   global check
   rospy.init_node("dados_laser",anonymous = True)#incia no do pacote
   rospy.Subscriber("/scan",LaserScan,callback)#subscreve no no do laser
   pub = rospy.Publisher("colisao",LaserScan,queue_size=10)
   rate = rospy.Rate(10)
   #f = open("/home/l/fora_colisa.txt","w")
   #d = open("/home/l/dentro_colisa.txt","w")
   while not rospy.is_shutdown():
         #f.write("%s\n" %vet[i])
        pub.publish(ponto_colisao)
   rate.sleep


if __name__== '__main__':
	try:
		deteccao_colisao()
	except rospy.ROSInterruptException:
		pass
