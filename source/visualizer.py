import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("/home/hadoop_user/lab/output.tsv", delimiter="\t", header=None, names=["key", "profit"])

df[["date", "country", "category"]] = df["key"].str.split('", "', expand=True)
df = df.drop(columns=["key"])
df["date"] = pd.to_datetime(df["date"].str.lstrip('["'), format="%Y-%m-%dT%H")
df["category"] = df["category"].str.rstrip('"]')
df["max_category_profit"] = df.groupby("category")["profit"].transform("max") 

vs = df[df["max_category_profit"] == df["max_category_profit"].max()]

fig, ax = plt.subplots(figsize=(8,6))
for country, values in vs.groupby('country'):
    ax.plot(values["date"], values["profit"], label=country)


plt.title(f'Profit of {vs.iloc[0]["category"]}')
plt.xlabel("Day, hour")
plt.ylabel("Profit, rub.")

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)

plt.savefig("/home/hadoop_user/lab/graph_profit.png")