import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from PIL import Image
from generators.generator import ChartGenerator

class BubbleGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_points: int = 10, question_template: Optional[str] = "Which point has the largest size?"):
        random.seed(seed)
        bgcolor = self._random_rgba()

        points = pd.DataFrame({
            'x': [random.uniform(0, 100) for _ in range(num_points)],
            'y': [random.uniform(0, 100) for _ in range(num_points)],
            'size': [random.randint(20, 200) for _ in range(num_points)],
            'label': [chr(65+i) for i in range(num_points)]
        })

        largest = points.loc[points['size'].idxmax(), 'label']
        color_scheme = random.choice(['category10', 'tableau10'])

        chart = alt.Chart(points).mark_circle(opacity=0.7).encode(
            x='x',
            y='y',
            size='size',
            color=alt.Color('label', scale=alt.Scale(scheme=color_scheme)),
            tooltip=['label', 'x', 'y', 'size']
        ).properties(width=self.width, height=self.height)

        filename = f"bubble_{seed}"
        self._save_chart(chart, filename)
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "bubble",
            "max_label": largest,
            "variation": {
                "color_scheme": color_scheme,
                "num_points": num_points
            },
            "question": question_template,
            "answer": largest
        }
        self._save_metadata(metadata, filename)
        return filename
