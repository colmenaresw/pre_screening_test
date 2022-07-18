"""
    code by Wilfredo Colmenares
    unit testing module for pre-screening code
"""
import unittest
import pre_screening

class testPreScreening(unittest.TestCase):
    
    def testPrint(self):
        """
            test if we are printing with the right format
        """
        t_obj = pre_screening.Time('01.01.1992', '12:30')
        self.assertEqual(t_obj.__str__(),'01.01.1992 - 12:30')

    def testLeapyear(self):
        """
            test if we are getting year leap when when we test, and the other way around
            for a non-leap year
        """
        t_obj = pre_screening.Time('29.02.2024', '00:00')
        self.assertTrue(t_obj.isLeapyear())
        t_obj2 = pre_screening.Time('28.02.2023', '00:00')
        self.assertFalse(t_obj2.isLeapyear())
        

    def testInput(self):
        """
            we test if we raise the exceptions when inputting the wrong dates and time
        """
        with self.assertRaises(pre_screening.ExceptionInDate):
            pre_screening.checkFormat('1.1.1992','13:00')
        with self.assertRaises(pre_screening.ExceptionInTime):
            pre_screening.checkFormat('01.01.1992','1:00pm')
        
    def testTime(self):
        """
            we test if inputing wrong dates or time (but good format) raise the exceptions
        """
        t_obj = pre_screening.Time('31.02.2023', '00:00')
        self.assertFalse(t_obj.checkTime())
        t_obj2 = pre_screening.Time('31.01.2023', '25:00')
        self.assertFalse(t_obj2.checkTime())

        
if __name__ == "__main__":
    unittest.main()