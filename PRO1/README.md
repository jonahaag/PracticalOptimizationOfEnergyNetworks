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