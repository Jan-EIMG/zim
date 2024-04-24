import datetime
from OPCUA import OPCUA
from MedienErzeuger import MedienErzeuger
from MedienVerbraucher import MedienVerbraucher
from MedienSpeicher import MedienSpeicher
from MedienVersorger import MedienVersorger
from globals import *
import time

class EMS():
    def __init__(self):
        self.OPCUA = OPCUA()
        MedienErzeuger.erstellen(self.OPCUA.json)
        MedienVerbraucher.erstellen(self.OPCUA.json)
        MedienSpeicher.erstellen(self.OPCUA.json)
        MedienVersorger.erstellen(self.OPCUA.json)

    # def __del__(self):
    #     self.quit()
        
    def start(self):
        # Zeit synkronisieren
        # time.sleep(60-(datetime.now().second+datetime.now().microsecond/1000000))
        
        # Hauptschleife
        i = 1
        while True:
            opcjson = self.OPCUA.pull_data()
            opcjson["Girea-Module"]["EMS"]["live bit"].set_value(not opcjson["Girea-Module"]["EMS"]["live bit"].get_value())
            opcjson["Girea-Module"]["EMS"]["zyklus"].set_value(i)
            i += 1
            
            print(i)

            self.OPCUA.pull_data()
            MedienErzeuger.update()
            MedienVerbraucher.update()
            MedienSpeicher.update()
            MedienVersorger.update()
            self.OPCUA.push_data()

            betriebsartID =self.betriebsarten()

            self.prioritasschaltung(betriebsartID)

            self.OPCUA.pull_data()
            MedienErzeuger.update()
            MedienVerbraucher.update()
            MedienSpeicher.update()
            MedienVersorger.update()
            self.OPCUA.push_data()

            # Zeit synkronisieren
            # time.sleep(60-(datetime.now().second+datetime.now().microsecond/1000000))
            # time.sleep(5)
            time.sleep(1-(datetime.datetime.now().microsecond/1000000))	#s

    def quit(self):
        # self.OPCUA.disconnect()
        pass


    def betriebsarten(self):
        opcjson = self.OPCUA.pull_data()

        Unwetter = opcjson["Girea-Module"]["Wetter"]["unwetter"].get_value()
        Leisung = opcjson["Girea-SPS"]["Erzeuger"]["gesamt kW"].get_value() + opcjson["Girea-SPS"]["Verbraucher"]["gesamt kW"].get_value()
        Speicher = opcjson["Girea-SPS"]["Speicher"]["[0]"]["Level in %"].get_value()        ######## todo ##########
        StromNetz = opcjson["Girea-SPS"]["Netzanbieter"]["[0]"]["ist an"].get_value()        ######## todo ##########

        EMS_ID = opcjson["Girea-HMI"]["EMS"]["betriebsarten"]["ID"]
        if Speicher > 95:
            if Leisung > 0:
                EMS_ID.set_value(Energieüberschuss)
                pass # Überschuss
            else:
                EMS_ID.set_value(Normalbetrieb)
                pass #Normalbetrieb
        elif Speicher < 5:
            if StromNetz == False:
                EMS_ID.set_value(Notbetrieb)
                pass #Notbetrieb
            else:
                if Unwetter == True:
                    EMS_ID.set_value(Sicherheitsbetrieb)
                    pass #Sicherheitsbetrieb
                else:
                    EMS_ID.set_value(Normalbetrieb)
                    pass #Normalbetrieb
        else:
            if StromNetz == False:
                EMS_ID.set_value(Notbetrieb)
                pass #Notbetrieb
            else:
                if Unwetter == True:
                    EMS_ID.set_value(Sicherheitsbetrieb)
                    pass #Sicherheitsbetrieb
                else:
                    EMS_ID.set_value(Normalbetrieb)
                    pass #Normalbetrieb 

        opcjson["Girea-HMI"]["EMS"]["betriebsarten"]["text"].set_value(betriebart[EMS_ID.get_value()])

        self.OPCUA.push_data()

        return EMS_ID.get_value()
    
    def prioritasschaltung(self, betriebsartID):
        opcjson = self.OPCUA.pull_data()
        Leisung = opcjson["Girea-SPS"]["Erzeuger"]["gesamt kW"].get_value()
        MedienVerbraucher.prio(betriebsartID, Leisung)
        # if betriebsartID == Notbetrieb:
        #     Leisung = opcjson["Girea-SPS"]["Erzeuger"]["gesamt kW"].get_value()# + opcjson["Girea-SPS"]["Verbraucher"]["gesamt kW"].get_value()
        #     MedienVerbraucher.prio( Leisung)
        # else:
        #     MedienVerbraucher.prio()

