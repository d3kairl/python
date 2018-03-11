import sys
import os
import math

def tiempodic2str(ti, tf):
	for t in ti.keys():
		if t=='ms':
			ti[t]=str(ti[t]).zfill(3)
		else:
			ti[t]=str(ti[t]).zfill(2)
	for t in tf.keys():
		if t=='ms':
			tf[t]=str(tf[t]).zfill(3)
		else:
			tf[t]=str(tf[t]).zfill(2)
	cad1=str(ti["h"]+':'+ti["m"]+':'+ti["s"]+','+ti["ms"])
	cad2=str(tf["h"]+':'+tf["m"]+':'+tf["s"]+','+tf["ms"])
	return cad1+" --> "+cad2

def ms2dict(ms):
	t = {}
	ms = int(ms)
	s = int((ms/1000)%60)
	m = int((ms/(1000*60))%60)
	h = int((ms/(1000*60*60))%24)
	t['ms'] = 0
	t['s'] = s
	t['m'] = m
	t['h'] = h
	ms = ms - dict2ms(t)
	t['ms'] = ms
	return t

def dict2ms(t):
	return t['ms']+1000*t['s']+1000*60*t['m']+1000*60*60*t['h']

def shiftTime(t, ms):
	ms = int(ms)
	t = ms2dict(dict2ms(t)+ms)
	return t

def escribeArchivo(archivoin, archivoout, desp):
	if os.access(archivoin, os.R_OK):
		f = open(archivoin, "r")
		fout = open(archivoout, "w")
		count = 1
		for linea in f.read().splitlines():
			if count == 2: # Es un apartado de tiempos
				tiempoini = {"h":int(linea.split()[0].split(':')[0]), \
				 			 "m":int(linea.split()[0].split(':')[1]), \
				 			 "s":int(linea.split()[0].split(':')[2].split(',')[0]), \
				 			"ms":int(linea.split()[0].split(':')[2].split(',')[1]) \
				 }
				tiempofin = {"h":int(linea.split()[2].split(':')[0]), \
							 "m":int(linea.split()[2].split(':')[1]), \
						 	 "s":int(linea.split()[2].split(':')[2].split(',')[0]), \
							"ms":int(linea.split()[2].split(':')[2].split(',')[1]) \
				} 
				tiempoini = shiftTime(tiempoini, desp)
				tiempofin = shiftTime(tiempofin, desp)
				fout.write(tiempodic2str(tiempoini, tiempofin)+'\n')
				count = count + 1
			elif count == 4:
				count = 1
				fout.write(linea+'\n')
			else:
				count = count + 1
				fout.write(linea+'\n')
		f.close()
		fout.close()
	else:
		print("El archivo no existe o no se puede acceder.")

def main():
	if len(sys.argv) < 3:
		print("FALTAN PARÁMETROS!")
		print("Uso: "+sys.argv[0]+" <fichero> (destino) <desplazamiento en ms>")
		print("\t El parámetro de destino puede omitirse.")
	elif len(sys.argv) == 3: # Destino no especificado, se crea por defecto
		fichero = sys.argv[1]
		destino = sys.argv[1]+".new"
		despl 	= sys.argv[3]
		escribeArchivo(fichero, destino, despl)
	elif len(sys.argv) == 4:
		fichero = sys.argv[1]
		destino = sys.argv[2]
		despl 	= sys.argv[3]
		escribeArchivo(fichero, destino, despl)
	else:
		print("SOBRAN PARÁMETROS!")
		print("Uso: "+sys.argv[0]+" <fichero> (destino) <desplazamiento en ms>")
		print("\t El parámetro de destino puede omitirse.")

if __name__ == "__main__": main()

