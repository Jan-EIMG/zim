
import datetime

OPCdata = {
    "Girea-HMI":{
        "EMS":{
            "system":{
                "Datum": datetime.datetime(2000, 1, 1),#datetime.datetime.now(),
                "debag": True,
                "aktuelle zeit in minuten": 0.0,
                "aktuelle zeit in sekunden": 0.0,
                "Loade backup": 1      #difoult lade modell 1          # 1=base; 2="Notbetrieb"; 3="Normalbetrieb"; 4="Sicherheitsbetrieb"; 5="Energieüberschuss"
            },
            "betriebsarten":{
                "ID":0,
                "text":"öäü"
            },
            "Parameter":{
                "api-Key-hand-eingabe": False,
                "Lizens":{
                    "Erzeuger": 10,
                    "Verbraucher": 10,
                    "Speicher": 5,
                    "Netzanbieter": 1
                },
                "standort":{
                    "longitude": "",
                    "latitude": ""
                }
            },
            "vorhersage":{
                "vorhersage zeitkunkt": datetime.datetime(2000, 1, 1),#datetime.datetime.now()
            }
        },
        "Erzeuger":[{
            "gesamt kW":0.0,
            "gesamt kW in einer stunde":0.0,
            "[0]":{
                "Parameter":{
                    "Geändert durch": "startwerte",
                    "Name":"Erzeuger",
                    "Kennzeichnung":"",
                    "DSW kW": 0.0,
                    "NennLeistung": 0.0,
                    "abschaltbar":False,
                    "Priotität":0,
                    "anlauf-zeit in s":0,
                    "MIN-Laufzeit in s": 0,
                    "DSW-Laufzeit in s": 0,
                    "MAX-Laufzeit in s": 0,
                    "MIN-Pausenzeit in s": 0,
                    "DSW-Pausenzeit in s": 0,
                    "MAX-Pausenzeit in s": 0,
                    "tages-Laufzeit in %": 0,

                    "heitzwert": 0.0,
                    "E-wirkungsgrad": 0.0,
                    "Gasmange": 0.0,
                    "wärmegeführt": False,
                    "elektrischer wirkungsgrad": 0.0,
                    "heitz wirkungsgrad": 0.0,
                    "Energieleistung kWh/mm3": 0.0,
                    "Heizwert kWh/m3": 0.0,
                    "dod Wert Gasspeicher": 0.0,
                    "Gasmenge m³":0.0,

                    "ausrichtung": 0.0,
                    "winkel": 0.0,
                    "dämpfung morgen": 0.0,
                    "dämpfung abend": 0.0,
                    "kWp": 0.0,
                    "max kVA": 0.0,

                },
                "type":"BHKW",
                "SIMstartstopp":2,    # 0=aus; 1=an; 2=auto
                "in Betrieb":False,
                "live kW":0.0,
                "live int kW":0,
                "kW in einer stunde":0.0,
                "verdrahtet":False,
            }
        }],
        "Verbraucher":[{
            "gesamt kW":0.0,
            "gesamt kW in einer stunde":0.0,
            "[0]":{
                "Parameter":{
                    "Komponenten art": "??- ",
                    "Geändert durch": "startwerte",
                    "Name":"Verbraucher",
                    "Kennzeichnung":"",
                    "DSW kW":0.0,
                    "NennLeistung":0,
                    "abschaltbar":False,
                    "ueberschuss":False,
                    "Priotität":0,
                    "anlauf-zeit in s":0,
                    "MIN-Laufzeit in s": 0,
                    "DSW-Laufzeit in s": 0,
                    "MAX-Laufzeit in s": 0,
                    "MIN-Pausenzeit in s": 0,
                    "DSW-Pausenzeit in s": 0,
                    "MAX-Pausenzeit in s": 0,
                    "tages-Laufzeit in %": 0
                },
                "SIMstartstopp":2,    # 0=aus; 1=an; 2=auto
                "in Betrieb":False,
                "live kW":0.0,
                "live int kW":0,
                "kW in einer stunde":0.0,
                "verdrahtet":False
            }
        }],
        "Speicher":[{
            "gesamt kW":0.0,
            "gesamt kW/h":0.0,
            "gesamt %":0.0,
            "restlauf-zeit in h":0,
            "gesamt kW in einer stunde":0.0,
            "gesamt % in einer stunde":0.0,
            "[0]":{
                "Parameter":{
                    "Geändert durch": "startwerte",
                    "Name":"Speicher",
                    "Kennzeichnung":"",
                    "max kW/h": 0.0,
                    "max kWh int": 0,
                    "max kW": 0.0,
                    "max lade kW":0.0,
                    "max etlade kW": 0.0,
                    "DoD": 0.0,
                    "c-rate": 0.0,
                    "SOC": 0.0,
                    "SOH": 0.0,
                    "Sicherheitspuffer": 0.0,
                    "anlauf-zeit in s":0
                },
                "aus wert in %": 0,
                "SIMstartstopp":2,    # 0=aus; 1=an; 2=auto
                "in Betrieb":False,
                "live kW":0.0,
                "live int kW":0,
                "live kW/h":0.0,
                "live int kWh":0,
                "verdrahtet":False,
                "MIN-Laufzeit in s": 0,
                "DSW-Laufzeit in s": 0,
                "MAX-Laufzeit in s": 0,
                "MIN-Pausenzeit in s": 0,
                "DSW-Pausenzeit in s": 0,
                "MAX-Pausenzeit in s": 0,
                "tages-Laufzeit in %": 0,
                "kW in einer stunde":0.0,
                "% in einer stunde":0.0
            }
        }],
        "Netzanbieter":[{
            "gesamt kW":0.0,
            "gesamt kW in einer stunde":0.0,
            "[0]":{
                "Parameter":{
                    "Geändert durch": "startwerte",
                    "Name":"Netzanbieter",
                    "Kennzeichnung":"",
                },
                "SIMstartstopp":1,    # 0=aus; 1=an; ohne 2=auto
                "in Betrieb":False,
                "live kW":0.0,
                "live int kW":0,
                "kW in einer stunde":0.0,
                "verdrahtet":False
            }
        }],
        "Wetter":{
            "API-Key": "",
            "unwetter": False,
            "SIMstartstopp":2,    # 0=aus; 1=unwetter; 2=auto
            "weather": [
            {
                "id": 501,
                "main": "Rain",
                "description": "moderate rain",
                "description-DE": "mäßiger Regen",
                "icon": "10d"
            }
            ],
            "main": {
                "temp": 298.48,
                "feels_like": 298.74,
                "temp_min": 297.56,
                "temp_max": 300.05,
                "pressure": 1015,
                "humidity": 64,
                "sea_level": 1015,
                "grnd_level": 933
            },
            "wind": {
                "speed": 0.62,
                "deg": 349,
                "gust": 1.18
            },
            "rain": {
                "1h": 3.16
            },
            "clouds": {
                "all": 100
            }
        },
        "PV-vorkas":{
            "API-Key": "",
            "live soll kW": 0.0
        },
        "Parameter":{
            "ID":"v00",
            "Geändert durch": "",
            "1 Bezeichnung": "Name",
            "1 Wert": "startwerte",
            "1 info": "",
            "1 max char len":10,
            "1 Falsche eingabe": False,
            "2 Bezeichnung": "",
            "2 info": "",
            "2 max char len":10,
            "2 Wert": "",
            "2 Falsche eingabe": False,
            "3 Bezeichnung": "",
            "3 info": "",
            "3 max char len":10,
            "3 Wert": 0.0,
            "3 Falsche eingabe": False,
            "4 Bezeichnung": "",
            "4 info": "",
            "4 max char len":10,
            "4 Wert": 0.0,
            "4 Falsche eingabe": False,
            "5 Bezeichnung": "",
            "5 info": "",
            "5 max char len":10,
            "5 Wert": 0.0,
            "5 Falsche eingabe": False,
            "6 Bezeichnung": "",
            "6 info": "",
            "6 max char len":10,
            "6 Wert": 0.0,
            "6 Falsche eingabe": False,
            "7 Bezeichnung": "",
            "7 info": "",
            "7 max char len":10,
            "7 Wert": 0.0,
            "7 Falsche eingabe": False,
            "8 Bezeichnung": "",
            "8 info": "",
            "8 max char len":10,
            "8 Wert": 0.0,
            "8 Falsche eingabe": False,
            "9 Bezeichnung": "",
            "9 info": "",
            "9 max char len":10,
            "9 Wert": 0.0,
            "9 Falsche eingabe": False,
            "10 Bezeichnung": "",
            "10 info": "",
            "10 max char len":10,
            "10 Wert": 0.0,
            "10 Falsche eingabe": False,
            "11 Bezeichnung": "Name",
            "11 info": "",
            "11 max char len":10,
            "11 Wert": 0.0,
            "11 Falsche eingabe": False,
            "12 Bezeichnung": "",
            "12 info": "",
            "12 max char len":10,
            "12 Wert": 0.0,
            "12 Falsche eingabe": False,
            "13 Bezeichnung": "",
            "13 info": "",
            "13 max char len":10,
            "13 Wert": 0.0,
            "13 Falsche eingabe": False,
            "14 Bezeichnung": "",
            "14 info": "",
            "14 max char len":10,
            "14 Wert": 0.0,
            "14 Falsche eingabe": False,
            "15 Bezeichnung": "",
            "15 info": "",
            "15 max char len":10,
            "15 Wert": 0.0,
            "15 Falsche eingabe": False,
            "16 Bezeichnung": "",
            "16 info": "",
            "16 max char len":10,
            "16 Wert": 0.0,
            "16 Falsche eingabe": False,
            "17 Bezeichnung": "",
            "17 info": "",
            "17 max char len":10,
            "17 Wert": 0.0,
            "17 Falsche eingabe": False,
            "18 Bezeichnung": "",
            "18 info": "",
            "18 max char len":10,
            "18 Wert": False,
            "18 Falsche eingabe": False,
            "19 Bezeichnung": "",
            "19 info": "",
            "19 max char len":10,
            "19 Wert": False,
            "19 Falsche eingabe": False,
            "20 Bezeichnung": "",
            "20 info": "",
            "20 max char len":10,
            "20 Wert": False,
            "20 Falsche eingabe": False,
            "Speichern": False,
            "Laden": False,
            "Clear": False,
        },
    },
    "Girea-SPS":{
        "Erzeuger":[{
            "gesamt kW":0.0,
            "[0]":{
                "simuliert": False,
                "automatik": False,
                "live bit": False,
                "verdrahtet":False,
                "ist an": False,
                "soll an": False,
                "start":False,
                "stopp":False,
                "kW":0.0,
                "potenziele kW/h":0.0
            }
        }],
        "Verbraucher":[{
            "gesamt kW":0.0,
            "[0]":{
                "simuliert": False,
                "automatik": False,
                "live bit": False,
                "verdrahtet":False,
                "ist an": False,
                "soll an": False,
                "start":False,
                "stopp":False,
                "kW":0.0

            }
        }],
        "Speicher":[{
            "gesamt kW":0.0,
            "gesamt kW/h":0.0,
            "[0]":{
                "simuliert": False,
                "automatik": False,
                "live bit": False,
                "verdrahtet": False,
                "ist an": False,
                "soll an": False,
                "start": False,
                "stopp": False,
                "kW": 0.0,
                "kW/h": 0.0,
                "Level in %":0.0

            }
        }],
        "Netzanbieter":[{
            "gesamt kW":0.0,
            "[0]":{
                "simuliert": False,
                "automatik": False,
                "live bit": False,
                "verdrahtet": False,
                "ist an": False,
                "soll an": False,
                "kW":0.0
            }
        }]
    },
    "Girea-Module":{
        "EMS":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0
        },
        "Wetter":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0,
            "unwetter": False
        },
        "DB":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0
        },
        "SIM":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0
        },
        "Summe":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0
        },
        "Parameter":{
            "live bit": False,
            "zyklus": 0,
            "zyklus-time": 0,
            "core-time": 0
        }
    }
}
    


