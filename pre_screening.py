"""
    code by Wilfredo Colmenares
    Program that allows the user to enter a date and time, whereupon 
    a simple message will be displayed at that time. 
""" 
from math import inf
import time
import ordinal_numbers as on
import logging
import re
import datetime

#########################  we create a logger for errors
logging.basicConfig(filename=r"./error.log", level=logging.DEBUG)
logger = logging.getLogger()

#########################  some clases for exception handling
class ExceptionInDate(Exception):
    pass

class ExceptionInTime(Exception):
    pass



######################### the requested classes
class Time:

    def __init__(self, date_time, time_time):
        self.day = date_time[0:2]
        self.month = date_time[3:5]
        self.year = date_time[6:10]
        self.hour = time_time[0:2]
        self.minute = time_time[3:5]
        self.dt = datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour), \
                                    int(self.minute))  # the time of the object
        self.DAYS_PER_MONTH = {
                            1 : 31,
                            2 : 28,
                            3: 31,
                            4: 30,
                            5: 31,
                            6: 30,
                            7: 31,
                            8 : 31,
                            9 : 30,
                            10: 31,
                            11: 30,
                            12: 31
                        }

    def checkTime(self):
        """ we check here if the time is logic: meaning, we have month values between 1 and 12
            hour betwen 0 and 23 and minutes between 0 and 59        
        """

        # we departure with date
        if int(self.year) >= 1000:
            # we need to check for leap years
            leap = self.isLeapyear()
            if leap:
                self.DAYS_PER_MONTH[2] = 29  # we change for february if neccesary
            if int(self.month) > 0 and int(self.month) < 13:
                if int(self.day) > 0 and int(self.day) < self.DAYS_PER_MONTH[int(self.month)] + 1:

                    # we check with time
                    if int(self.hour) >= 0 and int(self.hour)<24:
                        if int(self.minute) >= 0 and int(self.minute) < 60:
                            return True
        return False

    def isLeapyear(self):
        """ here we check if the year is leap (633 days)"""
        if int(self.year) % 4 == 0 and int(self.year) % 100 != 0 or int(self.year) % 400 == 0 :
            return True
        return False

    def timeToSeconds(self):
        """
            a function to make our time seconds
        """
        et = datetime.datetime(1970,1,1)  # the epoch time
        delta = (self.dt-et)
        return delta.total_seconds()

    def waitingTime(self):
        """
            here we calculate how much time do we need to wait
        """
        delta = self.dt - datetime.datetime.now()
        return delta.total_seconds()

    def __str__(self) -> str:
        return self.day + "." + self.month + "." + self.year + " - " + \
               self.hour + ":" + self.minute


######################### some helping functions
def checkFormat(d, t):
    """we check the input from the user"""
    try:
        # we check if we are getting the right input against some regex
        if re.search(r"\d{2}\.\d{2}\.\d{4}$",d)  == None:
            raise ExceptionInDate(f"date with incorrect format {d}")
        elif re.search(r"\d{2}:\d{2}$",t) == None:
            raise ExceptionInTime(f"time with incorrect format {t}")

        # we need to check if the time input make sense
        t_obj = Time(d, t)
        make_sence = t_obj.checkTime()

        if not(make_sence):
            raise Exception(f"time did not pass validation")

    except ExceptionInDate as err:
        logger.error(err)
        print("enter the date in the proper format")
        raise
    except ExceptionInTime as err:
        logger.error(err)
        print("enter the time in the proper format")
        raise
    except Exception as err:
        logger.error(err)
        print("something is wrong with the input, check time and date")
        raise
    else:
        return True


def sortTimes(array_of_times):
    """
        here we get an array with the right order of the dates, from soonest to latest
    """
    array_of_s = []  # here we transform the dates to seconds
    for eachTime in array_of_times:
        array_of_s.append(eachTime.timeToSeconds())

    # we build the array with the order we want
    order = [i[0] for i in sorted(enumerate(array_of_s), key = lambda x:x[1])]

    return order


######################### the main program #########################
def main():

    # first we ask how many data wants the user to enter
    while True:
        try:
            how_many_data = int(input("please enter how many data do you want to input:"))    
        except ValueError as err:
            logger.error(err)
            print("enter an integer number")

        else:
            break
        
    list_of_date = []  # here we store as many dates as needed

    for i in range(how_many_data):

        # we ask the user for the date and time
        d = input("please enter a date [dd.mm.yyyy]: ")
        t = input("please enter a time[hh:mm]: ")
        print("\n")
        checkFormat(d,t)

        # we create the objects
        list_of_date.append(Time(d,t))

    print("thank you very much, we will notify them!\n...")

    sorted_dates = sortTimes(list_of_date)

    for i in range(how_many_data):  # we print the date previously input
        waiting_time = list_of_date[sorted_dates[i]].waitingTime()  # we calculate how much do we wait for each date
        if waiting_time <= 0:  # if the date is in the past
            print(f"the {on.num2ordinal(i+1)} date has already been reached: {list_of_date[sorted_dates[i]]}")
        else:
            time.sleep(waiting_time)
            print(f"the {on.num2ordinal(i+1)} date has been reached: {list_of_date[sorted_dates[i]]}")



if __name__ == "__main__":
    main()
    print("\ndone")