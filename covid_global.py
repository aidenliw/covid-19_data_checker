"""
The API retrieving function is using the Facade Pattern

Facade is a structural design pattern that provides a simplified
(but limited) interface to a complex system of classes, library or framework.

Reference: https://refactoring.guru/design-patterns/facade/python/example
"""

import requests


class CovidGlobal:

    # makes the message to the API, returns the global summary data
    def get_global_summary(self):
        result = requests.get("https://api.covid19api.com/summary").json()
        return result

    # makes the message to the API, returns the country's summary data
    def get_country_summary(self, country_name):
        result = requests.get("https://api.covid19api.com/summary").json()
        country_holder = None
        for country in result["Countries"]:
            if country["Country"] == country_name:
                country_holder = country
        return country_holder

    # the facade provides a simple interface for accessing COVID-19 data
    # Print out all the Covid-19 data collected from the global summary
    def print_global_summary(self):
        data = self.get_global_summary()["Global"]
        print("| Total Confirmed: \t" + str(data["NewConfirmed"]) + "\n"
              + "| Total Deaths: \t" + str(data["TotalConfirmed"]) + "\n"
              + "| Total Recovered: \t" + str(data["NewDeaths"]) + "\n"
              + "| New Confirmed: \t" + str(data["TotalDeaths"]) + "\n"
              + "| New Deaths: \t\t" + str(data["NewRecovered"]) + "\n"
              + "| New Recovered: \t" + str(data["TotalRecovered"]))
        return data

    # Print out all the Covid-19 data collected from the country summary
    def print_country_summary(self, country_name):
        data = self.get_country_summary(country_name)
        print("| Total Confirmed: \t" + str(data["TotalConfirmed"]) + "\n"
              + "| Total Deaths: \t" + str(data["TotalDeaths"]) + "\n"
              + "| Total Recovered: \t" + str(data["TotalRecovered"]) + "\n"
              + "| New Confirmed: \t" + str(data["NewConfirmed"]) + "\n"
              + "| New Deaths: \t\t" + str(data["NewDeaths"]) + "\n"
              + "| New Recovered: \t" + str(data["NewRecovered"]))
        return data

    # makes the message to the API, returns the data for a country from the first recorded case
    def get_country_all_data(self, country_name):
        result = requests.get("https://api.covid19api.com/dayone/country/" + country_name).json()
        return result

    # makes the message to the API, returns the data for a country between the input date range
    def get_country_daterange_data(self, country_name, start, end):
        result = requests.get("https://api.covid19api.com/country/" + country_name +
                              "?from=" + start + "T00:00:00Z&to=" + end + "T00:00:00Z").json()
        return result


# create the covid object
covid = CovidGlobal()

# Test
# use the simplified interface to retrive data for different countries
# print(covid.total_confirmed("Canada"))
# print(covid.total_deaths("United States of America"))
# print(covid.new_deaths("Canada"))

# print(covid.get_result("Canada"))
# print(covid.get_result("United States of America"))

# print(covid.get_global_summary())
# print(covid.get_country_summary("Canada"))
# print(covid.get_country_all_data("Canada"))
# print(covid.get_country_daterange_data("Canada", "2022-07-01", "2022-07-10"))
