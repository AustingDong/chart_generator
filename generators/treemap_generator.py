import os
import random
import json
import pandas as pd
import plotly.express as px
from typing import Optional
from generators.generator import ChartGenerator

class TreeMapGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 500, height: int = 500):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_categories: int = 6,
                 question_template: Optional[str] = "Which category occupies the largest area?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()

        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"Tree map of {values_label}"
        categories = kwargs.get("categories") or [chr(65+i) for i in range(num_categories)]
        if (len(categories) != num_categories):
            categories = [chr(65+i) for i in range(num_categories)]
        
        values = [random.randint(10, 100) for _ in categories]
        df = pd.DataFrame({'category': categories, 'value': values})
        max_category = df.loc[df['value'].idxmax(), 'category']

        fig = px.treemap(
            df,
            path=['category'],
            values='value',
            color='category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(
            width=self.width,
            height=self.height,
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor,
            font=dict(family="Open Sans", size=12, color="black"),
            uniformtext=dict(minsize=10, mode='hide'),
            title=dict(
                text=title,
                font=dict(size=16, family="Arial Black"),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        filename = f"TreeMap"
        save_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        fig.write_image(save_path, width=self.width, height=self.height)

        self._make_square_padding(
            save_path,
            size=self.width,
            overlay_rgba=None
        )

        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "treemap",
            "max_category": max_category,
            "variation": {
                "num_categories": num_categories,
                "background_color": bgcolor
            },
            "question": question_template,
            "answer": max_category
        }
        self._save_metadata(metadata, filename)
        return filename
