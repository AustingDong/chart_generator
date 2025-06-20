import gradio as gr
import json
from generators.scatter_generator import ScatterGenerator
from generators.pie_generator import PieGenerator
from generators.bar_generator import BarGenerator
from generators.line_generator import LineGenerator
from generators.area_generator import AreaGenerator
from generators.bubble_generator import BubbleGenerator
from generators.choropleth_generator import ChoroplethGenerator
from generators.stackedarea_generator import StackedAreaGenerator
from generators.stackedbar_generator import StackedBarGenerator
from generators.treemap_generator import TreeMapGenerator
from generators.histogram_generator import HistogramGenerator
from generators.stacked100_generator import Stacked100Generator
import os

generators = {
    "Area Chart": AreaGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Bar Chart": BarGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Bubble Chart": BubbleGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Choropleth Map": ChoroplethGenerator(output_dir="./charts", img_format="png", width=700, height=500),
    "Line Chart": LineGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Pie Chart": PieGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Scatter Chart": ScatterGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Stacked Area Chart": StackedAreaGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Stacked Bar Chart": StackedBarGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "Treemap": TreeMapGenerator(output_dir="./charts", img_format="png", width=500, height=500),
    "Histogram": HistogramGenerator(output_dir="./charts", img_format="png", width=300, height=300),
    "100% Stacked Bar Chart": Stacked100Generator(output_dir="./charts", img_format="png", width=300, height=300)
}

def generate_chart(chart_type, seed, num_items, x_label, y_label, size_label, title, categories, series):
    kwargs = {
        "x_label": x_label,
        "y_label": y_label,
        "size_label": size_label,
        "title": title,
        "categories": categories.split(","),
        "series": series.split(",")
    }

    generator = generators[chart_type]
    if chart_type == "Pie Chart":
        filename = generator.generate(seed=seed, num_slices=num_items, **kwargs)
    elif chart_type == "Scatter Chart":
        filename = generator.generate(seed=seed, num_points=num_items, **kwargs)
    elif chart_type == "Bar Chart":
        filename = generator.generate(seed=seed, num_bars=num_items, **kwargs)
    elif chart_type == "Area Chart":
        filename = generator.generate(seed=seed, num_points=num_items, **kwargs)
    elif chart_type == "Bubble Chart":
        filename = generator.generate(seed=seed, num_points=num_items, **kwargs)
    elif chart_type == "Line Chart":
        filename = generator.generate(seed=seed, num_points=num_items, **kwargs)
    elif chart_type == "Choropleth Map":
        filename = generator.generate(seed=seed, **kwargs)
    elif chart_type == "Stacked Area Chart":
        filename = generator.generate(seed=seed, num_points=num_items, **kwargs)
    elif chart_type == "Stacked Bar Chart":
        filename = generator.generate(seed=seed, num_categories=num_items, **kwargs)
    elif chart_type == "Treemap":
        filename = generator.generate(seed=seed, num_categories=num_items, **kwargs)
    elif chart_type == "Histogram":
        filename = generator.generate(seed=seed, num_bins=num_items, **kwargs)
    elif chart_type == "100% Stacked Bar Chart":
        filename = generator.generate(seed=seed, num_categories=num_items, **kwargs)
    else:
        return None, "Unsupported chart type."

    img_path = os.path.join(generator.output_dir, f"{filename}.png")
    json_path = os.path.join(generator.output_dir, f"{filename}.json")
    return img_path, json_path


def generate_qa(chart_type, question, options, answer):
    QA_DIR = "./questions"
    json_path = os.path.join(QA_DIR, f"{chart_type}.json")
    opt = options.split(",")
    opt_sel = []
    for i, o in enumerate(opt):
        sel = {
            chr(65+i): o
        }
        opt_sel.append(sel)

    qa = {
        "type": chart_type,
        "question": question,
        "options": opt_sel,
        "correct_answer": answer # A, B, C, D
    }

    with open(json_path, "w") as f:
        json.dump(qa, f, indent=4)
    return json_path

with gr.Blocks() as demo:
    gr.Markdown("# 📊 Chart Generator")

    with gr.Row():
        chart_type = gr.Dropdown(generators.keys(), label="Chart Type", value="Area Chart")
        seed = gr.Number(label="Random Seed", value=42, precision=0)
        num_items = gr.Slider(3, 10, value=4, step=1, label="Number of Items (Slices or Points)")
    
    with gr.Row():
        x_label = gr.Textbox(label="x_label (category_label)", value=None)
        y_label = gr.Textbox(label="y_label (value_label)", value=None)
        size_label = gr.Textbox(label="size_label", value=None)
        title = gr.Textbox(label="title", value=None)
        categories = gr.Textbox(label="categories", value=None)
        series = gr.Textbox(label="series", value=None)

    generate_btn = gr.Button("Generate Chart")

    with gr.Row():
        with gr.Column():
            img_output = gr.Image(label="Generated Chart")
        with gr.Column():
            json_output = gr.File(label="Download Metadata (.json)")
            question_answer_json = gr.File(label="Download Qustion & Answer (.json)")

    with gr.Row():
        question = gr.Textbox(label="Question")
        options = gr.Textbox(label="Options")
        answer = gr.Textbox(label="Answer")
    
    generate_qa_btn = gr.Button("Generate Question & Answer")

    generate_btn.click(
        fn=generate_chart,
        inputs=[chart_type, seed, num_items, 
        x_label,
        y_label,
        size_label,
        title,
        categories,
        series
        ],
        outputs=[img_output, json_output]
    )

    generate_qa_btn.click(
        fn=generate_qa,
        inputs=[chart_type, question, options, answer],
        outputs=[question_answer_json]
    )



demo.launch()
