"""
Neural Network Visualization with Manim
========================================
This script creates an animated visualization of how a neural network processes data.
It demonstrates:
1. Network structure (input, hidden, output layers)
2. Forward propagation (data flowing through the network)
3. Activation visualization

Author: Created with Claude Code assistance
Purpose: Educational content for AI/ML courses
"""

from manim import *
import numpy as np


class NeuralNetworkScene(Scene):
    """
    Main scene that visualizes a simple feedforward neural network.
    Perfect for explaining the basics of deep learning.
    """

    def construct(self):
        # Title sequence
        title = Text("How Neural Networks Process Data", font_size=42)
        subtitle = Text("A Visual Journey", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Build the neural network visualization
        network = self.create_network()

        # Animate the network appearing
        self.play(
            LaggedStart(*[
                GrowFromCenter(layer)
                for layer in network["layers"]
            ], lag_ratio=0.3),
            run_time=2
        )
        self.wait(0.5)

        # Add layer labels
        labels = self.create_layer_labels(network)
        self.play(
            LaggedStart(*[Write(label) for label in labels], lag_ratio=0.2)
        )
        self.wait(1)

        # Draw connections between layers
        connections = self.create_connections(network)
        self.play(
            LaggedStart(*[
                Create(conn) for conn in connections
            ], lag_ratio=0.01),
            run_time=2
        )
        self.wait(1)

        # Animate forward propagation
        self.animate_forward_pass(network, connections)

        # Show output activation
        self.show_output_result(network)

        # Closing
        self.wait(1)
        closing = Text("Neural networks learn by adjusting connection weights", font_size=28)
        closing.to_edge(DOWN)
        self.play(Write(closing))
        self.wait(2)

    def create_network(self):
        """
        Create the visual structure of the neural network.
        Returns a dictionary with layers and neuron positions.
        """
        layer_sizes = [4, 6, 6, 3]  # Input, Hidden1, Hidden2, Output
        layer_spacing = 2.5
        neuron_radius = 0.25

        layers = []
        neuron_positions = []

        # Calculate total width and center offset
        total_width = (len(layer_sizes) - 1) * layer_spacing
        x_offset = -total_width / 2

        for layer_idx, size in enumerate(layer_sizes):
            layer_neurons = VGroup()
            positions = []

            # Calculate vertical spacing for this layer
            total_height = (size - 1) * 0.8
            y_offset = total_height / 2

            for neuron_idx in range(size):
                x = x_offset + layer_idx * layer_spacing
                y = y_offset - neuron_idx * 0.8

                # Create neuron circle
                neuron = Circle(
                    radius=neuron_radius,
                    color=self.get_layer_color(layer_idx),
                    fill_opacity=0.3,
                    stroke_width=2
                )
                neuron.move_to([x, y, 0])
                layer_neurons.add(neuron)
                positions.append(np.array([x, y, 0]))

            layers.append(layer_neurons)
            neuron_positions.append(positions)

        return {
            "layers": layers,
            "positions": neuron_positions,
            "sizes": layer_sizes
        }

    def get_layer_color(self, layer_idx):
        """Return color for each layer type."""
        colors = [BLUE, GREEN, GREEN, ORANGE]
        return colors[min(layer_idx, len(colors) - 1)]

    def create_layer_labels(self, network):
        """Create labels for each layer."""
        labels = []
        layer_names = ["Input\nLayer", "Hidden\nLayer 1", "Hidden\nLayer 2", "Output\nLayer"]

        for idx, (layer, name) in enumerate(zip(network["layers"], layer_names)):
            label = Text(name, font_size=20, color=self.get_layer_color(idx))
            label.next_to(layer, DOWN, buff=0.5)
            labels.append(label)

        return labels

    def create_connections(self, network):
        """Create connection lines between all neurons in adjacent layers."""
        connections = []
        positions = network["positions"]

        for layer_idx in range(len(positions) - 1):
            current_layer = positions[layer_idx]
            next_layer = positions[layer_idx + 1]

            for pos1 in current_layer:
                for pos2 in next_layer:
                    line = Line(
                        pos1, pos2,
                        stroke_width=0.5,
                        stroke_opacity=0.3,
                        color=GRAY
                    )
                    connections.append(line)

        return connections

    def animate_forward_pass(self, network, connections):
        """Animate data flowing through the network (forward propagation)."""

        # Add explanatory text
        text = Text("Forward Propagation: Data flows through the network", font_size=24)
        text.to_edge(UP)
        self.play(Write(text))

        positions = network["positions"]
        layers = network["layers"]

        # Activate input layer neurons one by one
        input_activations = []
        for neuron in layers[0]:
            activation = neuron.copy()
            activation.set_fill(BLUE, opacity=0.8)
            activation.set_stroke(BLUE_A, width=3)
            input_activations.append(activation)

        self.play(
            LaggedStart(*[
                Transform(layers[0][i], input_activations[i])
                for i in range(len(layers[0]))
            ], lag_ratio=0.1),
            run_time=1
        )

        # Propagate through each layer
        for layer_idx in range(len(positions) - 1):
            # Create signal dots
            signals = []
            current_layer = positions[layer_idx]
            next_layer = positions[layer_idx + 1]

            for pos2 in next_layer:
                # Create a dot that will move from multiple sources to this neuron
                dot = Dot(
                    point=current_layer[0],
                    color=YELLOW,
                    radius=0.1
                )
                signals.append(dot)

            # Add signals to scene
            self.add(*signals)

            # Animate signals moving to next layer
            self.play(
                *[
                    signal.animate.move_to(next_layer[i])
                    for i, signal in enumerate(signals)
                ],
                run_time=0.8
            )

            # Activate next layer neurons
            next_activations = []
            color = self.get_layer_color(layer_idx + 1)
            for neuron in layers[layer_idx + 1]:
                activation = neuron.copy()
                activation.set_fill(color, opacity=0.8)
                activation.set_stroke(WHITE, width=3)
                next_activations.append(activation)

            self.play(
                LaggedStart(*[
                    Transform(layers[layer_idx + 1][i], next_activations[i])
                    for i in range(len(layers[layer_idx + 1]))
                ], lag_ratio=0.05),
                *[FadeOut(signal) for signal in signals],
                run_time=0.6
            )

        self.play(FadeOut(text))

    def show_output_result(self, network):
        """Highlight the final output and show result."""
        text = Text("Output: The network makes a prediction!", font_size=28)
        text.to_edge(UP)
        self.play(Write(text))

        # Pulse the output layer
        output_layer = network["layers"][-1]
        self.play(
            output_layer.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=0.5
        )
        self.play(
            output_layer.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=0.5
        )

        # Show probability bars next to output neurons
        bars = VGroup()
        probs = [0.15, 0.75, 0.10]  # Simulated output probabilities
        labels = ["Cat", "Dog", "Bird"]

        for i, (neuron, prob, label) in enumerate(zip(output_layer, probs, labels)):
            # Create bar
            bar = Rectangle(
                width=prob * 2,
                height=0.3,
                fill_color=ORANGE,
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.next_to(neuron, RIGHT, buff=0.3)
            bar.align_to(neuron, LEFT)
            bar.shift(RIGHT * 0.5)

            # Create label
            prob_label = Text(f"{label}: {prob*100:.0f}%", font_size=18)
            prob_label.next_to(bar, RIGHT, buff=0.2)

            bars.add(bar, prob_label)

        self.play(
            LaggedStart(*[
                GrowFromEdge(bars[i*2], LEFT)
                for i in range(3)
            ], lag_ratio=0.2),
            LaggedStart(*[
                FadeIn(bars[i*2+1])
                for i in range(3)
            ], lag_ratio=0.2)
        )

        # Highlight the winner
        winner_text = Text("Prediction: Dog!", font_size=32, color=GREEN)
        winner_text.next_to(text, DOWN)
        self.play(Write(winner_text))

        self.wait(2)
        self.play(FadeOut(text), FadeOut(winner_text), FadeOut(bars))


class HelloManimTest(Scene):
    """
    Simple test scene to verify Manim installation.
    Run this first to ensure everything works.
    """

    def construct(self):
        # Create a circle
        circle = Circle(radius=2, color=BLUE)
        circle.set_fill(BLUE, opacity=0.5)

        # Create text
        text = Text("Manim is Working!", font_size=36)
        text.next_to(circle, DOWN)

        # Animate
        self.play(GrowFromCenter(circle))
        self.play(Write(text))
        self.play(circle.animate.set_color(GREEN))
        self.play(
            circle.animate.scale(0.5),
            text.animate.shift(UP * 1.5)
        )
        self.wait(1)


class GradientDescentVisualization(Scene):
    """
    Bonus scene: Visualize gradient descent optimization.
    Shows how neural networks learn by minimizing loss.
    """

    def construct(self):
        # Title
        title = Text("Gradient Descent: How Networks Learn", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.7))

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"color": GRAY}
        )
        axes.shift(DOWN * 0.5)

        # Create loss function (parabola)
        loss_curve = axes.plot(
            lambda x: x**2 + 1,
            color=BLUE,
            x_range=[-2.5, 2.5]
        )

        loss_label = Text("Loss Function", font_size=24, color=BLUE)
        loss_label.next_to(loss_curve, UP + RIGHT)

        self.play(Create(axes), Create(loss_curve), Write(loss_label))
        self.wait(1)

        # Create a ball that will roll down
        x_tracker = ValueTracker(2)

        ball = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2 + 1),
            color=RED,
            radius=0.15
        ))

        self.add(ball)

        # Add explanation
        explanation = Text(
            "The ball (our model) rolls down to find the minimum loss",
            font_size=22
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))

        # Animate gradient descent steps
        learning_rate = 0.3
        for step in range(8):
            current_x = x_tracker.get_value()
            gradient = 2 * current_x  # Derivative of x^2 + 1
            new_x = current_x - learning_rate * gradient

            # Show step
            step_text = Text(f"Step {step + 1}", font_size=20)
            step_text.to_corner(UR)

            self.play(
                x_tracker.animate.set_value(new_x),
                run_time=0.5
            )

            if abs(new_x) < 0.1:
                break

        # Celebrate reaching minimum
        success = Text("Minimum Found! Model Trained!", font_size=28, color=GREEN)
        success.next_to(axes, DOWN)
        self.play(
            FadeOut(explanation),
            Write(success)
        )
        self.wait(2)


if __name__ == "__main__":
    # This allows running with: python neural_network.py
    # But typically you'll use: manim -pql neural_network.py SceneName
    print("""
    To render these animations, use:

    1. Test installation (quick):
       manim -pql neural_network.py HelloManimTest

    2. Neural Network visualization:
       manim -pql neural_network.py NeuralNetworkScene

    3. Gradient Descent visualization:
       manim -pql neural_network.py GradientDescentVisualization

    Quality flags:
       -ql  = Low quality (480p, 15fps) - fastest for testing
       -qm  = Medium quality (720p, 30fps)
       -qh  = High quality (1080p, 60fps)
       -qk  = 4K quality (2160p, 60fps)

       -p   = Preview (opens video after rendering)
    """)
