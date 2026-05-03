import logging
import random

from kalman import KalmanFilter
from plot import plot_kalman

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# GPS accuracy for a typical consumer module is roughly ±3–5 m (1-sigma)
GPS_NOISE_STD = 4.0   # metres
VELOCITY = 5.0        # m/s northward
DT = 1.0              # seconds per step
STEPS = 20


def main() -> None:
    kf = KalmanFilter(
        # This 1D filter has no velocity state, so every real position change
        # looks like "process noise". Setting Q = (v*dt)^2 keeps the filter
        # responsive enough to track movement.
        process_variance=(VELOCITY * DT) ** 2,
        measurement_variance=GPS_NOISE_STD ** 2,
        initial_estimate=0.0,
    )

    logger.info("Simulating drone flying north at %.1f m/s — GPS noise std=%.1f m", VELOCITY, GPS_NOISE_STD)
    logger.info("%-6s  %-14s  %-14s  %-14s", "Step", "True pos (m)", "GPS (m)", "KF est (m)")
    logger.info("-" * 54)

    true_positions, gps_readings, estimates = [], [], []

    random.seed(7)
    for i in range(1, STEPS + 1):
        true_pos = VELOCITY * DT * i
        gps = true_pos + random.gauss(0, GPS_NOISE_STD)
        estimate = kf.update(gps)

        logger.info("%-6d  %-14.2f  %-14.2f  %-14.2f", i, true_pos, gps, estimate)

        true_positions.append(true_pos)
        gps_readings.append(gps)
        estimates.append(estimate)

    plot_kalman(
        true_positions,
        gps_readings,
        estimates,
        title="Kalman Filter — UAV north position (constant velocity, noisy GPS)",
        ylabel="Position north (m)",
    )


if __name__ == "__main__":
    main()
