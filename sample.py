import matplotlib.pyplot as plt
from skimage import color, data, img_as_float, io
from ianus import adk

def main():
    """ Main """
    # Get input
    inputs = adk.get_inputs()

    # use inputs
    # inputs are named same as in module_specifiction file and the values will resolved in run-time
    original_image = io.imread(inputs.input_image)
    grayscale_image = img_as_float(original_image[::2, ::2])
    image = color.gray2rgb(grayscale_image)
    multiplier = [float(inputs.red), float(inputs.green), float(inputs.blue)]
    io.imsave("tinted.jpg", multiplier * image)

    # write outputs
    adk.set_output("success", True)
    adk.set_file_output("tinted_image", "tinted.jpg")
    adk.finalize()

if __name__ == "__main__":
    main()