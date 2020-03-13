import subprocess
import time
import sys

from IDsend import IDsend

def reports(otsikko, lähettäjä):
    project = ""
    if "ncl" in otsikko:
        project = "NCL"
    if "icon" in otsikko:
        project = "ICON"
    if "seabourn" in otsikko:
        project = "Seabourn"

    if project == "":
        print("Ei projektia määritetty, poistutaan")
        time.sleep(2)
        exit()
    
    # Päivitä GIT (vaatii vissiin credentiaalit aina?)
    # subprocess.call([r"C:\Users\FIMAHEI2\Git\Git_branch_to_master.bat"])
    
    if "edc" in otsikko:
        subprocess.call([r"C:\Users\FIMAHEI2\Git\EngineeringTools\Scripts\eplan\Eplan_source_files.bat", project])
    if "signallist" in otsikko:
        subprocess.call([r"C:\Users\FIMAHEI2\Git\EngineeringTools\Scripts\eplan\Eplan_Excel.bat", project,"signallist"])
    if "cabling" in otsikko:
        subprocess.call([r"C:\Users\FIMAHEI2\Git\EngineeringTools\Scripts\eplan\Eplan_Excel.bat", project, "cabling"])
    if "equipment" in otsikko:
        subprocess.call([r"C:\Users\FIMAHEI2\Git\EngineeringTools\Scripts\eplan\Eplan_Excel.bat", project, "equipment"])
    if "connectionpoints" in otsikko:
        subprocess.call([r"C:\Users\FIMAHEI2\Git\EngineeringTools\Scripts\eplan\Eplan_Excel.bat", project, "connectionpoints"])

    return project

if __name__ == '__main__':
    otsikko = sys.argv[1].lower()
    lähettäjä = sys.argv[2].lower()
    # reports(otsikko, lähettäjä)
    project = reports(otsikko, lähettäjä)
    teksti = " edc/report run ended."
    IDsend(otsikko, lähettäjä, project, teksti)
    exit()