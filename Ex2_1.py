from scipy.integrate import solve_ivp, quad
import matplotlib.pyplot as plt
import numpy as np

def ivp_function(x, y):
    """
    Defines the differential equation for the initial value problem (IVP).

    This function represents the differential equation y' = (y - 0.01*x**2)**2 * np.sin(x**2) + 0.02*x, which is
    the equation governing the behavior of the system under study.

    Parameters:
    - x (float): The independent variable of the differential equation, often representing time or spatial coordinate.
    - y (float): The dependent variable or the current value of the function being solved for in the IVP.

    Returns:
    - float: The derivative of y at point x, based on the defined differential equation.
    """
    return (y - 0.01*x**2)**2 * np.sin(x**2) + 0.02*x

def S(x):
    """
    Computes the antiderivative of sin(t^2) from 0 to x using numerical integration.

    This function is part of the exact solution to the IVP and involves calculating the integral of a specific
    mathematical function, sin(t^2), where t is a dummy variable of integration.

    Parameters:
    - x (float): The upper limit of the integral.

    Returns:
    - float: The value of the integral from 0 to x.
    """
    return quad(lambda t: np.sin(t**2), 0, x)[0]

def exact_solution(x):
    """
    Calculates the exact solution of the differential equation at a given point x.

    This function provides the analytical solution to the IVP, which is used for comparison with the numerical
    solution obtained from solve_ivp.

    Parameters:
    - x (float): The point at which the exact solution is evaluated.

    Returns:
    - float: The value of the exact solution at x.
    """
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
