import pandas as pd
center_leading_step = None

center_description = pd.read_csv("../data/center_description.csv")
description = []
center_name = " 영감센터"
for i in range(0, 138):
    description.append(center_description.iloc[i,1])
print(description[0])
print(description[136]+center_name+description[137])

