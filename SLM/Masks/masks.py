import numpy as np

def CheckersBoard(nsquares=4, npixels=10, size=(1024, 768)):
    """Plots a two dimensional checkers board.

    Args:
        -> nsquares (int, optional): Number of squared places. Defaults to 4.
        -> npixels (int, optional): Number of pixels for the width and height of the squared places. Defaults to 10.
        -> size (tuple, optional): Tuple of ints describing the dimensions of the SLM. Defaults to (1024, 768).
    Returns:
        mask: Checkers board(array)
    """
    mask = np.zeros(size)

    aoi = np.kron([[1, 0] * nsquares, [0, 1] * nsquares] * nsquares, np.ones((npixels, npixels)))

    dim = nsquares*npixels*2

    mask[int(size[0]/2)-int(dim/2):int(size[0]/2)+int(dim/2), int(size[1]/2)-int(dim/2):int(size[1]/2)+int(dim/2)] = aoi

    return mask
