#!/usr/bin/env python

# Copyright 2016 DIANA-HEP
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

from histogrammar.defs import *
from histogrammar.util import *

identity = serializable(lambda x: x)

class Count(Factory, Container):
    """Count entries by accumulating the sum of all observed weights or a sum of transformed weights (e.g. sum of squares of weights).

    An optional ``transform`` function can be applied to the weights before summing. To accumulate the sum of squares of weights, use

    ::

        lambda x: x**2

    for instance. This is unlike any other primitive's ``quantity`` function in that its domain is the *weights* (always double), not *data* (any type).
    """

    @staticmethod
    def ed(entries):
        """Create a Count that is only capable of being added.

        Parameters:
            entries (float): the number of entries.
        """
        if not isinstance(entries, (int, long, float)):
            raise TypeError("entries ({0}) must be a number".format(entries))
        if entries < 0.0:
            raise ValueError("entries ({0}) cannot be negative".format(entries))
        out = Count()
        out.entries = float(entries)
        return out.specialize()

    @staticmethod
    def ing(transform=identity):
        """Synonym for ``__init__``."""
        return Count(transform)

    def __init__(self, transform=identity):
        """Create a Count that is capable of being filled and added.

        Parameters:
            transform (function from float to float): transforms each weight.

        Other parameters:
            entries (float): the number of entries, initially 0.0.
        """
        self.entries = 0.0
        self.transform = serializable(transform)
        super(Count, self).__init__()
        self.specialize()
    
    @inheritdoc(Container)
    def zero(self): return Count(self.transform)

    @inheritdoc(Container)
    def __add__(self, other):
        if isinstance(other, Count):
            out = Count(self.transform)
            out.entries = self.entries + other.entries
            return out.specialize()
        else:
            raise ContainerException("cannot add {0} and {1}".format(self.name, other.name))

    @inheritdoc(Container)
    def fill(self, datum, weight=1.0):
        self._checkForCrossReferences()
        if weight > 0.0:
            t = self.transform(weight)
            if not isinstance(t, (bool, int, long, float)):
                raise TypeError("function return value ({0}) must be boolean or number".format(t))

            # no possibility of exception from here on out (for rollback)
            self.entries += t

    def fillnp(self, data, weight=1.0):
        """Increment the aggregator by providing a one-dimensional Numpy array of ``data`` to the fill rule with given ``weight`` (number or array).

        This primitive is optimized with Numpy.

        The container is changed in-place.
        """
        self._checkForCrossReferences()

        import numpy

        if self.transform is identity:
            if isinstance(weight, numpy.ndarray):
                self.entries += float(weight[weight > 0.0].sum())
            elif weight > 0.0:
                self.entries += float(weight * len(data))
        else:
            if isinstance(weight, numpy.ndarray):
                self.entries += float(self.transform(weight[weight > 0.0]).sum())
            elif weight > 0.0:
                self.entries += float(self.transform(weight * numpy.ones(len(data))).sum())

    @property
    def children(self):
        """List of sub-aggregators, to make it possible to walk the tree."""
        return []

    @inheritdoc(Container)
    def toJsonFragment(self, suppressName): return floatToJson(self.entries)

    @staticmethod
    @inheritdoc(Factory)
    def fromJsonFragment(json, nameFromParent):
        if isinstance(json, (int, long, float)):
            return Count.ed(float(json))
        else:
            raise JsonFormatException(json, "Count")
        
    def __repr__(self):
        return "<Count {0}>".format(self.entries)

    def __eq__(self, other):
        return isinstance(other, Count) and numeq(self.entries, other.entries) and self.transform == other.transform

    def __ne__(self, other): return not self == other

    def __hash__(self):
        return hash((self.entries, self.transform))

Factory.register(Count)
