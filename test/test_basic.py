# Test the basic functionality
#
# Copyright (C) 2025 Simon Dobson
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/gpl.html>.

# find the project root directory
import os
cwd = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.dirname(cwd)

# add the root directory to the load path, for loading the configuration
import sys
sys.path.append(rootDir)

# load everything else
import chirpy
import numpy as np
import unittest

# find the model files relative to the project root
modelFile = os.path.join(rootDir, "models/audio-model-int8.tflite")
labelFile = os.path.join(rootDir, "models/labels/en_uk.txt")
sampleFile = os.path.join(rootDir, "sample.wav")


class TestBasics(unittest.TestCase):

    def testIdentify(self):
        """Test we can analyse an audio sample."""

        # load a model and its labels
        chirpy.loadModel(modelFile)
        chirpy.loadLabels(labelFile)

        # load a signal
        sig, sampleRate = chirpy.load(sampleFile)
        segments = chirpy.segment(sig, sampleRate, 3, 1)

        # classify the signal
        prediction = chirpy.classify(segments)
        mli = chirpy.mostLikelyIndex(prediction)
        self.assertEqual(chirpy.identify(mli)[0], "Fringilla coelebs")


    def testReporting(self):
        """Test we can report through MQTT."""

        # load a model and its labels
        chirpy.loadModel(modelFile)
        chirpy.loadLabels(labelFile)

        # load a signal
        sig, sampleRate = chirpy.load(sampleFile)
        segments = chirpy.segment(sig, sampleRate, 3, 1)

        # classify the signal
        prediction = chirpy.classify(segments)
        mli = chirpy.mostLikelyIndex(prediction)

        # report via MQTT
        scientific, common = chirpy.identify(mli)
        chirpy.report(f"{scientific}_{common}")


    def testSample(self):
        """Test we can read an audio sample."""
        sig = chirpy.record(2, sampleRate=44100)
        self.assertEqual(len(sig), 2 * 44100)
