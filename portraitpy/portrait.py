from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.axes import Axes
from matplotlib.collections import PolyCollection
from matplotlib.gridspec import GridSpec

from ._render import _draw_colorbar_inset, _draw_legend, _draw_main_mesh
from ._triangulation import _make_triangulation


def _setup_axes(nrows, ncols, figheight, has_legend, has_cbar, legend_kwargs, cbar_kwargs):
    """Create figure, GridSpec and return fig, main ax, legend_ax, cbar_ax."""
    # compute overall figure size
    aspect = ncols / nrows
    legend_space = has_legend * (figheight * aspect / ncols)
    cbar_space = has_cbar * (figheight * cbar_kwargs.get('width', 0.07))
    pad = 0.02
    base_width = figheight * aspect
    fig_width = base_width + legend_space + cbar_space
    total_width = fig_width * (1 + pad * (has_legend + has_cbar))

    fig = plt.figure(
        figsize=(total_width, figheight),
        dpi=rcParams['figure.dpi'],
        layout='constrained',
    )

    # layout grid: columns = main + optional legend + optional cbar
    ncols_sub = 1 + has_legend + has_cbar
    # width ratios
    main_w = ncols
    cbar_w = cbar_kwargs.get('width', 0.07) * ncols
    legend_w = legend_kwargs.get('width', 1 / ncols) * ncols
    width_ratios = [main_w]
    if has_legend:
        width_ratios.append(legend_w)
    if has_cbar:
        width_ratios.append(cbar_w)

    # height ratios: small top row for legend, equal size to one row, whitespace below
    legend_frac = 1 / nrows
    height_ratios = [legend_frac, 1 - legend_frac]

    gs = GridSpec(
        2,
        ncols_sub,
        figure=fig,
        width_ratios=width_ratios,
        height_ratios=height_ratios,
    )
    gs.tight_layout(fig, h_pad=0, w_pad=f'{int(pad*100)}%')

    # assign subplots in order
    ax = fig.add_subplot(gs[:, 0])
    legend_ax = fig.add_subplot(gs[0, 1]) if has_legend else None
    cbar_ax = fig.add_subplot(gs[:, -1]) if has_cbar else None
    return fig, ax, legend_ax, cbar_ax


def _make_inset_axes(ax, ncols, legend_kwargs, kwargs):
    """Create inset axes for colorbar, positioned to the right of the legend."""
    legend_w = legend_kwargs.get('width', 1 / ncols)
    pad = 0.05
    x0 = kwargs.pop('x0', 1.04 + legend_w + pad)
    y0 = kwargs.pop('y0', 0)
    width = kwargs.pop('width', 0.07)
    height = kwargs.pop('height', 1)
    return ax.inset_axes([x0, y0, width, height], transform=ax.transAxes)


