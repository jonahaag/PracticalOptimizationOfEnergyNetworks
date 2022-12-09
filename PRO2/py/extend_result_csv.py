import pandas as pd

def extend(file, save=True):
    df = pd.read_csv(file, decimal=".", sep=",")
    df = add_prices(df)
    df["Total Load"] = df["Demand Area 1"] + df["Demand Area 2"]
    df["HP Electricity Consumption [MW]"] = df["HP_Electricity_Consumption_A1[Dim 1][MW]"] + df["HP_Electricity_Consumption_A2[Dim 1][MW]"]
    df["Bio Oil Fuel Input [MW]"] = df["HOB_Fuel_Input_A1[Dim 1][MW]"] + df["HOB_Fuel_Input_A2[Dim 1][MW]"]
    df["HP Load Output [MW]"] = df["HP_Load_Output_A1[Dim 1][MW]"] + df["HP_Load_Output_A2[Dim 1][MW]"]
    df["Bio Oil Load Output [MW]"] = df["HOB_Output_Backup[Dim 1][MW]"] + df["HOB_Load_Output_A2[Dim 1][MW]"]
    # assert df.shape[1] == 43
    # assert df.shape[0] == 8760
    print(df.shape)
    if save:
        df.to_csv("results.csv", index=False)
        df.to_excel("results.csv", index=False)
    return df

def extend_step3_case1(file, save=True):
    df = pd.read_csv(file, decimal=".", sep=",")
    df = add_prices(df)
    df["Total Load"] = df["Demand Area 1"] + df["Demand Area 2"] + df["Demand Area 3"]
    df["HP Electricity Consumption [MW]"] = df["HP_Electricity_Consumption_A1[Dim 1][MW]"] + df["HP_Electricity_Consumption_A2[Dim 1][MW]"]
    df["Bio Oil Fuel Input A1 + A2 [MW]"] = df["HOB_Fuel_Input_A1[Dim 1][MW]"] + df["HOB_Fuel_Input_A2[Dim 1][MW]"]
    df["Bio Oil Fuel Input [MW]"] = df["HOB_Fuel_Input_A1[Dim 1][MW]"] + df["HOB_Fuel_Input_A2[Dim 1][MW]"] + df["HOB_Fuel_Input_A3[Dim 1][MW]"]
    df["HP Load Output [MW]"] = df["HP_Load_Output_A1[Dim 1][MW]"] + df["HP_Load_Output_A2[Dim 1][MW]"]
    df["Bio Oil Load Output A1 + A2 [MW]"] = df["HOB_Output_Backup[Dim 1][MW]"] + df["HOB_Load_Output_A2[Dim 1][MW]"]
    df["Bio Oil Load Output [MW]"] = df["HOB_Output_Backup[Dim 1][MW]"] + df["HOB_Load_Output_A2[Dim 1][MW]"] + df["HOB_Load_Output_A3[Dim 1][MW]"]
    # assert df.shape[1] == 43
    # assert df.shape[0] == 8760
    print(df.shape)
    if save:
        df.to_csv("results.csv", index=False)
        df.to_excel("results.csv", index=False)
    return df

def extend_step3_case2(file, save=True):
    df = pd.read_csv(file, decimal=".", sep=",")
    df = add_prices(df)
    df["Total Load"] = df["Demand Area 1"] + df["Demand Area 2"] + df["Demand Area 3"]
    df["HP Electricity Consumption [MW]"] = df["HP_Electricity_Consumption_A1[Dim 1][MW]"] + df["HP_Electricity_Consumption_A2[Dim 1][MW]"]
    df["Bio Oil Fuel Input [MW]"] = df["HOB_Fuel_Input_A1[Dim 1][MW]"] + df["HOB_Fuel_Input_A2[Dim 1][MW]"]
    df["HP Load Output [MW]"] = df["HP_Load_Output_A1[Dim 1][MW]"] + df["HP_Load_Output_A2[Dim 1][MW]"]
    df["Bio Oil Load Output [MW]"] = df["HOB_Output_Backup[Dim 1][MW]"] + df["HOB_Load_Output_A2[Dim 1][MW]"]
    df["Accumulator Storage Change"] = df["Accumulator_Input2[Dim 1][MW]"] - df["Accumulator_Output[Dim 1][MW]"]
    # df["Accumulator Storage Change"] = - df["Accumulator_Output[Dim 1][MW]"]
    # assert df.shape[1] == 43
    # assert df.shape[0] == 8760
    print(df.shape)
    if save:
        df.to_csv("results.csv", index=False)
        df.to_excel("results.csv", index=False)
    return df

def add_prices(df):
    prices_df = pd.read_csv("docs/prices.csv", decimal=",", sep=";", index_col=0)
    for column in prices_df.columns:
        df = df.join(prices_df[column])
    return df
