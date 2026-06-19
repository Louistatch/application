"""
Data ingestion pipeline.
Run once: python -m scripts.ingest --dict path/to/dict.pdf --audio path/to/bible.mp3
"""
import re
import uuid
from pathlib import Path

import fitz  # PyMuPDF

from rag.retriever import KabyleRetriever, COLLECTION_DICT, COLLECTION_BIBLE


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
        i += chunk_size - overlap
    return chunks


def extract_pdf_dictionary(pdf_path: str) -> list[dict]:
    """Extract entries from a French-Kabyle dictionary PDF."""
    doc = fitz.open(pdf_path)
    entries = []
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Split by newlines and group into entries
    lines = [l.strip() for l in full_text.split("\n") if l.strip()]
    chunks = chunk_text(" ".join(lines), chunk_size=200, overlap=30)

    for i, chunk in enumerate(chunks):
        entries.append({
            "text": chunk,
            "metadata": {"source": "dictionary", "chunk_id": i, "file": pdf_path},
        })
    return entries


def transcribe_audio(audio_path: str, model_size: str = "medium") -> str:
    """Transcribe Kabyle audio using Whisper."""
    import whisper
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language="fr")  # closest supported, will still capture kabyle phonemes
    return result["text"]


def ingest_dictionary(pdf_path: str):
    retriever = KabyleRetriever()
    print(f"Extracting dictionary from {pdf_path}...")
    entries = extract_pdf_dictionary(pdf_path)
    texts = [e["text"] for e in entries]
    metadatas = [e["metadata"] for e in entries]
    ids = [str(uuid.uuid4()) for _ in entries]
    count = retriever.add_documents(COLLECTION_DICT, texts, metadatas, ids)
    print(f"Indexed {count} dictionary chunks.")


def ingest_audio(audio_path: str, whisper_model: str = "medium"):
    retriever = KabyleRetriever()
    print(f"Transcribing audio {audio_path} with Whisper {whisper_model}...")
    text = transcribe_audio(audio_path, whisper_model)
    chunks = chunk_text(text, chunk_size=200, overlap=30)
    metadatas = [{"source": "bible_audio", "chunk_id": i, "file": audio_path} for i in range(len(chunks))]
    ids = [str(uuid.uuid4()) for _ in chunks]
    count = retriever.add_documents(COLLECTION_BIBLE, chunks, metadatas, ids)
    print(f"Indexed {count} Bible transcript chunks.")


def ingest_agro_seed_data():
    """Seed the agro collection with core Kabyle agricultural vocabulary."""
    agro_data = [
        ("Aẓar (racine) / Tafekka (souche)", {"topic": "anatomie_plante"}),
        ("Azemmur (olivier) - arbre emblématique de Kabylie. Taqlit n uzemmur = feuille d'olivier.", {"topic": "arbre_fruitier"}),
        ("Ithran (figuier) - Tha'ourt = figue. Récolte en août-septembre.", {"topic": "arbre_fruitier"}),
        ("Amzur (vigne) / Aẓyul (raisin). Récolte en septembre.", {"topic": "vigne"}),
        ("Amezruy n tsekla (histoire du jardinage): rotation des cultures = tamsettit n yibuyaden", {"topic": "technique_culture"}),
        ("Aman (eau) - irrigation: aseggaẓ n iman. Arrosage goutte à goutte = aman wis wis.", {"topic": "irrigation"}),
        ("Aberchum (compost) - engrais naturel. Aserreḥ n wakal = fertilisation du sol.", {"topic": "fertilisation"}),
        ("Tafat (soleil) - exposition. Timura tikerrist = terres exposées au sud.", {"topic": "exposition"}),
        ("Iḥenjiren (plants / semis). Asemli (graine/semence). Azag (sillon).", {"topic": "semis"}),
        ("Agerdal (jardin potager). Aḥric (parcelle). Azagur (champ cultivé).", {"topic": "espace_culture"}),
        ("Taɣellist (maladie / parasite). Izerman (insectes ravageurs). Tazart (ver).", {"topic": "phytosanite"}),
        ("Tamacahutt n wakal Aqbayli: rotation triannuelle - froment / légumineuses / jachère.", {"topic": "savoir_ancestral"}),
        ("Ifeggagen (pois chiches) - Ibawen (fèves) - Tiẓumert (lentilles). Légumineuses kabyliennes.", {"topic": "legumineuses"}),
        ("Tameddit n unebdu (calendrier agricole): Mars-Avril = semailles de printemps. Octobre = labours.", {"topic": "calendrier"}),
        ("Aberru (taille / élagage). Aberru n uzemmur = taille de l'olivier. Techniques traditionnelles kabyles.", {"topic": "taille"}),
    ]
    retriever = KabyleRetriever()
    texts = [d[0] for d in agro_data]
    metadatas = [d[1] for d in agro_data]
    ids = [str(uuid.uuid4()) for _ in agro_data]
    count = retriever.add_documents("kabyle_agro", texts, metadatas, ids)
    print(f"Seeded {count} agro vocabulary entries.")
