from input import *


class Entry:
    entry: tuple[int, Job, int] = None

    def __init__(self, start, job, end) -> None:
        self.entry = (start, job, end)
    
    def getJobName(self):
        if self.entry[1] == None:
            return None
        return self.entry[1].name

    def printEntry(self):
        print("(", self.entry[0], ", ",
              self.getJobName(), ", ", self.entry[2], ")")


class GanttChart:
    entrylist: list[Entry] = None

    def __init__(self) -> None:
        self.entrylist = []
        self.currEntry = None

    def clean(self):  # Not working for some reason
        prev = None
        entry = None
        l = []
        for x in self.entrylist:
            if prev == None:
                prev = x
                entry = x
                continue
            if x.entry[1] != prev.entry[1]:
                l.append(Entry(entry.entry[0], entry.entry[1], prev.entry[2]))
                entry = x

            prev = x
        if (prev):
            l.append(Entry(entry.entry[0], entry.entry[1], prev.entry[2]))

        self.entrylist = l
        l = []
        t = 0
        for x in self.entrylist:
            if t < x.entry[0]:
                l.append(Entry(t, None, x.entry[0]))
            l.append(x)
            t = x.entry[2]

        self.entrylist = l

    def printGantChartt(self) -> None:
        print("Gantt Chart: ")
        for entry in self.entrylist:
            entry.printEntry()


class GanttChartBuilder:
    chart: GanttChart = None
    currEntry: Entry = None

    def __init__(self) -> None:
        self.chart = GanttChart()

    def addEntry(self, entry: Entry) -> None:
        self.chart.entrylist.append(entry)

    def startProcess(self, job: Job, startTime: int) -> None:
        self.currEntry = Entry(startTime, job, None)

    def endProcess(self, endTime: int) -> None:
        self.currEntry = Entry(
            self.currEntry.entry[0], self.currEntry.entry[1], endTime)
        self.chart.entrylist.append(self.currEntry)
        self.currEntry = None

    def getGanttChart(self) -> GanttChart:
        t: GanttChart = self.chart
        self.chart = GanttChart()
        t.clean()
        return t
    

# class CT:
#     def __init__(self, time, name):
#         self.time = time
#         self.name = name

# class CTList:
#     def __init__(self):
#         self.entries = []

# class CTListBuilder:
#     def __init__(self) -> None:
#         self.ctlist = CTList()
#     def addCT(self, time, name):
#         self.ctlist.entries.append(CT(time, name))
#     def getCT(self):
#         t = self.ctlist
#         self.ctlist = CTList()
#         return t


class Output:
    gchart: GanttChart = None
    jobs: list[Job] = None

    def __init__(self) -> None:
        self.gchart = GanttChart()

    def printOutput(self) -> None:
        print("Output: ")
        self.gchart.printGantChartt()
    
    def getCompletionTime(self):
        obj = {}
        for x in self.jobs:
            max = None
            for t in self.gchart.entrylist:
                if t.getJobName() == x.name:
                    if max == None or t.entry[2] >= max:
                        max = t.entry[2]
            obj[x.name] = max
        return obj
    def getTurnarroundTime(self):
        obj = {}
        for x in self.jobs:
            max = None
            for t in self.gchart.entrylist:
                if t.getJobName() == x.name:
                    if max == None or t.entry[2] >= max:
                        max = t.entry[2]
            obj[x.name] = max - x.arrTime 
            
        return obj
    
    def getWaitingTime(self):
        obj = {}
        for x in self.jobs:
            max = None
            for t in self.gchart.entrylist:
                if t.getJobName() == x.name:
                    if max == None or t.entry[2] >= max:
                        max = t.entry[2]
            obj[x.name] = max - x.arrTime - x.timeLeft()
            
        return obj

    def getResponseTime(self):
        obj = {}
        for x in self.jobs:
            min = None
            for t in self.gchart.entrylist:
                if t.getJobName() == x.name:
                    if min == None or t.entry[0] <= min:
                        min = t.entry[0]
            obj[x.name] = min - x.arrTime
            
        return obj
    
    def Objectify(self):
        obj = {}
        l = []
        for x in self.gchart.entrylist:
            l.append([int(x.entry[0]), x.getJobName(), int(x.entry[2]),])

        obj['gant_chart'] = l

        obj['ct_list'] = self.getCompletionTime()

        obj['tat_list'] = self.getTurnarroundTime()

        obj['wt_list'] = self.getWaitingTime() 

        obj['rt_list'] = self.getResponseTime()

        return obj


class OutputBuilder:
    output: Output = None

    def __init__(self) -> None:
        self.output = Output()

    def addGanttChart(self, chart: GanttChart) -> None:
        self.output.gchart = chart

    def addJobs(self, jobs):
        self.output.jobs = jobs

    def getOutput(self) -> Output:
        t: Output = self.output
        self.output = Output()
        return t
