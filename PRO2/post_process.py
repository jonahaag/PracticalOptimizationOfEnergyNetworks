import py.extend_result_csv as extend
import os
import time

def calculate_yearly_cost_revenue(df,electricity_price):
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

    print("Production cost: ", waste_cost+wood_cost+pellet_cost+electricity_cost+oil_cost)
    print("Electricity revenue: ", electricity_revenue)
    print("DH revenue: ", dh_revenue)
    print("DH demand: ", df["Total Load"].sum())

if __name__ == "__main__":
    time_0 = time.time()
    save_merged_results = False
    show_plots = False
    save_plots = True

    electricity_price = "P25"   # 0: normal price, P25: higher price, M25: lower price
    step = 4 # 1: step 1, 2: step 2, step 3: 3.1 case1, step 4: 3.1 case 2
    if step == 1:
        import py.plot_results as plot
        result_file = os.path.join("bofit_results","Scenario_Step1_consolidated.csv")
        df = extend.extend(result_file, save_merged_results)    
        plot.create_plots(df, electricity_price="0", save=save_plots, show=show_plots)
    elif step == 2:
        import py.plot_results as plot
        if electricity_price == "P25":
            result_file = os.path.join("bofit_results","Scenario_Step2_P25_consolidated.csv")
            df = extend.extend(result_file, save_merged_results)    
            plot.create_plots(df, electricity_price, save_plots, show_plots)
        elif electricity_price == "M25":
            result_file = os.path.join("bofit_results","Scenario_Step2_M25_consolidated.csv")
            df = extend.extend(result_file, save_merged_results)    
            plot.create_plots(df, electricity_price, save_plots, show_plots)
    elif step == 3:
        import py.plot_results_step3_case1 as plot
        result_file = os.path.join("bofit_results","Scenario_Step3_Case1_consolidated.csv")
        df = extend.extend_step3_case1(result_file, save_merged_results)  
        plot.create_plots(df, electricity_price="0", save=save_plots, show=show_plots)
    elif step == 4:
        import py.plot_results_step3_case2 as plot
        result_file = os.path.join("bofit_results","Scenario_Step3_Case2_consolidated.csv")
        df = extend.extend_step3_case2(result_file, save_merged_results)   
        plot.create_plots(df, electricity_price="0", save=save_plots, show=show_plots)

    calculate_yearly_cost_revenue(df,electricity_price="0")
    print(time.time()-time_0)
