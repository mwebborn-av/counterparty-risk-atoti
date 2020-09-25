import atoti as tt

config = tt.config.create_config(port="9009")
session = tt.create_session(config=config)
session.load_all_data()

nettingSets_store = session.read_csv("data/nettingSets_20200316.csv", keys=["NettingSetId"])

print(nettingSets_store.head())

forex_store = session.read_csv("data/fxrates_20200316.csv", keys=["CounterCcy"])

print(forex_store.head())

cube = session.create_cube(nettingSets_store, name="NS Test Cube", mode="manual")

h = cube.hierarchies
l = cube.levels
m = cube.measures


h["Netting Sets"] = [
    nettingSets_store["NettingSetId"],
    nettingSets_store["NettingName"],
]
h["Netting Sets"].dimension = "Netting Sets"

m["Collateral.SUM"] = nettingSets_store["Collateral"]
m["Collateral.SUM"]


print(session.url)

session.wait()
