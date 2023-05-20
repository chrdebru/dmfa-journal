import pandas as pd

df = pd.read_csv("AN 2021-2-Frdmfas02.csv")
df["Déduction valide à partir du"] = df["Déduction valide à partir du"].map(lambda date: date.replace("/",''))
df["Déduction valide jusqu'au"] = df["Déduction valide jusqu'au"].map(lambda date: date.replace("/",''))
df["Niveau"] = df["Niveau"].map(lambda bloc : "http://kg.socialsecurity.be/resource/dmfa#WorkerRecord" if bloc == "Ligne travailleur" else "http://kg.socialsecurity.be/resource/dmfa#Occupation")

idVals = []
for index, row in df.iterrows():
    idVals.append(str(row["Code DMFA"]) + "-" + row["Déduction valide à partir du"])
    
df.insert(0, "Id", idVals, True)


# writing into the file
df.to_csv("Adjusted_AN 2021-2-Frdmfas02.csv", index=False)
