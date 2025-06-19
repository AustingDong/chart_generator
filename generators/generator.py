import os
import random
import json
import numpy as np
import pandas as pd
import altair as alt
from typing import Optional, Dict, Any
from PIL import Image

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

    def _random_rgba(self, alpha: float = 1.0) -> str:
        r = random.randint(220, 255)
        g = random.randint(220, 255)
        b = random.randint(220, 255)
        return f"rgba({r},{g},{b},{alpha})"
    
    def _rgba_str_to_tuple(self, rgba: str) -> tuple:
        rgba = rgba.replace("rgba(", "").replace(")", "")
        r, g, b, a = map(float, rgba.split(","))
        return int(r), int(g), int(b), float(a)
    
    def _make_square_padding(self, img_path: str, save_path: Optional[str] = None,
                              size: int = 224, 
                              overlay_rgba: Optional[str] = None, overlay_opacity: float = 0.15):
        img = Image.open(img_path).convert("RGBA")
        w, h = img.size
        dim = max(size, w, h)

        result = Image.new("RGBA", (dim, dim), (255, 255, 255, 255))

        paste_x = (dim - w) // 2
        paste_y = (dim - h) // 2
        result.paste(img, (paste_x, paste_y), img)

        # background
        if overlay_rgba is not None:
            r, g, b, a = self._rgba_str_to_tuple(overlay_rgba)
            overlay = Image.new("RGBA", (dim, dim), (r, g, b, int(255 * overlay_opacity)))
            result = Image.alpha_composite(result, overlay)

        if save_path is None:
            save_path = img_path

        # Saves RGB
        result.convert("RGB").save(save_path)

    def generate(*args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")
    