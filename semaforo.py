#!/usr/bin/env python
import pygame, sys
from pygame.locals import *
import datetime
import os

screen = pygame.display.set_mode((640,480))
#screen = pygame.display.set_mode((640, 480), FULLSCREEN | DOUBLEBUF)

cores = {}
for cor in ['red', 'yellow', 'green', 'red_off', 'green_off', 'yellow_off']:
	cores[cor] = pygame.image.load('60x88/%s.png' %cor)

def load_sound(name):
	class NoneSound:
		def play(self):
			pass
	
	fullname = os.path.join('data',name)
	
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error,message:
		print 'Cannot load sound: ' , fullname
		raise SystemExit, message

	return sound
	
def tratar_eventos():
	for event in pygame.event.get():
		if not hasattr(event,'key'): continue
		if event.key  == K_ESCAPE: sys.exit(0)

def exibir_semaforo(l,y):
	espaco_branco = 210
	for pos,cor in enumerate(l):
		if cor in cores:
			screen.blit(cores[cor],(10 +pos*espaco_branco,y))
		
				
alt_linha = 768/7
margem_topo =  ((768-alt_linha*7) / 2  ) + 30

dh_start = datetime.datetime.now()
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Semaforo do IX PUG-PE')

alerta = load_sound('alarm.wav')
nao_tocou = True

while 1:
	screen.fill(0)
	diff = datetime.datetime.now() - dh_start
	hours,remainder = divmod(diff.seconds,3600)
	minutes, seconds = divmod(remainder,60)
		
	#tudo normal, mas nos ultimos 10 segundos ai o bixo pega.
	if minutes == 4 and seconds in range(40,60):
		if seconds % 2 == 0:
			y = 'yellow'
		else:
			y = 'yellow_off'
		exibir_semaforo(['green_off',y,'red_off'], 1 * alt_linha + margem_topo)
	
	elif minutes == 5 and seconds in range(0,15):
		exibir_semaforo(['green_off','yellow_off','red'], 1 * alt_linha + margem_topo)
		if nao_tocou:
			alerta.play()
			nao_tocou = False
	else:
		if minutes == 5:
			sys.exit()
					
		exibir_semaforo(['green','yellow_off','red_off'], 1 * alt_linha + margem_topo)
			
	tratar_eventos()
	pygame.display.flip()
	clock.tick(60)