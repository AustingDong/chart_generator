import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional
from generators.generator import ChartGenerator

class StackedAreaGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_series: int = 3, num_points: int = 10,
                 question_template: Optional[str] = "Which category has the largest total value?"):
        random.seed(seed)
        bgcolor = self._random_rgba()

        # 构造数据
        data = []
        x_vals = list(range(1, num_points + 1))
        categories = [chr(65 + i) for i in range(num_series)]

        for cat in categories:
            for x in x_vals:
                data.append({
                    'x': x,
                    'category': cat,
                    'value': random.randint(10, 50)
                })

        df = pd.DataFrame(data)
        agg = df.groupby('category')['value'].sum()
        max_cat = agg.idxmax()

        color_scheme = random.choice(['category10', 'set2', 'dark2'])

        chart = alt.Chart(df).mark_area(interpolate='monotone').encode(
            x='x:O',
            y='value:Q',
            color=alt.Color('category:N', scale=alt.Scale(scheme=color_scheme)),
            tooltip=['category', 'x', 'value']
        ).properties(width=self.width, height=self.height)

        # 添加美化风格
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

        # 保存图和填充背景
        filename = f"stacked_area_{seed}"
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
            "chart_type": "stacked_area",
            "max_category": max_cat,
            "variation": {
                "color_scheme": color_scheme,
                "num_series": num_series,
                "num_points": num_points,
            },
            "question": question_template,
            "answer": max_cat
        }
        self._save_metadata(metadata, filename)
        return filename
