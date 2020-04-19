from datetime import datetime


class SnowFlake:
    def __init__(self):
        self.__dc_bit = 5
        self.__work_bits = 5
        self.__seq_bits = 12

        self.epoch = datetime.now()
        self.last = None


    def next_Id(self):
        pass