#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import PointCloud
from array import array
from math import atan2,degrees
from std_msgs .msg import Bool, Int32
vetx = []#Vetores de pontos
vety = []
vetz = []
sum_root = 0 # soma dos quadrados dos pontos
i = 0
aux_x = 0# auxiliar da variavel x para append
aux_y = 0# auxiliar da variavel y para append
aux_z = 0# auxiliar da variavel z para append
j = 0 # contador de nivel
nivel = 1 # incializa variavel nivel
controle_nivel = 0 #controle de nivel
cont = 0# Controle do for
angle = 0 # angulo entre pontos
comp = [] # Vetor de comparacao entre variaveis
compz = [] # Comparacao entre Z
ponto_z = 0# Pontos em Z
pontos = 0# Filtra dados
colisao = 0# Classifica como colisao e publica
pontos_colisao = 0 #Variavel de teste


d = 0
check_z = 0


def callback(data):
	global i,j,vetx,vety,vetz,cont,controle_nivel,nivel,angle,pontos,colisao,pontos_colisao,compz,comp
	for i in range (0,len(data.points)):
			aux_x  = float(data.points[i].x)#Pega os valores dos pontos
			vetx.append(aux_x)
			aux_y = float(data.points[i].y)
			vety.append(aux_y)
			aux_z = float(data.points[i].z)
			vetz.append(aux_z)
	#		if vetz[i] > 0.175:
	#			vetz[i] = vetz[i] -0.175
	#		if vetz[i] < -0.175:
	#			vetz[i] = vetz[i] +0.175
			sum_root = (vetx[i]**2 + vety[i]**2)**0.5
			if j >15:	# Controle de nivel dos 16 ponto em sequencia para varredura
				nivel = nivel +1
				j = 0
			if  sum_root>0.55 and sum_root<0.90 or cont == 1: #identifica colisao
				#print "Indice de colisao ", i
				#print sum_root
				if sum_root != 0.0 :
					print(" X \t" + str(aux_x) + "\t Y \t" + str(aux_y) + "\t Z \t" + str(aux_z))
					comp.append(sum_root)
				if len(comp) == 2:
					ponto_z =  len(vetz) - 1
					compz.append(vetz[ponto_z])
					if len(compz) >2:
						angle  = atan2((compz[1]-compz[0]),(comp[1]-comp[0]))
						#d = (comp[1]-comp[0])
						#check_z = (compz[1]-compz[0])
						comp.pop(0)
						compz.pop(0)
						angle = degrees(angle)
						print ("\n ANGULO " + str(angle))
					if abs(angle) >= 30 and abs(angle) != 180:
						pontos = pontos +1

						#print(" Angulo \t" + str(angle) + " distancia \t" + str(d) + " Z \t" + str(check_z))
				controle_nivel = (nivel*16) -1
				#Filtra se ele detecta apenas 1 ponto de colisao
				#se houver mais de um ponto significa que a risco de colisao
				if pontos >2:
					colisao = True
					#Local onde ha perigo de colisao em relacao ao robo
					if 12258<i<20480:
						pontos_colisao = 1 #Colisao Frontal
					if 8192<i<12258:
						pontos_colisao = 2 #Colisao da quina frontal esquerda
					if 20480<i<24576:
						pontos_colisao = 3 #Colisao da quina frontal direita
					if 4096<i<8192:
						pontos_colisao = 4 #Colisao da quina traseira esquerda
					if 24576<i<28672:
						pontos_colisao = 5 #Colisao da quina traseira direita
					if 28672<i<4096:
						pontos_colisao = 6 # Colisao traseira
				#Se nao entao variavel de controle de colisao permanece em zero
				else:
					pontos_colisao = 0
					colisao = False
				#Enquanto cont for igual a 1 ele continua varrendo meus 16 pontos
				if i<(controle_nivel):
					cont = 1
				#Se for igual a zero todos os valores recebem zero para poder calcular os proximos pontos
				if i == (controle_nivel):
					cont = 0
					pontos = 0
					comp = []
					compz = []
					print "\n\n\n"
			#Incrimento de J para controle de nivel
			j = j+1
			#Incremento de i para varrer os pontos
			i = i+1
			#Fim do loop zero os pontos
			if i ==len(data.points):
				i = 0
				nivel = 0
				vetx=[]
				vety=[]
				vetz=[]
def getdata():
	global colisao
	rospy.init_node("detect_colision",anonymous=True)
	rospy.Subscriber("/velodyne_points",PointCloud,callback)
	pub = rospy.Publisher("colisao",Bool,queue_size = 10)#Publica no topico colisao true se detectar colisao e false se nao
	col = rospy.Publisher("Pontos",Int32,queue_size = 10)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		pub.publish(colisao)
		col.publish(pontos_colisao)
	   	rate.sleep()
if __name__== '__main__':
	try:
		getdata()
	except rospy.ROSInterruptException:
		pass
