import numpy as np
from matplotlib import rcParams, tri
from matplotlib.collections import PolyCollection

from ._triangulation import _make_triangulation


def _draw_main_mesh(
    ax, points, triangles, array, rgba, cmap, linewidth, vmin=None, vmax=None, **kwargs
):
    """Draw the triangulated mesh.

    Draw the main portrait mesh, either with explicit RGBA facecolors or via tripcolor.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the mesh
    points : numpy.ndarray
        Array of points coordinates with shape (n_points, 2)
    triangles : numpy.ndarray
        Array of triangle indices with shape (n_triangles, 3)
    array : numpy.ndarray
        The data array with shape matching triangles
    rgba : int or None
        If not None, the last dimension of array contains RGBA values
    cmap : str or matplotlib.colors.Colormap
        Colormap to use for the plot if rgba is None
    linewidth : float
        Width of the lines between triangles
    vmin : Optional[float]
        The minimum value for color mapping
    vmax : Optional[float]
        The maximum value for color mapping
    **kwargs : dict
        Additional keyword arguments to pass to PolyCollection or tripcolor.
        For tripcolor, common options include 'vmin', 'vmax', 'norm', 'alpha', etc.

    Returns
    -------
    matplotlib.collections.PolyCollection or matplotlib.tri.TriMesh
        The collection or mesh object created
    """
    triang = tri.Triangulation(points[:, 0], points[:, 1], triangles)
    if rgba is not None:
        facecolors = array.reshape(-1, 4)
        verts = [points[tri] for tri in triangles]
        tpc = PolyCollection(verts, facecolors=facecolors, linewidths=linewidth, **kwargs)
        ax.add_collection(tpc)
    else:
        # Pass along vmin, vmax and other kwargs to tripcolor
        tpc = ax.tripcolor(
            triang, array.flatten(), cmap=cmap, linewidth=linewidth, vmin=vmin, vmax=vmax, **kwargs
        )
    return tpc


def _draw_legend(ax, labels, title, ntris, linewidth, **kwargs):
    """Draw the legend inset.

    Draw the legend showing a 1×1 cell subdivided into ntris, with optional labels and title.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the legend
    labels : list of str
        The labels to add to each triangle in the legend
    title : str or None
        Title for the legend
    ntris : int
        Number of triangles to draw (2 or 4)
    linewidth : float
        Width of the lines between triangles
    **kwargs : dict
        Additional keyword arguments passed to PolyCollection

    Returns
    -------
    matplotlib.collections.PolyCollection
        The collection object created for the legend
    """
    labels = labels or []
    title = title or ''
    kwargs.pop('width', None)
    kwargs.pop('height', None)

    # build a tiny 2×2 grid around (0,0)
    x, y = np.meshgrid(np.arange(2), np.arange(2))
    pts = np.column_stack([x.ravel() - 0.5, y.ravel() - 0.5])
    triangles, pts = _make_triangulation(1, 1, ntris, pts)

    # draw the white triangles
    verts = [pts[tri] for tri in triangles]
    pc = PolyCollection(
        verts,
        facecolors=kwargs.pop('facecolors', ['white'] * ntris),
        linewidths=linewidth,
        **kwargs,
    )
    ax.add_collection(pc)

    # add labels
    for i, txt in enumerate(labels):
        vert = pts[triangles[i]]
        cx, cy = vert[:, 0].mean(), vert[:, 1].mean()
        ax.text(cx, cy, txt, fontsize=8, ha='center', va='center')

    if title:
        ax.set_title(title, fontsize=rcParams['legend.fontsize'], ha='center')

    ax.set_aspect('equal')
    ax.set_xlim(-0.51, 0.51)
    ax.set_ylim(-0.51, 0.51)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    return pc


def _draw_colorbar_inset(fig, tpc, cax=None, **kwargs):
    """Private: Draw a colorbar inset.

    If legend is present, place it to the right of the legend inset;
    otherwise attach to main Axes.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to which the colorbar will be added
    tpc : matplotlib.collections.PolyCollection or matplotlib.collections.QuadMesh
        The artist to create a colorbar for
    cax : matplotlib.axes.Axes, optional
        The axes for the colorbar. If None, a new axes will be created.
    **kwargs : dict
        Additional keyword arguments to pass to fig.colorbar

    Returns
    -------
    matplotlib.colorbar.Colorbar
        The created colorbar object
    """
    kwargs.pop('width', None)
    kwargs.pop('height', None)
    if cax is not None:
        return fig.colorbar(tpc, cax=cax, **kwargs)
    else:
        return fig.colorbar(tpc, **kwargs)
