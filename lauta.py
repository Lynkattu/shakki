import sys
from termcolor import colored, cprint
import pelinappulat
import copy

class Lauta:
    def __init__(self):
        self.vaalea = colored(' #', 'yellow')
        self.tumma = colored(' #', 'green')
        self.lauta = {}
        self.__laudanluonti()
        self.__nappuloiden_luonti()

    def __laudanluonti(self):
        #luo pelilaudan 
        vaalea = True    
        for i in range(8):
            num = chr(56-i)# laudan sijainti 8
            for n in range(8):
                kirj = chr(65+n)# laudan sijainti A
                if vaalea == True:
                    self.lauta[f"{kirj}{num}"] = list([self.vaalea, -1])
                    vaalea = False
                else:
                    self.lauta[f"{kirj}{num}"] = list([self.tumma, -1])
                    vaalea = True
            if vaalea == True:
                vaalea = False
            else:
                vaalea = True

    def __nappuloiden_luonti(self):
    #luo pelinappulat ohjelman alussa
        tyypit = ["T","R","L","D","K","L","R","T"] #T=torni, R=ratsu, L=lähetti, D=daami, K=kuningas
        #luo sotilaat s pelaajalle 0
        for i in range(8):        
            num = chr(55)#laudan sijainti 7
            kirj = chr(65+i)#laudan sijainti A
            self.lauta[f"{kirj}{num}"][1]=(pelinappulat.Pelinappula(f"{kirj}{num}", "S", 0))
        
        #luo sotilaat s pelaajalle 1
        for i in range(8):        
            num = chr(50)#laudan sijainti 2
            kirj = chr(65+i)#laudan sijainti A
            self.lauta[f"{kirj}{num}"][1]=(pelinappulat.Pelinappula(f"{kirj}{num}", "S", 1))

        #luo loput nappulat pelaajalle 0
        for i in range(8):
            num = chr(56)#laudan sijainti 1
            kirj = chr(65+i)#laudan sijainti A
            self.lauta[f"{kirj}{num}"][1]=(pelinappulat.Pelinappula(f"{kirj}{num}", tyypit[i], 0))

        #luo loput nappulat pelaajalle 1
        for i in range(8):
            num = chr(49)#laudan sijainti 1
            kirj = chr(65+i)#laudan sijainti A
            self.lauta[f"{kirj}{num}"][1]=(pelinappulat.Pelinappula(f"{kirj}{num}", tyypit[i], 1))
    
    def tulosta_lauta(self):
        numerointi = 8
        for i in self.lauta:
            if i[0] == "A":
                cprint(colored(str(numerointi), 'cyan'), end="  ")
                numerointi -= 1
            if self.lauta[i][1] != -1:
                s = str(self.lauta[i][1])
                cprint(s, end="")
            else:
                cprint(self.lauta[i][0], end="")
            if i[0] == "H":
                print()
        cprint(colored("\n    A B C D E F G H", 'cyan')) #laudan kirjain koordinaatit
    
    def siirto_laudalla(self, pelaaja: int, sijainti: str, uusisijainti: str):
        try:
            # palauttaa arvot True tai False, riippuen onko kyseinen siirto sallittu
            sallittusiirto = self.lauta[sijainti][1].siirra(pelaaja, uusisijainti, self.lauta)
            oheista = self.lauta[sijainti][1].oheistalyonti(pelaaja, uusisijainti, self.lauta)
            # jos siirto on sallittu siirrä nappulaa
            if sallittusiirto == True or oheista == True:
                #oheista lyönti
                if oheista == True:
                    if pelaaja == 0:
                        self.lauta[f"{uusisijainti[0]}{chr(ord(uusisijainti[1]) + 1)}"][1] = -1
                    elif pelaaja == 1:
                        self.lauta[f"{uusisijainti[0]}{chr(ord(uusisijainti[1]) - 1)}"][1] = -1
                self.lauta[sijainti][1].sijainti = uusisijainti
                self.lauta[uusisijainti][1] = self.lauta[sijainti][1]
                self.lauta[sijainti][1] = -1
                return True
            return False
        except:
            return False
                            
    def kuningas_uhattu(self, pelaaja: int, lauta: dict = {}) -> bool:
        vastustajan_nappulat = {}
        kuningas = ""
        if len(lauta) < 1:
            lauta = self.lauta
        for i in lauta:
            if lauta[i][1] != -1:
                if lauta[i][1].pelaaja != pelaaja:
                    vastustajan_nappulat[i] = lauta[i][1]
                elif lauta[i][1].pelaaja == pelaaja and lauta[i][1].tyyppi == "K":
                    kuningas = lauta[i][1].sijainti
        if pelaaja == 1:
            siirtaja = 0
        else:
            siirtaja = 1
        for i in vastustajan_nappulat:
            uhka = lauta[i][1].siirra(siirtaja, kuningas, lauta)
            if uhka == True:
                uhka = lauta[i][1].siirra(siirtaja, kuningas, lauta)
                return True
        return False
    
    def shakkimatti(self, pelaaja: int) -> bool:
        vastustajan_nappulat = {}
        omat_nappulat = {}
        uhkaavat_nappulat = {}
        kuningas = ""
        #käyläpi laudan ja ottaa muistiin vastustajan nappulat ja omat nappulat, lisäksi myös oman kuninkaan sijainti otetaan muistiin
        for i in self.lauta:
            if self.lauta[i][1] != -1:                
                if self.lauta[i][1].pelaaja != pelaaja:
                    vastustajan_nappulat[i] = self.lauta[i][1]

                elif self.lauta[i][1].pelaaja == pelaaja:
                    omat_nappulat[i] = self.lauta[i][1]

                if self.lauta[i][1].pelaaja == pelaaja and self.lauta[i][1].tyyppi == "K":
                    kuningas = self.lauta[i][1].sijainti
        #kokeilee pystyykö vastustajan nappula uhkaamaan kuningasta, jos pystyy lisätään se uhkaaviin nappuloihin
        if pelaaja == 1:
            siirtaja = 0
        else:
            siirtaja = 1
        for i in vastustajan_nappulat:            
            uhka = self.lauta[i][1].siirra(siirtaja, kuningas, self.lauta)
            if uhka == True:                
                uhkaavat_nappulat[i] = self.lauta[i][1]
        #katsoo onko mahdollisia siirtoja
        if self.__siirtaminen(pelaaja, omat_nappulat, uhkaavat_nappulat) == False:
            return False         
        return True

    def __siirtaminen(self, pelaaja: int, omat_nappulat: dict, uhkaavat_nappulat: dict):
        for oma in omat_nappulat:
            for siirto in self.lauta:
                if self.lauta[oma][1].siirra(pelaaja, siirto, self.lauta) == True:
                    uusi_lauta = copy.deepcopy(self.lauta.copy())
                    uusi_lauta[siirto][1] = uusi_lauta[oma][1]
                    uusi_lauta[oma][1] = -1
                    if self.kuningas_uhattu(pelaaja, uusi_lauta) == False:
                        return False
        return True