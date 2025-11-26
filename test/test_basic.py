# Test the bsic functionality
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

from chirpy import *
import numpy as np
import unittest

# find the model files relative to the project root
import os
cwd = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.dirname(cwd)
modelFile = os.path.join(rootDir, "models/audio-model-int8.tflite")
labelFile = os.path.join(rootDir, "models/labels/en_uk.txt")
sampleFile = os.path.join(rootDir, "sample.wav")


class TestBasics(unittest.TestCase):

    def testSample(self):
        """Test we can analyse an audio sample."""

        # load a model and its labels
        loadModel(modelFile)
        loadLabels(labelFile)

        # load a signal
        sig, sampleRate = load(sampleFile)
        segments = segment(sig, sampleRate, 3, 1)

        # classify the signal
        prediction = classify(segments)
        mli = mostLikelyIndex(prediction)
        self.assertEqual(identify(mli)[0], "Fringilla coelebs")
