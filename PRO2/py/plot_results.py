import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

color_map = ["#d3bcaf", "#ffd14f", "#417505", "#9fb7c9", "#5e5e5e", "#B33F40"]
labels = ['Waste', 'Wood', 'Bio Pellet', 'Electricity', 'Bio Oil', 'DH']
  
def plot_load_duration_stackplot(df, plots_folder, save):
    # Sort loads
    df['interval'] = 1
    df_load_sorted = df.sort_values(by=['Total Load'], ascending = False)
    df_load_sorted['duration'] = df_load_sorted['interval'].cumsum()
    df_load_sorted['percentage'] = df_load_sorted['duration']*100/8760
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y4 = "HP Load Output [MW]"
    y5 = "Bio Oil Load Output [MW]"
    fig, ax = plt.subplots()
    plt.stackplot(df_load_sorted["percentage"], 
                df.sort_values(by=[y1], ascending = False)[y1],
                df.sort_values(by=[y2], ascending = False)[y2],
                df.sort_values(by=[y3], ascending = False)[y3],
                df.sort_values(by=[y4], ascending = False)[y4],
                df.sort_values(by=[y5], ascending = False)[y5],
                labels=labels,
                colors=color_map)
    plt.ylim(0, None)
    plt.xlim(0, None)
    ax.set_title("Load-Duration Curve")
    ax.set_xlabel("Time [%]")
    ax.set_ylabel("Load [MW]")
    plt.legend(loc='upper right')
    if save:
        plt.savefig(os.path.join(plots_folder, "load_duration_stackplot.png"), dpi=300)

def plot_chp_use(df, plots_folder, save):
    y = ["Waste_Turbine_Load_A1[Dim 1][MW]", "Wood_Turbine_Load_A1[Dim 1][MW]", "Pellet_Turbine_Load_A2[Dim 1][MW]",
        "Waste_BP_Load_A1[Dim 1][MW]", "Wood_BP_Load_A1[Dim 1][MW]", "Pellet_BP_Load_A2[Dim 1][MW]"]
    fig, axes = plt.subplots(3,1)
    plt.rc('legend', fontsize="x-small")
    for i in range(3):
        axes[i].plot(df["Date (CEST)"], df[y[i]], label=labels[i]+" Turbine", color=color_map[i])
        axes[i].plot(df["Date (CEST)"], df[y[i+3]], label=labels[i]+" BP", color=color_map[i+3], alpha=0.5)
        axes[i].xaxis.set_major_locator(ticker.MultipleLocator(2400))
        axes[i].xaxis.set_major_formatter(ticker.ScalarFormatter())
        axes[i].set_xlim([-0.5,8760.5])
        axes[i].set_ylim([0,None])
        axes[i].set_xlabel("Time [h]")
        axes[i].set_ylabel("Load [MW]")
        axes[i].legend(loc='best')
    plt.tight_layout()
    if save:
        plt.savefig(os.path.join(plots_folder,"chp_use.png"), dpi=300)

