import extend_result_csv as extend
import plot_results as plot

if __name__ == "__main__":

    save_merged_results = False
    show_plots = False
    save_plots = True

    electricity_price = "0"   # 0: normal price, P25: higher price, M25: lower price
    if electricity_price == "0":
        result_file = "Scenario_Step1_consolidated.csv"
    elif electricity_price == "P25":
        result_file = "Scenario_Step2_P25_consolidated.csv"
    elif electricity_price == "M25":
        result_file = "Scenario_Step2_M25_consolidated.csv"
    else:
        
    df = extend.extend(result_file, save=save_merged_results)    
    plot.plot(df, electricity_price, show=show_plots, save=save_plots)
