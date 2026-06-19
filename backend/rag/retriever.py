from rag.embeddings import get_or_create_collection

COLLECTION_DICT = "kabye_dictionary"
COLLECTION_BIBLE = "kabye_bible"
COLLECTION_AGRO = "kabye_agro"


class KabyeRetriever:
    def __init__(self):
        self._collections = None

    @property
    def collections(self):
        if self._collections is None:
            self._collections = {
                "dict": get_or_create_collection(COLLECTION_DICT),
                "bible": get_or_create_collection(COLLECTION_BIBLE),
                "agro": get_or_create_collection(COLLECTION_AGRO),
            }
        return self._collections

    def retrieve(self, query: str, n_results: int = 5) -> list[dict]:
        results = []
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                if count == 0:
                    continue
                res = collection.query(
                    query_texts=[query],
                    n_results=min(n_results, count),
                    include=["documents", "metadatas", "distances"],
                )
                for doc, meta, dist in zip(
                    res["documents"][0],
                    res["metadatas"][0],
                    res["distances"][0],
                ):
                    results.append({
                        "content": doc,
                        "source": name,
                        "metadata": meta,
                        "score": 1 - dist,
                    })
            except Exception:
                continue

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:n_results]

    def add_documents(self, collection_name: str, texts: list[str], metadatas: list[dict], ids: list[str]):
        collection = get_or_create_collection(collection_name)
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
        return len(texts)
