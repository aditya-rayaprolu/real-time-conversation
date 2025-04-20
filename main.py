import asyncio
from stt_stream import run_stt_stream
from audio_capture import close_audio

async def main():
    try:
        await run_stt_stream()
    except KeyboardInterrupt:
        print("\nUser stopped conversation.")
    finally:
        close_audio()

if __name__ == "__main__":
    asyncio.run(main())