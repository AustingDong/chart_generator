from generator import ChartGenerator

if __name__ == "__main__":
    # Initialize the chart generator
    generator = ChartGenerator(output_dir="./charts", img_format="png", width=300, height=200)

    # Generate a scatter chart with default parameters
    # generator.generate_scatter_chart(seed=42, num_points=10, question_template="Which point is the farthest from the origin?")
    generator.generate_bar_chart(seed=42)
