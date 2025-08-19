# Portraitpy

This is a matplotlib wrapper for generating portrait or Gleckler plots (Gleckler et al., 2008).

| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![Code Coverage Status][codecov-badge]][codecov-link] [![pre-commit.ci status][pre-commit.ci-badge]][pre-commit.ci-link] |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **License** |                                                                         [![License][license-badge]][repo-link]                                                                         |

## Usage

First we generate the data we want to visualize:

```python
import numpy as np
from portraitpy import portrait_plot

shape = (6, 4, 4)  # shape: (rows, columns, 4 triangles)
data = np.arange(np.prod(shape)).reshape(shape)
```

Then we can either visualize the data directly:

```python
result = portrait_plot(
    data,
    edgecolors="k",
    cmap="viridis",
    add_colorbar=True,
    legend_title="Legend",
    legend_labels=["A", "B", "C", "D"],
)

# Access individual components
collection = result['collection']  # The main PolyCollection
ax = result['ax']                  # The main Axes
fig = result['fig']                # The Figure
cbar = result['cbar']              # The Colorbar (if created)
legend_ax = result['legend_ax']    # The legend Axes (if created)
```

Or we visualize colors explicitly:

```python
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

norm = Normalize(vmin=0, vmax=np.max(data))
cmap = plt.get_cmap("plasma")
colors = cmap(norm(data))

result = portrait_plot(
    colors,
    edgecolors="k",
    legend_title="Legend",
    legend_labels=["A", "B", "C", "D"],
)
```

We can also do this with only 2 triangles per tile:

```python
shape = (6, 4, 2)  # shape: (rows, columns, 2 triangles)
data = np.arange(np.prod(shape)).reshape(shape)

result = portrait_plot(
    data,
    edgecolors="k",
    cmap="viridis",
    add_colorbar=True,
    legend_title="Legend",
    legend_labels=["A", "B"],
)
```

You can also control the colormap scaling with `vmin` and `vmax`:

```python
# Create a portrait plot with fixed color scaling
result = portrait_plot(
    data,
    edgecolors="k",
    cmap="RdBu_r",  # A diverging colormap
    add_colorbar=True,
    vmin=-10,       # Minimum value for colormap
    vmax=10,        # Maximum value for colormap
    legend_title="Legend",
    legend_labels=["A", "B"],
)
```

You can also provide your own axes to plot on:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
result = portrait_plot(
    data,
    ax=ax,
    add_colorbar=True,
    cbar_kwargs={'label': 'Values'},
)
fig.suptitle('My Custom Portrait Plot')
plt.tight_layout()
plt.show()
```

## Customization

The `portrait_plot` function accepts several parameters for customization:

- `figsize`: Tuple of (width, height) in inches for the figure (when creating a new figure)
- `cmap`: Colormap for the plot (e.g., 'viridis', 'plasma', etc.)
- `add_colorbar`: Whether to display a colorbar
- `cbar_kwargs`: Dictionary of keyword arguments passed to `fig.colorbar()`
- `legend_title`: Title for the legend inset
- `legend_labels`: List of labels for the legend inset (must match the number of triangles)
- `legend_kwargs`: Dictionary of keyword arguments for the legend inset
- `vmin`, `vmax`: Minimum and maximum values for colormap scaling (only used for 3D arrays)

The `legend_kwargs` parameter is custom and takes `width`, `height`, `x0`, and `y0` keys for positioning, while `cbar_kwargs` can carry additional keys which are passed to `plt.colorbar()`.

## References

Gleckler, P. J., K. E. Taylor, and C. Doutriaux (2008), Performance metrics for climate models, J. Geophys. Res., 113, D06104, doi:10.1029/2007JD008972.

[github-ci-badge]: https://img.shields.io/github/actions/workflow/status/ATMO-IUP-UHEI/portraitpy/ci.yaml?branch=main
[github-ci-link]: https://github.com/ATMO-IUP-UHEI/portraitpy/actions?query=workflow%3ACI
[codecov-badge]: https://img.shields.io/codecov/c/github/ATMO-IUP-UHEI/portraitpy.svg?logo=codecov
[codecov-link]: https://codecov.io/gh/ATMO-IUP-UHEI/portraitpy
[license-badge]: https://img.shields.io/github/license/ATMO-IUP-UHEI/portraitpy
[repo-link]: https://github.com/ATMO-IUP-UHEI/portraitpy
[pre-commit.ci-badge]: https://results.pre-commit.ci/badge/github/ATMO-IUP-UHEI/portraitpy/main.svg
[pre-commit.ci-link]: https://results.pre-commit.ci/latest/github/ATMO-IUP-UHEI/portraitpy/main
