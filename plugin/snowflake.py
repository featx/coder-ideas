import time

from plugin import synchronized, IdGenerate


class SnowFlake(IdGenerate):
    def __init__(self, epoch="2020-04-04 10:00:00", data_center_id=1, worker_id=1):
        self.__data_center_bits = 4
        self.__worker_bits = 6
        self.__seq_bits = 12

        self.__max_data_center = -1 ^ (-1 << self.__data_center_bits)
        self.__max_worker = -1 ^ (-1 << self.__worker_bits)

        self.__worker_shifts = self.__seq_bits
        self.__data_center_shifts = self.__seq_bits + self.__worker_bits
        self.__timestamp_shifts = self.__seq_bits + self.__worker_bits + self.__data_center_bits

        self.__seq_mask = -1 ^ (-1 << self.__seq_bits)

        self._epoch = int(time.mktime(time.strptime(epoch, "%Y-%m-%d %H:%M:%S"))*1000)
        self._data_center_id = data_center_id
        self._worker_id = worker_id
        self._sequence = 0
        self._last_timestamp = -1

    def __tick_next(self, time_stamp=None):
        new_stamp = int(time.time() * 1000)
        if time_stamp is None:
            return new_stamp
        while new_stamp <= time_stamp:
            new_stamp = int(time.time() * 1000)
        return new_stamp

    @synchronized
    def next_id(self):
        current_stamp = self.__tick_next()
        if current_stamp < self._last_timestamp:
            raise Exception()
        if current_stamp == self._last_timestamp:
            self._sequence = self._sequence + 1 & self.__seq_mask
            if self._sequence == 0:
                current_stamp = self.__tick_next(self._last_timestamp)
        else:
            self._sequence = 0

        self._last_timestamp = current_stamp
        return ((current_stamp - self._epoch) << self.__timestamp_shifts) | \
               (self._data_center_id << self.__data_center_bits) | \
               (self._worker_id << self.__worker_bits) | self._sequence
