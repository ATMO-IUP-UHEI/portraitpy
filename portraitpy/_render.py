import numpy as np
from matplotlib import rcParams, tri
from matplotlib.collections import PolyCollection

from ._triangulation import _make_triangulation


def _draw_main_mesh(ax, points, triangles, array, rgba, cmap, linewidth, **kwargs):
    """private: Draw the triangulated mesh.
    Draw the main portrait mesh, either with explicit RGBA facecolors or via tripcolor.
    """
    triang = tri.Triangulation(points[:, 0], points[:, 1], triangles)
    if rgba is not None:
        facecolors = array.reshape(-1, 4)
        verts = [points[tri] for tri in triangles]
        tpc = PolyCollection(verts, facecolors=facecolors, linewidths=linewidth, **kwargs)
        ax.add_collection(tpc)
    else:
        tpc = ax.tripcolor(triang, array.flatten(), cmap=cmap, linewidth=linewidth, **kwargs)
    return tpc


def _draw_legend(ax, labels, title, ntris, linewidth, **kwargs):
    """Private: Draw the legend inset.
    Draw the legend showing a 1×1 cell subdivided into ntris, with optional labels and title.
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


def _draw_colorbar_inset(fig, tpc, cax=None, **kwargs):
    """Private: Draw a colorbar inset.
    If legend is present, place it to the right of the legend inset; otherwise attach to main Axes.
    """
    kwargs.pop('width', None)
    kwargs.pop('height', None)
    if cax is not None:
        return fig.colorbar(tpc, cax=cax, **kwargs)
    else:
        return fig.colorbar(tpc, **kwargs)
