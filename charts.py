"""A set of functions to generate, store and retrieve charts."""
import random
import os
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

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
