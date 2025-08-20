# src/agents/semantic_agent.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class SemanticSearchAgent:
    def __init__(self, canonical_names: List[str]):
        print("SemanticSearchAgent: Initializing and loading model... (this may take a moment)")
        # This model is small and efficient
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.canonical_names = canonical_names
        # Pre-calculating embeddings is key for performance
        self.canonical_embeddings = self.model.encode(self.canonical_names)
        print("SemanticSearchAgent: Model and embeddings are ready.")

    def find_best_match(self, user_input: str) -> Dict:
        """Finds the best match based on semantic meaning."""
        input_embedding = self.model.encode([user_input])
        similarities = cosine_similarity(input_embedding, self.canonical_embeddings)
        best_match_index = similarities.argmax()
        return {
            "best_match_semantic": self.canonical_names[best_match_index],
            "score_semantic": similarities[0, best_match_index]
        }