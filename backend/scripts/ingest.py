"""
CLI ingestion script.
Usage:
  python -m scripts.ingest --seed
  python -m scripts.ingest --dict path/to/dictionnaire.pdf
  python -m scripts.ingest --audio path/to/bible_kabyle.mp3
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.pipeline import ingest_dictionary, ingest_audio, ingest_agro_seed_data


def main():
    parser = argparse.ArgumentParser(description="Kabyle RAG data ingestion")
    parser.add_argument("--seed", action="store_true", help="Seed base agro vocabulary")
    parser.add_argument("--dict", type=str, help="Path to French-Kabyle dictionary PDF")
    parser.add_argument("--audio", type=str, help="Path to Kabyle audio file (MP3/WAV)")
    parser.add_argument("--whisper-model", type=str, default="medium", help="Whisper model size")
    args = parser.parse_args()

    if args.seed:
        ingest_agro_seed_data()
    if args.dict:
        ingest_dictionary(args.dict)
    if args.audio:
        ingest_audio(args.audio, args.whisper_model)
    if not any([args.seed, args.dict, args.audio]):
        parser.print_help()


if __name__ == "__main__":
    main()
