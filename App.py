from input import *
from output import *
from scheduling_algos import *
from inputparser import *
import eel

eel.init("web")

class Result:
    def __init__(self) -> None:
        self.name = "hehe"

@eel.expose
def rand_python():
    return Result()

@eel.expose
def get_algo_names_python():
    return {
        "First Come First Served": "firstComeFirstServed",
        "Round Robin": "roundRobin",
        "Shortest Job First": "shortestJobFirst",
        "Longest Job First": "longestJobFirst",
        "Shortest Remaing Time First": "shortestRemainingTimeFirst",
        "Longest Remaing Time First": "longestRemainingTimeFirst",
        "Priority Based (Non-Premitive)": "priorityBased_NP",
        "Priority Based (Premitive)": "priorityBased_P"
    }

@eel.expose
def calculate_scheduling_python(input, func):
    parser = InputParser.getParser()
    inp = parser.parse(input)
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(func)
    output : Output = method(inp)
    output.printOutput()
    return output.Objectify()

eel.start("index.html")