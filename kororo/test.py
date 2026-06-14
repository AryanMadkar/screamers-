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
    lang_code="h",
    repo_id="hexgrad/Kokoro-82M",
    device="cpu",
)

generator = pipeline(
    """नमस्कार दोस्तों। आज हम कृत्रिम बुद्धिमत्ता के भविष्य के बारे में बात करेंगे।""",
    voice="hf_alpha"
)
chunks = []

for _, _, audio in generator:
    chunks.append(audio)

final_audio = np.concatenate(chunks)

sf.write("houtput.wav", final_audio, 24000)