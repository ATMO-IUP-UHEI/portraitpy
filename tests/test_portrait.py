import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.collections import PolyCollection

from portraitpy.portrait import portrait_plot


def test_plot_two_triangles_default():
    # 1×1 grid, two triangles, default cmap, no legend, no colorbar
    data = np.array([[[0.2, 0.8]]])  # shape (1,1,2)
    tpc = portrait_plot(data)
    # tripcolor → PolyCollection with array property
    assert isinstance(tpc, PolyCollection)
    arr = tpc.get_array()
    assert np.allclose(arr, data.flatten())


def test_plot_rgba_facecolors():
    # 1×1 grid, two triangles, explicit RGBA colors
    rgba = np.array([[[[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]]]])  # (1,1,2,4)
    tpc = portrait_plot(rgba)
    assert isinstance(tpc, PolyCollection)
    fc = tpc.get_facecolors()
    assert fc.shape[0] == 2
    assert np.allclose(fc[0], [1.0, 0.0, 0.0, 1.0])
    assert np.allclose(fc[1], [0.0, 1.0, 0.0, 1.0])


def test_legend_inset_added_and_labeled():
    data = np.array([[[0.1, 0.9]]])
    fig = plt.figure()
    ax = fig.add_subplot()
    labels = ['Low', 'High']
    title = 'Intensity'
    portrait_plot(data, ax=ax, legend_labels=labels, legend_title=title)
    # main axes + legend inset axes
    assert len(fig.axes[0].child_axes) == 1
    inset = fig.axes[0].child_axes[0]
    # check title and texts
    assert inset.get_title() == title
    txts = [t.get_text() for t in inset.texts]
    assert set(txts) == set(labels)


def test_colorbar_only():
    data = np.array([[[0.3, 0.7]]])
    fig = plt.figure()
    ax = fig.add_subplot()
    before = len(fig.axes[0].child_axes)
    portrait_plot(data, ax=ax, add_colorbar=True)
    # adds one colorbar axis
    assert len(fig.axes[0].child_axes) == before + 1


def test_colorbar_and_legend():
    data = np.array([[[0.4, 0.6]]])
    fig = plt.figure()
    ax = fig.add_subplot()
    portrait_plot(data, ax=ax, legend_labels=['A', 'B'], legend_title='L', add_colorbar=True)
    # adds legend inset + colorbar axes
    assert len(ax.child_axes) == 2


@pytest.mark.parametrize(
    'shape',
    [
        (1, 1),  # 2D
        (1, 1, 3),  # invalid ntris
        (1, 1, 2, 3),  # 4D last dim != 4
    ],
)
def test_invalid_array_shape_raises(shape):
    arr = np.zeros(shape)
    with pytest.raises(ValueError):
        portrait_plot(arr)


def test_legend_label_length_mismatch():
    # ntris=2 but only one label → error
    data = np.array([[[0.5, 0.5]]])
    with pytest.raises(ValueError):
        portrait_plot(data, legend_labels=['only_one'])
