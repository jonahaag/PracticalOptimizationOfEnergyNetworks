import py.extend_result_csv as extend
import py.plot_results as plot
import os

if __name__ == "__main__":

    save_merged_results = False
    show_plots = False
    save_plots = True

    electricity_price = "M25"   # 0: normal price, P25: higher price, M25: lower price
    if electricity_price == "0":
        result_file = os.path.join("bofit_results","Scenario_Step1_consolidated.csv")
    elif electricity_price == "P25":
        result_file = os.path.join("bofit_results","Scenario_Step2_P25_consolidated.csv")
    elif electricity_price == "M25":
        result_file = os.path.join("bofit_results","Scenario_Step2_M25_consolidated.csv")
        
    df = extend.extend(result_file, save_merged_results)    
    plot.plot(df, electricity_price, save_plots, show_plots)
