"""
The Plot displaying function is using the strategy pattern

Strategy is a behavioral design pattern that turns a set of behaviors into objects
and makes them interchangeable inside original context object.

Reference: https://refactoring.guru/design-patterns/strategy/python/example
"""

import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


# The Context defines the interface of interest to clients.
class Context:
    def __init__(self, strategy):
        self.prepare = strategy.prepare

    def display_plot(self, data, title):
        self.prepare(data, title)
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        plt.xlabel('Dates')
        plt.legend()
        plt.show()


# The Strategy interface declares operations common to all supported versions of some algorithm
class PlotStrategy(ABC):

    @abstractmethod
    def prepare(self):
        pass


# Concrete Strategies implement the algorithm while following the base Strategy
# interface. The interface makes them interchangeable in the Context.

# Global Plot Strategy to display data with global format
class GlobalPlotStrategy(PlotStrategy):

    def prepare(self, result, title):
        confirmed = []
        deaths = []
        recovered = []
        dates = []
        for data in result:
            confirmed.append(data["Confirmed"])
            deaths.append(data["Deaths"])
            recovered.append(data["Recovered"])
            dates.append(data["Date"][:10])

        plt.plot(dates, confirmed, label="Confirmed")
        plt.plot(dates, deaths, label="Deaths")
        plt.plot(dates, recovered, label="Recovered")
        plt.title(title)


# Canada Plot Strategy to display data with Canada format
class CanadaPlotStrategy(PlotStrategy):

    # draw the plot by using the matplotlib with the given data
    def prepare(self, result, title):
        confirmed = []
        deaths = []
        hospitalizations = []
        recovered = []
        vaccinated = []
        dates = []
        for data in result:
            confirmed.append(data["total_cases"])
            deaths.append(data["total_fatalities"])
            hospitalizations.append(data["total_hospitalizations"])
            recovered.append(data["total_recoveries"])
            vaccinated.append(data["total_vaccinated"])
            dates.append(data["date"][:10])

        plt.plot(dates, confirmed, label="Confirmed")
        plt.plot(dates, deaths, label="Deaths")
        plt.plot(dates, recovered, label="Recovered")
        plt.plot(dates, hospitalizations, label="Hospitalised")
        plt.plot(dates, vaccinated, label="Vaccinated")
        plt.title(title)

