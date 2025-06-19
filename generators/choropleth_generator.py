import os
import random
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from generators.generator import ChartGenerator

class ChoroplethGenerator(ChartGenerator):
    def __init__(self, output_dir: str = "./charts", img_format: str = "png", width: int = 700, height: int = 500):
        super().__init__(output_dir, img_format, width, height)

    def generate(self, seed: int = 0, question_template: str = "Which state has the highest value?", **kwargs):
        random.seed(seed)
        bgcolor = self._random_rgba()
        
        state_abbr = [
            'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
            'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
            'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
            'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
            'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
        ]

        df = pd.DataFrame({
            'state': state_abbr,
            'value': [random.randint(10, 100) for _ in state_abbr]
        })

        max_state = df.loc[df["value"].idxmax(), "state"]

        fig = px.choropleth(
            df,
            locations='state',
            locationmode="USA-states",
            color='value',
            scope="usa",
            color_continuous_scale="Blues",
            labels={'value': 'Value'}
        )

        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            locations=df['state'],
            text=df['state'],
            mode='text',
            textfont=dict(color='black', size=7, family="Arial Black"),
            showlegend=False
        ))

        fig.update_layout(
            width=self.width,
            height=self.height,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                scope="usa",
                projection=dict(type="albers usa"),
                showlakes=True,
                lakecolor="LightBlue",
                bgcolor=bgcolor,
            ),
            coloraxis_colorbar=dict(title="Value"),
            plot_bgcolor=bgcolor,
            paper_bgcolor=bgcolor,
        )

        filename = f"choropleth_{seed}"
        save_path = os.path.join(self.output_dir, f"{filename}.{self.img_format}")
        fig.write_image(save_path, width=self.width, height=self.height)
        self._make_square_padding(os.path.join(self.output_dir, 
                                               f"{filename}.{self.img_format}"), 
                                               size=self.width,
                                               overlay_rgba=bgcolor)
        metadata = {
            "filename": f"{filename}.{self.img_format}",
            "chart_type": "choropleth",
            "max_state": max_state,
            "variation": {
                "color_scheme": "Blues",
                "num_states": len(state_abbr)
            },
            "question": question_template,
            "answer": max_state
        }
        self._save_metadata(metadata, filename)
        return filename
