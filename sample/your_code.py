from skimage import color, img_as_float, io


def run(input_image_path, red, green, blue):

    original_image = io.imread(input_image_path)
    grayscale_image = img_as_float(original_image[::2, ::2])
    image = color.gray2rgb(grayscale_image)
    multiplier = [float(red), float(green), float(blue)]
    output_file_path = 'tinted.png'
    io.imsave(output_file_path, multiplier * image)

    return {'success': True, 'tinted_image': output_file_path}
