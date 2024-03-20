import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
R = 10  # Resistance in ohms
L = 20  # Inductance in henrys
C = 0.05  # Capacitance in farads

# Voltage source function
def v(t):
    return 20 * np.sin(20 * t)

# Differential equations
def circuit_equations(t, Y):
    i1, vC = Y
    di1_dt = (v(t) - i1*R - vC) / L
    dvC_dt = i1 / C
    return [di1_dt, dvC_dt]

# Initial conditions: i1(0) = 0, vC(0) = 0
Y0 = [0, 0]

# Time span to solve the differential equations over 10 seconds
t_span = (0, 10)
t_eval = np.linspace(*t_span, 1000)

# Solve the system of differential equations
sol = solve_ivp(circuit_equations, t_span, Y0, t_eval=t_eval)

# Plot the results
plt.figure(figsize=(14, 7))

# Current i1(t) and i2(t)
plt.plot(sol.t, sol.y[0], label='i1(t) = i2(t) [A]', linestyle='-')

# Voltage across capacitor vC(t)
plt.plot(sol.t, sol.y[1], label='vC(t) [V]', linestyle=':')

plt.title('Currents and Voltage in RLC Circuit')
plt.xlabel('Time (s)')
plt.ylabel('Current (A) / Voltage (V)')
plt.legend()
plt.grid(True)
plt.show()
