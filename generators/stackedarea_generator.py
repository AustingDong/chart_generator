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
                 question_template: Optional[str] = "Which serie has the largest total value?",
                 **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()

        data = []
        x_vals = list(range(1, num_points + 1))

        x_label = kwargs.get("x_label") or "x"
        values_label = kwargs.get("y_label") or "Value"
        series_label = kwargs.get("size_label") or "Series"
        title = kwargs.get("title") or f"Stacked Area Chart of {values_label}"

        series = kwargs.get("series") or [chr(65+i) for i in range(num_series)]
        if (len(series) != num_series):
            series = [chr(65+i) for i in range(num_series)]
        

        for se in series:
            for x in x_vals:
                data.append({
                    'x': x,
                    'serie': se,
                    'value': random.randint(10, 50)
                })

        df = pd.DataFrame(data)
        agg = df.groupby('serie')['value'].sum()
        max_se = agg.idxmax()

        color_scheme = random.choice(['category10', 'set2', 'dark2'])

        chart = alt.Chart(df).mark_area(interpolate='monotone').encode(
            x=alt.X('x:O', title=x_label),
            y=alt.Y('value:Q', title=values_label),
            color=alt.Color('serie:N', title=series_label, scale=alt.Scale(scheme=color_scheme)),
            tooltip=['serie', 'x', 'value']
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

        filename = f"StackedArea"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(
            img_path,
            size=self.width,
            overlay_rgba=bgcolor,
            overlay_opacity=0.15
        )

        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "stacked_area",
            "max_serie": max_se,
            "variation": {
                "color_scheme": color_scheme,
                "num_series": num_series,
                "num_points": num_points,
            },
            "question": question_template,
            "answer": max_se
        }
        self._save_metadata(metadata, filename)
        return filename
