from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from MoneyModel import MoneyModel

def agent_potrayal(agent):
  potrayal = {
    "Shape":  "circle",
    "Filled": "true",
    "r": agent.wealth + 0.5
  }
  if agent.wealth > 2:
    potrayal["Color"] = "red"
    potrayal["Layer"] = 0
  elif agent.wealth > 1:
    potrayal["Color"] = "orange"
    potrayal["Layer"] = 2
  elif agent.wealth > 0:
    potrayal["Color"] = "yellow"
    potrayal["Layer"] = 3
  else:
    potrayal["Color"] = "lightgrey"
    potrayal["Layer"] = 4
  return potrayal

grid = CanvasGrid(
  agent_potrayal,
  30,
  30,
  800,
  800
)

chart = ChartModule([{
  "Label": "Gini",
  "Color": "Black"}],
  data_collector_name = "datacollector")

server = ModularServer(
  MoneyModel,
  [grid, chart],
  "Money Model",
  {"N": 50, "width": 30, "height": 30}
  )
server.port = 8521
server.launch()