import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sb

def plot_load_duration_lineplot(df, save, show):
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
    if save:
        plt.savefig("plots/load_duration_lineplot.png")
    if show:
        plt.show()
    
def plot_load_duration_stackplot(df, save, show):
    # Sort loads
    df['interval'] = 1
    df_load_sorted = df.sort_values(by=['Load'], ascending = False)
    df_load_sorted['duration'] = df_load_sorted['interval'].cumsum()
    df_load_sorted['percentage'] = df_load_sorted['duration']*100/8759
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y4 = "HP_Load_Output_A1[Dim 1][MW]"
    y5 = "HP_Load_Output_A2[Dim 1][MW]"
    y6 = "HOB_Output_Backup[Dim 1][MW]"
    y7 = "HOB_Load_Output_A2[Dim 1][MW]"
    fig, ax = plt.subplots()
    plt.stackplot(df_load_sorted["percentage"], 
                df.sort_values(by=[y1], ascending = False)[y1],
                df.sort_values(by=[y2], ascending = False)[y2],
                df.sort_values(by=[y3], ascending = False)[y3],
                df.sort_values(by=[y4], ascending = False)[y4],
                df.sort_values(by=[y5], ascending = False)[y5],
                df.sort_values(by=[y6], ascending = False)[y6],
                df.sort_values(by=[y7], ascending = False)[y7],
                labels=['Waste', 'Wood', 'Pellet', 'HP1', 'HP2', 'HOB1', 'HOB2'])
    plt.ylim(0, None)
    plt.xlim(0, None)
    ax.set_title("Load-Duration Curve")
    ax.set_xlabel("Time [%]")
    ax.set_ylabel("Load [MW]")
    plt.legend(loc='upper right')
    if save:
        plt.savefig("plots/load_duration_stackplot.png", dpi=300)
    if show:
        plt.show()
    
def plot_fuel_input_to_boiler(df, axes):
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP_Electricity_Consumption_A1[Dim 1][MW]"
    y5 = "HP_Electricity_Consumption_A2[Dim 1][MW]"
    y6 = "HOB_Fuel_Input_A1[Dim 1][MW]"
    y7 = "HOB_Fuel_Input_A2[Dim 1][MW]"
    axes[0,0].stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4] + df[y5],
                df[y6] + df[y7],
                labels=['Waste', 'Wood', 'Pellet', 'Electricity', 'Bio Oil'])
    axes[0,0].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[0,0].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[0,0].set_xlim([0,23])
    axes[0,0].set_ylim([0,None])
    axes[0,0].set_title("Fuel input to boiler")
    axes[0,0].set_xlabel("Time [h]")
    axes[0,0].set_ylabel("Fuel Input [MW]")
    axes[0,0].legend(loc='lower right')
    return axes

def plot_dh_by_fuel(df, axes):
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y4 = "HP_Load_Output_A1[Dim 1][MW]"
    y5 = "HP_Load_Output_A2[Dim 1][MW]"
    y6 = "HOB_Output_Backup[Dim 1][MW]"
    y7 = "HOB_Load_Output_A2[Dim 1][MW]"
    axes[0,1].stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4] + df[y5],
                df[y6] + df[y7],
                labels=['Waste', 'Wood', 'Pellet', 'Electricity', 'Bio Oil'])
    axes[0,1].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[0,1].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[0,1].set_xlim([0,23])
    axes[0,1].set_ylim([0,None])
    axes[0,1].set_title("DH Supply by fuel")
    axes[0,1].set_xlabel("Time [h]")
    axes[0,1].set_ylabel("DH Supply [MW]")
    axes[0,1].legend(loc='lower right')
    return axes

def plot_electricity_production_by_fuel(df, axes):
    y1 = "Waste_CHP_Electricity_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Electricity_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Electricity_Output_A2[Dim 1][MW]"

    width = 0.5
    axes[1,0].bar(df["Date (CEST)"], df[y1], width, label='Waste')
    axes[1,0].bar(df["Date (CEST)"], df[y2], width, bottom=df[y1], label='Wood')
    axes[1,0].bar(df["Date (CEST)"], df[y3], width, bottom=df[y1]+df[y2], label='Pellet')

    axes[1,0].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[1,0].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[1,0].set_xlim([-0.5,23.5])
    axes[1,0].set_ylim([0,None])
    axes[1,0].set_title("Electricity production by fuel")
    axes[1,0].set_xlabel("Time [h]")
    axes[1,0].set_ylabel("Electricity supply [MW]")
    axes[1,0].legend(loc='lower right')
    return axes

def plot_fuel_cost(df, axes):
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP_Electricity_Consumption_A1[Dim 1][MW]"
    y5 = "HP_Electricity_Consumption_A2[Dim 1][MW]"
    electricity_consumption = df[y4] + df[y5]
    y6 = "HOB_Fuel_Input_A1[Dim 1][MW]"
    y7 = "HOB_Fuel_Input_A2[Dim 1][MW]"
    axes[1,1].stackplot(df["Date (CEST)"], 
                df[y1] * 1,
                df[y2] * 200,
                df[y3] * 1000,
                electricity_consumption.multiply(df["Retail Price"]),
                (df[y6] + df[y7]) * 1400,
                labels=['Waste', 'Wood', 'Pellet', 'Electricity', 'Bio Oil'])
    axes[1,1].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[1,1].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[1,1].set_xlim([0,23])
    axes[1,1].set_ylim([0,None])
    axes[1,1].set_title("Fuel cost")
    axes[1,1].set_xlabel("Time [h]")
    axes[1,1].set_ylabel("Costs [SEK]")
    axes[1,1].legend(loc='lower right')
    return axes

def create_subplots(df, day_label, save, show):
    fig, axes = plt.subplots(2, 2)
    axes = plot_fuel_input_to_boiler(df, axes)
    axes = plot_dh_by_fuel(df, axes)
    axes = plot_electricity_production_by_fuel(df, axes)
    axes = plot_fuel_cost(df, axes)
    # lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    # lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    # fig.legend(lines[0:5], labels[0:5])
    fig.suptitle(f"Results for {df[df.columns[0]].iloc[0][0:10]} ("+day_label+")", fontsize=20)
    # plt.rc('legend', fontsize="x-small")
    plt.tight_layout()
    if save:
        fig.set_size_inches((11,7), forward=False)
        fig.savefig(f"plots/results_{df[df.columns[0]].iloc[0][0:10]}.png", dpi=500)
    if show:
        plt.show()

if __name__ == "__main__":
    show = False
    save = True
    df = pd.read_csv("bofit_results/results.csv")
    load_df = df["Thermal_Output_A1[Dim 1][MW]"] + df["Thermal_Output_A2[Dim 1][MW]"]
    df["Load"] = load_df
    prices_df = pd.read_csv("electricity_prices.csv", decimal=",", sep=";", index_col=0)
    df = df.join(prices_df["Retail Price"])
    # Plot load duration curve
    plot_load_duration_stackplot(df, save=save, show=show)
    # plot_load_duration_lineplot(df, save=save, show=show)

    # Plot special days
    day_start_ids = [1392, 4727, 7968, 2255]
    day_labels = ["max load day", "min load day", "max avg electricity price day", "min avg electricity price day"]
    # for day_id in [59, 198, 333, 95]: # max load, min load, max elec. price, min elec. price
    for (day_start_id, day_label) in zip(day_start_ids, day_labels):
        # df_day = df.iloc[(day_id-1)*24:day_id*24]
        df_day = df.iloc[day_start_id:day_start_id+24] # some weird things going on
        # Create a plot of subplots
        create_subplots(df_day, day_label=day_label, save=save, show=show)