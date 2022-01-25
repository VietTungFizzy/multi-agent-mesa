from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement
import numpy as np

from MoneyModel import MoneyModel

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]

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
"""
server = ModularServer(
  MoneyModel,
  [grid, chart],
  "Money Model",
  {"N": 50, "width": 30, "height": 30}
  )
"""
histogram = HistogramModule(list(range(10)), 800, 800)
server = ModularServer(MoneyModel,
                       [grid, histogram, chart],
                       "Money Model",
                       {"N":100, "width":30, "height":30})
server.port = 8521
server.launch()