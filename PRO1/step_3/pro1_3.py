from json import loads
import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as pplt
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
import os

###############
# This code is mainly based on https://github.com/e2nIEE/pandapower/blob/develop/tutorials/time_series.ipynb
###############

def timeseries(file_dir, output_dir):
    # 1. create test net
    net = nw.create_cigre_network_mv()

    # 1.1 add CS and load for the EVs
    np.random.seed(200)
    cs_positions = np.random.choice(15, 5, replace=False)
    # Alternative: cs_positions = [1, 3, 7, 10, 13] simply giving the index of the buses

    # ev_profiles = pd.read_excel(os.path.join(file_dir, "PEV-Profiles-L2.xlsx"), sheet_name="PEV-Profiles-L2.csv", skiprows=2, nrows=2)
    # ev_profiles = pd.read_excel(os.path.join(file_dir, "profiles/ev_loads_one_day.xlsx"), skiprows=2)
    ev_profiles = np.loadtxt(os.path.join(file_dir, "profiles/peak_day.txt"))
    
    # each tuple is (ev_idx, cs_idx) where ev_idx is in range(1,348), cs_idx in range (1,5)
    # ev_allocation = [(2,3), (17, 5), (18,4), (30,2), (101,4), (170, 5)]
    # ev_idx = np.array([i[0] for i in ev_allocation])-1
    # allocation = np.array([i[1] for i in ev_allocation])

    # Alternative using random allocation:
    n_ev = 345
    ev_idx = np.random.choice(348, n_ev, replace=False)
    allocation = np.repeat(np.array(range(1,6)), n_ev//5)
    ev_allocation = [(e,c) for e,c in zip(ev_idx,allocation)]

    assert ev_idx.size == allocation.size

    net, loadshape_cs = add_cs_ev(net, cs_positions, ev_profiles, ev_idx, allocation)
    # Plot the updated network, including charging stations
    plot_network(net)

    # 2. create data source based on nominal loadshape
    n_timesteps = 24
    profiles, ds = create_data_source(net, loadshape_cs)

    # 3. create controllers
    create_controllers(net, ds)

    # time steps to be calculated. Could also be a list with non-consecutive time steps
    time_steps = range(0, n_timesteps)

    # 4. the output writer with the desired results to be stored to files.
    ow = create_output_writer(net, time_steps, output_dir=output_dir)

    # 5. the main time series function
    run_timeseries(net, time_steps)

    # 6. Save additional results: plots, CS positions, n_EVs, EV allocation
    plot_results(net, time_steps)
    save_configuration(cs_positions, ev_allocation, ev_idx, allocation)

def add_cs_ev(net, cs_positions, ev_profiles, ev_idx, allocation):
    # loadshape_ev is a 24 x N_evs numpy array containing the load for all electric vehicles to be added
    loadshape_ev = np.zeros((24,len(ev_idx)))
    loadshape_cs = np.zeros((24,5))
    for j, ev in enumerate(ev_idx):
        loadshape_ev[:, j] = ev_profiles[:, ev]/1e6
        loadshape_cs[:,allocation[j]-1] += loadshape_ev[:,j]
    # Add a low voltage bus, transformer and connected load for the 5 CS add the high voltage buses specified in cs_positions
    for i, cs in enumerate(cs_positions):
        geodata = (net.bus_geodata.iloc[cs]["x"]-1.0, net.bus_geodata.iloc[cs]["y"]-1.0)
        name = "Bus CS "+str(i+1)
        name_2 = "CS "+str(i+1)
        pp.create_bus(net, name=name, vn_kv=0.4, type="b", geodata=(geodata))
        pp.create_transformer(net, hv_bus=cs, lv_bus=pp.get_element_index(net, "bus", name), name=name_2, std_type="0.63 MVA 20/0.4 kV") # 0.4 MVA 20/0.4 kV, 0.63 MVA 20/0.4 kV
        # Create a load at low voltage bus, load = number of connected evs * their max_load (this will be overwritten during the simulation)
        pp.create_load(net, bus=net.bus.iloc[-1].name, p_mw=6.6*np.size(np.where(allocation==i+1)), name="Load CS"+str(i+1))
    return net, loadshape_cs

def plot_network(net, critical=[]):
    # Plot the network
    ax = pplt.simple_plot(net, show_plot=False)
    clc = pplt.create_line_collection(net, critical, color="r", linewidth=3., use_bus_geodata=True)
    pplt.draw_collections([clc], ax=ax)
    plt.savefig("results/network.png")
    # plt.show()

def contigency_analysis(net, switch_positions, vmax, vmin, max_ll):
    lines = net.line.index
    critical = list()
    for l in lines:
        net.line.loc[l, "in_service"] = False
        # S1 is 4, S2 is 1, S3 is 2
        net.switch.loc[4, "closed"] = switch_positions.loc[l, "S1"]
        net.switch.loc[1, "closed"] = switch_positions.loc[l, "S2"]
        net.switch.loc[2, "closed"] = switch_positions.loc[l, "S3"]
        pp.runpp(net)
        print(f"Line {l}, max voltage {net.res_bus.vm_pu.max()}, min voltage {net.res_bus.vm_pu.min()}, max line loading {net.res_line.loading_percent.max()}")
        if net.res_bus.vm_pu.max() > vmax or net.res_bus.vm_pu.min() < vmin or net.res_line.loading_percent.max() > max_ll:
            critical.append(l)
        net.line.loc[l, "in_service"] = True
    net.switch.loc[4, "closed"] = False
    net.switch.loc[1, "closed"] = False
    net.switch.loc[2, "closed"] = False
    return critical

def create_data_source(net, loadshape_cs):
    # Reshape the reactive and active power of the existing loads to row vectors
    # 18 predefined loads
    p_mw_existing = np.array(net.load.p_mw)[0:18].reshape((1,18))
    q_mvar_existing = np.array(net.load.q_mvar)[0:18].reshape((1,18))
    # Loadshape as given in the project description as column vector
    loadshape_nominal = np.array([0.28285, 0.272295, 0.2613828, 0.261328, 0.254316, 0.259789, 0.272966, 0.30915, 0.433979, 0.542955, 0.717333, 0.851829, 0.864118, 0.854116, 0.853815, 0.852508, 0.723452, 0.490362, 0.428271, 0.361402, 0.336596, 0.328176, 0.307331, 0.297966]).reshape((24,1))
    # Multiply, result is a 24 x 18 matrix with a column for each preexisting load and a row for each hour of the day 
    loadshape_p_mw_existing = np.multiply(loadshape_nominal, p_mw_existing)
    loadshape_q_mvar_existing = np.multiply(loadshape_nominal, q_mvar_existing)
    # Merge the two arrays (preexisting loads + new EV loads), results is a 24 x 23 matrix 
    loadshape_p_mw = np.concatenate((loadshape_p_mw_existing, loadshape_cs), axis=1)
    loadshape_q_mvar = np.concatenate((loadshape_q_mvar_existing, np.zeros_like(loadshape_cs)), axis=1)
    # e.g. to access loadshape of load 0 use loadshape_p_mw[:,0]
    assert np.shape(loadshape_p_mw) == (24,23)
    assert np.shape(loadshape_q_mvar) == (24,23)

    # Convert to pandas dataframe out of pure convenience
    profiles = pd.DataFrame()
    for id, l in net.load.iterrows():
        profiles[l["name"]+"_p_mw"] = loadshape_p_mw[:,id]
        profiles[l["name"]+"_q_mvar"] = loadshape_q_mvar[:,id]
    ds = DFData(profiles)

    return profiles, ds

def create_controllers(net, ds):
    for i, l in net.load.iterrows():
        ConstControl(net, element='load', variable='p_mw', element_index=[i],
                 data_source=ds, profile_name=[l["name"]+"_p_mw"])
        ConstControl(net, element='load', variable='q_mvar', element_index=[i],
                 data_source=ds, profile_name=[l["name"]+"_q_mvar"])

def create_output_writer(net, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    # these variables are saved
    # ow.log_variable{'subfolder', 'variable'} where variable will also be the name of the resulting excel file
    ow.log_variable('res_load', 'p_mw')
    ow.log_variable('res_bus', 'vm_pu')
    ow.log_variable('res_line', 'loading_percent')
    ow.log_variable('res_line', 'i_ka')
    ow.log_variable('res_trafo', 'loading_percent')
    return ow

def plot_results(net, time_steps):
    loads = np.array(pd.read_excel('results/res_load/p_mw.xlsx'))[:,1:]
    buses = np.array(pd.read_excel('results/res_bus/vm_pu.xlsx'))[:,1:]
    lines = np.array(pd.read_excel('results/res_line/loading_percent.xlsx'))[:,1:]
    trafos = np.array(pd.read_excel('results/res_trafo/loading_percent.xlsx'))[:,1:]
    time_steps = np.array(time_steps).reshape(24,1)

    fig, axs = plt.subplots(2, 2, figsize=(16,9))

    plt.subplot(2,2,1)
    plt.title("Loads")
    plt.xlim((0,23))
    plt.ylim((0,15))
    plt.plot(np.repeat(time_steps, loads.shape[1], axis=1), loads)
    plt.legend([f'Load {i}' for i in range(loads.shape[1])], ncol=2, fontsize='x-small', loc="upper left")
    plt.grid(True, alpha=0.5)
    plt.xlabel("Time [hour]")
    plt.ylabel("Active power [MW]")

    plt.subplot(2,2,2)
    plt.title("Buses")
    plt.plot(np.repeat(time_steps, buses.shape[1], axis=1), buses)
    plt.legend([f'Bus {i}' for i in range(buses.shape[1])], ncol=3, fontsize='x-small', loc="upper left")
    plt.plot(time_steps,1.1*np.ones(24), color='k')
    plt.plot(time_steps,0.9*np.ones(24), color='k')
    plt.grid(True, alpha=0.5)
    plt.xlim((0,23))
    plt.ylim((0.8,1.2))
    plt.xlabel("Time [hour]")
    plt.ylabel("Voltage [pu]")

    plt.subplot(2,2,3)
    plt.title("Lines")
    plt.plot(np.repeat(time_steps, lines.shape[1], axis=1), lines)
    plt.legend([f'Line {i}' for i in range(lines.shape[1])], ncol=2, fontsize='x-small', loc="upper left")
    plt.plot(time_steps,100*np.ones(24), color='k')
    plt.grid(True, alpha=0.5)
    plt.xlim((0,23))
    plt.ylim((0,110))
    plt.xlabel("Time [hour]")
    plt.ylabel("Loading [%]")

    plt.subplot(2,2,4)
    plt.title("Trafos")
    plt.plot(np.repeat(time_steps, trafos.shape[1], axis=1), trafos)
    plt.legend([f'Trafo {i}' for i in range(trafos.shape[1])], ncol=2, fontsize='x-small', loc="upper left")
    plt.plot(time_steps,100*np.ones(24), color='k')
    plt.grid(True, alpha=0.5)
    plt.xlim((0,23))
    plt.ylim((0,110))
    plt.xlabel("Time [hour]")
    plt.ylabel("Loading [%]")

    plt.savefig("results/results.png", dpi=300)
    plt.show()

def save_configuration(cs_positions, ev_allocation, ev_idx, allocation):
    with open("results/cs_ev_configuration.txt", 'w') as f:
        f.write(f"There were {ev_idx.size} EVs connected to the network.\n\n")
        for i in range(5):
            f.write(f"CS{i+1} was connected to high voltage bus {cs_positions[i]}.\n{np.count_nonzero(allocation==i+1)} EVs were connected to CS {i+1}.\n\n")
        f.write("\nDetailed allocation:\n")
        # TODO sort this after CS
        for a in ev_allocation:
            f.write(f"EV {a[0]} connected to CS {a[1]}\n")
        

if __name__ == "__main__":
    # Set directory to store results
    file_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(file_dir, "results")
    print("Results can be found in your local temp folder: {}".format(output_dir))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    timeseries(file_dir, output_dir)