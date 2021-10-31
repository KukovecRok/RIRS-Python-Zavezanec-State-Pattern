from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

# Razred zavezanec. Nastavitev osnovnega stanja
class Zavezanec(object):

    _state = "Neobdelan"
    indeks =0
    prvi=""
    drugi=""
    davcna=""
    maticna =""
    datum_opdrtja =""
    SKD_sifra =""
    naziv =""
    naslov =""
    okrozje =""

    def __init__(self, state: State, indeks, prvi, drugi, davcna, maticna, datum_opdrtja, SKD_sifra, naziv, naslov, okrozje) -> None:
        self.setZavezanec(state)
        self.indeks=indeks
        self.prvi = prvi
        self.drugi = drugi
        self.davcna = davcna
        self.maticna=maticna
        self.datum_opdrtja = datum_opdrtja
        self.SKD_sifra = SKD_sifra
        self.naziv = naziv
        self.naslov=naslov
        self.okrozje=okrozje

    def __str__(self):
        return "Stanje: {0}, Naziv: {1}, Davcna: {2}, Maticna: {3}, datum_opdrtja: {4}, SKD_sifra: {5}, naslov: {6}, okrozje: {7}".format(self._state, self.naziv, self.davcna, self.maticna, self.datum_opdrtja, self.SKD_sifra, self.naslov, self.okrozje)

    # metoda za spremembo stanja
    def setZavezanec(self, state: State):
        self._state = state
        self._state.zavezanec = self

    def stanjeTrenutno(self):
        print(f"Zavezanec je {type(self._state).__name__}")

    # metode za spreminjanje funkcionalnosti - odvisne od trenutnega stanja objektov
        def stanjeVPrebran(self):
            self._state.stanjeVPrebran()

    def stanjeVPomanjkljiv(self):
        self._state.stanjeVPomanjkljiv()


    def stanjeVOboje(self) -> None:
        print("Oops.. zavezanec-objekt ne more imeti dveh stanj hkrati :)")


    def stanjeNiSprememb(self) -> None:
        print("Po zelji spremeni stanje")


# Vmesnik za vsa stanja
class State(ABC):
    @property
    def zavezanec(self) -> Zavezanec:
        return self._zavezanec

    @zavezanec.setter
    def zavezanec(self, zavezanec: Zavezanec) -> None:
        self._zavezanec = zavezanec

    @abstractmethod
    def stanjeVPrebran(self) -> None:
        pass

    @abstractmethod
    def stanjeVPomanjkljiv(self) -> None:
        pass


# Dva konktertna stanja - prebran in pomanjljiv
class prebran(State):

    def stanjeVPrebran(self) -> None:
        print("Zavezanec-objekt je že v stanju prebran")

    def stanjeVPomanjkljiv(self) -> None:
        print("Premikam stanje v pomanjljivo")
        self.zavezanec.setZavezanec(pomanjkljiv())


class pomanjkljiv(State):

    def stanjeVPrebran(self) -> None:
        print("Premikam stanje v prebrano")
        self.zavezanec.setZavezanec(prebran())

    def stanjeVPomanjkljiv(self) -> None:
        print("Zavezanec-objekt je že pomanjkljiv")

if __name__ == "__main__":

    stevec_napak=0

    def naletelNaNapako(vrstica, stevec_napak):
        print("Napaka v vrstici: " + str(vrstica))
        stevec_napak += 1
        return stevec_napak

    def podatkiPrebrani(myListPravilnih, myZavezanec):
        myListPravilnih.append(myZavezanec)
        return myListPravilnih

    df = pd.read_fwf('DURS_zavezanci_PO.csv')
    pd.set_option('display.max_columns', None)
    df.append(pd.Series(dtype = 'object'), ignore_index=True)
    df.columns = ['Prvi', 'Drugi', 'davcna', 'maticna', 'datum_opdrtja', 'SKD_sifra', 'naziv', 'A','B','C','D','naslov','okrozje']
    df = df.drop(columns=['A', 'B','C','D'])
    df.insert(0, "State", "zacetni")

    df['Prvi'] = df['Prvi'].fillna("NE")
    df['Drugi'] = df['Drugi'].fillna("NE")

    myList = []
    myListPravilnih = []

    for vrstica, row in df.iterrows():
        if(row.isnull().any()):
            stevec_napak = naletelNaNapako(vrstica, stevec_napak)
            myZavezanec = Zavezanec(pomanjkljiv(), *df.iloc[vrstica, :])
            myList.append(myZavezanec)
        else:
            myZavezanec = Zavezanec(prebran(), *df.iloc[vrstica, :])
            myListPravilnih = podatkiPrebrani(myListPravilnih, myZavezanec)
            myList.append(myZavezanec)

    print("\nStevilo napak:" + str(stevec_napak) + "\n")

    #for zavezanec in myList:
        #print(zavezanec.stanjeTrenutno())

    print("Stevilo prebranih vrstic (objektov): " + str(len(myList)) + "; Stevilo pravilnih: " + str(len(myList)-stevec_napak) )
    #print(myList.__getitem__(1)._state)

    #print(sum(p.stanjeTrenutno() == "kerokoli stanje" for p in myList))
    print("Dolzina liste samo pravilnih je: " + str(len(myListPravilnih)))
'''
    myList.__getitem__(1).stanjeTrenutno()
    myList.__getitem__(1).stanjeVPrebran()
    myList.__getitem__(1).stanjeVPomanjkljiv()
    myList.__getitem__(1).stanjeVPomanjkljiv()
    myList.__getitem__(1).stanjeVPrebran()
    myList.__getitem__(1).stanjeTrenutno()
'''