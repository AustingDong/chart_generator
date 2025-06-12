import os
import random
import json
import numpy as np
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any

class ChartGenerator:
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 200):
        self.output_dir = output_dir
        self.img_format = img_format
        self.width = width
        self.height = height
        os.makedirs(self.output_dir, exist_ok=True)

    def _save_chart(self, chart: alt.Chart, filename: str):
        chart_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        chart.save(chart_path)

    def _save_metadata(self, metadata: Dict[str, Any], filename: str):
        meta_path = os.path.join(self.output_dir, f"{filename}.json")
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def generate_bar_chart(self, seed: int = 0, num_bars: int = 4, question_template: Optional[str] = "Which category has the highest value?"):
        random.seed(seed)

        categories = [chr(65+i) for i in range(num_bars)]
        values = [random.randint(10, 100) for _ in categories]
        df = pd.DataFrame({'Category': categories, 'Value': values})

        color_scheme = random.choice(['category10', 'dark2'])
        sort = random.choice([True, False])
        orientation = random.choice(['vertical', 'horizontal'])

        if sort:
            df = df.sort_values('Value')

        if orientation == 'vertical':
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Category', sort=None),
                y='Value',
                color=alt.Color('Category', scale=alt.Scale(scheme=color_scheme))
            )
        else:
            chart = alt.Chart(df).mark_bar().encode(
                y=alt.Y('Category', sort=None),
                x='Value',
                color=alt.Color('Category', scale=alt.Scale(scheme=color_scheme))
            )

        chart = chart.properties(width=self.width, height=self.height)

        filename = f"bar_{seed}"
        self._save_chart(chart, filename)

        max_category = df.loc[df['Value'].idxmax(), 'Category']
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "bar",
            "max_category": max_category,
            "variation": {
                "color_scheme": color_scheme,
                "sorted": sort,
                "orientation": orientation,
                "num_bars": num_bars
            },
            "question": question_template,
            "answer": max_category
        }
        self._save_metadata(metadata, filename)
        return filename
    
    def generate_scatter_chart(self, seed: int = 0, num_points: int = 10, question_template: Optional[str] = "Which point is the farthest from the origin?"):
        random.seed(seed)
        np.random.seed(seed)

        points = pd.DataFrame({
            'x': np.random.uniform(-10, 10, num_points),
            'y': np.random.uniform(-10, 10, num_points),
            'label': [chr(65+i) for i in range(num_points)]
        })
        points['distance'] = np.sqrt(points['x']**2 + points['y']**2)
        farthest_label = points.loc[points['distance'].idxmax(), 'label']

        color_scheme = random.choice(['category10', 'accent'])
        shape_options = ['circle', 'square', 'triangle']
        point_shape = random.choice(shape_options)

        # 构建图表
        chart = alt.Chart(points).mark_point(filled=True, shape=point_shape).encode(
            x='x',
            y='y',
            color=alt.Color('label', scale=alt.Scale(scheme=color_scheme)),
            tooltip=['label', 'x', 'y']
        ).properties(width=self.width, height=self.height)

        filename = f"scatter_{seed}"
        self._save_chart(chart, filename)

        # 保存标注信息
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "scatter",
            "farthest_label": farthest_label,
            "variation": {
                "color_scheme": color_scheme,
                "point_shape": point_shape,
                "num_points": num_points
            },
            "question": question_template,
            "answer": farthest_label
        }
        self._save_metadata(metadata, filename)
        return filename
