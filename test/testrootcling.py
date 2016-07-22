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

import json
import unittest

from histogrammar import *

class TestRootCling(unittest.TestCase):
    ttreeFlat = None
    ttreeEvent = None

    try:
        import ROOT
        ROOT.gInterpreter.AddIncludePath("test/Event.h")
        ROOT.gInterpreter.ProcessLine(".L test/Event.cxx")
        tfileFlat = ROOT.TFile("test/flat.root")
        ttreeFlat = tfileFlat.Get("simple")
        tfileEvent = ROOT.TFile("test/Event.root")
        ttreeEvent = tfileEvent.Get("T")
    except ImportError:
        pass

    ################################################################ Count

    def testCount(self):
        if TestRootCling.ttreeFlat is not None:
            hg = Count()
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"type": "Count", "data": 10000})
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"type": "Count", "data": 20000})

            hg = Count("0.5 * weight")
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"type": "Count", "data": 5000})
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"type": "Count", "data": 10000})

    #     if TestRootCling.ttreeEvent is not None:
    #         hg = Count()
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"type": "Count", "data": 1000})
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"type": "Count", "data": 2000})

    #         hg = Count("0.5 * weight")
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"type": "Count", "data": 500})
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"type": "Count", "data": 1000})

    ################################################################ Sum

    def testSum(self):
        if TestRootCling.ttreeFlat is not None:
            hg = Sum("positive")
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"data": {"sum": 7970.933535083706, "name": "positive", "entries": 10000}, "type": "Sum"})
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"data": {"sum": 2*7970.933535083706, "name": "positive", "entries": 20000}, "type": "Sum"})

            hg = Sum("2 * noholes")
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"data": {"sum": 137.62044119255137, "name": "2 * noholes", "entries": 10000}, "type": "Sum"})
            hg.cling(TestRootCling.ttreeFlat, debug=True)
            self.assertEqual(hg.toJson(), {"data": {"sum": 2*137.62044119255137, "name": "2 * noholes", "entries": 20000}, "type": "Sum"})

    #     if TestRootCling.ttreeEvent is not None:
    #         hg = Sum("event.GetNtrack()")
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"data": {"sum": 599640, "name": "event.GetNtrack()", "entries": 1000}, "type": "Sum"})
    #         hg.cling(TestRootCling.ttreeEvent, debug=False)
    #         self.assertEqual(hg.toJson(), {"data": {"sum": 2*599640, "name": "event.GetNtrack()", "entries": 2*1000}, "type": "Sum"})

    ################################################################ Bin

    def testBin(self):
        if TestRootCling.ttreeFlat is not None:
            hg = Bin(20, -10, 10, "withholes")
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"data": {
    "nanflow:type": "Count", 
    "name": "withholes", 
    "nanflow": 96.0, 
    "overflow:type": "Count", 
    "values:type": "Count", 
    "high": 10.0, 
    "values": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 201.0, 1346.0, 3385.0, 3182.0, 1358.0, 211.0, 15.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "low": -10.0, 
    "entries": 10000.0, 
    "overflow": 99.0, 
    "underflow": 96.0, 
    "underflow:type": "Count"
  }, 
  "type": "Bin"})

            hg = Bin(20, -10, 10, "2 * withholes", Sum("positive"))
            hg.cling(TestRootCling.ttreeFlat, debug=False)
            self.assertEqual(hg.toJson(), {"data": {
    "values:name": "positive",
    "nanflow:type": "Count",
    "name": "2 * withholes",
    "nanflow": 96.0,
    "overflow:type": "Count",
    "values:type": "Sum",
    "high": 10.0,
    "values": [
      {"sum": 0.0, "entries": 0.0},
      {"sum": 0.0, "entries": 0.0},
      {"sum": 0.48081424832344055, "entries": 1.0},
      {"sum": 10.879940822720528, "entries": 9.0},
      {"sum": 43.35080977156758, "entries": 54.0},
      {"sum": 113.69398449920118, "entries": 147.0},
      {"sum": 349.6867558255326, "entries": 449.0},
      {"sum": 729.5858678516815, "entries": 897.0},
      {"sum": 1155.193773361767, "entries": 1451.0},
      {"sum": 1520.5854493912775, "entries": 1934.0},
      {"sum": 1436.6912576352042, "entries": 1796.0},
      {"sum": 1116.2790022112895, "entries": 1386.0},
      {"sum": 728.2537153647281, "entries": 922.0},
      {"sum": 353.9190010114107, "entries": 436.0},
      {"sum": 121.04832566762343, "entries": 158.0},
      {"sum": 42.87702897598501, "entries": 53.0},
      {"sum": 8.222344039008021, "entries": 13.0},
      {"sum": 2.8457946181297302, "entries": 2.0},
      {"sum": 0.36020421981811523, "entries": 1.0},
      {"sum": 0.0, "entries": 0.0}
    ],
    "low": -10.0,
    "entries": 10000.0,
    "overflow": 99.0,
    "underflow": 96.0,
    "underflow:type": "Count"
  },
  "type": "Bin"})

