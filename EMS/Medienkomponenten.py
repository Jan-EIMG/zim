from globals import *


class Medienkomponenten():
    # eList = []
    # spsgesamtkW = None
    # hmigesamtkW = None

    # _name = "E11rzeuger"

    def __init__(self, hmiJson, spsJson):
        # super().__init__()
        self.parameter = hmiJson["Parameter"]
        self.hmiJson = hmiJson.copy()
        self.hmiJson.pop("Parameter", None)
        self.spsJson = spsJson
        self.an = self.spsJson["soll an"]



    @classmethod
    def erstellen(cls, json):
        cls.spsgesamtkW = json["Girea-SPS"][cls._name]["gesamt kW"]
        cls.hmigesamtkW = json["Girea-HMI"][cls._name]["gesamt kW"]
        mini = json["Girea-SPS"][cls._name]["min index"].get_value()
        maxi = json["Girea-SPS"][cls._name]["max index"].get_value()
        # print(mini,maxi)
        for i in range(mini,maxi+1):
            hmiJson = json["Girea-HMI"][cls._name][f"[{i}]"]
            spsJson = json["Girea-SPS"][cls._name][f"[{i}]"]
            cls.eList.append(cls(hmiJson, spsJson))
    
    @classmethod
    def update(cls):
        leistunglist = []
        # print("test list:", len(cls.eList))
        for eself in cls.eList:
            eself.hmiJson["in Betrieb"].set_value(eself.spsJson["ist an"].get_value())
            eself.hmiJson["verdrahtet"].set_value(eself.spsJson["verdrahtet"].get_value())
            leistung = eself.spsJson["kW"].get_value()
            eself.hmiJson["live kW"].set_value(round(leistung,2))
        #     leistunglist.append(leistung)
        # cls.spsgesamtkW.set_value(sum(leistunglist))
        # cls.hmigesamtkW.set_value(round(sum(leistunglist),2))

    @classmethod
    def prio(cls,betriebsartID, erzeugerkW=None):
        # sorted_keys = sorted(cls.eList, key=lambda x: x.parameter["Priotität"].get_value())
        # reverse_keys = sorted([value for value in cls.eList if value.hmiJson["SIMstartstopp"].get_value() == 2], key=lambda x: x.parameter["Priotität"].get_value(), reverse=True)
        
        all_keys = sorted(cls.eList, key=lambda x: x.parameter["Priotität"].get_value(), reverse=True)
        # hand_keys = [value for value in cls.eList if value.hmiJson["SIMstartstopp"].get_value() != 2]
        # normal_keys = [value for value in cls.eList if value.parameter["abschaltbar"].get_value() == True]
        # ueberschuss_keys = [value for value in cls.eList if value.parameter["ueberschuss"].get_value() == True]
        
        

        hand_keys = []
        normal_keys = []
        ueberschuss_keys = []
        not_keys = []
        for eself in cls.eList:
            if eself.hmiJson["SIMstartstopp"].get_value() != 2:
                hand_keys.append(eself)
            elif eself.parameter["abschaltbar"].get_value():
                normal_keys.append(eself)
            elif eself.parameter["ueberschuss"].get_value():
                ueberschuss_keys.append(eself)
            else:
                not_keys.append(eself)

        
        print("all_keys")
        print(len(all_keys))
        summenkW = 0

        for eself in hand_keys:
            if eself in all_keys:
                all_keys.remove(eself)
            kW = eself.spsJson["kW"].get_value()
            if kW == 0:
                kW = eself.parameter["DSW kW"].get_value()

            if eself.hmiJson["SIMstartstopp"].get_value() == 0:
                sollan = "Hand"
            elif eself.hmiJson["SIMstartstopp"].get_value() == 1:
                summenkW += abs(kW)
                sollan = "Hand"

        
        for eself in not_keys:
            if eself in all_keys:
                all_keys.remove(eself)

            if not eself.spsJson["ist an"].get_value():
                eself.spsJson["start"].set_value(True)


        # if betriebsartID != Energieüberschuss:
        #     for eself in ueberschuss_keys:
        #         if eself in all_keys:
        #             all_keys.remove(eself)
                
        #         if eself.spsJson["ist an"].get_value():
        #             eself.spsJson["stopp"].set_value(True)

        if betriebsartID != Notbetrieb:
            for eself in normal_keys:
                if eself in all_keys:
                    all_keys.remove(eself)

                if not eself.spsJson["ist an"].get_value():
                    eself.spsJson["start"].set_value(True)

        print(len(all_keys))
        #for i,eself in enumerate(reverse_keys):
        for eself in all_keys:
            kW = eself.spsJson["kW"].get_value()
            if kW == 0:
                kW = eself.parameter["DSW kW"].get_value()
            if erzeugerkW == None:
                eself.spsJson["start"].set_value(True)
                # summenkW += abs(kW)
                sollan = True
            if erzeugerkW-summenkW >= abs(kW):
                eself.spsJson["start"].set_value(True)
                summenkW += abs(kW)
                sollan = True
            else:
                eself.spsJson["stopp"].set_value(True)
                sollan = False
                
            
            # eself.an 
            # eself.spsJson["ist an"]
            # eself.spsJson["soll an"]
            # print("prio:",eself.parameter["Priotität"].get_value(),"soll an:", sollan, "rest leistung:",erzeugerkW-summenkW)#get_live
        print("---------------------------------------------")
            