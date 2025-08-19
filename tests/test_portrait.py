import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.collections import PolyCollection

from portraitpy.portrait import portrait_plot


def test_plot_two_triangles_default():
    # 1×1 grid, two triangles, default cmap, no legend, no colorbar
    data = np.array([[[0.2, 0.8]]])  # shape (1,1,2)
    result = portrait_plot(data)
    tpc = result['collection']
    # tripcolor → PolyCollection with array property
    assert isinstance(tpc, PolyCollection)
    arr = tpc.get_array()
    assert np.allclose(arr, data.flatten())


def test_plot_rgba_facecolors():
    # 1×1 grid, two triangles, explicit RGBA colors
    rgba = np.array([[[[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]]]])  # (1,1,2,4)
    result = portrait_plot(rgba)
    tpc = result['collection']
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
    result = portrait_plot(data, ax=ax, legend_labels=labels, legend_title=title)

    # Check that we have a legend_ax in the result
    assert result['legend_ax'] is not None

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
    result = portrait_plot(data, ax=ax, add_colorbar=True)

    # Check that we have a cbar and cbar_ax in the result
    assert result['cbar'] is not None
    assert result['cbar_ax'] is not None

    # adds one colorbar axis
    assert len(fig.axes[0].child_axes) == before + 1


def test_colorbar_and_legend():
    data = np.array([[[0.4, 0.6]]])
    fig = plt.figure()
    ax = fig.add_subplot()
    result = portrait_plot(
        data, ax=ax, legend_labels=['A', 'B'], legend_title='L', add_colorbar=True
    )

    # Check all the expected components are in the result
    assert result['collection'] is not None
    assert result['ax'] is ax
    assert result['fig'] is fig
    assert result['legend_ax'] is not None
    assert result['cbar_ax'] is not None
    assert result['cbar'] is not None

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


def test_figure_created_when_no_ax_provided():
    # When no ax is provided, a new figure should be created
    data = np.array([[[0.2, 0.8]]])
    result = portrait_plot(data)
    assert result['fig'] is not None
    assert result['ax'] is not None


def test_figsize_parameter():
    # Test that the figsize parameter works
    data = np.array([[[0.2, 0.8]]])
    figsize = (10, 5)
    result = portrait_plot(data, figsize=figsize)
    fig = result['fig']

    # The exact size may vary slightly due to DPI and other factors
    # and portrait_plot prioritizes the height, not the width
    # so we just check the height is approximately right
    assert abs(fig.get_figheight() - figsize[1]) < 1


def test_vmin_vmax_parameters():
    # Test that vmin and vmax are passed to the collection
    data = np.array([[[0.3, 0.7]]])
    vmin, vmax = 0.2, 0.8

    # Create plot with vmin and vmax
    result = portrait_plot(data, vmin=vmin, vmax=vmax)
    collection = result['collection']

    # Check that the collection has the correct clim values
    assert collection.get_clim()[0] == vmin
    assert collection.get_clim()[1] == vmax
