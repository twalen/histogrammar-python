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

from histogrammar.defs import *

class Label(Factory, Container):
    @staticmethod
    def ed(entries, **pairs):
        if entries < 0.0:
            raise ContainerException("entries ({}) cannot be negative".format(entries))

        out = Label(**pairs)
        out.entries = float(entries)
        return out

    @staticmethod
    def ing(**pairs):
        return Label(**pairs)

    def __init__(self, **pairs):
        if any(not isinstance(x, basestring) for x in pairs.keys()):
            raise ContainerException("all Label keys must be strings")
        if len(pairs) < 1:
            raise ContainerException("at least one pair required")
        contentType = pairs.values()[0].name
        if any(x.name != contentType for x in pairs.values()):
            raise ContainerException("all Label values must have the same type")

        self.entries = 0
        self.pairs = pairs

        super(Label, self).__init__()

    @property
    def pairsMap(self): return self.pairs
    @property
    def size(self): return len(self.pairs)
    @property
    def keys(self): return self.pairs.keys()
    @property
    def values(self): return self.pairs.values()
    @property
    def keySet(self): return set(self.pairs.keys())

    def __call__(self, x): return self.pairs[x]
    def get(self, x): return self.pairs.get(x, None)
    def getOrElse(self, x, default): return self.pairs.get(x, default)

    @property
    def zero(self): return Label(**{k: v.zero for k, v in self.pairs.items()})

    def __add__(self, other):
        if isinstance(other, Label):
            if self.keySet != other.keySet:
                raise ContainerException("cannot add Labels because keys differ:\n    {}\n    {}".format(", ".join(sorted(self.keys)), ", ".join(sorted(other.keys))))

            out = Label(**{k: self(k) + other(k) for k in self.keys})
            out.entries = self.entries + other.entries
            return out

        else:
            raise ContainerException("cannot add {} and {}".format(self.name, other.name))

    def fill(self, datum, weight=1.0):
        for x in self.values:
            x.fill(datum, weight)

    def toJsonFragment(self): return {
        "entries": self.entries,
        "type": self.values[0].name,
        "data": {k: v.toJsonFragment() for k, v in self.pairs.items()},
        }

    @staticmethod
    def fromJsonFragment(json):
        if isinstance(json, dict) and set(json.keys()) == set(["entries", "type", "data"]):
            if isinstance(json["entries"], (int, long, float)):
                entries = json["entries"]
            else:
                raise JsonFormatException(json, "Label.entries")

            if isinstance(json["type"], basestring):
                factory = Factory.registered[json["type"]]
            else:
                raise JsonFormatException(json, "Label.type")

            if isinstance(json["data"], dict):
                pairs = {k: factory.fromJsonFragment(v) for k, v in json["data"].items()}
            else:
                raise JsonFormatException(json, "Label.data")

            return Label.ed(entries, **pairs)

    def __repr__(self):
        return "Label[{}..., size={}]".format(repr(self.values[0]), self.size)

    def __eq__(self, other):
        return isinstance(other, Label) and exact(self.entries, other.entries) and self.pairs == other.pairs

    def __hash__(self):
        return hash((self.entries, tuple(sorted(self.pairs.items()))))

Factory.register(Label)
