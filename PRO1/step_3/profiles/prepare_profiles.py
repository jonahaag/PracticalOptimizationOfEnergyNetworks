import profile
import pandas as pd
import numpy as np
import os

profiles = pd.read_excel("PEV-Profiles-L2.xlsx", sheet_name="PEV-Profiles-L2.csv", skiprows=2, usecols=lambda x: 'Time' not in x)
profiles_as_np = profiles.to_numpy()
print(np.shape(profiles_as_np))

profiles_hourly = np.zeros((8760, 348))
for v in range(348):
    profiles_hourly[:,v] = np.array([max(profiles_as_np[i*6:i*6+6,v]) for i in range(np.shape(profiles_as_np)[0]//6)])
assert np.shape(profiles_hourly) == (8760, 348)
np.savetxt("hourly_profiles.txt", profiles_hourly)
df = pd.DataFrame(profiles_hourly)
df.to_excel("hourly_profiles.xlsx", index=False)

# pick max day
summed_daily_loads = np.array([np.sum(profiles_hourly[day*24:day*24+24,:], axis=None) for day in range(365)])
max_day_id = np.argmax(summed_daily_loads)
print(f"Day id {max_day_id}")
np.savetxt("peak_day.txt", profiles_hourly[max_day_id*24:max_day_id*24+24,:])
df = pd.DataFrame(profiles_hourly[max_day_id*24:max_day_id*24+24,:])
df.to_excel("peak_day.xlsx", index=False)