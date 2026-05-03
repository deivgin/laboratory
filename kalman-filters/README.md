# Kalman Filters

A learning project for understanding Kalman filtering, motivated by UAV navigation. Contains clean implementations of increasing complexity alongside a visualisation layer for comparing them.

## Project structure

```
kalman-filters/
├── kalman/
│   ├── __init__.py
│   ├── filter_1d.py   — 1-state filter (position only)
│   └── filter_2d.py   — 2-state filter (position + velocity)
├── main.py            — example: drone flying north, 1D vs 2D compared
├── plot.py            — matplotlib visualisation
└── pyproject.toml
```

## Running

```bash
python main.py
```

Prints a step-by-step table and opens a plot showing the true position, raw GPS readings, and both filter estimates side by side.

---

## What is a Kalman filter?

A Kalman filter is an optimal recursive estimator. Given a system with noisy dynamics and noisy sensors, it produces the **minimum variance unbiased estimate** of the true state by combining a physical motion model with incoming measurements.

At every time step the filter maintains:

- $\hat{x}$ — the current state estimate
- $P$ — the covariance of the estimation error (how uncertain we are)

Each step has two phases: **predict** and **update**.

### Assumptions

The filter is optimal under these conditions:

1. The system evolves linearly: $x_k = F x_{k-1} + w_k$
2. Measurements are linear in the state: $z_k = H x_k + v_k$
3. Process noise $w_k \sim \mathcal{N}(0, Q)$ and measurement noise $v_k \sim \mathcal{N}(0, R)$ are both white Gaussian

When these hold, the Kalman filter is provably the best possible estimator. For non-linear systems (e.g. 3D attitude estimation on a UAV) the Extended or Unscented Kalman Filter applies instead.

---

## The general Kalman equations

### Predict step

Project the state and its uncertainty forward using the motion model, before observing any new measurement.

$$\hat{x}_{k|k-1} = F \hat{x}_{k-1|k-1}$$

$$P_{k|k-1} = F P_{k-1|k-1} F^\top + Q$$

| Symbol | Meaning |
|---|---|
| $F$ | State transition matrix — encodes the physics of how the state evolves |
| $Q$ | Process noise covariance — uncertainty introduced by unmodelled forces (wind, vibration) |

### Update step

Incorporate the new measurement $z_k$ to correct the prediction.

**Innovation** — the gap between what we measured and what we predicted:

$$y_k = z_k - H \hat{x}_{k|k-1}$$

**Innovation covariance** — total uncertainty in that gap:

$$S_k = H P_{k|k-1} H^\top + R$$

**Kalman gain** — how much weight to give the measurement vs the prediction:

$$K_k = P_{k|k-1} H^\top S_k^{-1}$$

**State update**:

$$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k y_k$$

**Covariance update**:

$$P_{k|k} = (I - K_k H) P_{k|k-1}$$

The Kalman gain $K$ is the key quantity. When $P \gg R$ (prediction is uncertain, sensor is reliable), $K \to H^{-1}$ and we trust the measurement almost completely. When $P \ll R$ (prediction is confident, sensor is noisy), $K \to 0$ and we mostly ignore the measurement.

---

## The two implementations

### `KalmanFilter1D` — position only

The simplest case: a scalar state $x$ (position) with scalar uncertainty $p$.

**State model:**

$$x_k = x_{k-1} + w_k, \quad w_k \sim \mathcal{N}(0, Q)$$

$$z_k = x_k + v_k, \quad v_k \sim \mathcal{N}(0, R)$$

Here $F = 1$ and $H = 1$, so the general matrix equations collapse to scalars:

**Predict:**

$$p_{k|k-1} = p_{k-1} + Q$$

**Update:**

$$K_k = \frac{p_{k|k-1}}{p_{k|k-1} + R}$$

$$\hat{x}_k = \hat{x}_{k|k-1} + K_k (z_k - \hat{x}_{k|k-1})$$

$$p_k = (1 - K_k)\, p_{k|k-1}$$

**Limitation for moving systems:** the model assumes $x_k \approx x_{k-1}$. A drone flying at 5 m/s moves 5 m every second, which the filter has no way to anticipate — it looks like process noise. The workaround is to inflate $Q$ to $(v \cdot \Delta t)^2$ so the filter stays responsive, but this makes it reactive rather than predictive.

---

### `KalmanFilter2D` — position + velocity

Extends the state to a 2-element vector, giving the filter an explicit model of motion.

**State vector:**

$$\mathbf{x}_k = \begin{bmatrix} p_k \\ \dot{p}_k \end{bmatrix}$$

**State transition** (constant-velocity model):

$$F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}$$

This encodes $p_k = p_{k-1} + \dot{p}_{k-1} \cdot \Delta t$, i.e. the drone is expected to move forward at its current velocity each step.

**Measurement matrix** — GPS observes position only, not velocity:

$$H = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

**Process noise covariance** — uncertainty in acceleration (unmodelled forces):

$$Q = \begin{bmatrix} \sigma_a^2 & 0 \\ 0 & \sigma_a^2 \end{bmatrix}$$

**Measurement noise covariance** — GPS accuracy:

$$R = \begin{bmatrix} \sigma_{GPS}^2 \end{bmatrix}$$

The full predict/update equations are the general ones above, applied to these matrices. The Kalman gain $K$ is now a $2 \times 1$ vector, so both position and velocity are corrected by each GPS reading — even though GPS only directly measures position. The velocity estimate is updated because the filter knows they are coupled through $F$.

Because velocity is part of the state, the filter predicts where the drone will be at the next step rather than reacting. This also enables **dead reckoning**: if GPS drops out, the predict step continues advancing the position estimate from velocity alone until the signal returns.

---

## Key parameters

| Parameter | Symbol | Effect |
|---|---|---|
| `process_variance` | $Q$ | Trust in the motion model. Higher $Q$ → filter reacts faster to changes but is noisier. |
| `measurement_variance` | $R$ | Sensor noise. For GPS with $\sigma = 4\,\text{m}$, set $R = 16$. |
| Initial covariance | $P_0$ | Set high (e.g. $100 \cdot I$) so early measurements dominate and pull the estimate toward the true value quickly. |

The ratio $Q/R$ is the fundamental tuning knob: it controls whether the filter trusts its own model or the incoming sensor data more.

---

## Relevance to UAV navigation

Real UAV navigation typically uses a **6-state filter** with state:

$$\mathbf{x} = \begin{bmatrix} x & y & z & \dot{x} & \dot{y} & \dot{z} \end{bmatrix}^\top$$

and fuses multiple sensors:

- **GPS** — absolute position, $\sigma \approx 3\text{–}5\,\text{m}$, low rate (~1–10 Hz)
- **IMU** — acceleration and angular rates, low noise, high rate (~100–1000 Hz), but velocity and position estimates drift without correction

The standard fusion strategy is:

1. IMU drives the **predict** step at high frequency, propagating state forward between GPS fixes
2. GPS triggers the **update** step whenever a new fix arrives, correcting the accumulated IMU drift

This project builds the intuition for that architecture from the ground up, starting with the simplest scalar case and adding velocity as the first extension toward the full navigation filter.
