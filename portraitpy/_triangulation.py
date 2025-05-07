import numpy as np


def _generate_four_triangles(nrows, ncols, points):
    """Private: Generate four triangles for each cell in a grid.
    Each triangle is represented by three vertices (corners of the cell).
    """
    triangles = []
    for i in range(nrows):
        for j in range(ncols):
            # corners and center starting with top left corner
            # p0 = top left, p1 = top right, p2 = bottom left, p3 = bottom right
            p0 = i * (ncols + 1) + j
            p1 = p0 + 1
            p2 = p0 + (ncols + 1)
            p3 = p2 + 1
            pc = len(points)
            # Add center point
            xc = (points[p0, 0] + points[p3, 0]) / 2
            yc = (points[p0, 1] + points[p3, 1]) / 2
            points = np.vstack([points, [xc, yc]])

            # Add four triangles: TL, TR, BR, BL
            triangles += [[p0, p1, pc], [p1, p3, pc], [p3, p2, pc], [p2, p0, pc]]
    return np.array(triangles), points


def _generate_two_triangles(nrows, ncols):
    """Private: Generate two triangles for each cell in a grid.
    Each triangle is represented by three vertices (corners of the cell).
    """
    triangles = []
    for i in range(nrows):
        for j in range(ncols):
            # corners and center starting with top left corner
            # p0 = top left, p1 = top right, p2 = bottom left, p3 = bottom right
            p0 = i * (ncols + 1) + j
            p1 = p0 + 1
            p2 = p0 + (ncols + 1)
            p3 = p2 + 1

            # Add two triangles: TL, BR
            triangles += [[p0, p1, p2], [p2, p1, p3]]
    return np.array(triangles)


def _make_triangulation(nrows, ncols, ntris, points):
    """Private: Generate triangles and updated points for a grid."""
    if ntris == 4:
        return _generate_four_triangles(nrows, ncols, points)
    # for 2 triangles we do not add new points
    return _generate_two_triangles(nrows, ncols), points
