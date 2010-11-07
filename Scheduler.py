from SimPy.Simulation import *
from AbstractResource import *

class Scheduler(Process):
    def __init__(self, scenario, name="Scheduler"):
        Process.__init__ (self, name=name)
        self.scenario = scenario

        self.tasks = {}
        self.running = 0

    def addJob(self, job):
        jobList = self.tasks.get(job.taskId)
        
        if(jobList == None):
          jobList = []
        
        jobList.append(job)
        self.tasks[job.taskId] = jobList

    def run(self):
        while (1):
          allocations = self.scenario.schedule_algorithm (self.scenario.machines, self.tasks)

          # iterate over allocations generated by scheduling algorithm
          for machine_job in allocations:
            machine = machine_job[0]
            
            # if machine is undefined, create and start machine
            if(machine == None):
              machine = self.scenario.createMachine()
              activate(machine, machine.start())
            
            # start job on machine
            machine.addJob(machine_job[1])

          yield hold,self,self.scenario.sch_interval