def plot_chp_use_bar(df, plots_folder, save):
    fig, ax = plt.subplots()
    width = 0.8
    ax.bar("Waste", df["Waste_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, label="Turbine", color="#e69138")
    ax.bar("Waste", df["Waste_BP_Load_A1[Dim 1][MW]"].sum(), bottom=df["Waste_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, label="BP", color="#3d85c6")
    ax.bar("Wood", df["Wood_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, color="#e69138")
    ax.bar("Wood", df["Wood_BP_Load_A1[Dim 1][MW]"].sum(), bottom=df["Wood_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, color="#3d85c6")
    ax.bar("Bio Pellet", df["Pellet_Turbine_Load_A2[Dim 1][MW]"].sum(), width=width, color="#e69138")
    ax.bar("Bio Pellet", df["Pellet_BP_Load_A2[Dim 1][MW]"].sum(), bottom=df["Pellet_Turbine_Load_A2[Dim 1][MW]"].sum(), width=width, color="#3d85c6")
    ax.legend(loc='best')
    ax.set_ylabel("Load [MW]")
    if save:
        plt.savefig(os.path.join(plots_folder,"chp_use_bar.png"), dpi=300)

def plot_fuel_input(df, ax, title):
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP Electricity Consumption [MW]"
    y5 = "Bio Oil Fuel Input [MW]"
    ax.stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4],
                df[y5],
                labels=labels,
                colors=color_map)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xlim([0,23])
    ax.set_ylim([0,None])
    ax.set_title(title)
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Fuel Input [MW]")

def plot_dh_by_fuel(df, ax, title):
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y4 = "HP Load Output [MW]"
    y5 = "Bio Oil Load Output [MW]"
    ax.stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4],
                df[y5],
                labels=labels,
                colors=color_map)
    ax.plot(df["Date (CEST)"],
            df["Total Load"],
            label=labels[5],
            color=color_map[5])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xlim([0,23])
    ax.set_ylim([0,None])
    ax.set_title(title)
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("DH Supply [MW]")

def plot_electricity_production_by_fuel(df, ax, title):
    y1 = "Waste_CHP_Electricity_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Electricity_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Electricity_Output_A2[Dim 1][MW]"

    width = 0.5
    ax.bar(df["Date (CEST)"], df[y1], width, label=labels[0], color=color_map[0])
    ax.bar(df["Date (CEST)"], df[y2], width, bottom=df[y1], label=labels[1], color=color_map[1])
    ax.bar(df["Date (CEST)"], df[y3], width, bottom=df[y1]+df[y2], label=labels[2], color=color_map[2])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xlim([-0.5,23.5])
    ax.set_ylim([0,(df[y1]+df[y2]+df[y3]).max()*1.1])
    ax.set_title(title)
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Electricity supply [MW]")

def plot_fuel_cost(df, ax, electricity_price, title):
    electricity_price_label = "Retail Price " + electricity_price
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP Electricity Consumption [MW]"
    y5 = "Bio Oil Fuel Input [MW]"
    ax.stackplot(df["Date (CEST)"], 
                df[y1].multiply(df["Waste Price"]),
                df[y2].multiply(df["Wood Price"]),
                df[y3].multiply(df["Bio Pellet Price"]),
                df[y4].multiply(df[electricity_price_label]),
                df[y5].multiply(df["Bio Oil Price"]),
                labels=labels,
                colors=color_map)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xlim([0,23])
    ax.set_ylim([0,None])
    ax.set_title(title)
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Costs [SEK]")

def pick_position_of_subplot(i):
    if i == 0:
        return 0, 0
    elif i == 1:
        return 0,1
    elif i == 2:
        return 1,0
    elif i == 3:
        return 1,1
    
def plot_subplots(df, electricity_price, plots_folder, save):
    fig_1, axes_1 = plt.subplots(2,2)
    fig_2, axes_2 = plt.subplots(2,2)
    fig_3, axes_3 = plt.subplots(2,2)
    fig_4, axes_4 = plt.subplots(2,2)
    fig_5, axes_5 = plt.subplots(2,2)
    fig_6, axes_6 = plt.subplots(2,2)
    fig_7, axes_7 = plt.subplots(2,2)
    fig_8, axes_8 = plt.subplots(2,2)
    figs = [fig_1, fig_2, fig_3, fig_4, fig_5, fig_6 , fig_7, fig_8]
    axes = [axes_1, axes_2, axes_3, axes_4, axes_5, axes_6, axes_7, axes_8]

    for i, day_start_id in enumerate([1392, 4727, 7968, 2255]):
        df_day = df.iloc[day_start_id:day_start_id+24]
        day_string = str(df_day[df_day.columns[0]].iloc[0][0:10])
        j, k = pick_position_of_subplot(i)

        plot_fuel_input(df_day, axes[i][0,0], title="Fuel input to boiler")
        plot_fuel_input(df_day, axes[4][j,k], title=day_string)

        plot_dh_by_fuel(df_day, axes[i][0,1], title="DH Supply by fuel")
        plot_dh_by_fuel(df_day, axes[5][j,k], title=day_string)

        plot_electricity_production_by_fuel(df_day, axes[i][1,0], title="Electricity production by fuel")
        plot_electricity_production_by_fuel(df_day, axes[6][j,k], title=day_string)

        plot_fuel_cost(df_day, axes[i][1,1], electricity_price, title="Fuel Cost")
        plot_fuel_cost(df_day, axes[7][j,k], electricity_price, title=day_string)

        lines_labels = [ax.get_legend_handles_labels() for ax in figs[i].axes]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        figs[i].legend(lines[0:6], labels[0:5]+["Demand"], ncol=6, loc='center')
        figs[i].tight_layout()
        if save:
            figs[i].set_size_inches((11,7), forward=False)
            figs[i].savefig(os.path.join(plots_folder,f"results_{day_string}.png"), dpi=500)
        
        plot_cost_revenue(df_day, electricity_price, plots_folder, save)
        plot_prices(df_day, electricity_price, plots_folder, save)

    for i, result_type in enumerate(["fuel_input", "dh_by_fuel", "electricity_production", "fuel_cost"]):
        lines_labels = [ax.get_legend_handles_labels() for ax in figs[i+4].axes]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        if i == 1:
            figs[i+4].legend(lines[0:6], ["Demand"]+labels[1:6], ncol=6, loc='center')
        elif i == 2:
            figs[i+4].legend(lines[0:3], labels[0:3], ncol=3, loc='center')
        else:
            figs[i+4].legend(lines[0:5], labels[0:5], ncol=5, loc='center')
        figs[i+4].suptitle(result_type)
        figs[i+4].tight_layout()
        if save:
            figs[i+4].set_size_inches((11,7), forward=False)
            figs[i+4].savefig(os.path.join(plots_folder,f"results_{result_type}_all_days.png"), dpi=500)

def plot_cost_revenue(df, electricity_price, plots_folder, save):
    retail_label = "Retail Price " + electricity_price
    spot_label = "Spot Price " + electricity_price

    waste_cost = df["Waste_Fuel_Input_A1[Dim 1][MW]"].multiply(df["Waste Price"]).sum()
    wood_cost = df["Wood_Fuel_Input_A1[Dim 1][MW]"].multiply(df["Wood Price"]).sum()
    pellet_cost = df["Pellet_Fuel_Input_A2[Dim 1][MW]"].multiply(df["Bio Pellet Price"]).sum()
    electricity_cost = df["HP Electricity Consumption [MW]"].multiply(df[retail_label]).sum()
    oil_cost = df["Bio Oil Fuel Input [MW]"].multiply(df["Bio Oil Price"]).sum()

    waste_revenue = df["Waste_CHP_Electricity_Output_A1[Dim 1][MW]"].multiply(df[spot_label]).sum()
    wood_revenue = df["Wood_CHP_Electricity_Output_A1[Dim 1][MW]"].multiply(df[spot_label]).sum()
    pellet_revenue = df["Pellet_CHP_Electricity_Output_A2[Dim 1][MW]"].multiply(df[spot_label]).sum()
    electricity_revenue = waste_revenue + wood_revenue + pellet_revenue
    dh_revenue = df["Total Load"].multiply(df["DH Price"]).sum()

    width = .8
    fig, ax = plt.subplots()

    bottom = 0
    # for i, cost in enumerate([waste_cost, wood_cost, pellet_cost, electricity_cost, oil_cost]):
    costs = sorted(list(zip([waste_cost, wood_cost, pellet_cost, electricity_cost, oil_cost],range(5))),reverse=True)
    for cost, i in costs:
        ax.bar("Cost", cost, width=width, bottom=bottom, label=labels[i], color=color_map[i])
        bottom += cost
    
    bottom = 0
    # for i, revenue in enumerate([waste_revenue, wood_revenue, pellet_revenue, dh_revenue]):
    revenues = sorted(list(zip([electricity_revenue, dh_revenue],range(2))),reverse=True)
    for revenue, i in revenues:
        ax.bar("Revenue", revenue, width=width, bottom=bottom, label="" if i==0 else labels[5], color=color_map[i*2+3])
        bottom += revenue

    # ax.set_xlabel("Time [%]")
    ax.set_ylabel("Money [SEK]")
    ax.legend(loc='upper left')
    if save:
        plt.savefig(os.path.join(plots_folder,f"costs_{df[df.columns[0]].iloc[0][0:10]}.png"), dpi=300)

def plot_prices(df, electricity_price, plots_folder, save):
    plt.subplot(111)
    for i, price in enumerate(["Waste Price", "Wood Price", "Bio Pellet Price", "Retail Price " + electricity_price, "Bio Oil Price", "Spot Price " + electricity_price]):
        plt.plot(df["Date (CEST)"], df[price], label=price, color=color_map[i])
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xlim([0,23])
    ax.set_ylim([0,None])
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Price [SEK/kWh]")
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=3)
    if save:
        plt.savefig(os.path.join(plots_folder,f"prices_{df[df.columns[0]].iloc[0][0:10]}.png"), dpi=300)

def create_plots(df, electricity_price, save, show):
    plots_folder = "plots_" + electricity_price
    if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)

    plot_load_duration_stackplot(df, plots_folder, save)
    plot_chp_use(df, plots_folder, save)
    plot_chp_use_bar(df, plots_folder, save)
    plot_subplots(df, electricity_price, plots_folder, save)

    if show:
        #TODO this is a bit messed up
        plt.show()