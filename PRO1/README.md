## TODO PRO1

Step 1:
- Merge scenarios1.xslx (max/min bus levels and line loadings) and scenarios2.xlsx (count of (potentially) critical buses and lines) to identify most critical cases

Step 2:
- Compare state of the network at peak load with steady state in step 1. Should be very similar, maybe slightly better since max_nominal_load = 0.8... < 1

Step 3:

- Add EV as load to network (if multiple EVs are connected to a single CS sum their power and add one larger load only)
- Check state of the network and iterate CS positions and EV allocation
- Consider transformers
- Perform N-1 again, focusing on critical cases and switch configuration from step 1
- Adjust excel output to reflect trafos
- Add some plotting after running the time series:
    - Line loadings for all lines with peak load >95%
    - Trafo loading for all trafos with peak load > 95%, maybe allow for a short overload (1-2 hourse at 150% for example)
    - Buses with minimum voltage level at peak load < 0.95 or < 0.9