"""GraphQL API for NLP Pipeline embeddings."""

from nlp_pipeline.graphql.app import create_app
from nlp_pipeline.graphql.schema import schema

__all__ = ["create_app", "schema"]
