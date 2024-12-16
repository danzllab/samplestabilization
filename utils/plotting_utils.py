def clean_axes(axes, x_lim=(0, 10), y_lim=(0, 2), font_size=6):
    xlabel = axes.get_xlabel()
    ylabel = axes.get_ylabel()
    axes.clear()
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_ylim(*y_lim)
    axes.set_xlim(*x_lim)
    for label in axes.get_xticklabels() + axes.get_yticklabels():
        label.set_fontsize(font_size)

    # Major grid lines
    axes.grid(True, which="major", linestyle="-", linewidth="0.5", color="black")

    # Minor grid lines
    axes.minorticks_on()
    axes.grid(True, which="minor", linestyle=":", linewidth="0.5", color="gray")
