from input import *
from output import *

from collections import deque


class Response:
    completed: bool = None
    end: bool = None
    delta: bool = None

    def __init__(self, completed=False, end=False, delta=None) -> None:
        self.completed = completed
        self.end = end
        self.delta = delta


class Queue:
    queue: deque[Job] = None

    def __init__(self) -> None:
        self.queue = deque()

    def enqueue(self, job: Job) -> None:
        self.queue.append(job)

    def peek(self, key=None, reverse=False) -> None:
        if len(self.queue) > 0:
            if key == None:
                return self.queue[0]
            a = list(self.queue)
            a.sort(key=key, reverse=reverse)
            return a[0]
        else:
            return None

    def deque(self, key=None, reverse=False) -> Job:
        if key == None:
            return self.queue.popleft()
        a = list(self.queue)
        a.sort(key=key, reverse=reverse)
        self.queue.remove(a[0])
        return a[0]


class Timer:
    time: int = None
    tq: int = None
    delta: int = None

    def __init__(self, callback, next=None, end=None,  time: int = 0, delta: int = 1, tq: int = None) -> None:
        self.time = time
        self.tq = tq
        self.delta = delta
        self.callback = callback
        self.next = next
        self.end = end

    def start(self) -> None:
        t = 0
        while True:
            res = self.callback(self.time, self.delta)
            if res.end == True:
                self.end()
                t = 0
                return
            if res.completed:
                self.time += res.delta
                self.stop()
                t = 0
                continue
            self.time += self.delta
            t += self.delta
            if (self.tq != None and t >= self.tq):
                self.time -= t - self.tq
                self.stop()
                t = 0
                # self.stop()
                # res = self.callback(self.time, self.delta + self.tq - t)
                # try:
                #     if res.end == True:
                #         self.end()
                #         t = 0
                #         return
                # except:
                #     1 + 1
                # if res.completed:
                #     self.time += res.delta
                #     self.stop()
                #     t = 0
                #     continue
                # t = 0
                # continue

    def stop(self) -> None:
        self.next(self.time, self.delta)

    def end(self) -> None:
        self.end()


def firstComeFirstServed(data: Input) -> Output:
    def findJob(arr, t):
        for x in arr:
            if x.arrTime <= t:
                return x
        return None

    out = OutputBuilder()

    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)
    
    t = 0
    prev_t = 0
    currJob = None
    while len(arr):
        if currJob == None:
            if (len(arr)):
                currJob = findJob(arr, t)
                if (currJob) and t != 0:
                    t = currJob.arrTime
                    chart.addEntry(Entry(prev_t, None, t))
                    prev_t = t
        else:
            currJob.decrementTime(1)
            if (currJob.timeLeft() <= 0):
                arr.remove(currJob)
                chart.addEntry(Entry(prev_t, currJob, t))
                prev_t = t
                if (len(arr)):
                    currJob = findJob(arr, t)
        t += 1

    chart = chart.getGanttChart()
    out.addGanttChart(chart=chart)
    out = out.getOutput()
    return out


