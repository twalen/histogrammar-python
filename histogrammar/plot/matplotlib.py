#!/usr/bin/env python

# Copyright 2016 Jim Pivarski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import types

# python 2/3 compatibility fixes
from histogrammar.util import *

def prepare2Dsparse(sparse):
    yminBins = [v.minBin for v in sparse.bins.values() if v.minBin is not None]
    ymaxBins = [v.maxBin for v in sparse.bins.values() if v.maxBin is not None]
    if len(yminBins) > 0 and len(ymaxBins) > 0:
        yminBin = min(yminBins)
        ymaxBin = max(ymaxBins)
    else:
        yminBin = 0
        ymaxBin = 0
    sample = list(sparse.bins.values())[0]
    ynum = 1 + ymaxBin - yminBin
    ylow = yminBin * sample.binWidth + sample.origin
    yhigh = (ymaxBin + 1.0) * sample.binWidth + sample.origin
    return yminBin, ymaxBin, ynum, ylow, yhigh

def set2Dsparse(sparse, yminBin, ymaxBin, grid):
    for i, iindex in enumerate(xrange(sparse.minBin, sparse.maxBin + 1)):
        for j, jindex in enumerate(xrange(yminBin, ymaxBin + 1)):
            if iindex in sparse.bins and jindex in sparse.bins[iindex].bins:
                grid[j, i] = sparse.bins[iindex].bins[jindex].entries
    return grid

class HistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """
            name : title of the plot.
            kwargs :  `matplotlib.patches.Rectangle` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        edges = self.bin_edges()
        entries = self.bin_entries()
        width = self.bin_width()

        ax.bar(edges[:-1], entries, width=width, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

    def num_bins(self):
        """
        Returns number of bins
        """
        return len(self.values)
    
    def bin_width(self):
        """
        Returns bin width
        """
        return (self.high - self.low) / self.num_bins()
    
    def bin_entries(self):
        """
        Returns bin values
        """
        import numpy as np
        return np.array([x.entries for x in self.values])

    def bin_edges(self):
        """
        Returns bin edges
        """
        import numpy as np
        num_bins = self.num_bins()
        edges = np.linspace(self.low, self.high, num_bins + 1)
        return edges

    def bin_centers(self):
        """
        Returns bin centers
        """
        import numpy as np
        return np.array([sum(self.range(i))/2.0 for i in self.indexes])


class SparselyHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """
            name : title of the plot.
            kwargs :  `matplotlib.patches.Rectangle` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        edges = self.bin_edges()
        entries = self.bin_entries()
        width = self.bin_width()

        ax.bar(edges[:-1], entries, width=width, **kwargs)
        ax.set_xlim(self.low,self.high)
        
        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

    def num_bins(self):
        """
        Returns number of bins
        """
        if self.minBin is None or self.maxBin is None:
            return 0
        nbins = self.maxBin - self.minBin + 1
        return nbins
    
    def bin_width(self):
        """
        Returns bin width
        """
        return self.binWidth

    def bin_edges(self):
        """
        Returns bin_edges
        """
        import numpy as np

        if self.minBin is None or self.maxBin is None:
            edges = np.array([self.origin, self.origin + 1])
        else:
            num_bins = self.maxBin - self.minBin + 1
            edges = np.linspace(self.low, self.high, num_bins + 1)
        return edges
    
    def bin_entries(self):
        """
        Returns bin values
        """
        import numpy as np

        if self.minBin is None or self.maxBin is None:
            entries = [self.bins[0].entries]
        else:
            entries = [self.bins[i].entries if i in self.bins else 0.0 \
                       for i in range(self.minBin, self.maxBin + 1)]
        return np.array(entries)

    def bin_centers(self):
        """
        Returns bin centers
        """
        import numpy as np

        bin_edges = self.bin_edges()
        centers = [(bin_edges[i]+bin_edges[i+1])/2. for i in range(len(bin_edges)-1)]
        return np.array(centers)
        
    
class ProfileMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for Bin of Average
              name : title of the plot.
              kwargs : matplotlib.collections.LineCollection properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        xranges = [self.range(x) for x in self.indexes]
        means = self.meanValues

        xmins = [x[0] for x in xranges]
        xmaxs = [x[1] for x in xranges]
        ax.hlines(self.meanValues, xmins, xmaxs, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class SparselyProfileMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for SparselyBin of Average
              name : title of the plot.
              kwargs : matplotlib.collections.LineCollection properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        xmins = np.arange(self.low, self.high, self.binWidth)
        xmaxs = np.arange(self.low + self.binWidth, self.high + self.binWidth, self.binWidth)

        means = np.nan*np.ones(xmaxs.shape)

        for i in xrange(self.minBin, self.maxBin + 1):
            if i in self.bins:
                means[i - self.minBin] = self.bins[i].mean
        idx = np.isfinite(means)

        ax.hlines(means[idx], xmins[idx], xmaxs[idx], **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class ProfileErrMethods(object):
    def plotmatplotlib(self, name=None, aspect=True, **kwargs):
        """ Plotting method for Bin of Deviate
              name : title of the plot.
              aspect :
              kwargs :  `matplotlib.collections.LineCollection` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        bin_centers = [sum(self.range(x))/2.0 for x in self.indexes]
        xranges = [self.range(x) for x in self.indexes]
        means = self.meanValues
        variances = self.varianceValues
        num_bins = len(variances)

        xmins = [x[0] for x in xranges]
        xmaxs = [x[1] for x in xranges]
        ax.hlines(self.meanValues, xmins, xmaxs, **kwargs)

        if aspect is True:
            counts = [p.entries for p in self.values]
            ymins = [means[i] - np.sqrt(variances[i])/np.sqrt(counts[i]) for i in range(num_bins)]
            ymaxs = [means[i] + np.sqrt(variances[i])/np.sqrt(counts[i]) for i in range(num_bins)]
        else:
            ymins = [means[i] - np.sqrt(variances[i]) for i in range(num_bins)]
            ymaxs = [means[i] + np.sqrt(variances[i]) for i in range(num_bins)]
        ax.vlines(bin_centers, ymins, ymaxs, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

class SparselyProfileErrMethods(object):
    def plotmatplotlib(self, name=None, aspect=True, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        xmins = np.arange(self.low, self.high, self.binWidth)
        xmaxs = np.arange(self.low + self.binWidth, self.high + self.binWidth, self.binWidth)

        means = np.nan*np.ones(xmaxs.shape)
        variances = np.nan*np.ones(xmaxs.shape)
        counts = np.nan*np.ones(xmaxs.shape)

        for i in xrange(self.minBin, self.maxBin + 1):
            if i in self.bins:
                means[i - self.minBin] = self.bins[i].mean
                variances[i - self.minBin] = self.bins[i].variance
                counts[i - self.minBin] = self.bins[i].entries
        idx = np.isfinite(means)

        # pull out non nans
        means = means[idx]
        xmins = xmins[idx]
        xmaxs = xmaxs[idx]
        variances = variances[idx]

        ax.hlines(means, xmins, xmaxs, **kwargs)

        bin_centers = (self.binWidth/2.0) + xmins
        if aspect is True:
            ymins = [means[i] - np.sqrt(variances[i])/np.sqrt(counts[i]) for i in xrange(len(means))]
            ymaxs = [means[i] + np.sqrt(variances[i])/np.sqrt(counts[i]) for i in xrange(len(means))]
        else:
            ymins = [means[i] - np.sqrt(variances[i]) for i in xrange(len(means))]
            ymaxs = [means[i] + np.sqrt(variances[i]) for i in xrange(len(means))]

        ax.vlines(bin_centers, ymins, ymaxs, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class StackedHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()
        color_cycle = plt.rcParams['axes.color_cycle']
        if "color" in kwargs:
            kwargs.pop("color")

        for i, hist in enumerate(self.values):
            color = color_cycle[i]
            hist.plotmatplotlib(color=color, label=hist.name, **kwargs)
            color_cycle.append(color)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class PartitionedHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()
        color_cycle = plt.rcParams['axes.color_cycle']
        if "color" in kwargs:
            kwargs.pop("color")

        for i, hist in enumerate(self.values):
            color = color_cycle[i]
            hist.plotmatplotlib(color=color, label=hist.name, **kwargs)
            color_cycle.append(color)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class FractionedHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        if isinstance(self.numerator, HistogramMethods):
            fracs = [x[0].entries / float(x[1].entries) for x in zip(self.numerator.values, self.denominator.values)]
            xranges = [self.numerator.range(x) for x in self.numerator.indexes]

            xmins = [x[0] for x in xranges]
            xmaxs = [x[1] for x in xranges]
            ax.hlines(fracs, xmins, xmaxs, **kwargs)


        elif isinstance(self.numerator, SparselyHistogramMethods):
            assert self.numerator.binWidth == self.denominator.binWidth,\
                   "Fraction numerator and denominator histograms must have same binWidth."
            numerator = self.numerator
            denominator = self.denominator
            xmins = np.arange(numerator.low, numerator.high, numerator.binWidth)
            xmaxs = np.arange(numerator.low + numerator.binWidth, numerator.high + numerator.binWidth, numerator.binWidth)

            fracs = np.nan*np.zeros(xmaxs.shape)

            for i in xrange(denominator.minBin, denominator.maxBin + 1):
                if i in self.numerator.bins and i in self.denominator.bins:
                    fracs[i - denominator.minBin] = numerator.bins[i].entries / denominator.bins[i].entries
            idx = np.isfinite(fracs)
            ax.hlines(fracs[idx], xmins[idx], xmaxs[idx], **kwargs)

        ax.set_ylim((0.0, 1.0))
        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class TwoDimensionallyHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for Bin of Bin of Count
              name : title of the plot.
              kwargs: matplotlib.collections.QuadMesh properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        x_ranges, y_ranges, grid = self.xy_ranges_grid()
        ax.set_ylim(self.y_lim())
        ax.set_xlim(self.x_lim())

        ax.pcolormesh(x_ranges, y_ranges, grid, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

    def xy_ranges_grid(self):
        """ Return x and y ranges and x,y grid
        """
        import numpy as np

        samp = self.values[0]
        x_ranges = np.unique(np.array([self.range(i) for i in self.indexes]).flatten())
        y_ranges = np.unique(np.array([samp.range(i) for i in samp.indexes]).flatten())

        grid = np.zeros((samp.num, self.num))

        for j in range(self.num):
            for i in range(samp.num):
                grid[i,j] = self.values[j].values[i].entries

        return x_ranges, y_ranges, grid

    def x_lim(self):
        """ return x low high tuble
        """
        return (self.low,self.high)
    
    def y_lim(self):
        """ return y low high tuble
        """
        samp = self.values[0]
        return (samp.low,samp.high)
        

class SparselyTwoDimensionallyHistogramMethods(object):
    def plotmatplotlib(self, name=None, **kwargs):
        """ Plotting method for SparselyBin of SparselyBin of Count
              name : title of the plot.
              kwargs: matplotlib.collections.QuadMesh properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        ax = plt.gca()

        x_ranges, y_ranges, grid = self.xy_ranges_grid()
        
        ax.pcolormesh(x_ranges, y_ranges, grid, **kwargs)
        ax.set_ylim(self.y_lim())
        ax.set_xlim(self.x_lim())

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

    def xy_ranges_grid(self):
        """ Return x and y ranges and x,y grid
        """
        import numpy as np

        yminBin, ymaxBin, ynum, ylow, yhigh = prepare2Dsparse(self)

        xbinWidth = self.binWidth
        ybinWidth = self.bins[0].binWidth

        xmaxBin = max(self.bins.keys())
        xminBin = min(self.bins.keys())
        xnum = 1 + xmaxBin - xminBin
        xlow = xminBin * self.binWidth + self.origin
        xhigh = (xmaxBin + 1) * self.binWidth + self.origin

        grid = set2Dsparse(self, yminBin, ymaxBin, np.zeros((ynum, xnum)))

        x_ranges = np.arange(xlow, xhigh + xbinWidth, xbinWidth)
        y_ranges = np.arange(ylow, yhigh + ybinWidth, ybinWidth)

        return x_ranges, y_ranges, grid

    def x_lim(self):
        """ return x low high tuble
        """
        xmaxBin = max(self.bins.keys())
        xminBin = min(self.bins.keys())
        xlow = xminBin * self.binWidth + self.origin
        xhigh = (xmaxBin + 1) * self.binWidth + self.origin
        return (xlow,xhigh)
    
    def y_lim(self):
        """ return y low high tuble
        """
        yminBin, ymaxBin, ynum, ylow, yhigh = prepare2Dsparse(self)
        return (ylow,yhigh)
        
