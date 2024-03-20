import numpy as np

# Constants
g = 32.2  # Acceleration due to gravity (ft/s^2)
rho = 62.3  # Density of water (lb/ft^3)
mu = 20.50e-6  # Viscosity of water (lb/(ft*s))
inch_to_ft = 1 / 12  # Conversion factor from inches to feet

class Pipe:
    """Represents a pipe in the pipe network."""

    def __init__(self, diameter, length, roughness, start_node, end_node):
        """Initialize the Pipe object.

        Args:
            diameter (float): Diameter of the pipe in inches.
            length (float): Length of the pipe in inches.
            roughness (float): Roughness of the pipe in ft.
            start_node (Node): Start node of the pipe.
            end_node (Node): End node of the pipe.
        """
        self.diameter = diameter  # inches
        self.length = length  # inches
        self.roughness = roughness  # ft
        self.start_node = start_node
        self.end_node = end_node
        self.flow_rate = 0  # cfs

    def calculate_flow_rate(self):
        """Calculate the flow rate through the pipe using Darcy-Weisbach equation.

        Returns:
            float: Head loss in the pipe.
        """
        # Calculate Reynolds number
        velocity = self.flow_rate / (np.pi * (self.diameter * inch_to_ft / 2) ** 2)
        Re = (velocity * self.diameter * inch_to_ft) / mu

        # Calculate friction factor
        if Re < 2000:
            f = 64 / Re
        else:
            # Use Colebrook equation for turbulent flow
            # Since it requires iteration, for simplicity, we'll use a fixed value for f
            f = 0.02

        # Calculate head loss using Darcy-Weisbach equation
        head_loss = f * (self.length * inch_to_ft) / (self.diameter * inch_to_ft) * (rho * velocity ** 2) / (2 * g)
        return head_loss

class Node:
    """Represents a node in the pipe network."""

    def __init__(self, name, pressure=80):
        """Initialize the Node object.

        Args:
            name (str): Name of the node.
            pressure (float, optional): Pressure at the node in psi. Defaults to 80.
        """
        self.name = name
        self.pressure = pressure  # psi
        self.connected_pipes = []

    def add_pipe(self, pipe):
        """Add a pipe connected to the node.

        Args:
            pipe (Pipe): Pipe object connected to the node.
        """
        self.connected_pipes.append(pipe)

class PipeNetwork:
    """Represents a pipe network consisting of nodes and pipes."""

    def __init__(self):
        """Initialize the PipeNetwork object."""
        # Create nodes
        self.nodes = {name: Node(name) for name in 'abcdefghij'}

        # Define pipe connections
        self.pipe_connections = {
            'a-b': ('a', 'b'),
            'a-h': ('a', 'h'),
            'b-c': ('b', 'c'),
            'b-e': ('b', 'e'),
            'c-d': ('c', 'd'),
            'c-f': ('c', 'f'),
            'd-g': ('d', 'g'),
            'e-f': ('e', 'f'),
            'e-i': ('e', 'i'),
            'f-g': ('f', 'g'),
            'g-j': ('g', 'j'),
            'h-i': ('h', 'i'),
            'i-j': ('i', 'j'),
        }

        # Create pipes
        self.pipes = {}
        for pipe_name, (start_node_name, end_node_name) in self.pipe_connections.items():
            start_node = self.nodes[start_node_name]
            end_node = self.nodes[end_node_name]
            diameter, length, roughness = self.get_pipe_properties(pipe_name)
            pipe = Pipe(diameter, length, roughness, start_node, end_node)
            start_node.add_pipe(pipe)
            end_node.add_pipe(pipe)
            self.pipes[pipe_name] = pipe

    def get_pipe_properties(self, pipe_name):
        """Get properties (diameter, length, roughness) of a pipe based on its name.

        Args:
            pipe_name (str): Name of the pipe.

        Returns:
            tuple: Tuple containing diameter, length, and roughness.
        """
        # Assign properties based on pipe size and material
        properties = {
            'a-b': (18, 1000, 0.00085),  # inches, inches, ft
            'a-h': (24, 1600, 0.00085),
            'b-c': (18, 500, 0.00085),
            'b-e': (16, 800, 0.00085),
            'c-d': (18, 500, 0.00085),
            'c-f': (16, 800, 0.00085),
            'd-g': (16, 800, 0.00085),
            'e-f': (12, 500, 0.00085),
            'e-i': (18, 800, 0.003),
            'f-g': (12, 500, 0.00085),
            'g-j': (18, 800, 0.003),
            'h-i': (24, 1000, 0.003),
            'i-j': (24, 1000, 0.003),
        }
        return properties[pipe_name]

    def calculate_flow_rates(self):
        """Calculate flow rates for all pipes in the network."""
        for pipe_name, pipe in self.pipes.items():
            # Assume flow direction from start to end node
            flow_rate = np.random.uniform(-5, 5)  # Placeholder random value
            pipe.flow_rate = flow_rate

    def print_flow_rates(self):
        """Print flow rates for all pipes in the network."""
        for pipe_name, pipe in self.pipes.items():
            start_node_name, end_node_name = pipe_name.split('-')
            print(f"The flow in segment {pipe_name} is {pipe.flow_rate:.2f} (cfs)")

    def check_loop_head_loss(self):
        """Calculate and print the head loss for each loop in the pipe network."""
        loop_connections = [('a', 'b'), ('b', 'e'), ('e', 'i'), ('i', 'h')]
        for i, (start_node_name, end_node_name) in enumerate(loop_connections):
            start_node = self.nodes[start_node_name]
            end_node = self.nodes[end_node_name]
            delta_p = start_node.pressure - end_node.pressure
            print(f"Head loss for loop {chr(65 + i)} is {delta_p:.2f} psi.")

    def calculate_head_loss(self):
        """Calculate and print the head loss for each pipe in the pipe network."""
        for pipe_name, pipe in self.pipes.items():
            head_loss = pipe.calculate_flow_rate()
            print(
                f"Head loss in pipe {pipe_name} (Length={pipe.length:.2f} in, Diameter={pipe.diameter:.2f} in) is {head_loss:.2f} in of water.")

    def calculate_pressures(self):
        """Print the pressure at each node in the pipe network."""
        for node_name, node in self.nodes.items():
            print(f"Pressure at node {node_name} = {node.pressure:.2f} psi.")

    def check_node_flows(self):
        """Check and print the net flow into each node in the pipe network.

        This method calculates the net flow into each node by summing the flow rates of pipes connected
        to the node. Positive flow rates indicate flow into the node, while negative flow rates indicate
        flow out of the node.

        Prints the net flow into each node in cubic feet per second (cfs).
        """
        for node_name, node in self.nodes.items():
            net_flow = sum(
                pipe.flow_rate if pipe.start_node == node else -pipe.flow_rate for pipe in node.connected_pipes)
            print(f"net flow into node {node_name} is {net_flow:.2f} (cfs)")

def main():
    """Main function to create and analyze the pipe network."""
    network = PipeNetwork()
    network.calculate_flow_rates()
    network.print_flow_rates()
    print("\nCheck node flows:")
    network.check_node_flows()
    print("\nCheck loop head loss:")
    network.check_loop_head_loss()
    print("\nCheck Head loss")
    network.calculate_head_loss()
    print("\nCheck Pressure at every node")
    network.calculate_pressures()

if __name__ == "__main__":
    main()
