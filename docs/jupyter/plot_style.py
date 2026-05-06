from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt


SCALABLE_DEFAULT_RCPARAMS = [
    # axes geometry
    "axes.titlepad",
    "axes.labelpad",

    # tick padding
    "xtick.major.pad",
    "ytick.major.pad",
    "xtick.minor.pad",
    "ytick.minor.pad",

    # tick geometry
    "xtick.major.size",
    "ytick.major.size",
    "xtick.minor.size",
    "ytick.minor.size",
    "xtick.major.width",
    "ytick.major.width",
    "xtick.minor.width",
    "ytick.minor.width",

    # legend geometry
    "legend.borderpad",
    "legend.labelspacing",
    "legend.handlelength",
    "legend.handleheight",
    "legend.handletextpad",
    "legend.borderaxespad",
    "legend.columnspacing",

    # patches and special artists
    "patch.linewidth",
    "hatch.linewidth",
    "errorbar.capsize",

    # boxplots
    "boxplot.boxprops.linewidth",
    "boxplot.capprops.linewidth",
    "boxplot.flierprops.linewidth",
    "boxplot.flierprops.markersize",
    "boxplot.meanprops.linewidth",
    "boxplot.meanprops.markersize",
    "boxplot.medianprops.linewidth",
    "boxplot.whiskerprops.linewidth",
]


def _scale_default_rcparams(names, scale):
    """return selected matplotlib default rcParams multiplied by scale."""
    return {
        name: mpl.rcParamsDefault[name] * scale
        for name in names
    }


def set_pub_style(width_fraction=1.0, view_scale=1.0, columns=1, height_ratio=0.618):
    """
    set matplotlib defaults for publication-style figures.

    Parameters
    ----------
    width_fraction : float
        fraction of the target LaTeX text or column width.
    view_scale : float
        multiplier applied to figure size, fonts, linewidths, markers, and common
        point-based spacing parameters for comfortable viewing and editing. use
        values larger than 1 while developing figures, especially small
        two-column figures. for final manuscript export, use view_scale=1.0 and
        insert the saved PDF into LaTeX at the matching target width, e.g.
        \\includegraphics[width=0.9\\textwidth]{...} for width_fraction=0.9 in
        a one-column figure, or
        \\includegraphics[width=1.0\\columnwidth]{...} for width_fraction=1.0
        in a two-column figure.
    columns : int
        use 1 for full text width or 2 for one column in a two-column layout.
    height_ratio : float
        figure height as a fraction of figure width.

    Returns
    -------
    style : dict
        dictionary containing PDF metadata and the effective style values used.
    """

    total_text_width_cm = 15.0

    if columns == 2:
        col_width_cm = (total_text_width_cm - 0.5) / 2
    else:
        col_width_cm = total_text_width_cm

    true_width_in = (col_width_cm * width_fraction) / 2.54
    view_width_in = true_width_in * view_scale
    view_height_in = view_width_in * height_ratio

    base_font = 11 * view_scale
    small_font = 9 * view_scale
    large_font = 14 * view_scale

    axis_line_width = 1.0 * view_scale
    grid_line_width = 0.5 * view_scale
    plot_line_width = 1.5 * view_scale
    marker_size = 4.0 * view_scale

    scaled_default_params = _scale_default_rcparams(
        SCALABLE_DEFAULT_RCPARAMS,
        view_scale,
    )

    scaled_style_params = {
        "axes.linewidth": axis_line_width,
        "grid.linewidth": grid_line_width,
        "lines.linewidth": plot_line_width,
        "lines.markersize": marker_size,
    }

    params = {
        "figure.figsize": (view_width_in, view_height_in),

        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Noto Sans", "DejaVu Sans", "Helvetica"],
        "font.size": base_font,

        "axes.labelsize": base_font,
        "axes.titlesize": large_font,

        "xtick.labelsize": small_font,
        "ytick.labelsize": small_font,

        "legend.fontsize": small_font,

        "mathtext.fontset": "stix",

        "pdf.fonttype": 42,
        "ps.fonttype": 42,

        "figure.autolayout": False,

        **scaled_default_params,
        **scaled_style_params,
    }

    plt.rcParams.update(params)

    metadata = {
        "Creator": "",
        "Producer": "",
        "CreationDate": datetime(2000, 1, 1),
    }

    style = {
        "metadata": metadata,
        "font": {
            "small": small_font,
            "base": base_font,
            "large": large_font,
        },
        "line": {
            "axis": axis_line_width,
            "grid": grid_line_width,
            "plot": plot_line_width,
        },
        "marker": {
            "size": marker_size,
        },
        "figure": {
            "true_width_in": true_width_in,
            "view_width_in": view_width_in,
            "view_height_in": view_height_in,
            "width_fraction": width_fraction,
            "height_ratio": height_ratio,
            "columns": columns,
            "view_scale": view_scale,
        },
        "rcparams": params,
    }

    return style


def print_scaled_rcparams():
    """print rcParams intentionally scaled by set_pub_style."""
    for name in SCALABLE_DEFAULT_RCPARAMS:
        print(f"{name}: {plt.rcParams[name]}")