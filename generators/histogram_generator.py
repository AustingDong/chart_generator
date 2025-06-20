import os
import random
import json
import pandas as pd
import altair as alt
from typing import Optional
from generators.generator import ChartGenerator

class HistogramGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 300, height: int = 300):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, num_bins: int = 10, num_values: int = 100,
                 distribution: str = "gaussian",
                 question_template: Optional[str] = "Which bin has the most values?", **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()
        values_label = kwargs.get("y_label") or "Value"
        title = kwargs.get("title") or f"Histogram of {values_label}"

        if distribution == "gaussian":
            values = [random.gauss(50, 15) for _ in range(num_values)]
        elif distribution == "uniform":
            values = [random.uniform(0, 100) for _ in range(num_values)]
        elif distribution == "exponential":
            values = [random.expovariate(1 / 30) for _ in range(num_values)]
        elif distribution == "bimodal":
            values = [
                random.gauss(30, 5) if i < num_values // 2 else random.gauss(70, 5)
                for i in range(num_values)
            ]
        else:
            raise ValueError(f"Unsupported distribution type: {distribution}")

        df = pd.DataFrame({'value': values})


        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('value:Q', bin=alt.Bin(maxbins=num_bins), title=values_label),
            y=alt.Y('count()', title="Frequency"),
            tooltip=['count()']
        ).properties(width=self.width, height=self.height, title=title)

        chart = chart.configure_view(
            stroke=None
        ).configure_axis(
            labelFontSize=11, titleFontSize=13,
            labelColor="#444", titleColor="#222",
            gridColor="rgba(0,0,0,0.08)"
        )

        filename = f"histogram_{seed}"
        self._save_chart(chart, filename)
        img_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        self._make_square_padding(
            img_path,
            size=self.width,
            overlay_rgba=bgcolor,
            overlay_opacity=0.15
        )

        bins = pd.cut(df['value'], bins=num_bins)
        bin_counts = bins.value_counts().sort_values(ascending=False)
        max_bin = str(bin_counts.index[0])

        # Save metadata
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "histogram",
            "max_bin": max_bin,
            "variation": {
                "num_bins": num_bins,
                "num_values": num_values,
                "distribution": distribution
            },
            "question": question_template,
            "answer": max_bin
        }
        self._save_metadata(metadata, filename)
        return filename
