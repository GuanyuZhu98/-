from main.dialgage_reader import testPotCirc_oscillation
import datetime

class easytest_module():
    def __init__(self):
        self.mytest = testPotCirc_oscillation()
        self.running = False
        self.data = []
        self.time_data = []
        self.mytest.send_data("01 06 08 00 AB 56 74 A4")

    def runTest(self):
        self.mytest.send_data("01 03 00 00 00 02 C4 0B")
        return self.mytest.receive_data()
    
    def endTest(self):
        self.mytest.ser.close()