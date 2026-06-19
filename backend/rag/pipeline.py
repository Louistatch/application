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
    """Seed the agro collection with core Kabyè agricultural vocabulary (Togo)."""
    agro_data = [
        ("Ignames (ñûmŸ) — culture principale des Kabyè. Plantation: mars-avril (LAKòò - ɔOMAŋ). Récolte: octobre-novembre (ALOMA - KAMèò). Variétés locales: kokoro, kponan, florido.", {"topic": "igname"}),
        ("Sorgho et mil (Kabyè: céréales principales). Semailles: mai-juin (AGOZA - MòSòGúM). Récolte: septembre-octobre (SALAò - ALOMA). Base alimentaire des Kabyè.", {"topic": "cereales"}),
        ("Maïs (Kabyè: deux saisons). 1ère saison: semailles avril (ɔOMAŋ), récolte juillet (HASòYAɔè). 2e saison: semailles août (KòYèNA), récolte novembre (KAMèò).", {"topic": "mais"}),
        ("Haricots et niébé (Kabyè: légumineuses locales). Semailles avec les céréales. Fixent l'azote dans le sol. Culture associée fréquente avec maïs et sorgho.", {"topic": "legumineuses"}),
        ("Arachides (Kabyè: culture de rente). Semailles début saison des pluies (AGOZA/Mai). Récolte septembre (SALAò). Transformation en huile et pâte.", {"topic": "arachides"}),
        ("Coton (Kabyè: culture principale de rente, région KOZAH et BINAH). Semailles mai-juin. Récolte novembre-décembre. Vendu à la SOTOCO (société cotonnière Togo).", {"topic": "coton"}),
        ("Soja (Kabyè: culture en développement). Semailles mai (AGOZA). Récolte août-septembre. Bon fixateur d'azote. Marché en croissance au Togo.", {"topic": "soja"}),
        ("Irrigation Kabyè: rivières Kara et tributaires. Maraîchage en saison sèche (KüLAŋ à LAKòò = janvier à mars) le long des berges. Oignons, tomates, piments.", {"topic": "irrigation"}),
        ("Fumure et compost Kabyè: utilisation des résidus de récolte. Fumier de bœuf et petit bétail. Pratique du zaï (poquets enrichis) pour améliorer la fertilité.", {"topic": "fertilisation"}),
        ("Maladies cultures Kabyè: Striure du maïs (virus). Rouille du sorgho. Mildiou. Foreur des tiges (Busseola fusca). Traitement: insecticides bio, variétés résistantes.", {"topic": "phytosanitaire"}),
        ("Marchés agricoles Kabyè: cycle de 7 jours. Marchés importants: Kara (quotidien), Piyà (Lundi/Hodo), Kozah (cycle KujukŸ). Vente ignames, céréales, légumes, bétail.", {"topic": "marches"}),
        ("Outillage agricole traditionnel Kabyè: daba (houe), pioche, machette. Labour attelé (bœufs) en développement. Stockage en grenier (siloproblèmes aflatoxine).", {"topic": "outillage"}),
        ("Jachère Kabyè: pratique de rotation terres/jachère pour régénération. Durée: 2-3 ans. Menacée par pression foncière. Agroforesterie comme alternative.", {"topic": "jachère"}),
        ("Élevage associé agriculture Kabyè: bovins, caprins, ovins, volailles. Fumier valorisé. Vente au marché de Kara. Période de soudure (juillet-août): pression sur stocks.", {"topic": "elevage"}),
        ("Calendrier des marchés hebdomadaires région KOZAH: KujukŸ(Dim)=Yàndÿ/Somdinà/Làzà. Hodo(Lun)=Piyà/Càƒÿ. CùlŸ(Mer)=Kàyàŋ/Sàràkàwàŋ. MàzàŋSam=Làzà/Làmà/PiyàLàw.", {"topic": "marches_kozah"}),
    ]
    retriever = KabyleRetriever()
    texts = [d[0] for d in agro_data]
    metadatas = [d[1] for d in agro_data]
    ids = [str(uuid.uuid4()) for _ in agro_data]
    count = retriever.add_documents("kabyle_agro", texts, metadatas, ids)
    print(f"Seeded {count} agro vocabulary entries.")
