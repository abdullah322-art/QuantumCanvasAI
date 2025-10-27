from __future__ import annotations

import io
import math
import struct
import wave
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import Response


router = APIRouter(prefix="/v1/voice", tags=["voice"])


def _synthesize_wave(text: str, sample_rate: int = 16000) -> bytes:
    """Generate a simple sine-tone WAV that encodes characters as tones.

    This is a tiny placeholder without external deps so the endpoint works on
    Render out-of-the-box. Replace with a real TTS provider later.
    """
    duration_per_char = 0.06
    amplitude = 16000

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        frames: list[bytes] = []
        for ch in text or "QCA":
            freq = 440 + (ord(ch) % 32) * 12
            num_samples = int(sample_rate * duration_per_char)
            for n in range(num_samples):
                val = int(amplitude * math.sin(2 * math.pi * freq * (n / sample_rate)))
                frames.append(struct.pack('<h', val))
        wf.writeframes(b"".join(frames))
    return buf.getvalue()


@router.get("/synthesize")
def synthesize(text: Annotated[str | None, Query(max_length=200)] = None):
    data = _synthesize_wave(text or "QCA")
    return Response(content=data, media_type="audio/wav")

