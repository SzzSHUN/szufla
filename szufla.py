#!/bin/env python3
# vim: ts=4:sw=4:sts=4:noet:fileencoding=utf-8

import sys
import os
import datetime
import time

#A jelenlegi felhasználó HOME könyta útvonalának tárolása.
strHomePath = os.path.expanduser("~")
#A GIT repo útvonala a lokális gépen.
strGITpath = f"{strHomePath}/GIT/szufla"
#A naplófájl neve, útvonal nélkül
strKimenetifajlNeve = "szufla.stamp"
#A naplófájl teljes útvonalának összeállítása
strKimenetifajl = f"{strGITpath}/{strKimenetifajlNeve}"

#A fájlbaírás és repo frissítés időköze percben.
intPerc = 1

#Globális változó a gép indulási idejének eltárolásához.
dtBoot = 0

#Kiírás a standard kimenetre.
def print_message(strText):
	print(strText)

#Elválasztó sor kiírása a standard kimenetre.
def print_elvalaszto():
	print_message("___{}{}".format(time.strftime("%H:%M:%S",time.localtime()),"_"*20))

#A bekapcsolás óta eltelt másodpercek értékének kiolvasása.
def get_uptime():
	print_message("Bootolási idő kiolvasása...")
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
	print_message(f"Bootolási idő : {uptime_seconds} másodperc.")
	return uptime_seconds

#A jelenlegi időpont és a bekapcsolás óta eltelt idő meghatározása
#és kiírása a 'strKimenetifajl' változóban beállított naplófájlba.
def write_stamp():
	print_message(f"Írás: {strKimenetifajlNeve}")
	#A jelenlegi időpont tárolása.
	dtMost = datetime.datetime.now()
	#A gép indítása óta eltelt idő kiszámítása.
	dtEltelt = dtMost - dtBoot
	#Naplófájl megnyitása írásra és a tárolt, kiszámított adatok kiírása.
	with open(strKimenetifajl,'w') as f:
		f.write("BOOT:\t{0}\nMOST:\t{1}\nDELTA:\t{2}\n".format(dtBoot,dtMost,dtEltelt))
	print_message("Fájlba írás befejezve.")

#A szufla.stamp feltöltése a GIT tárolóba.
def git_push():
	print_message("GIT repó frissítése...")
	try:
		#Az aktuális könyvtárat a helyi GIT tárolóra állítjuk.
		os.chdir(strGITpath)
		print_message("GIT repó PULL...")
		#Frissítjük a repót.
		os.system("git pull")
		print_message("GIT repó ADD...")
		#Felvesszük a módosított naplófájlt.
		os.system(f"git add {strKimenetifajlNeve}")
		print_message("GIT repó COMMIT...")
		os.system(f"git commit -m 'Pecsét frissítése'")
		print_message("GIT repó PUSH...")
		#Feltöltjük a módosított naplófájlt.
		os.system("git push")
	except Exception as e:
		print_message("Hiba a GIT repó frissítése közben:\n{}".format(str(e)))
		return
	print_message("GIT repó frissítése befejezve.")
	#Elválasztó sor kiírása a standard kimenetre.
	print_elvalaszto()

#A program futtatása CTRL-C lenyomásáig.
def main():
	global dtBoot
	#Elválasztó sor kiírása a standard kimenetre.
	print_elvalaszto()
	try:
		#A gép indulási idejének eltárolása globális változóba, mivel ez nem fog változni.
		dtBoot = datetime.datetime.now()-datetime.timedelta(seconds=int(get_uptime()))
		#Ciklus indítása, ami a CTRL-C lenyomásáig futtatja a kódot.
		while True:
			#Az aktuális és az eltelt idő kiírása fájlba.
			write_stamp()
			#GIT repó frissítése.
			git_push()
			#Várakozás az 'intPerc' változóban megadott percig.
			time.sleep(intPerc*60)
	except KeyboardInterrupt:
		#CTRL-C billentyű lenyomásakor megszakítjuk a futást.
		print_message("Futás megszakítva")
		sys.exit(0)
	except Exception as e:
		#Hiba esetén kiírjuk a hibát, de a kód fut tovább.
		print_message(str(e))
	
#A program belépési pontja
if __name__ == "__main__":
	main();
