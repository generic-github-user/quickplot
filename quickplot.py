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
        
#         for paramset in [aliases, values]:
        for a in list(kwargs.keys()):
            for z in values.keys():
                if kwargs[a] == z:
                    kwargs[a] = values[z]
            for z in aliases.keys():
                if a in aliases[z]:
                    kwargs[z] = kwargs[a]
                    kwargs.pop(a)
                
        fig = plt.figure(figsize=(8, 8))
#         plt.style.use('fivethirtyeight')
        plt.style.use('seaborn-white')
        ax = fig.add_subplot(**kwargs)
        params = list('xysc')+['alpha']
        ranges = [None, None, [2, 10], None, [0,1]]
        projection = '2d'
        if 'projection' in kwargs:
            if kwargs['projection']:
                projection = kwargs['projection']
        else:
            projection = '2d'
        if use_density:
            si = params.index('s')
            print(self.data.shape)
            print(num_points)
            ranges[si] = np.array(ranges[si]) * (20 / (num_points ** (1/1.5)))
#         print(ax.set_xtitle)
        plot_params = dict(zip(
            params,
            [Plot.rescale(d, *ranges[i]) if (ranges[i] is not None) else d for (i, d) in enumerate(self.data)]
        ))
        spatial = list('xyz')
        numdims = int(projection[0])
        print(spatial[:numdims])
        
        for i, a in enumerate(spatial[:numdims]):
            label = varnames[i]
            print(f'Setting axis label: {label}')
            getattr(ax, f'set_{a}label')(label)
#             if np.log10(self.data.data[i].max()-self.data.data[i].min()) > 1.5:
            if Plot.get_scale(self.data.data[i]):
                getattr(ax, f'set_{a}scale')('log')
        self.axis = ax.scatter(**plot_params, cmap='hsv')
        
#         for point in random.sample(self.data, k=annotate):

        P = self.data.T[:,:2]
#          np.stack([P]*P.shape[0], axis=1)
        subsamples = np.clip(num_points//10, 0, 100)
        weights = np.mean(
                np.linalg.norm(np.expand_dims(P, 0) - np.stack([Plot.sample(P, subsamples)]*num_points, axis=1), axis=2),
                axis=0
            ) ** 3
        weights /= weights.sum()
        print(weights.shape)
        points = Plot.sample(self.data.T[:,:2], annotate, weights=weights)#.copy()
        
#         breakpoint()
#         points += (1 / np.linalg.norm(points - np.repeat(points, ))) * ()
        for i in range(100):
#         axis?
            deltas = np.expand_dims(points,0)-np.stack([points]*points.shape[0],axis=1)#.transpose([2,0,1])
#             deltas = np.min(deltas, axis=0, keepdims=True)
            distances = np.min(np.linalg.norm((-deltas)+0.0001, axis=2, ord=2), axis=1, keepdims=True)**1
            forces = np.expand_dims(0.000001 / distances, 2) ** 1.05
            forces = np.where(distances<0.02, forces, 0)
#             print(np.mean(distances), distances.shape)
#             distances = np.max(distances, axis=1, keepdims=True)
            shift = distances * deltas * np.array([3, 1])
#             print(np.mean(deltas, axis=0))
            points = points + np.mean(shift, axis=0)
#             -distances?
        self.place_coords(points)
#         fig.colorbar(matplotlib.cm.hsv())
        
        return self.axis

    def get_scale(A):
        gamma = np.log10(A.max()-A.min())
        print(gamma)
        return gamma > 1.2
    
    def place_coords(self, points):
        for point in points:
            coordinate = ", ".join(map(str, point[:2].round(2)))
            text = f'$({coordinate})$'
#             text = '.'
            plt.text(*point[:2], text, size=12)
    
    def sample(A, n, weights=None):
        return A[np.random.choice(A.shape[0], n, replace=False, p=weights)]
    
#     scatterplot density estimation?
    def grid(shape):
        return np.stack(np.meshgrid(*[np.arange(0, dim, 1) for dim in shape]), axis=2)
    
    def grid_like(A):
        return Plot.grid(A.shape)
    
    def rescale(a, n, m):
        return np.interp(a, (a.min(), a.max()), (n, m))

    def pickle(self, include_imports=True):
#         source = ''
        lines = []
        if include_imports:
            lines.extend(f'import {m}' for m in ['matplotlib.pyplot as plt', 'numpy as np'])
        source = '\n'.join(lines)
        return source
    
# TODO: add methods for interactive plotting (and editing, saving, etc.)
# TODO: automatically choose scale(s)
# TODO: add NetworkX functions (and handling for other classes/datatypes)
# TODO: add automatic label overlap reduction/text spacing
# t-sne

class Array:
    def __init__(self, data):
        self.data = data
        self.shape = self.data.shape
        self.T = self.data.T
        
    def prod(self, *args, **kwargs):
        return Array(self.data.prod(*args, **kwargs))
    
    def sin(self, *args, **kwargs):
        return Array(np.sin(self.data, *args, **kwargs))
    
    def __iter__(self):
        return iter(self.data)
# cyclic animations
# test = Array(np.random.normal([[0]*5], [[1, 2, 1, 1, 1]], size=[1, 5, 1000])).prod(axis=0)
test = Array(np.random.normal(0, 2, size=[5, 5, 5000])).prod(axis=0)
print(test.data.std())
v = np.abs(test.data)
print(np.log10(
    v.max()-v.min()
))
z = np.histogram2d(*test.data[:2], bins=50)
# print(z)
z = [z[i]for i in[1,2,0]]
z = [z[i][:p or len(z[i])]for i, p in enumerate([-1,-1,0])]
# plt.contour(X=None, Y=None, Z=np.array(z))

c = Plot(test, p='2d')


# In[538]:


plt.close('all')
fig = plt.figure()
ax = fig.add_subplot()
R = 100
a = np.random.normal(0,1,[R]*2)
g = Plot.grid_like(a)-R//2
q = np.linalg.norm(g, axis=2)
k = lambda: np.random.normal(10, 2)
a += ((np.cos(g[:,:,0] * k() + k()) * k() + np.sin(g[:,:,1] * k() + 0.1) * k()) + (q * 0.1)) * 0.1
ax.contour(
    a,
    cmap='inferno', antialiased=False, nchunk=1, levels=4, linewidths=1)
# plt.imshow(a)
# In[ ]:


plt.scatter()


# In[ ]:


np.random.


# In[23]:


import nltk


# In[ ]:


colors = np.stack(np.meshgrid(*[np.arange(0, dim, 1) for dim in canvas.shape[:2]]), axis=2)

