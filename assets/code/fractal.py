import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def julia_set(width, height, x_min, x_max, y_min, y_max, c, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    image = np.zeros(Z.shape, dtype=float)

    for _ in range(max_iter):
        Z = Z**2 + c
        mask = np.abs(Z) < 1000
        image += mask

    return image


def plot_julia_set(image, x_min, x_max, y_min, y_max):
    plt.imshow(image, cmap="viridis", extent=(x_min, x_max, y_min, y_max))
    plt.colorbar()
    plt.title("Julia Set")
    plt.xlabel("Real")
    plt.ylabel("Imaginary")
    plt.show()


def save_julia_set(image, file_path, cmap="viridis"):
    norm_image = (image - np.min(image)) / (np.max(image) - np.min(image))
    rgba_image = plt.get_cmap(cmap)(norm_image)
    rgb_array = (rgba_image[:, :, :3] * 255).astype(np.uint8)
    Image.fromarray(rgb_array).save(file_path)


if __name__ == "__main__":
    width, height = 6400, 6400
    x_min, x_max = -2, 2
    y_min, y_max = -2, 2
    c = -0.8 + 0.156j  # changeable constant for different Julia sets
    max_iter = 100

    julia_image = julia_set(width, height, x_min, x_max, y_min, y_max, c, max_iter)
    save_julia_set(julia_image, "julia_set.png")
    # plot_julia_set(julia_image, x_min, x_max, y_min, y_max)
