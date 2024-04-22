import csv
import pandas as pd


def budget_check():
    df_result = pd.read_csv("../result.csv", names = ["material", "material_kg"])
    df = pd.read_csv("all_material_new.csv")
    material_budget = 0
    for name in df_result["material"]:
    #df_search = df.query(f"phonetic == {name}")
        df_search = df[df["phonetic"] == name]
        if len(df_search) == 0:
            continue
        else:
            price_mean = df_search["average_price"].mean()
        #print(price_mean)
        df_material_kg = df_result[df_result["material"] == name]
        if len(df_material_kg) == 0:
            continue
        else:
            material_kg = float(df_material_kg["material_kg"])
            material_budget += material_kg * price_mean

    return(int(material_budget))
#print(material_budget)
