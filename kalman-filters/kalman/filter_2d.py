class KalmanFilter2D:
    """
    2-state Kalman filter tracking position and velocity.

    State vector:      [position, velocity]
    State transition:  x_k = F * x_{k-1}   where F = [[1, dt], [0, 1]]
    Measurement:       z_k = position + noise   (GPS only observes position)

    Because velocity is explicitly modelled, the filter predicts where the
    drone will be before consulting the GPS, rather than just reacting to it.
    """

    def __init__(
        self,
        dt: float,
        process_variance: float,
        measurement_variance: float,
        initial_position: float = 0.0,
        initial_velocity: float = 0.0,
    ):
        self.dt = dt

        # State: [position, velocity]
        self.x = [initial_position, initial_velocity]

        # State covariance matrix (2x2), start with high uncertainty
        self.p = [
            [100.0, 0.0],
            [0.0,   100.0],
        ]

        # Process noise covariance — models acceleration uncertainty
        self.q = [
            [process_variance, 0.0],
            [0.0,              process_variance],
        ]

        self.r = measurement_variance  # GPS measurement noise

    # ------------------------------------------------------------------
    # Minimal matrix helpers (avoids a numpy dependency for now)
    # ------------------------------------------------------------------

    @staticmethod
    def _mat_add(a: list, b: list) -> list:
        return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    @staticmethod
    def _mat_mul(a: list, b: list) -> list:
        rows_a, cols_a, cols_b = len(a), len(a[0]), len(b[0])
        return [
            [sum(a[i][k] * b[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)
        ]

    @staticmethod
    def _mat_transpose(m: list) -> list:
        return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

    # ------------------------------------------------------------------

    def update(self, measurement: float) -> tuple[float, float]:
        dt = self.dt

        # State transition matrix  F = [[1, dt], [0, 1]]
        F = [[1, dt], [0, 1]]

        # Measurement matrix  H = [[1, 0]]  — we only observe position
        H = [[1, 0]]
        H_T = [[1], [0]]

        # --- Predict ---
        self.x = [
            self.x[0] + dt * self.x[1],
            self.x[1],
        ]
        self.p = self._mat_add(self._mat_mul(self._mat_mul(F, self.p), self._mat_transpose(F)), self.q)

        # --- Update ---
        # Innovation:  y = z - H*x
        y = measurement - self.x[0]

        # Innovation covariance:  S = H*P*H^T + R
        HP = self._mat_mul(H, self.p)       # 1x2
        S = HP[0][0] + self.r               # scalar

        # Kalman gain:  K = P*H^T / S
        PH_T = self._mat_mul(self.p, H_T)   # 2x1
        K = [[PH_T[i][0] / S] for i in range(2)]

        # State update:  x = x + K*y
        self.x[0] += K[0][0] * y
        self.x[1] += K[1][0] * y

        # Covariance update:  P = (I - K*H) * P
        KH = self._mat_mul(K, H)            # 2x2
        I_KH = [[float(i == j) - KH[i][j] for j in range(2)] for i in range(2)]
        self.p = self._mat_mul(I_KH, self.p)

        return self.x[0], self.x[1]         # (position, velocity)
