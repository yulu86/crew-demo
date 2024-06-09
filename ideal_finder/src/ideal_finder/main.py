#!/usr/bin/env python
from ideal_finder.crew import IdealFinderCrew


def run():
    inputs = {
        'topic': '工具类互联网服务开发的创意'
    }
    IdealFinderCrew().crew().kickoff(inputs=inputs)