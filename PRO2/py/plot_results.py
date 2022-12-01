import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

color_map = ["#d3bcaf", "#ffd14f", "#417505", "#9fb7c9", "#5e5e5e", "#B33F40"]
labels = ['Waste', 'Wood', 'Bio Pellet', 'Electricity', 'Bio Oil', 'DH']
  
def plot_load_duration_stackplot(df, plots_folder, save, show):
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
    if show:
        plt.show()
    
def plot_fuel_input_to_boiler(df, axes):
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP Load Output [MW]"
    y5 = "Bio Oil Load Output [MW]"
    axes[0,0].stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4],
                df[y5],
                labels=labels,
                colors=color_map)
    axes[0,0].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[0,0].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[0,0].set_xlim([0,23])
    axes[0,0].set_ylim([0,None])
    axes[0,0].set_title("Fuel input to boiler")
    axes[0,0].set_xlabel("Time [h]")
    axes[0,0].set_ylabel("Fuel Input [MW]")
    return axes

def plot_dh_by_fuel(df, axes):
    y1 = "Waste_CHP_Load_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Load_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Load_Output_A2[Dim 1][MW]"
    y4 = "HP Load Output [MW]"
    y5 = "Bio Oil Load Output [MW]"
    axes[0,1].stackplot(df["Date (CEST)"], 
                df[y1],
                df[y2],
                df[y3],
                df[y4],
                df[y5],
                labels=labels,
                colors=color_map)
    axes[0,1].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[0,1].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[0,1].set_xlim([0,23])
    axes[0,1].set_ylim([0,None])
    axes[0,1].set_title("DH Supply by fuel")
    axes[0,1].set_xlabel("Time [h]")
    axes[0,1].set_ylabel("DH Supply [MW]")
    return axes

def plot_electricity_production_by_fuel(df, axes):
    y1 = "Waste_CHP_Electricity_Output_A1[Dim 1][MW]"
    y2 = "Wood_CHP_Electricity_Output_A1[Dim 1][MW]"
    y3 = "Pellet_CHP_Electricity_Output_A2[Dim 1][MW]"

    width = 0.5
    axes[1,0].bar(df["Date (CEST)"], df[y1], width, label=labels[0], color=color_map[0])
    axes[1,0].bar(df["Date (CEST)"], df[y2], width, bottom=df[y1], label=labels[1], color=color_map[1])
    axes[1,0].bar(df["Date (CEST)"], df[y3], width, bottom=df[y1]+df[y2], label=labels[2], color=color_map[2])
    axes[1,0].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[1,0].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[1,0].set_xlim([-0.5,23.5])
    axes[1,0].set_ylim([0,(df[y1]+df[y2]+df[y3]).max()*1.1])
    axes[1,0].set_title("Electricity production by fuel")
    axes[1,0].set_xlabel("Time [h]")
    axes[1,0].set_ylabel("Electricity supply [MW]")
    return axes

def plot_fuel_cost(df, axes, electricity_price):
    electricity_price_label = "Retail Price " + electricity_price
    y1 = "Waste_Fuel_Input_A1[Dim 1][MW]"
    y2 = "Wood_Fuel_Input_A1[Dim 1][MW]"
    y3 = "Pellet_Fuel_Input_A2[Dim 1][MW]"
    y4 = "HP Electricity Consumption [MW]"
    y5 = "Bio Oil Fuel Input [MW]"
    axes[1,1].stackplot(df["Date (CEST)"], 
                df[y1].multiply(df["Waste Price"]),
                df[y2].multiply(df["Wood Price"]),
                df[y3].multiply(df["Bio Pellet Price"]),
                df[y4].multiply(df[electricity_price_label]),
                df[y5].multiply(df["Bio Oil Price"]),
                labels=labels,
                colors=color_map)
    axes[1,1].xaxis.set_major_locator(ticker.MultipleLocator(2))
    axes[1,1].xaxis.set_major_formatter(ticker.ScalarFormatter())
    axes[1,1].set_xlim([0,23])
    axes[1,1].set_ylim([0,None])
    axes[1,1].set_title("Fuel cost")
    axes[1,1].set_xlabel("Time [h]")
    axes[1,1].set_ylabel("Costs [SEK]")
    return axes

