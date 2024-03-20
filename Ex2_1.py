from scipy.integrate import solve_ivp, quad
import matplotlib.pyplot as plt
import numpy as np

# Given initial value problem
def ivp_function(x, y):
    return (y - 0.01*x**2)**2 * np.sin(x**2) + 0.02*x

# Exact solution S(x)
def S(x):
    return quad(lambda t: np.sin(t**2), 0, x)[0]

# Exact solution y
def exact_solution(x):
    return 1 / (2.5 - S(x)) + 0.01*x**2

# Define the time points where we want to compute the solution
x_points = np.arange(0, 5.1, 0.2)
y_exact = np.array([exact_solution(x) for x in x_points])

# Solve the initial value problem using solve_ivp
sol = solve_ivp(ivp_function, [0, 5], [0.4], t_eval=x_points)

# Plot the numerical and exact solutions
plt.figure(figsize=(10, 5))

# Exact solution plot
plt.plot(x_points, y_exact, label='Exact', linestyle='-', color='blue')

# Numerical solution plot
plt.plot(sol.t, sol.y[0], label='Numerical', linestyle='', marker='^', color='orange')

# Formatting the plot
plt.xlim(0.0, 6.0)
plt.ylim(0.0, 1.0)
plt.xlabel('x')
plt.ylabel('y')
plt.xticks(np.arange(0.0, 6.1, 0.2), rotation=90)
plt.yticks(np.arange(0.0, 1.1, 0.1))
plt.gca().tick_params(axis='x', direction='in', top=True)
plt.gca().tick_params(axis='y', direction='in', right=True)
plt.title("IVP: y'=(y-0.01x^2)^2 sin(x^2)+0.02x, y(0)=0.4")
plt.legend()
plt.grid(True)
plt.show()
