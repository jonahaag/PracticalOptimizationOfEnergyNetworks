import py.extend_result_csv as extend
import py.plot_results as plot
import os
import time
if __name__ == "__main__":
    time_0 = time.time()
    save_merged_results = False
    show_plots = False
    save_plots = True

    electricity_price = "0"   # 0: normal price, P25: higher price, M25: lower price
    step = 2 # 1: step 1, 2: step 3.1 scenario 1, step 3: 3.1 scenario 2
    if electricity_price == "0":
        if step == 1:
            result_file = os.path.join("bofit_results","Scenario_Step1_consolidated.csv")
        elif step == 2:
            result_file = os.path.join("bofit_results","Scenario_Step3_Case1_consolidated.csv")
        elif step == 3:
            result_file = os.path.join("bofit_results","Scenario_Step3_Case2_consolidated.csv")
    elif electricity_price == "P25":
        result_file = os.path.join("bofit_results","Scenario_Step2_P25_consolidated.csv")
    elif electricity_price == "M25":
        result_file = os.path.join("bofit_results","Scenario_Step2_M25_consolidated.csv")
        
    df = extend.extend(result_file, save_merged_results)    
    plot.create_plots(df, electricity_price, save_plots, show_plots)
    print(time.time()-time_0)
