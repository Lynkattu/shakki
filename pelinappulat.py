import sys
from termcolor import colored, cprint

class Pelinappula:
    def __init__(self, sijainti: str, tyyppi: str, pelaaja: int) -> bool:
        self.__sijainti = sijainti
        self.__tyyppi = tyyppi # [S=sotilas,R=ratsu,T=torni,L=lähetti,D=kuningatar,K=kuningas]
        self.pelaaja = pelaaja # 0 = vaalea, 1 = tumma
        self.__ensisiirto = True # huom vaikutta vain sotilaaseen
        self.__oheista_mahdollisuus = False

    def __str__(self):
        if self.pelaaja == 0:
            return colored(f" {self.__tyyppi}", 'yellow')    
        return colored(f" {self.__tyyppi}", 'green')

    @property
    def sijainti(self):
        return self.__sijainti

    @property
    def tyyppi(self):
        return self.__tyyppi

    @property
    def oheista(self):
        return self.__oheista_mahdollisuus

    @sijainti.setter
    def sijainti(self, sijainti: str):
        if self.__tyyppi == "S" and abs(int(sijainti[1]) - int(self.__sijainti[1])) == 2:
            self.__oheista_mahdollisuus = True
        elif self.__tyyppi == "S" and self.__oheista_mahdollisuus == True:
            self.__oheista_mahdollisuus = False
        self.__ensisiirto = False
        self.__sijainti = sijainti

    def siirra(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        palautus = False
        if pelaaja == self.pelaaja:
            if self.__tyyppi == "S":
                palautus = self.__siirto_sotilas(pelaaja, uusisijainti, lauta)
            elif self.__tyyppi == "T":
                palautus = self.__siirto_torni(pelaaja, uusisijainti, lauta)
            elif self.__tyyppi == "R":
                palautus = self.__siirto_ratsu(pelaaja, uusisijainti, lauta)
            elif self.__tyyppi == "L":
                palautus = self.__siirto_lahetti(pelaaja, uusisijainti, lauta)
            elif self.__tyyppi == "D":
                palautus = self.__siirto_daami(pelaaja, uusisijainti, lauta)
            elif self.__tyyppi == "K":
                palautus = self.__siirto_kuningas(pelaaja, uusisijainti, lauta)
        return palautus
    
    def __siirto_sotilas(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        try:
            #solitaaan hyökkäys P0
            if pelaaja == 0 and ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 1 and ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 1 and lauta[uusisijainti][1] != -1 or pelaaja == 0 and ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 1 and ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 1 and lauta[uusisijainti][1] != -1:
                if lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    if uusisijainti[1] == "1":
                        self.__tyyppi = "D"
                    return True
            #sotilaan liikerata P0
            if self.__ensisiirto == True and pelaaja == 0 and uusisijainti[0] == self.__sijainti[0] and int(uusisijainti[1]) == int(self.__sijainti[1]) - 2:
                for i in range(1,3):
                    if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])-i}"][1] != -1:
                        return False                                       
                return True
            elif pelaaja == 0 and uusisijainti[0] == self.__sijainti[0] and int(uusisijainti[1]) == int(self.__sijainti[1]) - 1:
                if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])-1}"][1] != -1:
                    return False
                if uusisijainti[1] == "1":
                    self.__tyyppi = "D"  
                return True
            #solitaaan hyökkäys P1
            if pelaaja == 1 and ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 1 and ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 1 and lauta[uusisijainti][1] != -1 or pelaaja == 1 and ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 1 and ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 1 and lauta[uusisijainti][1] != -1:
                if lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    if uusisijainti[1] == "8":
                        self.__tyyppi = "D"
                    return True
            #sotilaan liikerata P1
            if self.__ensisiirto == True and pelaaja == 1 and uusisijainti[0] == self.__sijainti[0] and int(uusisijainti[1]) == int(self.__sijainti[1]) + 2:
                for i in range(1,3):
                    if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])+i}"][1] != -1:
                        return False
                return True
            elif pelaaja == 1 and uusisijainti[0] == self.__sijainti[0] and int(uusisijainti[1]) == int(self.__sijainti[1]) + 1:
                if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])+1}"][1] != -1:
                    return False
                if uusisijainti[1] == "8":
                    self.__tyyppi = "D"            
                return True
            return False
        except:
            return False

    def __siirto_torni(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        try:
            if pelaaja != self.pelaaja or uusisijainti == self.__sijainti:
                return False
            #pystytasossa
            if uusisijainti[0] == self.__sijainti[0] and uusisijainti[1] != self.__sijainti[1]:
                for i in range(1, 8):
                    if uusisijainti[1] > self.__sijainti[1]:
                        if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])+i}"][1] != -1:
                            if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])+i}"][1].pelaaja != pelaaja and uusisijainti == lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])+i}"][1].sijainti:
                                return True
                            return False
                    if uusisijainti[1] < self.__sijainti[1]:
                        if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])-i}"][1] != -1:
                            if lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])-i}"][1].pelaaja != pelaaja and uusisijainti == lauta[f"{self.__sijainti[0]}{int(self.__sijainti[1])-i}"][1].sijainti:
                                return True
                            return False
                    if f"{self.__sijainti[0]}{int(self.__sijainti[1])-i}" == uusisijainti or f"{self.__sijainti[0]}{int(self.__sijainti[1])+i}" == uusisijainti:
                        break
                return True
            #vaakatasossa
            elif uusisijainti[0] != self.__sijainti[0] and uusisijainti[1] == self.__sijainti[1]:
                for i in range(1, 8):
                    if uusisijainti[0] > self.__sijainti[0]:
                        if lauta[f"{chr(ord(self.__sijainti[0])+i)}{self.__sijainti[1]}"][1] != -1:
                            if lauta[f"{chr(ord(self.__sijainti[0])+i)}{self.__sijainti[1]}"][1].pelaaja != pelaaja and uusisijainti == lauta[f"{chr(ord(self.__sijainti[0])+i)}{self.__sijainti[1]}"][1].sijainti:
                                return True
                            return False
                    if uusisijainti[0] < self.__sijainti[0]:
                        if lauta[f"{chr(ord(self.__sijainti[0])-i)}{self.__sijainti[1]}"][1] != -1:
                            if lauta[f"{chr(ord(self.__sijainti[0])-i)}{self.__sijainti[1]}"][1].pelaaja != pelaaja and uusisijainti == lauta[f"{chr(ord(self.__sijainti[0])-i)}{self.__sijainti[1]}"][1].sijainti:
                                return True
                            return False
                    if f"{chr(ord(self.__sijainti[0])-i)}{self.__sijainti[1]}" == uusisijainti or f"{chr(ord(self.__sijainti[0])+i)}{self.__sijainti[1]}" == uusisijainti:
                        break
                return True
        except:
            return False

    def __siirto_ratsu(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        try:
            if pelaaja != self.pelaaja or uusisijainti == self.__sijainti:
                return False
            #yläliike
            if ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 1 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 2 or ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 1 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 2: 
                if lauta[uusisijainti][1] == -1:
                    return True
                elif lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    return True
            #alaliike
            if ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 1 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 2 or ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 1 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 2:
                if lauta[uusisijainti][1] == -1:
                    return True
                elif lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    return True
            #oikealiike
            if ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 2 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 1 or ord(uusisijainti[0]) == ord(self.__sijainti[0]) + 2 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 1:
                if lauta[uusisijainti][1] == -1:
                    return True
                elif lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    return True
            #vasenliike
            if ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 2 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) + 1 or ord(uusisijainti[0]) == ord(self.__sijainti[0]) - 2 and  ord(uusisijainti[1]) == ord(self.__sijainti[1]) - 1:
                if lauta[uusisijainti][1] == -1:
                    return True
                elif lauta[uusisijainti][1].pelaaja != self.pelaaja:
                    return True
            return False
        except:
            return False
    
    def __siirto_lahetti(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        if pelaaja != self.pelaaja or uusisijainti == self.__sijainti:
            return False
        try:
            for i in range(1, 8):
                #koilinen
                if uusisijainti[0] > self.__sijainti[0] and uusisijainti[1] > self.__sijainti[1]:
                    if lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) + i)}"][1] != -1:
                        if lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) + i)}"][1].pelaaja != self.pelaaja and lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) + i)}"][1].sijainti == uusisijainti:                       
                            return True
                        else:
                            return False
                #lounas
                elif uusisijainti[0] < self.__sijainti[0] and uusisijainti[1] < self.__sijainti[1]:
                    if lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) - i)}"][1] != -1:
                        if lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) - i)}"][1].pelaaja != self.pelaaja and lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) - i)}"][1].sijainti == uusisijainti:                       
                            return True
                        else:
                            return False
                #kaakko
                elif uusisijainti[0] > self.__sijainti[0] and uusisijainti[1] < self.__sijainti[1]:
                    if lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) - i)}"][1] != -1:
                        if lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) - i)}"][1].pelaaja != self.pelaaja and lauta[f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) - i)}"][1].sijainti == uusisijainti:                       
                            return True
                        else:
                            return False
                #luode
                elif uusisijainti[0] < self.__sijainti[0] and uusisijainti[1] > self.__sijainti[1]:
                    if lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) + i)}"][1] != -1:
                        if lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) + i)}"][1].pelaaja != self.pelaaja and lauta[f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) + i)}"][1].sijainti == uusisijainti:                       
                            return True
                        else:
                            return False
                if f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) + i)}" == uusisijainti or f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) - i)}" == uusisijainti or f"{chr(ord(self.__sijainti[0]) + i)}{chr(ord(self.__sijainti[1]) + i)}" == uusisijainti or f"{chr(ord(self.__sijainti[0]) - i)}{chr(ord(self.__sijainti[1]) - i)}" == uusisijainti:
                    return True
        except:
            return False

    def __siirto_daami(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:        
        if pelaaja != self.pelaaja or uusisijainti == self.__sijainti:
            return False
        if self.__siirto_torni(pelaaja, uusisijainti, lauta) == True:
            return True
        if self.__siirto_lahetti(pelaaja, uusisijainti, lauta) == True:
            return True
        return False

    def __siirto_kuningas(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        if pelaaja != self.pelaaja or uusisijainti == self.__sijainti:
            return False
        if abs(ord(self.__sijainti[0]) - ord(uusisijainti[0])) <= 1 and abs(ord(self.__sijainti[0]) - ord(uusisijainti[0])) >= 0 and abs(ord(self.__sijainti[1]) - ord(uusisijainti[1])) <= 1 and abs(ord(self.__sijainti[1]) - ord(uusisijainti[1])) >= 0:
            if lauta[uusisijainti][1] == -1:
                return True 
            elif lauta[uusisijainti][1].pelaaja != self.pelaaja:
                return True
        return False

    def oheistalyonti(self, pelaaja: int, uusisijainti: str, lauta: dict) -> bool:
        if uusisijainti == self.__sijainti or self.__tyyppi != "S":
            return False
        try:
            if self.pelaaja == 0 and lauta[uusisijainti][1] == -1 and ord(self.__sijainti[0]) - 1 == ord(uusisijainti[0]) and ord(self.__sijainti[1]) - 1 == ord(uusisijainti[1]) or self.pelaaja == 0 and lauta[uusisijainti][1] == -1 and ord(self.__sijainti[0]) + 1 == ord(uusisijainti[0]) and ord(self.__sijainti[1]) - 1 == ord(uusisijainti[1]):
                if lauta[f"{uusisijainti[0]}{chr(ord(uusisijainti[1]) + 1)}"][1].oheista == True:
                    return True
            if self.pelaaja == 1 and lauta[uusisijainti][1] == -1 and ord(self.__sijainti[0]) - 1 == ord(uusisijainti[0]) and ord(self.__sijainti[1]) + 1 == ord(uusisijainti[1]) or self.pelaaja == 1 and lauta[uusisijainti][1] == -1 and ord(self.__sijainti[0]) + 1 == ord(uusisijainti[0]) and ord(self.__sijainti[1]) + 1 == ord(uusisijainti[1]):
                if lauta[f"{uusisijainti[0]}{chr(ord(uusisijainti[1]) - 1)}"][1].oheista == True:
                    return True
            return False
        except:
            return False