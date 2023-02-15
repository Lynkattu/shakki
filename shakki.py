import sys
from termcolor import colored, cprint

import lauta

class Kayttoliittyma:
    def __init__(self):
        self.l = lauta.Lauta()
    
    def valikko(self) -> None:
        while True:
            print("1) Aloita peli")
            print("0) Sulje ohjelma")       
            komento = input("Komento: ")
            if komento == "0":
                print("\nPeli suljetaan")
                break
            elif komento == "1":
                self.__peli()
            else:
                print("Virheellinen komento.\n")
        return None
    
    def __peli(self) -> None:
        pelaaja = 0
        self.l = lauta.Lauta()
        print("0) Luovuta")
        print("Siirrot tehdään muodossa: A7 A5")
        while True:        
            if pelaaja == 0:
                lopetus = self.__vuorot(pelaaja, "Vaalean")
                if lopetus == True:
                    print("Vaalea luovutti")
                    break
                pelaaja = 1
            else: 
                lopetus = self.__vuorot(pelaaja, "Tumman")
                if lopetus == True:
                    print("Tumma luovutti")
                    break
                pelaaja = 0
            vaarassa = self.l.kuningas_uhattu(pelaaja)
            if vaarassa == True:                
                if self.l.shakkimatti(pelaaja) == True:
                    if pelaaja == 0:
                        print("Shakkimatti, tumma voitti")
                        break
                    else:
                        print("Shakkimatti, vaalea voitti")
                        break
                else:
                    print("Shakki")
        return None
       
    def __vuorot(self, pelaaja: int, vari: str) -> bool:
        while True:
            siirtosallittu = False
            self.l.tulosta_lauta()
            komento = input(f"{vari} siirto: ")
            komento = komento.split(" ")                 
            try:
                if komento[0][0] >= "A" and komento[0][0] <= "H" and komento[0][1] >= "1" and komento[0][1] <= "8" and komento[1][0] >= "A" and komento[1][0] <= "H" and komento[1][1] >= "1" and komento[1][1] <= "8":
                    siirtosallittu = self.l.siirto_laudalla(pelaaja, komento[0], komento[1])
                elif komento[0] == "0":
                    break
                else:
                    raise ValueError()
                if siirtosallittu == True:
                    break
                elif siirtosallittu == False:
                    print("Virheellinen siirto")
            except:
                print("Virheellinen syöte.")
                print("0) Luovuta")
                print("Siirrot tehdään muodossa: A7 A5")
        if komento[0] == "0":
            return True
        return False

ohjelma = Kayttoliittyma()
ohjelma.valikko()



