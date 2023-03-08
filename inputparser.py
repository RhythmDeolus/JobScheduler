from input import *


class InputParser:
    parser = None

    @staticmethod
    def getParser():
        if (InputParser.parser == None):
            InputParser.parser = InputParser()
        return InputParser.parser

    def parse(self, input) -> Input:
        # print(input)
        file = input
        file = file.split('\n')

        head = file[0]

        head = head.split()
        prio = head[0] == "True"

        result = InputBuilder()
        result.setPrimitive(prio)
        try:
            result.setTQ(int(head[1]))
        except:
            result.setTQ(None)

        for line in file[1:]:
            data = line.split()
            i = 0
            job = JobBuilder()
            if (data[i].isalpha()):
                job.setName(data[i])
                i += 1

            if (prio):
                job.setPriority(int(data[i]))
                i += 1
            job.setArrivalTime(int(data[i]))
            i += 1
            seq = SequenceBuilder()
            for c in data[i:]:
                seq.addtoSeq(self.parseTime(c))
            seq = seq.getSequence()
            job.setSequence(seq)
            job = job.getJob()
            result.addJob(job)
        result = result.getInput()
        return result

    def parseTime(self, text: str):
        if (text[0] == 'c'):
            return CPUBurst(int(text[1:]))
        elif (text[0] == 'i'):
            return IOWait(int(text[2:]))
        else:
            raise Exception("Unable to parse time")
