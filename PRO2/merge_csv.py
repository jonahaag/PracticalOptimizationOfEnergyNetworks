import pandas as pd
import os

def merge(save=True):
    folder = input("Enter the path to the folder that contains the results as .csv-files: ")
    csv_folder_path = os.path.join(os.path.dirname(__file__),folder)
    for i, file in enumerate(os.listdir(csv_folder_path)):
        if file == ".DS_Store":
            continue
        new_df = pd.read_csv(os.path.join(csv_folder_path,file))
        if i == 0:
            df = new_df
            continue
        df = df.join(new_df[new_df.columns[1]])
    assert df.shape[1] == 21
    if save:
        # df.to_csv(os.path.join(folder, "results.csv"), index=False)
        # df.to_excel(os.path.join(folder, "results.csv"), index=False)
        df.to_csv("results.csv", index=False)
        df.to_excel("results.csv", index=False)
    return df
