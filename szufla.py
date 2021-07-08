#!/usr/bin/python3
# vim: ts=4:sw=4:sts=4:noet:fileencoding=utf-8

import sys
import os
import datetime
import time

#A kimeneti fájl útvonalának meghatározása
strHomePath = os.path.expanduser("~")
strGITpath = f"{strHomePath}/GIT/szufla"
strKimenetifajlNeve = "szufla.stamp"
strKimenetifajl = f"{strGITpath}/{strKimenetifajlNeve}"

#A fájlbaírás és repo frissítés időköze percben.
intPerc = 1

#Globális változó a gép indulási idejének eltárolásához
dtBoot = 0

#Kiírás a standard kimenetre
def print_message(strText):
	print(strText)

def print_elvalaszto():
	print_message("___{}{}".format(time.strftime("%H:%M:%S",time.localtime()),"_"*20))

def get_uptime():
	print_message("Bootolási idő kiolvasása...")
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
	print_message(f"Bootolási idő : {uptime_seconds} másodperc.")
	return uptime_seconds

def write_stamp():
	print_message(f"Írás: {strKimenetifajlNeve}")
	dtMost = datetime.datetime.now()
	dtEltelt = dtMost - dtBoot
	with open(strKimenetifajl,'w') as f:
		f.write("BOOT:\t{0}\nMOST:\t{1}\nDELTA:\t{2}\n".format(dtBoot,dtMost,dtEltelt))
	print_message("Fájlba írás befejezve.")

def git_push():
	print_message("GIT repó frissítése...")
	try:
		os.chdir(strGITpath)
		print_message("GIT repó PULL...")
		os.system("git pull")
		print_message("GIT repó ADD...")
		os.system(f"git add {strKimenetifajlNeve}")
		print_message("GIT repó COMMIT...")
		os.system(f"git commit -m 'Pecsét frissítése'")
		print_message("GIT repó PUSH...")
		os.system("git push")
	except Exception as e:
		print_message("Hiba a GIT repó frissítése közben:\n{}".format(str(e)))
		return
	print_message("GIT repó frissítése befejezve.")
	print_elvalaszto()


def main():
	global dtBoot
	print_elvalaszto()
	try:
		dtBoot = datetime.datetime.now()-datetime.timedelta(seconds=int(get_uptime()))
		while True:
			write_stamp()
			git_push()
			time.sleep(intPerc*60)
	except KeyboardInterrupt:
		print_message("Futás megszakítva")
		sys.exit(0)
	except Exception as e:
		print_message(str(e))
	

if __name__ == "__main__":
	main();
