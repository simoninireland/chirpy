# Signal classification
#
# Copyright (C) 2025--2026 Simon Dobson
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

import chirpy
import numpy as np
from typing import Tuple, List

# Import a version of Tensorflow Lite
try:
    # prefer Tensorflow Lite for Microcontrollers
    from ai_edge_litert.interpreter import Interpreter
    chirpy.logger.debug("Running on AI edge")
except ModuleNotFoundError:
    try:
        from tflite_runtime.interpreter import Interpreter
        chirpy.logger.debug("Running on TFLite for Micro")
    except ModuleNotFoundError:
        # fall-back to Tensorflow Lite
        from tensorflow.lite.interpreter import Interpreter
        chirpy.logger.debug("Running on TFLite")


# Global model
interpreter : Interpreter = None
inputLayerIndex : int = -1
outputLayerIndex : int = -1
labels : List[Tuple[str, str]] = []


# Labels to ignore
ignored = [944,    # Coyote
           945,    # Grey wolf
           1949,   # Dog
           2818,   # Human non-vocal
           2919,   # Human vocal
           2820,   # Human whistle
           2143,   # Engine
           2325,   # Fireworks
           2609,   # Gunshot  <-- should we keep this?
           4862,   # Power tools
           ]


def loadModel(fn):
    """Load a classifier and configure it for use.

    This function should be called before any analysis is performed.

    @param fn: the model filename
    """
    global interpreter, inputLayerIndex, outputLayerIndex

    interpreter = Interpreter(model_path=fn)
    interpreter.allocate_tensors()

    # extract the input and output tensors
    inputDetails = interpreter.get_input_details()
    outputDetails = interpreter.get_output_details()
    inputLayerIndex = inputDetails[0]["index"]
    outputLayerIndex = outputDetails[0]["index"]
    chirpy.logger.info(f"Loaded model from {fn}")


def loadLabels(fn):
    """Load a label file.

    This function should be called before any labels are requested.

    @param fn: the label filename
    """
    global labels

    labels = []
    with open(fn, "r", encoding="utf-8") as lls:
        chirpy.logger.info(f"Loaded labels from {fn}")
        for line in lls:
            sci, com = line.strip().split("_")
            labels.append((sci, com))
    chirpy.logger.info(f"{len(labels)} classes, including {len(ignored)} ignored")


def segment(sig, sampleRate, segment, overlap) -> List[np.ndarray]:
    """Split a signal into fixed-length segments.

    @param sig: the signal
    @param sampleRate: the sample rate
    @param segment: the size of a chunk in seconds
    @param overlap: the overlapping of segments in seconds
    @returns: a list of sub-signal chunks
    """
    chunkSize = int(sampleRate * segment)
    stepSize = int(sampleRate * (segment - overlap))
    lastChunk = max(0, int((sig.size - chunkSize + stepSize - 1) / stepSize) * stepSize)

    # append silence to the end of the sample to make sure
    # all splits are the same length
    padding = np.zeros(shape=chunkSize, dtype=sig.dtype)
    data = np.concatenate((sig, padding))

    # chunk the signal into segments
    segments = [ data[i: i + chunkSize] for i in range(0, lastChunk + 1, stepSize) ]

    return segments


def flatSigmoid(x, sensitivity=-1, bias=0.0):
    tb = (bias - 1.0) * 10.0
    return 1 / (1.0 + np.exp(sensitivity * np.clip(x + tb, -20, 20)))


def classify(segments):
    """Classify a list of segments of a signal.

    @param segments: a list of signals
    @returns: a list of prediction scores per segment
    """
    data = np.array(segments, dtype=np.float32)
    interpreter.resize_tensor_input(inputLayerIndex,
                                    [len(segments), *segments[0].shape])
    interpreter.allocate_tensors()
    interpreter.set_tensor(inputLayerIndex, data)
    interpreter.invoke()

    prediction = interpreter.get_tensor(outputLayerIndex)
    #prediction = flatSigmoid(prediction)

    return prediction


def mostLikelyIndex(prediction):
    """Extract the highest confidence identification..

    This finds the best (most confident) prediction in each segment,
    and then the best (most confident) across the segments.

    If the result is an ignored label, return None for both index and confidence.

    @param prediction: the prediction scores per segment
    @returns: a pair of the most likely index overall and its corresponding confidence
    """
    mostConfidentPerSample = np.argmax(prediction, axis=1)
    confidencePerSample = [ prediction[i][mostConfidentPerSample[i]] for i in range(len(mostConfidentPerSample)) ]
    mostConfidentSample = np.argmax(confidencePerSample)
    mostConfident = max(confidencePerSample)
    index =  mostConfidentPerSample[mostConfidentSample]

    if labelIsIgnored(index):
        # ignore the classification
        return None, None

    return index, mostConfident


def getLabelsMapping():
    """Return the mapping from species id to a pair of common and scientific names.

    @returns: the label mapping"""
    return labels


def labelIsIgnored(id):
    """Test whether a label is on the ignored list.

    Ignpored labels refer to classes that aren't birds, and so shouldn't be recorded.

    @param id: the label
    @returns: True if the labelm should be ignored"""
    return id in ignored


def identify(mli) -> Tuple[str, str]:
    """Return the labels associated with sample mli.

    @param mli: the most likely index of the prediction classifier
    @returns: a pair of scientific and common name as strings
    """
    return labels[mli]
