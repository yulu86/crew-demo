#!/usr/bin/env python
from ideal_finder.crew import IdealFinderCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    IdealFinderCrew().crew().kickoff(inputs=inputs)