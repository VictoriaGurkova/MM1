from queue import Queue
import random
import time
from Demand import Demand
from Device import Device


class MM1:
    def __init__(self, mu, lambd):
        self.mu = mu
        self.lambd = lambd

        self.average_time = 0
        self.leaving_count = 0

        self.current_time = 0
        self.arrival_time = random.expovariate(lambd)
        self.service_start_time = float('inf')
        self.leaving_time = float('inf')

        self.queue = Queue()
        self.device = Device()

    def receipt_of_demand(self):
        print("Требование поступило", self.current_time, end=" ||| ")
        demand = Demand(self.arrival_time)
        print("Demand ID:", demand.id)
        if self.queue.empty() and not self.device.serves:
            self.service_start_time = self.current_time
        self.queue.put(demand)
        self.arrival_time += random.expovariate(self.lambd)

    def service_start(self):
        print("Требование начало обслуживаться", self.current_time, end=" ||| ")
        service_time = random.expovariate(self.mu)
        self.leaving_time = self.current_time + service_time
        self.device.service_demand(self.queue.get())
        self.device.to_occupy()
        print("Demand ID:", self.device.demand.id)
        self.device.demand.service_start_time = self.current_time
        self.service_start_time = float('inf')

    def leaving_demand(self):
        print("Требование покинуло систему", self.current_time, end=" ||| ")
        demand = self.device.get_demand()
        print("Demand ID:", demand.id)
        self.device.to_free()
        demand.set_leaving_time(self.current_time)
        self.average_time += demand.leaving_time - demand.arrival_time
        self.leaving_count += 1
        if not self.queue.empty():
            self.service_start_time = self.current_time
        self.leaving_time = float('inf')

    def main(self, max_time):
        while self.current_time < max_time:
            self.current_time = min(self.arrival_time, self.service_start_time, self.leaving_time)
            if self.current_time == self.arrival_time:
                self.receipt_of_demand()
                time.sleep(0.8)
                continue
            if self.current_time == self.service_start_time:
                self.service_start()
                time.sleep(0.8)
                continue
            if self.current_time == self.leaving_time:
                self.leaving_demand()
                time.sleep(0.8)
                continue
        print(self.average_time / self.leaving_count)


if __name__ == '__main__':
    mm1 = MM1(1, 0.5)
    mm1.main(10000)
