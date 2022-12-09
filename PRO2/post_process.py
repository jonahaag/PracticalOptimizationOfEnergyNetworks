import py.extend_result_csv as extend
import os
import time
if __name__ == "__main__":
    time_0 = time.time()
    save_merged_results = False
    show_plots = False
    save_plots = True

    electricity_price = "M25"   # 0: normal price, P25: higher price, M25: lower price
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
        
    print(time.time()-time_0)
