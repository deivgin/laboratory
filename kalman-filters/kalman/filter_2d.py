import numpy as np


class KalmanFilter2D:
    """
    2-state Kalman filter tracking position and velocity.

    State vector:      [position, velocity]
    State transition:  x_k = F * x_{k-1}   where F = [[1, dt], [0, 1]]
    Measurement:       z_k = position + noise   (GPS only observes position)
    """

    def __init__(
        self,
        dt: float,
        process_variance: float,
        measurement_variance: float,
        initial_position: float = 0.0,
        initial_velocity: float = 0.0,
    ):
        self.F = np.array([[1, dt], [0, 1]])          # state transition
        self.H = np.array([[1, 0]])                    # measurement (position only)
        self.Q = np.eye(2) * process_variance          # process noise
        self.R = np.array([[measurement_variance]])    # measurement noise
        self.x = np.array([[initial_position], [initial_velocity]])
        self.p = np.eye(2) * 100.0                     # initial uncertainty

    def update(self, measurement: float) -> tuple[float, float]:
        # Predict
        self.x = self.F @ self.x
        self.p = self.F @ self.p @ self.F.T + self.Q

        # Update
        y = measurement - (self.H @ self.x)
        S = self.H @ self.p @ self.H.T + self.R
        K = self.p @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.p = (np.eye(2) - K @ self.H) @ self.p

        return float(self.x[0, 0]), float(self.x[1, 0])     # (position, velocity)
