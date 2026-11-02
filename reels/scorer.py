"""CLIP frame scorer: how likely is a tarantula visible in each frame.

Needs torch + transformers + pillow (run it where those exist, e.g. the
a venv with PyTorch). Checked on 77 frames from one enclosure (CLIP
ViT-L/14): >0.8 clear spider, 0.5-0.8 mixed, <0.5 empty; small spiders at the
hide entrance can score near 0 (missed).
"""
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL = "openai/clip-vit-large-patch14"
POS = ["a photo of a tarantula on the ground", "a hairy spider walking in a terrarium"]
NEG = ["an empty terrarium with no animal", "a dark empty enclosure",
       "a terrarium hide and substrate, no spider"]


def _feat(out):
    out = getattr(out, "pooler_output", out)  # transformers 5 returns an output object
    return out / out.norm(dim=-1, keepdim=True)


class ClipScorer:
    def __init__(self, device=None):
        if device:
            self.dev = device
        elif torch.cuda.is_available():
            self.dev = "cuda"
        elif hasattr(torch, "xpu") and torch.xpu.is_available():  # Intel Arc (Arc GPU)
            self.dev = "xpu"
        else:
            self.dev = "cpu"
        dt = torch.float32 if self.dev == "cpu" else torch.float16
        self.dt = dt
        self.model = CLIPModel.from_pretrained(MODEL, torch_dtype=dt).to(self.dev).eval()
        self.proc = CLIPProcessor.from_pretrained(MODEL)
        with torch.no_grad():
            t = self.proc(text=POS + NEG, return_tensors="pt", padding=True).to(self.dev)
            self.text = _feat(self.model.get_text_features(**t))

    @staticmethod
    def views(im, zoom):
        """Square crops. CLIP resizes to 224 and centre-crops, so a 16:9 frame fed whole
        loses its left and right edges and shrinks a small spider to a few pixels.
        wide: 3 full-height squares cover the whole width. zoom: half-height squares on a grid."""
        w, h = im.size
        side = h // 2 if zoom else h
        nx = max(1, round((w - side) / (side / 2)) + 1) if zoom else 3
        ny = 3 if zoom else 1
        xs = [round(i * (w - side) / (nx - 1)) for i in range(nx)] if nx > 1 else [0]
        ys = [round(j * (h - side) / (ny - 1)) for j in range(ny)] if ny > 1 else [0]
        return [im.crop((x, y, x + side, y + side)) for y in ys for x in xs]

    def score(self, paths, zoom=False, batch=32):
        """Per-frame spider probability: the best of all views of that frame."""
        out = []
        with torch.no_grad():
            for p in paths:
                ims = self.views(Image.open(p).convert("RGB"), zoom)
                best = 0.0
                for i in range(0, len(ims), batch):
                    px = self.proc(images=ims[i:i + batch], return_tensors="pt")["pixel_values"].to(self.dev, self.dt)
                    pr = (100 * _feat(self.model.get_image_features(pixel_values=px)) @ self.text.T).float().softmax(-1)
                    best = max(best, pr[:, :len(POS)].sum(-1).max().item())
                out.append(best)
        return out
