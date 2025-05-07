import numpy as np

from portraitpy._triangulation import (
    _generate_four_triangles,
    _generate_two_triangles,
    _make_triangulation,
)


def test_generate_two_triangles_1x1():
    # 1×1 grid → 4 points, 2 triangles
    tris = _generate_two_triangles(1, 1)
    expected = np.array([[0, 1, 2], [2, 1, 3]])
    assert tris.shape == (2, 3)
    assert np.array_equal(tris, expected)


def test_generate_two_triangles_2x2():
    # 2×2 grid → (3×3)=9 points, 2*2*2=8 triangles
    tris = _generate_two_triangles(2, 2)
    # build expected manually
    exp = []
    for i in range(2):
        for j in range(2):
            p0 = i * 3 + j
            p1 = p0 + 1
            p2 = p0 + 3
            p3 = p2 + 1
            exp += [[p0, p1, p2], [p2, p1, p3]]
    exp = np.array(exp)
    assert tris.shape == (8, 3)
    assert np.array_equal(tris, exp)


def test_generate_four_triangles_1x1():
    # start with the 4 cell corners
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    tris, new_pts = _generate_four_triangles(1, 1, points.copy())
    # should append center at index 4
    assert new_pts.shape == (5, 2)
    assert np.allclose(new_pts[4], [0.5, 0.5])
    # expected 4 triangles around the center
    expected = np.array(
        [
            [0, 1, 4],
            [1, 3, 4],
            [3, 2, 4],
            [2, 0, 4],
        ]
    )
    assert tris.shape == (4, 3)
    assert np.array_equal(tris, expected)


def test_make_triangulation_two_triangles_preserves_points():
    # dummy points array
    pts = np.arange(6 * 2).reshape(6, 2).astype(float)
    tris, out_pts = _make_triangulation(2, 2, 2, pts)
    # for 2 triangles, points should be unchanged
    assert np.shares_memory(out_pts, pts) or np.array_equal(out_pts, pts)
    # triangles must match generate_two_triangles
    expected = _generate_two_triangles(2, 2)
    assert np.array_equal(tris, expected)


def test_make_triangulation_four_triangles_consistency():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    tris1, pts1 = _make_triangulation(1, 1, 4, points.copy())
    tris2, pts2 = _generate_four_triangles(1, 1, points.copy())
    # check triangles and points match the helper
    assert np.array_equal(tris1, tris2)
    assert np.array_equal(pts1, pts2)
