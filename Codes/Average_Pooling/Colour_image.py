import cv2
import numpy as np

def exact_average_pooling_color(image, pool_size=(2, 2)):
    """Performs exact average pooling on a color image with a given pool size."""
    if image is None:
        raise ValueError("Error: Image is None. Please check the file path.")

    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Error: Input must be a color image with 3 channels (RGB/BGR).")

    h, w, c = image.shape  # Height, width, channels
    ph, pw = pool_size  # Pooling height & width

    # Ensure dimensions are divisible by pool size
    new_h, new_w = h // ph, w // pw
    pooled_image = np.zeros((new_h, new_w, c), dtype=np.uint8)

    for ch in range(c):  # Loop over each channel (R, G, B)
        for i in range(0, h, ph):
            for j in range(0, w, pw):
                patch = image[i:i+ph, j:j+pw, ch]  # Extract 2×2 patch for channel `ch`
                avg_value = np.mean(patch)  # Compute mean
                pooled_image[i//ph, j//pw, ch] = int(avg_value)  # Store integer result

    return pooled_image


def approximate_average_pooling_color(image, pool_size=(2, 2)):
    """Performs approximate average pooling on a color image with a given pool size."""
    if image is None:
        raise ValueError("Error: Image is None. Please check the file path.")

    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Error: Input must be a color image with 3 channels (RGB/BGR).")

    h, w, c = image.shape  # Height, width, channels
    ph, pw = pool_size  # Pooling height & width

    # Ensure dimensions are divisible by pool size
    new_h, new_w = h // ph, w // pw
    pooled_image = np.zeros((new_h, new_w, c), dtype=np.uint8)

    for ch in range(c):  # Loop over each channel (R, G, B)
        for i in range(0, h, ph):
            for j in range(0, w, pw):
                patch = image[i:i+ph, j:j+pw, ch]  # Extract 2×2 patch for channel `ch`

                # Use your approximate adder function
                #pooled_value = Aprx_adder(patch[0, 0], patch[0, 1], patch[1, 0], patch[1, 1])
                pooled_value = Aprx_propose_adder_1(patch[0, 0], patch[0, 1], patch[1, 0], patch[1, 1])
                pooled_image[i//ph, j//pw, ch] = pooled_value

    return pooled_image


# Load the original image
image = Input_image

# Perform pooling
pool_size = (2, 2)
exact_pooled_image = exact_average_pooling_color(image, pool_size)
approx_pooled_image = approximate_average_pooling_color(image, pool_size)

# Display images
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(image)
plt.title("Original Image")
plt.axis("ON")

plt.subplot(1, 3, 2)
plt.imshow(exact_pooled_image)
plt.title("Exact Average Pooling")
plt.axis("ON")

plt.subplot(1, 3, 3)
plt.imshow(approx_pooled_image)
plt.title("Approximate Average Pooling")
plt.axis("ON")

plt.show()
