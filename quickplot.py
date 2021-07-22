#!/usr/bin/env python
# coding: utf-8

# QuickPlot contains cleaner and more coherent versions of some functions I commonly use for rapid multidimensional data visualization based on Matplotlib/Pyplot. The idea is to be able to display most types of data with 1-2 lines of code by handling boilerplate and automatically inferring which strategy is preferred for plotting a specific dataset; along with providing an interface to customize the generated plots at multiple levels of abstraction. The tools are mainly NumPy-focused and I am writing this mainly for my own use, so support/stability is not guaranteed.

# In[543]:


get_ipython().run_line_magic('matplotlib', 'widget')

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random


# In[542]:


plt.cm


# In[549]:


class ClassTemplate:
    pass

class Plot(ClassTemplate):
    def __init__(self, data, generate_plot=True, **kwargs):
        self.data = data
        if generate_plot:
            self.plot(**kwargs)
        
    def plot(self, use_density=True, use_latex=True, annotate=10, norm_annotate=True, **kwargs):
        plt.close('all')
        aliases = {
            'projection': ['p']
        }
        values = {
            '2d': None
        }
        varnames = list('xyzw')
        if use_latex:
            varnames = [f'${v}$' for v in varnames]
        params = list('xysc')+['alpha']
        ranges = [None, None, [2, 10], None, [0,1]]
        plot_params = dict(zip(
            params,
            [Plot.rescale(d, *ranges[i]) if (ranges[i] is not None) else d for (i, d) in enumerate(self.data)]
        ))
        self.axis = ax.scatter(**plot_params, cmap='hsv')
        return self.axis

    def get_scale(A):
        gamma = np.log10(A.max()-A.min())
        print(gamma)
        return gamma > 1.2
    def rescale(a, n, m):
        return np.interp(a, (a.min(), a.max()), (n, m))
