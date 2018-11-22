from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy


def plot_coils(coils, out="coils.pdf"):
    fig = pyplot.figure(figsize=(16, 12))
    ax1 = fig.add_subplot(221, projection="3d")
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(224)

    phi = numpy.linspace(0, 2 * numpy.pi, 1000)
    for coil in coils:
        x = coil.radius * numpy.cos(phi)
        y = coil.radius * numpy.sin(phi)
        z = coil.pos_z

        ax1.plot(x, y, z, "-", lw=coil.num_turns / 10, color=coil.color)
        ax2.plot(x, y, "-", lw=coil.num_turns / 10, color=coil.color)
        ax3.plot(x, [z] * len(x), "-", lw=coil.num_turns / 10, color=coil.color)

    ax3.set_ylim(ax3.get_xlim())
    
    ax1.set_xlabel(r"$x$", fontsize=30)
    ax1.set_ylabel(r"$y$", fontsize=30)
    ax1.set_zlabel(r"$z$", fontsize=30)

    ax2.set_xlabel(r"$x$", fontsize=30)
    ax2.set_ylabel(r"$y$", fontsize=30)

    ax3.set_xlabel(r"$x$", fontsize=30)
    ax3.set_ylabel(r"$z$", fontsize=30)

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    ax3.set_aspect("equal")


    pyplot.tight_layout()
    pyplot.savefig(out)
    pyplot.close()