def roundRobin(data: Input) -> Output:
    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    arr.sort(key=lambda a: a.arrTime, reverse=True)

    timer = None
    currJob = None
    jobQueue = Queue()

    def callback(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        while len(arr) != 0 and arr[-1].arrTime <= time:
            jobQueue.enqueue(arr.pop(-1))
        if (currJob == None):
            try:
                currJob = jobQueue.deque()
                chart.startProcess(currJob, time)
            except:
                currJob = None
        if currJob == None and len(arr) == 0:
            return Response(end=True)
        if currJob == None:
            return Response(completed=False)

        if currJob.timeLeft() - delta >= 0:
            currJob.decrementTime(delta)
            if (currJob.timeLeft() == 0):
                return Response(completed=True, delta=delta)
            return Response(completed=False)
        else:
            currJob.decrementTime(currJob.timeLeft())
            return Response(completed=True, delta=currJob.timeLeft())

    def next(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        if currJob == None:
            return
        if currJob.timeLeft() > 0:
            while len(arr) != 0 and arr[-1].arrTime <= time:
                jobQueue.enqueue(arr.pop(-1))
            jobQueue.enqueue(currJob)
            # try:
            #     t = jobQueue.queue[0]
            #     if (t != currJob):
            #         chart.endProcess(time)
            # except:
            chart.endProcess(time)
            currJob = None
            return
        chart.endProcess(time)
        currJob = None

    def end():
        nonlocal chart
        nonlocal out
        chart = chart.getGanttChart()
        out.addGanttChart(chart=chart)
        out = out.getOutput()
        return out

    timer = Timer(callback, next=next, end=end, tq=data.time_quantum)

    timer.start()

    return out


def shortestJobFirst(data: Input) -> Output:
    def findJob(arr, t):
        a = []
        for x in arr:
            if x.arrTime <= t:
                a.append(x)
        if len(a) == 0:
            return None
        a.sort(key=lambda a: a.timeLeft())
        return a[0]

    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    t = 0
    prev_t = 0
    currJob = None
    while len(arr):
        if currJob == None:
            if (len(arr)):
                currJob = findJob(arr, t)
                if (currJob) and t != 0:
                    t = currJob.arrTime
                    chart.addEntry(Entry(prev_t, None, t))
                    prev_t = t
        else:
            currJob.decrementTime(1)
            if (currJob.timeLeft() <= 0):
                arr.remove(currJob)
                chart.addEntry(Entry(prev_t, currJob, t))
                prev_t = t
                if (len(arr)):
                    currJob = findJob(arr, t)
        t += 1

    chart = chart.getGanttChart()
    out.addGanttChart(chart=chart)
    out = out.getOutput()
    return out

def longestJobFirst(data: Input) -> Output:
    def findJob(arr, t):
        a = []
        for x in arr:
            if x.arrTime <= t:
                a.append(x)
        if len(a) == 0:
            return None
        a.sort(key=lambda a: a.timeLeft(), reverse=True)
        return a[0]

    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    t = 0
    prev_t = 0
    currJob = None
    while len(arr):
        if currJob == None:
            if (len(arr)):
                currJob = findJob(arr, t)
                if (currJob) and t != 0:
                    t = currJob.arrTime
                    chart.addEntry(Entry(prev_t, None, t))
                    prev_t = t
        else:
            currJob.decrementTime(1)
            if (currJob.timeLeft() <= 0):
                arr.remove(currJob)
                chart.addEntry(Entry(prev_t, currJob, t))
                prev_t = t
                if (len(arr)):
                    currJob = findJob(arr, t)
        t += 1

    chart = chart.getGanttChart()
    out.addGanttChart(chart=chart)
    out = out.getOutput()
    return out

def shortestRemainingTimeFirst(data: Input) -> Output:
    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    arr.sort(key=lambda a: a.arrTime, reverse=True)

    def key(a): return a.timeLeft()

    timer = None
    currJob = None
    jobQueue = Queue()

    def callback(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        while len(arr) != 0 and arr[-1].arrTime <= time:
            jobQueue.enqueue(arr.pop(-1))

        if (currJob == None):
            try:
                currJob = jobQueue.deque(key=key)
                chart.startProcess(currJob, time)
            except:
                currJob = None
        if currJob == None and len(arr) == 0:
            return Response(end=True)
        if currJob == None:
            return Response(completed=False)

        t = jobQueue.peek(key=key)
        if t != None and currJob.timeLeft() > t.timeLeft():
            jobQueue.enqueue(currJob)
            chart.endProcess(time)
            jobQueue.deque(key=key)
            currJob = t
            chart.startProcess(currJob, time)

        if currJob.timeLeft() - delta >= 0:
            currJob.decrementTime(delta)
            if (currJob.timeLeft() == 0):
                return Response(completed=True, delta=delta)
            return Response(completed=False)
        else:
            currJob.decrementTime(currJob.timeLeft())
            return Response(completed=True, delta=currJob.timeLeft())

    def next(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        if currJob == None:
            return
        if currJob.timeLeft() > 0:
            while len(arr) != 0 and arr[-1].arrTime <= time:
                jobQueue.enqueue(arr.pop(-1))
            jobQueue.enqueue(currJob)
            # try:
            #     t = jobQueue.queue[0]
            #     if (t != currJob):
            #         chart.endProcess(time)
            # except:
            chart.endProcess(time)
            currJob = None
            return
        chart.endProcess(time)
        currJob = None

    def end():
        nonlocal chart
        nonlocal out
        chart = chart.getGanttChart()
        out.addGanttChart(chart=chart)
        out = out.getOutput()
        return out

    timer = Timer(callback, next=next, end=end, tq=data.time_quantum)

    timer.start()

    return out

def longestRemainingTimeFirst(data: Input) -> Output:
    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    arr.sort(key=lambda a: a.arrTime, reverse=True)

    def key(a): return a.timeLeft()

    timer = None
    currJob = None
    jobQueue = Queue()

    def callback(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        while len(arr) != 0 and arr[-1].arrTime <= time:
            jobQueue.enqueue(arr.pop(-1))

        if (currJob == None):
            try:
                currJob = jobQueue.deque(key=key, reverse=True)
                chart.startProcess(currJob, time)
            except:
                currJob = None
        if currJob == None and len(arr) == 0:
            return Response(end=True)
        if currJob == None:
            return Response(completed=False)

        t = jobQueue.peek(key=key)
        if t != None and currJob.timeLeft() < t.timeLeft():
            jobQueue.enqueue(currJob)
            chart.endProcess(time)
            jobQueue.deque(key=key, reverse=True)
            currJob = t
            chart.startProcess(currJob, time)

        if currJob.timeLeft() - delta >= 0:
            currJob.decrementTime(delta)
            if (currJob.timeLeft() == 0):
                return Response(completed=True, delta=delta)
            return Response(completed=False)
        else:
            currJob.decrementTime(currJob.timeLeft())
            return Response(completed=True, delta=currJob.timeLeft())

    def next(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        if currJob == None:
            return
        if currJob.timeLeft() > 0:
            while len(arr) != 0 and arr[-1].arrTime <= time:
                jobQueue.enqueue(arr.pop(-1))
            jobQueue.enqueue(currJob)
            # try:
            #     t = jobQueue.queue[0]
            #     if (t != currJob):
            #         chart.endProcess(time)
            # except:
            chart.endProcess(time)
            currJob = None
            return
        chart.endProcess(time)
        currJob = None

    # def next(time, delta):
    #     pass

    def end():
        nonlocal chart
        nonlocal out
        chart = chart.getGanttChart()
        out.addGanttChart(chart=chart)
        out = out.getOutput()
        return out

    timer = Timer(callback, next=next, end=end, tq=data.time_quantum)

    timer.start()

    return out

def priorityBased_NP(data: Input) -> Output:
    def findJob(arr, t):
        a = []
        for x in arr:
            if x.arrTime <= t:
                a.append(x)
        if len(a) == 0:
            return None
        a.sort(key=lambda a: a.priority)
        return a[0]

    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    t = 0
    prev_t = 0
    currJob = None
    while len(arr):
        if currJob == None:
            if (len(arr)):
                currJob = findJob(arr, t)
                if (currJob) and t != 0:
                    t = currJob.arrTime
                    chart.addEntry(Entry(prev_t, None, t))
                    prev_t = t
        else:
            currJob.decrementTime(1)
            if (currJob.timeLeft() <= 0):
                arr.remove(currJob)
                chart.addEntry(Entry(prev_t, currJob, t))
                prev_t = t
                if (len(arr)):
                    currJob = findJob(arr, t)
        t += 1

    chart = chart.getGanttChart()
    out.addGanttChart(chart=chart)
    out = out.getOutput()
    return out


def priorityBased_P(data: Input, reverse=False) -> Output:
    out = OutputBuilder()
    chart = GanttChartBuilder()
    arr: list[Job] = [x.clone() for x in data.jobs]
    arr2: list[Job] = [x.clone() for x in data.jobs]

    out.addJobs(arr2)

    arr.sort(key=lambda a: a.arrTime, reverse=True)

    def key(a): return a.priority

    timer = None
    currJob = None
    jobQueue = Queue()

    def callback(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        while len(arr) != 0 and arr[-1].arrTime <= time:
            jobQueue.enqueue(arr.pop(-1))

        if (currJob == None):
            try:
                currJob = jobQueue.deque(key=key, reverse=reverse)
                chart.startProcess(currJob, time)
            except:
                currJob = None
        if currJob == None and len(arr) == 0:
            return Response(end=True)
        if currJob == None:
            return Response(completed=False)

        t = jobQueue.peek(key=key)
        if t != None and key(currJob) > key(t) != reverse:
            jobQueue.enqueue(currJob)
            chart.endProcess(time)
            jobQueue.deque(key=key, reverse=reverse)
            currJob = t
            chart.startProcess(currJob, time)

        if currJob.timeLeft() - delta >= 0:
            currJob.decrementTime(delta)
            if (currJob.timeLeft() == 0):
                return Response(completed=True, delta=delta)
            return Response(completed=False)
        else:
            currJob.decrementTime(currJob.timeLeft())
            return Response(completed=True, delta=currJob.timeLeft())

    def next(time, delta):
        nonlocal currJob
        nonlocal chart
        nonlocal jobQueue
        if currJob == None:
            return
        if currJob.timeLeft() > 0:
            while len(arr) != 0 and arr[-1].arrTime <= time:
                jobQueue.enqueue(arr.pop(-1))
            jobQueue.enqueue(currJob)
            # try:
            #     t = jobQueue.queue[0]
            #     if (t != currJob):
            #         chart.endProcess(time)
            # except:
            chart.endProcess(time)
            currJob = None
            return
        chart.endProcess(time)
        currJob = None

    def end():
        nonlocal chart
        nonlocal out
        # chart.clean()
        chart = chart.getGanttChart()
        # chart.clean()
        out.addGanttChart(chart=chart)
        out = out.getOutput()
        return out

    timer = Timer(callback, next=next, end=end, tq=data.time_quantum)

    timer.start()

    return out
