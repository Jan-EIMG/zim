from EMS import EMS

def main():
    #todo: # Laden der "Lizensdatei"

    #todo: # Laden der "Configdatai"

    # erstellen eines neuen GIREA EMS
    ems = EMS()

    # Sterten des erstellen GIREA EMS
    ems.start()

    # wenn des erstellen GIREA EMS nicht mehr im Mail Loop ist
    ems.quit()


if __name__ == '__main__':
    main()