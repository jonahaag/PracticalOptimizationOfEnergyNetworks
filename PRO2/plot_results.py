import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


def plot_load_duration_curve(df):
    # Sort loads
    df['interval'] = 1
    df_load_sorted = df.sort_values(by=['Load'], ascending = False)
    df_load_sorted['duration'] = df_load_sorted['interval'].cumsum()
    df_load_sorted['percentage'] = df_load_sorted['duration']*100/8759
    fig, ax = plt.subplots()
    sb.lineplot(x = "percentage", y = "Load", data = df_load_sorted, color="black")

    # Sort one source at a time
    df_sorted_last = df
    df_sorted_last["percentage"] = 0
    y_last = "percentage"
    for y in ["Waste_CHP_Load_Output_A1[Dim 1][MW]", "Wood_CHP_Load_Output_A1[Dim 1][MW]", "HP_Load_Output_A1[Dim 1][MW]", "HP_Load_Output_A2[Dim 1][MW]", "Pellet_CHP_Load_Output_A2[Dim 1][MW]", "HOB_Output_Backup[Dim 1][MW]", "HOB_Load_Output_A2[Dim 1][MW]"]:
        df_sorted_last = df_sorted_last.sort_values(by=["Date (CEST)"])
        df[y] = df[y] + df_sorted_last[y_last]
        df_sorted = df.sort_values(by=[y],ascending=False)
        df_sorted['duration'] = df_sorted['interval'].cumsum()
        df_sorted['percentage'] = df_sorted['duration']*100/8759
        sb.lineplot(x = "percentage", y = y, data = df_sorted)
        ax.fill_between("percentage", df_sorted[y], alpha=0.2)
        df_sorted_last = df_sorted
        y_last = y
    plt.ylim(0, None)
    plt.xlim(0, None)
    ax.set_title("Load-Duration Curve")
    ax.set_xlabel("Time (%)")
    ax.set_ylabel("Load (MW)")
    plt.show()

def plot_load_duration(df):
    # Sort loads
    df['interval'] = 1
    df_load_sorted = df.sort_values(by=['Load'], ascending = False)
    df_load_sorted['duration'] = df_load_sorted['interval'].cumsum()
    df_load_sorted['percentage'] = df_load_sorted['duration']*100/8759
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "HP_Load_Output_A1[Dim 1][MW]"
    y4 = "HP_Load_Output_A2[Dim 1][MW]"
    y5 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y6 = "HOB_Output_Backup[Dim 1][MW]"
    y7 = "HOB_Load_Output_A2[Dim 1][MW]"
    fig, ax = plt.subplots()
    plt.stackplot(df_load_sorted["percentage"], df.sort_values(by=[y1], ascending = False)[y1], df.sort_values(by=[y2], ascending = False)[y2], df.sort_values(by=[y3], ascending = False)[y3], df.sort_values(by=[y4], ascending = False)[y4], df.sort_values(by=[y5], ascending = False)[y5], df.sort_values(by=[y6], ascending = False)[y6], df.sort_values(by=[y7], ascending = False)[y7])
    plt.ylim(0, None)
    plt.xlim(0, None)
    ax.set_title("Load-Duration Curve")
    ax.set_xlabel("Time (%)")
    ax.set_ylabel("Load (MW)")
    plt.show()

# def create_subplots():
#     plot_fuel_input_to_boiler()
#     plot_dh_by_fuel()
#     plot_fuel_cost()
#     plot_electricity_production_by_fuel()


if __name__ == "__main__":
    df = pd.read_csv("bofit_results/results.csv")
    load_df = df["Thermal_Output_A1[Dim 1][MW]"] + df["Thermal_Output_A2[Dim 1][MW]"]
    df["Load"] = load_df

    # Plot load duration curve
    plot_load_duration(df)
    # plot_load_duration_curve(df)
 