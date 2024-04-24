import math
from scipy.interpolate import interp1d
from numpy import linspace
import numpy as np


class NilorFloats:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # Dictionary that defines input types for each field
        return {
            "required": {
                "number_of_frames": ("INT", {"forceInput": False}),
                "number_of_images": ("INT", {"forceInput": False}),
                "image_number": ("INT", {"forceInput": False}),
            },
        }

    # Define return types and names for outputs of the node
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("floats",)

    FUNCTION = "test"
    CATEGORY = "nilor-nodes"

    @staticmethod
    def interpolate_values(start, end, num_points):
        # Linear interpolation between start and end over num_points
        x = linspace(0, num_points - 1, num_points)
        y = linspace(start, end, num_points)
        f = interp1d(x, y, kind="cubic")
        return f(x)

    def test(self, number_of_frames, number_of_images, image_number):
        # Initializes the array with zeros
        my_floats = [0.0] * number_of_frames
        # Calculate the length of each portion based on total frames and number of images
        portion_length = int((number_of_frames - 1) / (number_of_images - 1))

        # Handling the first image (special case for the first segment)
        if image_number == 1:
            portion_values = NilorFloats.interpolate_values(1, 0, portion_length)
            my_floats[0:portion_length] = portion_values
        # Handling the last image (special case for the last segment)
        elif image_number == number_of_images:
            portion_values = NilorFloats.interpolate_values(0, 1, portion_length)
            start_index = int((number_of_images - 2) * portion_length)
            my_floats[start_index:] = portion_values
        # Handling middle images (general case for dual segments)
        else:
            portion_values = np.concatenate(
                [
                    NilorFloats.interpolate_values(0, 1, portion_length),
                    NilorFloats.interpolate_values(1, 0, portion_length),
                ]
            )
            start_index = int((image_number - 2) * portion_length)
            end_index = start_index + (2 * portion_length)
            my_floats[start_index:end_index] = portion_values
        # Returns the modified list of float values
        return (my_floats,)


class NilorIntToListOfBools:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # Dictionary that defines input types for each field
        return {
            "required": {
                "number_of_images": ("INT", {"forceInput": False}),
            },
        }

    # Define return types and names for outputs of the node
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("booleans",)

    FUNCTION = "boolify"
    CATEGORY = "nilor-nodes"
    OUTPUT_IS_LIST = (True,)

    def boolify(self, number_of_images, max_images=10):
        # Initializes the array with zeros
        my_bools = [False] * max_images

        for i in range(max_images):
            # Set the boolean value to True if the index is less than the number of images
            my_bools[i] = i < number_of_images

        return (my_bools,)


class NilorBoolFromListOfBools:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # Dictionary that defines input types for each field
        return {
            "required": {
                "booleans": ("BOOLEAN", {"forceInput": False}),
                "index": ("INT", {"forceInput": False}),
            },
        }

    # Define return types and names for outputs of the node
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("boolean",)

    FUNCTION = "bool_by_index"
    CATEGORY = "nilor-nodes"

    INPUT_IS_LIST = True

    def bool_by_index(self, booleans, index):
        # Returns the boolean value at the given index
        actual_index = index[0] if isinstance(index, list) else index
        desired_bool = booleans[actual_index]
        return [desired_bool]


# Mapping class names to objects for potential export
NODE_CLASS_MAPPINGS = {
    "Nilor Floats": NilorFloats,
    "Nilor Int To List Of Bools": NilorIntToListOfBools,
    "Nilor Bool From List Of Bools": NilorBoolFromListOfBools,
}
# Mapping nodes to human-readable names
NODE_DISPLAY_NAME_MAPPINGS = {
    "FirstNode": "My First Node",
    "SecondNode": "My Second Node",
    "ThirdNode": "My Third Node",
}
