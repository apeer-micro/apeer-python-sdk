from apeer_dev_kit import adk
import your_code

if __name__ == "__main__":
    inputs = adk.get_inputs()

    outputs = your_code.run(inputs["input_image_path"], inputs["red"], inputs["green"], inputs["blue"])

    adk.set_output("success", outputs["success"])
    adk.set_file_output("tinted_image", outputs["tinted_image"])
    adk.finalize()
