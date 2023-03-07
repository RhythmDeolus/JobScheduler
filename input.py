class CPUBurst:
    time: int = None

    def __init__(self, time: int) -> None:
        self.time = time

    def clone(self):
        return CPUBurst(self.time)


class IOWait:
    time: int = None

    def __init__(self, time: int) -> None:
        self.time = time

    def clone(self):
        return IOWait(self.time)


class Sequence:
    seq = None

    def __init__(self) -> None:
        self.seq = []

    def clone(self):
        s = SequenceBuilder()
        for x in self.seq:
            s.addtoSeq(x.clone())
        return s.getSequence()

    def printSequence(self, front=""):
        # print(front, end="")
        for item in self.seq:
            print(item.time, end="  ")
        print()


class SequenceBuilder:
    sequence: Sequence = None

    def __init__(self) -> None:
        self.sequence = Sequence()

    def addtoSeq(self, item):
        self.sequence.seq.append(item)

    def getSequence(self) -> Sequence:
        t: Sequence = self.sequence
        self.sequence = Sequence()
        return t


class Job:
    name: str = None
    priority: int = None
    arrTime: int = None
    curr: int = 97
    seq: Sequence = None

    def __init__(self) -> None:
        self.priority = 0
        self.arrTime = 0
        self.name = chr(Job.curr)
        self.seq = Sequence()
        Job.curr += 1
        if (Job.curr > 97 + 26):
            Job.curr = 97

    def timeLeft(self):
        sum = 0
        for x in self.seq.seq:
            sum += x.time
        return sum

    def decrementTime(self, time):
        i = 0
        for i in range(len(self.seq.seq)):
            if (self.seq.seq[i].time != 0):
                self.seq.seq[i].time -= time
                return True
        return False

    def clone(self):
        j = Job()
        j.priority = self.priority
        j.arrTime = self.arrTime
        j.name = self.name
        j.seq = self.seq.clone()
        return j

    def printJob(self, front=""):
        print(front, "Name: ", self.name)
        print(front, "Priority: ", self.priority)
        print(front, "Arrival Time: ", self.arrTime)
        print(front, "Sequence: ", end="")
        self.seq.printSequence(front=front + "\t")


class JobBuilder:
    job: Job = None

    def __init__(self) -> None:
        self.job = Job()

    def setPriority(self, priority: int):
        self.job.priority = priority

    def setName(self, name: str):
        self.job.name = name

    def setSequence(self, seq: Sequence):
        self.job.seq = seq

    def setArrivalTime(self, time: int):
        self.job.arrTime = time

    def getJob(self) -> Job:
        t: Job = self.job
        self.job = Job()
        return t


class Input:
    jobs: list[Job] = None
    primitive: bool = None
    time_quantum: int = None

    def __init__(self) -> None:
        self.jobs = []
        self.primitive = False
        self.time_quantum = 3

    def printInput(self) -> None:
        print("Primitve: ", self.primitive)
        if (self.primitive):
            print("Time Quantum: ", self.time_quantum)
        print("Jobs: ")
        for job in self.jobs:
            job.printJob(front="\t")
            print()


class InputBuilder:
    input_var: Input = None

    def __init__(self) -> None:
        self.input_var = Input()

    def addJob(self, job: Job) -> None:
        if (self.input_var):
            self.input_var.jobs.append(job)

    def setPrimitive(self, val: bool):
        self.input_var.primitive = val

    def setTQ(self, val: int):
        self.input_var.time_quantum = val

    def getInput(self) -> Input:
        t: Input = self.input_var
        self.input_var = Input()
        return t
