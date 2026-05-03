class KalmanFilter1D:
    """
    1D Kalman filter tracking a single scalar state (e.g. position only).

    State transition:  x_k = x_{k-1} + process_noise
    Measurement:       z_k = x_k     + measurement_noise

    Has no velocity state, so movement must be absorbed into process_variance.
    """

    def __init__(self, process_variance: float, measurement_variance: float, initial_estimate: float = 0.0):
        self.q = process_variance
        self.r = measurement_variance
        self.x = initial_estimate
        self.p = 100.0

    def update(self, measurement: float) -> float:
        # Predict
        self.p += self.q

        # Update
        k = self.p / (self.p + self.r)
        self.x += k * (measurement - self.x)
        self.p *= 1 - k

        return self.x
