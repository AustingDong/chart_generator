import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from PIL import Image
from generators.generator import ChartGenerator

class LineGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_points: int = 10, 
                 question_template: Optional[str] = "At which x-position is the value highest?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()
        
        x_vals = list(range(1, num_points + 1))
        y_vals = [random.randint(10, 100) for _ in x_vals]
        df = pd.DataFrame({'x': x_vals, 'y': y_vals})
        max_x = df.loc[df['y'].idxmax(), 'x']

        color = random.choice(['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        x_label = kwargs.get("x_label") or "x"
        y_label = kwargs.get("y_label") or "y"
        title = kwargs.get("title") or f"Line Chart between {x_label} and {y_label}"

        chart = alt.Chart(df).mark_line(color=color, point=True, interpolate="monotone").encode(
            x=alt.X('x:Q', title=x_label),
            y=alt.Y('y:Q', title=y_label),
            tooltip=["x", "y"]
        ).properties(width=self.width, height=self.height, title=title).configure_view(stroke=None)

        filename = f"LineChart"
        self._save_chart(chart, filename)
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)

        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "line",
            "max_x": int(max_x),
            "variation": {
                "color": color,
                "num_points": num_points
            },
            "question": question_template,
            "answer": int(max_x)
        }
        self._save_metadata(metadata, filename)
        return filename
