
from Medienkomponenten import Medienkomponenten

class MedienSpeicher(Medienkomponenten):
    eList = []
    spsgesamtkW = None
    hmigesamtkW = None
    spsgesamtkWh = None
    hmigesamtkWh = None

    _name = "Speicher"


    @classmethod
    def erstellen(cls, json):
        cls.spsgesamtkWh = json["Girea-SPS"][cls._name]["gesamt kW/h"]
        cls.hmigesamtkWh = json["Girea-HMI"][cls._name]["gesamt kW/h"]
        super().erstellen(json)

    @classmethod
    def update(cls):
        super().update()
        leistunglisth = []
        for eself in cls.eList:
            leistungh = eself.spsJson["kW/h"].get_value()
            eself.hmiJson["live kW/h"].set_value(round(leistungh,2))
            leistunglisth.append(leistungh)
        cls.spsgesamtkWh.set_value(sum(leistunglisth))
        cls.hmigesamtkWh.set_value(round(sum(leistunglisth),2))