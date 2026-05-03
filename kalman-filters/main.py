import logging
import random

from kalman import KalmanFilter1D, KalmanFilter2D
from plot import plot_kalman

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

GPS_NOISE_STD = 4.0
VELOCITY = 5.0
DT = 1.0
STEPS = 20


def main() -> None:
    kf1 = KalmanFilter1D(
        process_variance=(VELOCITY * DT) ** 2,
        measurement_variance=GPS_NOISE_STD ** 2,
        initial_estimate=0.0,
    )
    kf2 = KalmanFilter2D(
        dt=DT,
        process_variance=1.0,
        measurement_variance=GPS_NOISE_STD ** 2,
        initial_position=0.0,
        initial_velocity=0.0,
    )

    logger.info("Drone flying north at %.1f m/s — GPS noise std=%.1f m", VELOCITY, GPS_NOISE_STD)
    logger.info("%-6s  %-12s  %-12s  %-12s  %-12s", "Step", "True (m)", "GPS (m)", "1D est (m)", "2D est (m)")
    logger.info("-" * 62)

    true_positions, gps_readings, estimates_1d, estimates_2d = [], [], [], []

    random.seed(7)
    for i in range(1, STEPS + 1):
        true_pos = VELOCITY * DT * i
        gps = true_pos + random.gauss(0, GPS_NOISE_STD)

        est_1d = kf1.update(gps)
        est_2d, _ = kf2.update(gps)

        logger.info("%-6d  %-12.2f  %-12.2f  %-12.2f  %-12.2f", i, true_pos, gps, est_1d, est_2d)

        true_positions.append(true_pos)
        gps_readings.append(gps)
        estimates_1d.append(est_1d)
        estimates_2d.append(est_2d)

    plot_kalman(
        true_positions,
        gps_readings,
        estimates_1d,
        estimates_2d,
        title="UAV position — 1D vs 2D Kalman filter",
        ylabel="Position north (m)",
    )


if __name__ == "__main__":
    main()
