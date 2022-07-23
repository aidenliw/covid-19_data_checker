"""
The API retrieving function is using the Facade Pattern

Facade is a structural design pattern that provides a simplified
(but limited) interface to a complex system of classes, library or framework.

Reference: https://refactoring.guru/design-patterns/facade/python/example
"""

import requests


class CovidCanada:

    canada_provinces = {
        "AB": "Alberta",
        "BC": "British Columbia",
        "MB": "Manitoba",
        "NB": "New Brunswick",
        "NL": "Newfoundland and Labrador",
        "NT": "Northwest Territories",
        "NS": "Nova Scotia",
        "NU": "Nunavut",
        "ON": "Ontario",
        "PE": "Prince Edward Island",
        "QC": "Quebec",
        "SK": "Saskatchewan",
        "YT": "Yukon",
    }

    # makes the message to the API, returns Canada's summary data
    def get_canada_summary(self):
        result = requests.get("https://api.covid19tracker.ca/summary").json()
        return result

    # makes the message to the API, returns the province's summary data
    def get_province_summary(self, province_abb):
        result = requests.get("https://api.covid19tracker.ca/summary/split").json()
        province_holder = None
        for province in result["data"]:
            if province["province"] == province_abb.upper():
                province_holder = province
        return province_holder

    # the facade provides a simple interface for accessing COVID-19 data
    # Print out all the Covid-19 data collected from the canada summary
    def print_canada_summary(self):
        data = self.get_canada_summary()["data"][0]
        print("| Total Cases: \t\t\t" + str(data["total_cases"]) + "\n"
              + "| Death Cases: \t\t\t" + str(data["total_fatalities"]) + "\n"
              + "| Hospitalizations: \t" + str(data["total_hospitalizations"]) + "\n"
              + "| Criticals: \t\t\t" + str(data["total_criticals"]) + "\n"
              + "| Recoveries: \t\t\t" + str(data["total_recoveries"]) + "\n"
              + "| Vaccinated: \t\t\t" + str(data["total_vaccinated"]))
        return data

    # Print out all the Covid-19 data collected from the province summary
    def print_province_summary(self, province_abb):
        data = self.get_province_summary(province_abb)
        print("| Total Cases: \t\t\t" + "" + str(data["total_cases"]) + "\n"
              + "| Death Cases: \t\t\t" + str(data["total_fatalities"]) + "\n"
              + "| Hospitalizations: \t" + str(data["total_hospitalizations"]) + "\n"
              + "| Criticals: \t\t\t" + str(data["total_criticals"]) + "\n"
              + "| Recoveries: \t\t\t" + str(data["total_recoveries"]) + "\n"
              + "| Vaccinated: \t\t\t" + str(data["total_vaccinated"]))
        return data

    # makes the message to the API, returns the data for a province from the first recorded case
    def get_province_all_data(self, province_abb):
        result = requests.get("https://api.covid19tracker.ca/reports/province/" + province_abb).json()
        return result["data"]

    # makes the message to the API, returns the data for a province between the input date range
    def get_province_daterange_data(self, province_abb, start, end):
        result = requests.get("https://api.covid19tracker.ca/reports/province/" + province_abb +
                              "?after=" + start + "&before=" + end).json()
        return result["data"]


# create the covid object
covid = CovidCanada()

# Test
# print(covid.get_canada_summary())
# print(covid.get_province_summary("ON"))
# print(covid.get_province_all_data("ON"))
# print(covid.get_province_daterange_data("ON", "2022-07-01", "2022-07-10"))
