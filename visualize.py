#!/usr/bin/env python
'''
This example demonstrates a simple use of pycallgraph.
'''
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph.output import GraphvizOutput

from main import main as test


def main():
    config = Config()
    config.trace_filter = GlobbingFilter(exclude=[
        'pycallgraph.*',
        # '_*',
        # '*.secret_function',
    ])

    graphviz = GraphvizOutput(output_file='filter_exclude.png')

    with PyCallGraph(output=graphviz, config=config):
        test('/home/meiji/pictures/wally/general/')


if __name__ == '__main__':
    main()
