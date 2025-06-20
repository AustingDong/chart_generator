import os
import random
import json
import numpy as np
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from generators.generator import ChartGenerator

class BarGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 200):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_bars: int = 4, 
                 question_template: Optional[str] = "Which category has the highest value?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()

        x_label = kwargs.get("x_label") or "Category"
        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"Bar Chart of {values_label}"
        categories = kwargs.get("categories") or [chr(65+i) for i in range(num_bars)]
        if (len(categories) != num_bars):
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
                x=alt.X('Category', title=x_label, sort=None),
                y=alt.Y("Value:Q", title=values_label),
                color=alt.Color('Category', title=x_label, scale=alt.Scale(scheme=color_scheme))
            )
        else:
            chart = alt.Chart(df).mark_bar().encode(
                y=alt.Y('Category', title=x_label, sort=None),
                x=alt.X('Value:Q', title=values_label),
                color=alt.Color('Category', title=x_label, scale=alt.Scale(scheme=color_scheme))
            )

        chart = chart.properties(width=self.width, height=self.height, title=title).configure_view(stroke=None)

        filename = f"BarChart"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)

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
