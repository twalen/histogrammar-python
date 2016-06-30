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


def prepare2Dsparse(sparse):
    yminBins = [v.minBin for v in sparse.bins.values() if v.minBin is not None]
    ymaxBins = [v.maxBin for v in sparse.bins.values() if v.maxBin is not None]
    if len(yminBins) > 0 and len(ymaxBins) > 0:
        yminBin = min(yminBins)
        ymaxBin = max(ymaxBins)
    else:
        yminBin = 0.0
        ymaxBin = 0.0
    sample = list(sparse.bins.values())[0]
    ynum = 1.0 + ymaxBin - yminBin
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
    def matplotlib(self, name=None, **kwargs):
        """
            kwargs :  `matplotlib.patches.Rectangle` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()

        entries = [x.entries for x in self.values]

        num_bins = len(self.values)
        width = (self.high - self.low)/num_bins
        edges = np.linspace(self.low, self.high, num_bins + 1)[:-1]

        ax.bar(edges, entries, width=width, **kwargs)
        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

class SparselyHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """
            kwargs :  `matplotlib.patches.Rectangle` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()

        if self.minBin is None or self.maxBin is None:
            ax.bar([self.origin, self.origin + 1], self.bins[0].entries, width=self.binWidth, **kwargs)
        else:
            size = 1 + self.maxBin - self.minBin
            entries = [self.bins[i].entries if i in self.bins else 0.0 for i in xrange(self.minBin, self.maxBin + 1)]
            edges = np.linspace(self.minBin, self.maxBin, len(entries) + 1)[:-1]
            ax.bar(edges, entries, width=self.binWidth, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

class ProfileMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class SparselyProfileMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class ProfileErrMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for Bin of Deviate
              kwargs :  `matplotlib.collections.LineCollection` properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()

        bin_centers = [sum(self.range(x))/2.0 for x in self.indexes]
        xranges = [self.range(x) for x in self.indexes]
        means = self.meanValues
        variances = self.varianceValues
        num_bins = len(variances)

        xmins = [x[0] for x in xranges]
        xmaxs = [x[1] for x in xranges]
        ax.hlines(self.meanValues, xmins, xmaxs, **kwargs)

        ymins = [means[i] - np.sqrt(variances[i]) for i in range(num_bins)]
        ymaxs = [means[i] + np.sqrt(variances[i]) for i in range(num_bins)]
        ax.vlines(bin_centers, ymins, ymaxs, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax

class SparselyProfileErrMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class StackedHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class PartitionedHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class FractionedHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()


        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax

class TwoDimensionallyHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for Bin of Bin of Count
              kwargs: matplotlib.collections.QuadMesh properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()

        samp = self.values[0]
        x_ranges = np.unique(np.array([self.range(i) for i in self.indexes]).flatten())
        y_ranges = np.unique(np.array([samp.range(i) for i in samp.indexes]).flatten())

        grid = np.zeros((samp.num, self.num))

        for j in xrange(self.num):
            for i in xrange(samp.num):
                grid[i,j] = self.values[j].values[i].entries

        ax.pcolormesh(x_ranges, y_ranges, grid, **kwargs)

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)
        return ax


class SparselyTwoDimensionallyHistogramMethods(object):
    def matplotlib(self, name=None, **kwargs):
        """ Plotting method for SparselyBin of SparselyBin of Count
              kwargs: matplotlib.collections.QuadMesh properties.

            Returns a matplotlib.axes instance
        """
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.gcf()
        ax = fig.gca()

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

        ax.pcolormesh(x_ranges, y_ranges, grid, **kwargs)
        ax.set_ylim((ylow, yhigh))
        ax.set_xlim((xlow, xhigh))

        if name is not None:
            ax.set_title(name)
        else:
            ax.set_title(self.name)

        return ax




