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
portrait_plot(
    data,
    edgecolors = "k",
    cmap = "viridis",
    add_colorbar = True,
    legend_title = "Legend",
    legend_labels = ["A", "B", "C", "D"],
)
```

Or we visualize colors explicitely

```python
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

norm = Normalize(vmin=0, vmax=np.max(data))
cmap = plt.get_cmap("plasma")
colors = cmap(norm(data))

portrait_plot(
    colors,
    edgecolors = "k",
    legend_title = "Legend",
    legend_labels = ["A", "B", "C", "D"],
)
```

We can also do this with only 2 triangles per tile:

```python
shape = (6, 4, 2)  # shape: (rows, columns, 2 triangles)
data = np.arange(np.prod(shape)).reshape(shape)

portrait_plot(
    data,
    edgecolors = "k",
    cmap = "viridis",
    add_colorbar = True,
    legend_title = "Legend",
    legend_labels = ["A", "B"],
)
```

Legend and colorbar can be customized with `legend_kwargs` and `cbar_kwargs`.
The `legend_kwargs` parameter is custom and takes `width` and `height` keys, while `cbar_kwargs` can carry additional keys which are passed to `plt.colorbar`.

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
