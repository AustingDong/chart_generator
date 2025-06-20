import os
import random
import json
import numpy as np
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from generators.generator import ChartGenerator

class ScatterGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 200):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_points: int = 10, 
                 question_template: Optional[str] = "What is the x value of point that is the farthest from the origin?",
                 **kwargs):
        random.seed(seed)
        np.random.seed(seed)
        bgcolor = self._random_rgba()

        points = pd.DataFrame({
            'x': np.random.uniform(10, 100, num_points),
            'y': np.random.uniform(10, 100, num_points),
        })
        points['distance'] = np.sqrt(points['x']**2 + points['y']**2)
        farthest_x = points.loc[points['distance'].idxmax(), 'x']


        x_label = kwargs.get("x_label") or "x"
        y_label = kwargs.get("y_label") or "y"
        title = kwargs.get("title") or f"Scatter Plot between {x_label} and {y_label}"

        color_scheme = random.choice(['red', 'blue', 'teal', 'orange'])
        shape_options = ['circle', 'square', 'triangle']
        point_shape = random.choice(shape_options)

        # build chart
        chart = alt.Chart(points).mark_point(color=color_scheme, filled=True, shape=point_shape).encode(
            x=alt.X('x:Q', title=x_label),
            y=alt.Y('y:Q', title=y_label),
            tooltip=['x', 'y']
        ).properties(width=self.width, height=self.height, title=title).configure_view(stroke=None)

        filename = f"scatter_{seed}"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)

        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "scatter",
            "farthest_x": farthest_x,
            "variation": {
                "color_scheme": color_scheme,
                "point_shape": point_shape,
                "num_points": num_points
            },
            "question": question_template,
            "answer": farthest_x
        }
        self._save_metadata(metadata, filename)
        return filename
