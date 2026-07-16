from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct

from app.core.settings import settings



class QdrantService:

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL
        )

    def create_collection(self):

        collections = self.client.get_collections()

        names = [
            collection.name
            for collection in collections.collections
        ]

        if settings.QDRANT_COLLECTION in names:
            return

        self.client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )
        
    def store_vector(
        self,
        point_id: int,
        embedding: list,
        payload: dict
    ):

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        
        
    def search(
        self,
        embedding: list,
        top_k: int = 5
    ):

        response = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=embedding,
            limit=top_k
        )

        return response.points