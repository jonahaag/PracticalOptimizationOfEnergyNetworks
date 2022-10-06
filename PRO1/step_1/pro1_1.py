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
vmax = 1.05
vmin = .95
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
        pp.runpp(net)
        print(f"S1 {switch_position[0]}, S2 {switch_position[1]}, S3 {switch_position[2]}, Max voltage {net.res_bus.vm_pu.max()}, Min voltage {net.res_bus.vm_pu.min()}, Max line loading {net.res_line.loading_percent.max()}")
        n_critical_lines = 0
        n_overloaded_lines = 0
        n_critical_buses = 0
        n_very_critical_buses = 0
        for line in net.res_line.loading_percent:
            if line > 95.0:
                n_critical_lines += 1
            if line > 100.0:
                n_overloaded_lines += 1
        for bus in net.res_bus.vm_pu:
            if bus < 0.95:
                n_critical_buses += 1
            if bus < 0.9:
                n_very_critical_buses += 1
        print(f"{n_critical_lines} lines over 95% loading, {n_overloaded_lines} lines over 100% loading")
        print(f"{n_critical_buses} buses under 0.95 voltage, {n_very_critical_buses} buses under 0.90 voltage")
        # if net.res_bus.vm_pu.max() > vmax or net.res_bus.vm_pu.min() < vmin or net.res_line.loading_percent.max() > max_ll:
        #     critical.append([l,switch_position])
        # lines over 95% / 100% ll, buses under 0.95 / 0.9 pu
        # ax = pplt.simple_plot(net, show_plot=False)
        # clc = pplt.create_line_collection(net, critical, color="r", linewidth=3., use_bus_geodata=True)
        # pplt.draw_collections([clc], ax=ax)
        pplt.plotly.pf_res_plotly(net)
        plt.show()
        input()
        # critical = list()
    net.line.loc[l, "in_service"] = True
