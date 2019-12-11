import numpy as np
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt


# calculate 2-dimensional normal distribution with math. expectation at some point
def two_d_normal_distribution(shape: tuple, point: tuple, sigma):
    plane = np.zeros(shape, dtype=float)
    x, y = point
    plane[x, y] = 1
    return filters.gaussian_filter(plane, sigma)


# calculate intersection of distributions of one organization
def intersect_distributions(shape: tuple, points, deviations):
    fullone_plane = np.ones(shape, dtype=float)
    result = fullone_plane.copy()

    if np.size(deviations) == 1:
        temp = deviations
        deviations = np.zeros(len(points), dtype=float)
        deviations[:] = temp

    for point, sigma in zip(points, deviations):
        result *= fullone_plane - two_d_normal_distribution(shape, point, sigma)

    return fullone_plane - result


# calculate probability of how good is position
def get_distribution_in_points(distributions):
    fullone_plane = np.ones(distributions[0].shape, dtype=float)
    result = fullone_plane.copy()
    for d in distributions:
        result *= fullone_plane - d
    return fullone_plane - result


def get_distribution_in_region(plane, radius):
    N, M = plane.shape
    result = np.zeros((N, M), dtype=float)
    tmp = np.zeros((N + radius * 2, M + radius * 2), dtype=float)

    tmp[radius:N + radius, radius:M + radius] = plane

    k = np.zeros((radius * 2 + 1, radius * 2 + 1), dtype=float)
    k[radius, radius] = 1.0
    k = filters.gaussian_filter(k, radius / 2)

    for x in range(0, radius * 2 + 1):
        for y in range(0, radius * 2 + 1):
            if np.hypot(x - radius, y - radius) > radius:
                k[x, y] = 0.0

    for i in range(radius, N + radius):
        for j in range(radius, M + radius):
            result[i - radius, j - radius] = (tmp[i - radius:i + radius + 1, j - radius:j + radius + 1] * k).sum()

    return result


# Debug
# org1 = intersect_distributions((200, 200), [(50, 50), (100, 150), (170, 60)], 30)
# org2 = intersect_distributions((200, 200), [(100, 100)], 30)
#
# plt.imshow(get_distribution_in_points([org1, org2]))
# plt.gca().invert_yaxis()
# plt.imshow(two_d_normal_distribution((200, 200), (100, 100), 70))
# plt.show()
#
#
# plt.imshow(get_distribution_in_region(get_distribution_in_points([org1, org2]), 50))
# plt.gca().invert_yaxis()
# plt.show()
