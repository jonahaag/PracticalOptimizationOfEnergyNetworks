import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as pplt
import matplotlib.pyplot as plt
import numpy as np
import numba
import pandas as pd
import pulp as pl
import xlsxwriter as xl

net = nw.create_cigre_network_mv()

# limits
vmax = 1.1
vmin = .9
max_ll = 100.

lines = net.line.index
critical = list()

switch_positions = [[False, False, False],[True, False, False],[False, True, False],[False, False, True],[True, True, False],[True, False, True],[False, True, True],[True, True, True]]

for l in lines:
    net.line.loc[l, "in_service"] = False
    for switch_position in switch_positions:
        # S1 is 4, S2 is 1, S3 is 2
        net.switch.loc[4, "closed"] = switch_position[0]
        net.switch.loc[1, "closed"] = switch_position[1]
        net.switch.loc[2, "closed"] = switch_position[2] 
        print(f"S1 {switch_position[0]}, S2 {switch_position[1]}, S3 {switch_position[2]}")
        pp.runpp(net)
        if net.res_bus.vm_pu.max() > vmax or net.res_bus.vm_pu.min() < vmin or net.res_line.loading_percent.max() > max_ll:
            critical.append(l)
        ax = pplt.simple_plot(net, show_plot=False)
        clc = pplt.create_line_collection(net, critical, color="r", linewidth=3., use_bus_geodata=True)
        pplt.draw_collections([clc], ax=ax)
        plt.show()
    net.line.loc[l, "in_service"] = True

