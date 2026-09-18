import os

os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

embedding_model = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
)
