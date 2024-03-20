import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
R = 10  # Resistance in ohms
L = 20  # Inductance in henrys
C = 0.05  # Capacitance in farads

def v(t):
    """
    Defines the voltage source function in the circuit.

    This function models the time-varying voltage source in the circuit, which in this case is a sinusoidal function.

    Parameters:
    - t (float): Time variable, representing the point in time at which the voltage is calculated.

    Returns:
    - float: The voltage at time t.
    """
    return 20 * np.sin(20 * t)

def circuit_equations(t, Y):
    """
    Represents the system of differential equations for an RLC circuit.

    This function models the behavior of an RLC circuit using two coupled first-order differential equations,
    describing the time evolution of the current through the inductor and the voltage across the capacitor.

    Parameters:
    - t (float): Time variable, the point in time at which the system is evaluated.
    - Y (list of floats): A list containing the current state of the system, where Y[0] is the current through the
      inductor (i1) and Y[1] is the voltage across the capacitor (vC).

    Returns:
    - list of floats: The derivatives of i1 and vC as a list, where the first element is di1/dt and the second is dvC/dt.
    """
    i1, vC = Y
    di1_dt = (v(t) - i1*R - vC) / L  # Differential equation for the inductor's current
    dvC_dt = i1 / C  # Differential equation for the capacitor's voltage
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
