import asyncio
import websockets
import json
import pyaudio

# Deepgram config
DEEPGRAM_API_KEY = "dc834953c96279787af5494a868bec58ea58df38"
DG_ENDPOINT = (
    "wss://api.deepgram.com/v1/listen"
    "?encoding=linear16"
    "&channels=1"
    "&sample_rate=16000"
    "&punctuate=true"
    "&interim_results=true"
)

# Audio config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

async def run_stt_stream():
    async with websockets.connect(
        DG_ENDPOINT,
        extra_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"}
    ) as ws:
        print("Connected to Deepgram.")
        while True:
            # Read a chunk of audio
            chunk = stream.read(CHUNK, exception_on_overflow=False)
            # Send it as binary
            await ws.send(chunk)

            try:
                response = await asyncio.wait_for(ws.recv(), timeout=0.05)
                data = json.loads(response)
                handle_deepgram_response(data)
            except asyncio.TimeoutError:
                # No transcript this moment, continue
                pass

current_partial = ""

def handle_deepgram_response(data):
    global current_partial
    if "channel" not in data or "alternatives" not in data["channel"]:
        return
    alt = data["channel"]["alternatives"][0]
    transcript = alt.get("punctuated_transcript", "")
    is_final = alt.get("final", False)

    if is_final:
        print(f"\n[User Final] {transcript}")
        # Next: pass to GPT or whatever logic
        current_partial = ""
    else:
        current_partial = transcript
        # Overwrite partial
        print("[User Partial]", transcript)

async def main():
    try:
        await run_stt_stream()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    asyncio.run(main())