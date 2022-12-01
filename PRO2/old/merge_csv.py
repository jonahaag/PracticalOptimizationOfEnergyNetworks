import pandas as pd
import os

def merge(folder, save=True):
    csv_folder_path = os.path.join(os.path.dirname(__file__),folder)
    for i, file in enumerate(os.listdir(csv_folder_path)):
        if file == ".DS_Store":
            continue
        new_df = pd.read_csv(os.path.join(csv_folder_path,file))
        if i == 0:
            df = new_df
            continue
        df = df.join(new_df[new_df.columns[1]])
    df["Total Load"] = df["Thermal_Output_A1[Dim 1][MW]"] + df["Thermal_Output_A2[Dim 1][MW]"]
    df["HP Electricity Consumption [MW]"] = df["HP_Electricity_Consumption_A1[Dim 1][MW]"] + df["HP_Electricity_Consumption_A2[Dim 1][MW]"]
    df["Bio Oil Fuel Input [MW]"] = df["HOB_Fuel_Input_A1[Dim 1][MW]"] + df["HOB_Fuel_Input_A2[Dim 1][MW]"]
    df["HP Load Output [MW]"] = df["HP_Load_Output_A1[Dim 1][MW]"] + df["HP_Load_Output_A2[Dim 1][MW]"]
    df["Bio Oil Load Output [MW]"] = df["HOB_Output_Backup[Dim 1][MW]"] + df["HOB_Load_Output_A2[Dim 1][MW]"]
    df = add_prices(df)
    assert df.shape[1] == 37
    if save:
        # df.to_csv(os.path.join(folder, "results.csv"), index=False)
        # df.to_excel(os.path.join(folder, "results.csv"), index=False)
        df.to_csv("results.csv", index=False)
        df.to_excel("results.csv", index=False)
    return df

def add_prices(df):
    prices_df = pd.read_csv("prices.csv", decimal=",", sep=";", index_col=0)
    for column in prices_df.columns:
        df = df.join(prices_df[column])
    return df