def create_subplots(df, electricity_price, plots_folder, save, show):
    fig, axes = plt.subplots(2, 2)
    # plt.rc('legend', fontsize="x-small")
    axes = plot_fuel_input_to_boiler(df, axes)
    axes = plot_dh_by_fuel(df, axes)
    axes = plot_electricity_production_by_fuel(df, axes)
    axes = plot_fuel_cost(df,axes,electricity_price)

    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines[0:5], labels[0:5], ncol=5, loc='center')
    plt.tight_layout()
    if save:
        fig.set_size_inches((11,7), forward=False)
        fig.savefig(os.path.join(plots_folder,f"results_{df[df.columns[0]].iloc[0][0:10]}.png"), dpi=500)
    if show:
        plt.show()

def plot_cost_revenue(df, electricity_price, plots_folder, save, show):
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
    revenues = sorted(list(zip([waste_revenue, wood_revenue, pellet_revenue, dh_revenue],range(4))),reverse=True)
    for revenue, i in revenues:
        ax.bar("Revenue", revenue, width=width, bottom=bottom, label=labels[5] if i == 3 else "", color=color_map[5] if i ==3 else color_map[i])
        bottom += revenue

    # ax.set_xlabel("Time [%]")
    ax.set_ylabel("Money [SEK]")
    ax.legend(loc='upper left')
    if save:
        plt.savefig(os.path.join(plots_folder,f"costs_{df[df.columns[0]].iloc[0][0:10]}.png"), dpi=300)
    if show:
        plt.show()

def plot_prices(df, electricity_price, plots_folder, save, show):
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
    if show:
        plt.show()

def plot_chp_use(df, plots_folder, save, show):
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
    if show:
        plt.show()

def plot_chp_use_bar(df, plots_folder, save, show):
    fig, ax = plt.subplots()
    width = 0.8
    ax.bar("Waste", df["Waste_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, label="Turbine", color=color_map[0])
    ax.bar("Waste", df["Waste_BP_Load_A1[Dim 1][MW]"].sum(), bottom=df["Waste_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, label="BP", color=color_map[1])
    ax.bar("Wood", df["Wood_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, color=color_map[0])
    ax.bar("Wood", df["Wood_BP_Load_A1[Dim 1][MW]"].sum(), bottom=df["Wood_Turbine_Load_A1[Dim 1][MW]"].sum(), width=width, color=color_map[1])
    ax.bar("Bio Pellet", df["Pellet_Turbine_Load_A2[Dim 1][MW]"].sum(), width=width, color=color_map[0])
    ax.bar("Bio Pellet", df["Pellet_BP_Load_A2[Dim 1][MW]"].sum(), bottom=df["Pellet_Turbine_Load_A2[Dim 1][MW]"].sum(), width=width, color=color_map[1])
    ax.legend(loc='best')
    ax.set_ylabel("Load [MW]")
    if save:
        plt.savefig(os.path.join(plots_folder,"chp_use_bar.png"), dpi=300)
    if show:
        plt.show()

def plot(df, electricity_price, save, show):
    plots_folder = "plots_" + electricity_price
    if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)
    # Plot load duration curve
    plot_load_duration_stackplot(df, plots_folder, save, show)
    plot_chp_use(df, plots_folder, save, show)
    plot_chp_use_bar(df, plots_folder, save, show)

    # Plot special days
    day_start_ids = [1392, 4727, 7968, 2255]
    # for day_id in [59, 198, 333, 95]: # max load, min load, max elec. price, min elec. price
    for day_start_id in day_start_ids:
        # df_day = df.iloc[(day_id-1)*24:day_id*24]
        df_day = df.iloc[day_start_id:day_start_id+24] # some weird things going on
        # Create a plot of subplots
        create_subplots(df_day, electricity_price, plots_folder, save, show)
        plot_cost_revenue(df_day, electricity_price, plots_folder, save, show)
        plot_prices(df_day, electricity_price, plots_folder, save, show)