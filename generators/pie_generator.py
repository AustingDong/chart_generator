import os
import random
import json
import numpy as np
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from generators.generator import ChartGenerator

class PieGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 200):
        super().__init__(output_dir, img_format, width, height)
    
    def generate(self, seed: int = 0, num_slices: int = 4, question_template: Optional[str] = "Which category has the largest proportion?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()
        
        category_label = kwargs.get("x_label") or "Category"
        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"Pie Chart of {values_label}"
        categories = kwargs.get("categories") or [chr(65+i) for i in range(num_slices)]
        if (len(categories) != num_slices):
            categories = [chr(65+i) for i in range(num_slices)]

        values = [random.randint(10, 100) for _ in categories]
        df = pd.DataFrame({'Category': categories, 'Value': values})
        df['Percentage'] = df['Value'] / df['Value'].sum()

        color_scheme = random.choice(['category10', 'set2'])

        chart = alt.Chart(df).mark_arc(innerRadius=0).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color("Category", title=category_label, scale=alt.Scale(scheme=color_scheme)),
            tooltip=["Category", "Value"]
        ).properties(width=self.width, height=self.height, title=title).configure_view(stroke=None)

        filename = f"pie_{seed}"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)

        max_category = df.loc[df['Value'].idxmax(), 'Category']
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "pie",
            "max_category": max_category,
            "variation": {
                "color_scheme": color_scheme,
                "num_slices": num_slices
            },
            "question": question_template,
            "answer": max_category
        }
        self._save_metadata(metadata, filename)
        return filename

