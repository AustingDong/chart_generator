import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional
from generators.generator import ChartGenerator

class StackedBarGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_series: int = 3, num_categories: int = 4,
                 question_template: Optional[str] = "Which category has the highest total value?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()

        x_label = kwargs.get("x_label") or "Category"
        series_label = kwargs.get("size_label") or "Series"
        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"Stacked Bar Chart of {values_label}"

        categories = kwargs.get("categories") or [chr(65+i) for i in range(num_categories)]
        if (len(categories) != num_categories):
            categories = [chr(65+i) for i in range(num_categories)]
        
        series = kwargs.get("series") or [f"S{i+1}" for i in range(num_series)]
        if (len(series) != num_series):
            series = [f"S{i+1}" for i in range(num_series)]

        data = []

        for cat in categories:
            for s in series:
                data.append({
                    'category': cat,
                    'series': s,
                    'value': random.randint(10, 60)
                })

        df = pd.DataFrame(data)
        agg = df.groupby('category')['value'].sum()
        max_cat = agg.idxmax()

        color_scheme = random.choice(['category10', 'set2', 'dark2'])

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('category:N', title=x_label),
            y=alt.Y('value:Q', stack='zero', title=values_label),
            color=alt.Color('series:N', scale=alt.Scale(scheme=color_scheme), title=series_label),
            tooltip=['series', 'category', 'value']
        ).properties(width=self.width, height=self.height, title=title)

        chart = chart.configure_view(
            stroke=None
        ).configure_axis(
            labelFontSize=11, titleFontSize=13,
            labelColor="#444", titleColor="#222",
            gridColor="rgba(0,0,0,0.08)"
        ).configure_legend(
            labelFontSize=11, titleFontSize=12,
            strokeColor="rgba(0,0,0,0.1)"
        )

        # 保存图像和滤镜背景
        filename = f"stacked_bar_{seed}"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(
            img_path,
            size=self.width,
            overlay_rgba=bgcolor,
            overlay_opacity=0.15
        )

        # 保存 metadata
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "stacked_bar",
            "max_category": max_cat,
            "variation": {
                "color_scheme": color_scheme,
                "num_series": num_series,
                "num_categories": num_categories
            },
            "question": question_template,
            "answer": max_cat
        }
        self._save_metadata(metadata, filename)
        return filename
