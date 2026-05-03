class KalmanFilter:
    """
    1D Kalman filter tracking a scalar state (e.g. position).

    State transition:  x_k = x_{k-1} + process_noise
    Measurement:       z_k = x_k     + measurement_noise
    """

    def __init__(self, process_variance: float, measurement_variance: float, initial_estimate: float = 0.0):
        self.q = process_variance       # how much the true value can drift per step
        self.r = measurement_variance   # how noisy the sensor is
        self.x = initial_estimate       # current state estimate
        self.p = 100.0                  # start with high uncertainty so first measurements pull hard

    def update(self, measurement: float) -> float:
        # Predict
        self.p += self.q

        # Update (Kalman gain)
        k = self.p / (self.p + self.r)
        self.x += k * (measurement - self.x)
        self.p *= 1 - k

        return self.x
