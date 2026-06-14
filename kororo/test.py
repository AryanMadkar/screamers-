from kokoro import KPipeline
import soundfile as sf
import os
import numpy as np
import torch
from dotenv import load_dotenv
load_dotenv()
os.environ["KOKORO_CACHE_DIR"] = "./cache"
os.environ["HF_HOME"] = "./cache"
HF_TOKEN = os.getenv("HF_TOKEN")

torch.set_num_threads(os.cpu_count())
pipeline = KPipeline(
    lang_code="a",
    repo_id="hexgrad/Kokoro-82M",
    device="cpu",
)

generator = pipeline(
    """Hello everyone...

Welcome to the future of artificial intelligence.

Today, we are going to explore something truly fascinating.""",
    voice="af_heart"
)
chunks = []

for _, _, audio in generator:
    chunks.append(audio)

final_audio = np.concatenate(chunks)

sf.write("output.wav", final_audio, 24000)