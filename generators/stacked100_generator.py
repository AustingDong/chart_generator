import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional
from generators.generator import ChartGenerator

class Stacked100Generator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_series: int = 3, num_categories: int = 4,
                 question_template: Optional[str] = "In which category does a segment occupy the largest proportion?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()

        x_label = kwargs.get("x_label") or "Category"
        series_label = kwargs.get("size_label") or "Series"
        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"100% Stacked Bar Chart of {values_label}"

        categories = kwargs.get("categories") or [chr(65+i) for i in range(num_categories)]
        if (len(categories) != num_categories):
            categories = [chr(65+i) for i in range(num_categories)]
        
        series = kwargs.get("series") or [f"S{i+1}" for i in range(num_series)]
        if (len(series) != num_series):
            series = [f"S{i+1}" for i in range(num_series)]

        data = []

        for cat in categories:
            proportions = [random.randint(1, 100) for _ in series]
            total = sum(proportions)
            for s, val in zip(series, proportions):
                data.append({
                    'category': cat,
                    'series': s,
                    'value': val / total
                })

        df = pd.DataFrame(data)

        # 找出最大比例 segment
        df['key'] = df['category'] + "-" + df['series']
        max_segment = df.loc[df['value'].idxmax()]
        max_cat = max_segment['category']
        max_series = max_segment['series']

        color_scheme = random.choice(['category10', 'set2', 'dark2'])

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('category:N', title=x_label),
            y=alt.Y('value:Q', stack='normalize', title=f"Proportion of {values_label}"),
            color=alt.Color('series:N', scale=alt.Scale(scheme=color_scheme), title=series_label),
            tooltip=['category', 'series', alt.Tooltip('value:Q', format=".2%")]
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
        filename = f"stacked_bar_100_{seed}"
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
            "chart_type": "stacked_bar_100",
            "max_segment": {
                "category": max_cat,
                "series": max_series
            },
            "variation": {
                "color_scheme": color_scheme,
                "num_series": num_series,
                "num_categories": num_categories
            },
            "question": question_template,
            "answer": {
                "category": max_cat,
                "series": max_series
            }
        }
        self._save_metadata(metadata, filename)
        return filename
