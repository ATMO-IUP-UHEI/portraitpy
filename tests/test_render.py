import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection

from portraitpy._render import _draw_legend, _draw_main_mesh
from portraitpy._triangulation import _generate_two_triangles


def make_grid(nrows, ncols):
    # reproduce meshgrid logic from portrait_plot
    x, y = np.meshgrid(np.arange(ncols + 1), np.arange(nrows + 1))
    x, y = x - 0.5, y - 0.5
    pts = np.column_stack([x.ravel(), y.ravel()])
    tris = _generate_two_triangles(nrows, ncols)
    return pts, tris


def test_draw_main_mesh_rgba():
    fig, ax = plt.subplots()
    pts, tris = make_grid(1, 1)
    # two triangles per cell, RGBA per triangle
    data = np.array([[[[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]]]])
    # reshape to (1,1,2,4)
    tpc = _draw_main_mesh(
        ax, pts, tris, data, rgba=4, cmap=None, linewidth=0.1, vmin=None, vmax=None
    )
    assert isinstance(tpc, PolyCollection)
    # two triangles → two facecolors
    facecolors = tpc.get_facecolors()
    assert facecolors.shape[0] == 2
    # check first is red, second is green
    assert np.allclose(facecolors[0], [1.0, 0.0, 0.0, 1.0])
    assert np.allclose(facecolors[1], [0.0, 1.0, 0.0, 1.0])


def test_draw_main_mesh_colormap():
    fig, ax = plt.subplots()
    pts, tris = make_grid(1, 1)
    # data per triangle
    data = np.array([[[0.2, 0.8]]])  # shape (1,1,2)
    tpc = _draw_main_mesh(
        ax, pts, tris, data, rgba=None, cmap='viridis', linewidth=0.2, vmin=None, vmax=None
    )
    # tripcolor returns a QuadMesh or PolyCollection-like mappable with .get_array()
    arr = tpc.get_array()
    assert np.allclose(arr, data.flatten())


def test_draw_legend_no_labels_or_title():
    fig, ax = plt.subplots()
    # draw legend inset with no labels/title
    _draw_legend(ax, labels=None, title=None, ntris=2, linewidth=0.3, edgecolors='black')
    # should contain one PolyCollection with two patches
    cols = [c for c in ax.collections if isinstance(c, PolyCollection)]
    assert len(cols) == 1
    poly = cols[0]
    assert len(poly.get_paths()) == 2
    # no text or title
    assert len(ax.texts) == 0
    assert ax.get_title() == ''


def test_draw_legend_with_labels_and_title():
    fig, ax = plt.subplots()
    labels = ['A', 'B', 'C', 'D']
    title = 'MyLegend'
    _draw_legend(ax, labels=labels, title=title, ntris=4, linewidth=0.4)
    # texts for each label
    txts = [t.get_text() for t in ax.texts]
    assert set(txts) == set(labels)
    # title matches
    assert ax.get_title() == title
