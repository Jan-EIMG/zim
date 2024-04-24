import os.path
import sys
import time
import datetime

import json

from lxml import etree
import csv

from OPCdata import OPCdata


Lizens = {
    "Erzeuger": 3,
    "Verbraucher": 12,
    "Speicher": 2,
    "Netzanbieter": 1
}


def initDaten():    ###  initalisiere geräte parameter & debug log
    ### Log.txt saven und löschen
    File = ""
    try:
        with open("Log.txt", "r", encoding='utf-8') as inFile:
            File = inFile.read()
        with open("Log.txt", "w", encoding='utf-8') as outfile:
            outfile.write("")
    except:
        with open("Log.txt", "x", encoding='utf-8') as outfile:
            outfile.write("")

    try:
        with open("Log_historie.txt", "a", encoding='utf-8') as outfile:
            outfile.write(File)
    except:
        with open("Log_historie.txt", "x", encoding='utf-8') as outfile:
            outfile.write(File)

def log(text):
    if not isinstance(text, str):
        text = str(text)
    print("Log"+text)
    try:
        with open("Log.txt", "x", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")
    except:
        with open("Log.txt", "a", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")



def idtext(DisplayName):

    # print(DisplayName)
    if DisplayName == "root":
        return "i=85"
    with open(r"XML_generierung\NodeIds.json", "r", encoding='utf-8') as jsonFile:
        try:
            jsondata = json.load(jsonFile)
        except: 
            jsondata = {}
    try:
        ns= jsondata[DisplayName]["ns"]
        i = jsondata[DisplayName]["i"]
    except:
        try:
            ns = max(jsondata.values(), key=lambda x: x["ns"])["ns"]
            i = max(jsondata.values(), key=lambda x: x["i"])["i"] + 1
        except:
            ns = 1
            i =  1
        jsondata[DisplayName] = {"ns":ns,"i":i}
        with open(r"XML_generierung\NodeIds.json", "w", encoding='utf-8') as jsonFile:
            json.dump(jsondata, jsonFile, indent=4)

    return f"ns={ns};i={i}" 

def references(ua_object,mother, kits=[]):
    references = etree.SubElement(ua_object, "References")
    etree.SubElement(references, "Reference", ReferenceType="HasComponent", IsForward="false").text = idtext(mother)
    etree.SubElement(references, "Reference", ReferenceType="HasTypeDefinition").text = "i=58"
    for kit in kits:
        etree.SubElement(references, "Reference", ReferenceType="HasComponent").text = idtext(kit)

def ua_object(DisplayName,mother, kits=[]):
    ua_object = etree.SubElement(root, "UAObject", NodeId=idtext(DisplayName), BrowseName=f"1:{DisplayName}", ParentNodeId=idtext(mother))
    etree.SubElement(ua_object, "DisplayName").text = DisplayName
    etree.SubElement(ua_object, "Description").text = DisplayName
    references(ua_object, mother , kits)

def ua_type(Value):
    if isinstance(Value, bool):
        return "Boolean"
    elif isinstance(Value, int):
        return "Int64"
        # return "Int16"
    elif isinstance(Value, float):
        return "Double"
    elif isinstance(Value, str):
        return "String"
    elif isinstance(Value, datetime.date):
        return "DateTime"
    # elif isinstance(Value, ):
    #     return "Int64"
    # elif isinstance(Value, ):
    #     return "Int64"
    # elif isinstance(Value, ):
    #     return "Int64"

def ua_variable(DisplayName,mother, Value):
    # ua_variable = etree.SubElement(root, "UAVariable", NodeId="ns=1;i=5", BrowseName="1:EMS_system_aktuelle zeit in minuten", ParentNodeId="ns=1;i=3", DataType="Double", AccessLevel="3", UserAccessLevel="3")
    ua_variable = etree.SubElement(root, "UAVariable", NodeId=idtext(DisplayName), BrowseName=f"1:{DisplayName}", ParentNodeId=idtext(mother), DataType=ua_type(Value), AccessLevel="3", UserAccessLevel="3")
    etree.SubElement(ua_variable, "DisplayName").text = DisplayName
    etree.SubElement(ua_variable, "Description").text = DisplayName
    references(ua_variable, mother)
    ua_value = etree.SubElement(ua_variable, "Value")
    etree.SubElement(ua_value, "{http://opcfoundation.org/UA/2008/02/Types.xsd}"+ua_type(Value)).text = str(Value)

def Create_ua_object(jsondata, mother="root",  i=0, object_name=""):
    if i <= 25:
        for a, b in jsondata.items():
            
            # new_object_name = object_name+"_"+a
            # next_object_name = object_name+"_"+a
            if   i == 0:
                new_object_name = a
                # new_variable_name = ""

            elif i == 1:
                new_object_name = object_name+"_"+a
                # new_variable_name = a
            elif i >= 2:
                new_object_name = object_name+"_"+a
                # new_variable_name = object_name+"_"+a
            
            if isinstance(b, dict):
                # ua_object(new_object_name,mother, b.keys())
                ua_object(new_object_name,mother, [new_object_name+"_"+ string for string in b.keys()])
                Create_ua_object(b, new_object_name, i+1, new_object_name)

            elif isinstance(b, list):
                if a in Lizens.keys():
                    subobjects = {}
                    # subobjects = objects.add_object(idx, a)

                    mylist = list(b[0].keys())
                    # try:
                    mylist.remove("[0]")
                    # except:
                    #     pass
                    for k in mylist:
                        subobjects[k] = b[0][k]
                        # bs = {k: b[0][k]}
                        # Create_form(idx, subobjects, bs, i+1, new_object_name)

                    mylist = range(Lizens[a])
                    subobjects["min index"]= min(mylist)
                    # Create_form(idx, subobjects, bs, i+1, new_object_name)
                    subobjects["max index"]= max(mylist)
                    # Create_form(idx, subobjects, bs, i+1, new_object_name)

                    for j in mylist:
                        # bs = {str(list(b[0].keys())[0]).replace("0",str(j)): b[0][list(b[0].keys())[0]]}
                        # bs = {f"[{j}]": b[0]["[0]"]}
                        subobjects[f"[{j}]"]= b[0]["[0]"]
                        # log(bs)
                        # Create_form(idx, subobjects, bs, i+1, new_object_name)
                else:
                    subobjects = {}
                    for index, item in enumerate(b):
                        subobjects[f"[{index}]"] = item

                ua_object(new_object_name,mother, [new_object_name+"_"+ string for string in subobjects.keys()])
                Create_ua_object(subobjects, new_object_name, i+1, new_object_name)
                    

            else:
                # print(new_object_name)
                ua_variable(new_object_name,mother, b)

    return jsondata



if __name__ == "__main__":
    # initDaten()


    # with open("OPC-Data.json", "r", encoding='utf-8') as jsonFile:
    #     jsondata = json.load(jsonFile)
    #     Create_form(idx,objects, jsondata)


    # Create the root element
    # <UANodeSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:uax="http://opcfoundation.org/UA/2008/02/Types.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd">
    root = etree.Element("UANodeSet", nsmap={None: "http://opcfoundation.org/UA/2011/03/UANodeSet.xsd", 
                                             "xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                             "uax": "http://opcfoundation.org/UA/2008/02/Types.xsd",
                                             "xsd": "http://www.w3.org/2001/XMLSchema"})


    namespace_uris = etree.SubElement(root, "NamespaceUris")
    uri = etree.SubElement(namespace_uris, "Uri")
    uri.text = "http://examples.freeopcua.github.io"

    aliases = etree.SubElement(root, "Aliases")
    alias_list = [
        ("Boolean", "i=1"),
        ("Int64", "i=8"),
        ("Double", "i=11"),
        ("String", "i=12"),
        ("DateTime", "i=13"),
        ("Organizes", "i=35"),
        ("HasTypeDefinition", "i=40"),
        ("HasComponent", "i=47")
    ]
    for alias, value in alias_list:
        etree.SubElement(aliases, "Alias", Alias=alias).text = value

    # with open(r"XML_generierung\OPC-Data.json", "r", encoding='utf-8') as jsonFile:
    #     jsondata = json.load(jsonFile)
    #     Create_ua_object(jsondata)
    Create_ua_object(OPCdata)
    # XML-Datei schreiben
    tree = etree.ElementTree(root)
    # tree.write(r'XML_generierung\OPC-UA.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
    tree.write(r'OPCUA\OPC-UA.xml', pretty_print=True, xml_declaration=True, encoding='utf-8') 


    