def portrait_plot(
    array: np.ndarray,
    ax: Optional[Axes] = None,
    figheight: Optional[float] = 6,
    cmap: Optional[str] = 'viridis',
    add_colorbar: Optional[bool] = False,
    cbar_kwargs: Optional[Dict[str, Any]] = None,
    legend_title: Optional[str] = None,
    legend_labels: Optional[List[str]] = None,
    legend_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> PolyCollection:
    """
    Create a portrait or Gleckler plot (cf. Gleckler, 2008) using matplotlib.

    Parameters
    ----------
    array : numpy.ndarray
        A 3D or 4D numpy array with shape (rows, cols, [2,4], 4).
        If 3D, the last dimension must be 2 or 4 (triangles per cell).
        If 4D, the last dimension must be 4 (RGBA).
    ax : matplotlib.axes.Axes, optional
        The axes on which to plot the portrait.
    figheight : float, optional
        The height of the figure in inches. Will be used if ax is None. The width is
        calculated based on the aspect ratio of the data and the existence of legend and cbar.
    cmap : str, optional
        The colormap to use for the plot if array is 3D. Default is 'viridis'.
    add_colorbar : bool, optional
        Whether to display a colorbar. Default is False.
    cbar_kwargs : dict, optional
        Additional keyword arguments to pass to the colorbar.
    legend_title : str, optional
        The title for the legend inset. Default is None.
    legend_labels : list of str, optional
        The labels for the legend inset. Must match the number of triangles.
    legend_kwargs : dict, optional
        Additional keyword arguments to pass to the legend inset.
    **kwargs : keyword arguments
        Additional keyword arguments to pass to the PolyCollection or tripcolor.

    Returns
    -------
    PolyCollection
        The PolyCollection object created for the plot.

    Raises
    ValueError
        If the input array does not have the correct shape or if the number of triangles
        does not match the number of labels in the legend.

    Notes
    -----
    The function generates a portrait plot using the provided array. It creates a triangulation
    of the points and colors the triangles based on the values in the array and the provided colormap.
    It also handles the case where the array is 4D (RGBA) and allows for customization of the plot
    through keyword arguments. The function can also display a colorbar and a legend for the triangles.
    If an Axes object is provided, legend and colorbar will be addes as child_axes using inset_axes.
    If no Axes is provided, a new figure and Axes will be created and the layout will be adjusted
    using GridSpec.

    Each of the squares in the grid is divided into triangles, and the color of each triangle
    is determined by the corresponding value in the array. The center of each square is 1-spaced
    and starts at (0,0). The y-axis is inverted to match the standard orientation of a grid.

    References
    ----------
    Gleckler, P. J., K. E. Taylor, and C. Doutriaux (2008), Performance metrics for climate models,
    J. Geophys. Res., 113, D06104, doi:10.1029/2007JD008972.
    """
    linewidth = kwargs.pop('linewidth', 0.3)
    kwargs.setdefault('edgecolors', 'black')
    cbar_kwargs = cbar_kwargs or {}
    legend_kwargs = legend_kwargs or {}

    rgba = None
    if array.ndim == 3:
        nrows, ncols, ntris = array.shape
    elif array.ndim == 4:
        nrows, ncols, ntris, rgba = array.shape
        if rgba != 4:
            raise ValueError('If array is 4D, the last dimension must be 4 (RGBA).')
    else:
        raise ValueError('Input array must be 3D or 4D with shape (rows, cols, [2,4], 4)')

    if ntris not in [2, 4]:
        raise ValueError('Only 2 or 4 triangles per cell are supported.')

    has_legend = bool(legend_labels or legend_title)
    has_cbar = add_colorbar

    # if no Axes passed in, build a figure+GridSpec
    has_axes = ax is not None
    if not has_axes:
        fig, ax, legend_ax, cbar_ax = _setup_axes(
            nrows,
            ncols,
            figheight,
            has_legend,
            has_cbar,
            legend_kwargs,
            cbar_kwargs,
        )
    else:
        fig = ax.figure
        legend_ax = None
        cbar_ax = None

    # Generate mesh points
    x, y = np.meshgrid(np.arange(ncols + 1), np.arange(nrows + 1))
    x, y = x - 0.5, y - 0.5
    points = np.column_stack([x.ravel(), y.ravel()])

    # build triangulation and draw main mesh
    triangles, points = _make_triangulation(nrows, ncols, ntris, points)
    tpc = _draw_main_mesh(ax, points, triangles, array, rgba, cmap, linewidth, **kwargs)

    # draw legend into its own Axes
    if has_legend:
        labels = legend_labels or []
        if len(labels) not in [ntris, 0]:
            raise ValueError(
                f'Number of legend labels ({len(labels)}) '
                f'must match number of triangles ({ntris}).'
            )
        if has_axes:
            width = legend_kwargs.get('width', 1 / ncols)
            height = legend_kwargs.get('height', 1 / nrows)
            x0 = legend_kwargs.get('x0', 1.04)
            y0 = legend_kwargs.get('y0', 1 - height)
            legend_ax = ax.inset_axes([x0, y0, width, height], transform=ax.transAxes)
        _draw_legend(legend_ax, labels, legend_title, ntris, linewidth, **kwargs)

    # draw colorbar into its own Axes
    if has_cbar:
        if has_axes:
            # compute inset position after legend (if present)
            cbar_ax = _make_inset_axes(ax, ncols, legend_kwargs, cbar_kwargs)
        # if axes were created via _setup_axes, cbar_ax is already set
        _draw_colorbar_inset(fig, tpc, cax=cbar_ax, **cbar_kwargs)

    # finalize main axes limits etc.
    ax.set_xlim(-0.51, ncols - 0.49)
    ax.set_ylim(-0.51, nrows - 0.49)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    return tpc
