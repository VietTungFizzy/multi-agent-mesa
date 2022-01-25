from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

def compute_gini(model):
  # DO MATH HERE
  agent_wealths = [agent.wealth for agent in model.schedule.agents]
  x = sorted(agent_wealths)
  N = model.num_agents
  B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
  return (1 + (1 / N) - 2 * B)

class MoneyAgent(Agent):
  """An agent with hopes and dreams"""
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.wealth = 1

  def step(self):
    self.move()
    if self.wealth > 0:
      self.give_money()

  def move(self):
    possible_steps = self.model.grid.get_neighborhood(
        self.pos,
        moore = False,
        include_center = True
      )

    new_position = self.random.choice(possible_steps)
    self.model.grid.move_agent(self, new_position)

  def give_money(self):
    cellmates = self.model.grid.get_cell_list_contents([self.pos])
    if len(cellmates) > 1:
      other = self.random.choice(cellmates)
      other.wealth += 1
      self.wealth -= 1

class MoneyModel(Model):
  """Where all agents gather"""
  def __init__(self, N, width, height):
    # A physic world to place our agent
    self.num_agents = N
    self.grid = MultiGrid(width, height, True)
    self.schedule = RandomActivation(self)
    self.running = True

    for i in range(self.num_agents):
      a = MoneyAgent(i, self)
      self.schedule.add(a)
      x = self.random.randrange(self.grid.width)
      y = self.random.randrange(self.grid.height)
      self.grid.place_agent(a, (x, y))

    # Some metric to measure our model
    self.datacollector = DataCollector(
      model_reporters = {"Gini": compute_gini},
      agent_reporters = {"wealth": "wealth"}
    )

  def step(self):
    """ Run a singl tick in this simulation """
    self.datacollector.collect(self)
    self.schedule.step()