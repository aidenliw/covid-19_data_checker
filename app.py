"""
Covid-19 Data Checker

The application is a console app, it will provide a platform for users to check
the real-time Covid-19 world data and the provincial data in Canada.
The data includes Covid-19 infection, fatality, and recovery cases.
Vaccination data will be provided for the Canada’s provincial data.

The target audience of the software are the people who care about the covid-19
trend and situation. For someone who will go on a business trip, it will be
useful to be prepared in advance to understand the covid-19 situation in the destination country

Author: Aiden WangYang Li
"""

from controller import *

controller = Controller()
controller.run()
