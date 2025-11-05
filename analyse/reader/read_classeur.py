import pandas as pd

def read_classeur(path):
    df = pd.read_excel(path)
    text = ""
    for colonne in df:
        for case in df[colonne]:
            text += " " + str(case)
    return text
