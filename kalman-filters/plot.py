import matplotlib.pyplot as plt


def plot_kalman(
    true_values: list[float],
    measurements: list[float],
    estimates: list[float],
    title: str = "Kalman Filter",
    ylabel: str = "Value",
) -> None:
    steps = range(1, len(measurements) + 1)

    plt.figure(figsize=(10, 4))
    plt.plot(steps, true_values, label="True position", color="green", linewidth=2)
    plt.scatter(steps, measurements, label="GPS measurement", color="red", zorder=3, s=30)
    plt.plot(steps, estimates, label="KF estimate", color="blue", linewidth=2)

    plt.xlabel("Time step (s)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()
