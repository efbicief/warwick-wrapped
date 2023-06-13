"""A set of functions to generate, store and retrieve charts."""
import random
import os
from typing import Callable

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

import numpy as np

from dataFormat import Image


def load_chart(name:str)->bytes:
    """Load a chart from a file."""
    with open(f'charts/{name}.png', 'rb') as file:
        data = file.read()
    #This is cursed IDK if it wil deploy properly but prevents file buildup
    os.remove(f'charts/{name}.png')
    return data

def save_chart(func)->Callable[[],Image]:
    """A decorator to save the chart to a file."""
    def wrapper(*args, **kwargs)-> Image:
        """Save the chart to a file with a hashed name."""
        axes = func(*args, **kwargs)
        name = abs(hash(axes))
        plt.savefig(f'charts/{name}')
        plt.close()
        return Image(str(name))
    return wrapper

@save_chart
def test_chart()->Axes:
    """Generate a test chart"""
    x_list:list[float] =[random.random() for i in range(10)]
    y_list:list[float] =[random.random() for i in range(10)]

    _, axes = plt.subplots()

    axes.scatter(x_list, y_list)
    axes.set_title('Test Chart')
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    return axes

@save_chart
def graph_before_deadline(deadlines) -> Axes:
    deadlines.sort(key=lambda x: x[4])
    time_deltas = [(ded[3] - ded[4]).total_seconds()/86400 for ded in deadlines] # time_delta in days

    _, axes = plt.subplots()

    axes.scatter(range(len(time_deltas)), time_deltas)
    axes.set_title('Time before deadline for each submission')
    axes.set_xlabel('Submission number')
    axes.set_ylabel('Time before deadline (days)')
    axes.set_ylim(-5,14)
    axes.plot(np.poly1d(time_deltas))

    return axes

@save_chart
def module_grade_histogram(modules) -> Axes:
    bins = [i*2 for i in range(51)]
    marks = [i[4] for i in modules]
    
    _, axes = plt.subplots()

    axes.hist(marks, bins)
    axes.set_title('Your module grades distribution')
    axes.set_xlabel('Mark')
    axes.set_ylabel('Number of modules')

    return axes
