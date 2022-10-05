import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as pplt
import matplotlib.pyplot as plt
import numpy as np
import numba
import pandas as pd
import pulp as pl
import xlsxwriter as xl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
import os
import tempfile


def timeseries_example(output_dir):
    # 1. create test net
    net = nw.create_cigre_network_mv()

    # 1.1 add CS, perform N-1 analysis and plot the network
    np.random.seed(200)
    cs_positions = np.random.choice(15, 5, replace=False)
    net = add_cs(net, cs_positions)
    switch_positions = pd.read_excel("contigency_switch_positions.xlsx")
    # critical = contigency_analysis(net, switch_positions, vmax=1.05, vmin=0.95, max_ll=100.)
    # plot_network(net, critical)
    critical_loose = contigency_analysis(net, switch_positions, vmax=1.1, vmin=0.9, max_ll=100.)
    plot_network(net, critical_loose)
    # TODO add iterating over random choices and picking the "best" positions

    # 2. create (random) data source
    n_timesteps = 24
    profiles, ds = create_data_source(net, n_timesteps)

    # 3. create controllers (to control P values of the load and the sgen)
    create_controllers(net, ds)

    # time steps to be calculated. Could also be a list with non-consecutive time steps
    time_steps = range(0, n_timesteps)

    # 4. the output writer with the desired results to be stored to files.
    ow = create_output_writer(net, time_steps, output_dir=output_dir)

    # 5. the main time series function
    run_timeseries(net, time_steps)

def add_cs(net, cs_positions):
    i = 1
    for cs in cs_positions:
        geodata = (net.bus_geodata.iloc[cs]["x"]-1.0, net.bus_geodata.iloc[cs]["y"]-1.0)
        name = "Bus CS "+str(i)
        name_2 = "CS "+str(i)
        pp.create_bus(net, name=name, vn_kv=0.4, type="b", geodata=(geodata))
        pp.create_transformer(net, hv_bus=cs, lv_bus=pp.get_element_index(net, "bus", name), name=name_2, std_type="0.25 MVA 20/0.4 kV") # 0.4 MVA 20/0.4 kV, 0.63 MVA 20/0.4 kV
        i += 1
    return net

def plot_network(net, critical=[]):
    # Plot the network
    ax = pplt.simple_plot(net, show_plot=False)
    clc = pplt.create_line_collection(net, critical, color="r", linewidth=3., use_bus_geodata=True)
    pplt.draw_collections([clc], ax=ax)
    plt.show()

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

def create_data_source(net, n_timesteps=24):

    p_mw = np.array(net.load.p_mw).reshape((1,18))
    q_mvar = np.array(net.load.q_mvar).reshape((1,18))
    loadshape_nominal = np.array([0.28285, 0.272295, 0.2613828, 0.261328, 0.254316, 0.259789, 0.272966, 0.30915, 0.433979, 0.542955, 0.717333, 0.851829, 0.864118, 0.854116, 0.853815, 0.852508, 0.723452, 0.490362, 0.428271, 0.361402, 0.336596, 0.328176, 0.307331, 0.297966]).reshape((24,1))
    loadshape_p_mw = np.multiply(loadshape_nominal, p_mw)
    loadshape_q_mvar = np.multiply(loadshape_nominal, q_mvar)
    # e.g. to access loadshape of load 0 use loadshape_p_mw[:,0]

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
                 data_source=ds, profile_name=[l["name"]+"_p_mw"])

def create_output_writer(net, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    # these variables are saved to the harddisk after / during the time series loop
    ow.log_variable('res_load', 'p_mw')
    ow.log_variable('res_bus', 'vm_pu')
    ow.log_variable('res_line', 'loading_percent')
    ow.log_variable('res_line', 'i_ka')
    return ow

output_dir = os.path.join(os.getcwd(), "time_series_example")
print("Results can be found in your local temp folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_example(output_dir)