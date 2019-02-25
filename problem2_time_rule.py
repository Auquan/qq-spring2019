from backtester.timeRule.custom_time_rule import CustomTimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay


class Problem2TimeRule(CustomTimeRule):
    def __init__(self, startDate, endDate, startTime='9:00', endTime='16:00', holidays = [], weekmask = 'Mon Tue Wed Thu Fri', calendar = None, frequency='H', sample='1'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__sample = sample

        acceptable_freq = ['D', 'M', 'H', 'S', 'm']
        if frequency not in acceptable_freq:
            raise ValueError('Frequency Value Not acceptable. Specify D(day), M(minute), H(hour), S(second), m(month)')
        self.__frequency = frequency

        start = datetime.strptime(startTime, '%H:%M')
        self.startMinuteDelta = start.hour * 60 + start.minute
        end = datetime.strptime(endTime, '%H:%M')
        self.endMinuteDelta = end.hour * 60 + end.minute

        if(calendar != None):
            self.__bday = CustomBusinessDay(calendar = calendar)
            self.__bhour =  CustomBusinessHour(start = startTime, end = endTime, calendar = calendar)
        else:
            self.__bday = CustomBusinessDay(holidays = holidays, weekmask = weekmask)
            self.__bhour = CustomBusinessHour(start = startTime, end = endTime, holidays = holidays, weekmask = weekmask)

    def createMonthSeries(self):
        return pd.date_range(self.__startDate, self.__endDate , freq= self.__sample + 'M')

    def emitTimeToTrade(self):
        time_range = None
        if(self.__frequency == 'D'):
            time_range = self.createBusinessDaySeries()
        elif(self.__frequency == 'H'):
            time_range = self.createBusinessHourSeries()
        elif(self.__frequency == 'M'):
            time_range = self.createBusinessMinSeries()
        elif(self.__frequency == 'S'):
            time_range = self.createBusinessSecSeries()
        elif(self.__frequency == 'm'):
            time_range = self.createMonthSeries()

        for timestamp in time_range:
            yield timestamp
