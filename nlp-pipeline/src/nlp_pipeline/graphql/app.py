"""Flask application for GraphQL API."""

from flask import Flask, jsonify, request

from nlp_pipeline.embeddings import WordEmbeddings
from nlp_pipeline.graphql.schema import schema, set_embeddings

# Simple HTML for GraphiQL interface
GRAPHIQL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NLP Pipeline GraphQL</title>
    <link href="https://unpkg.com/graphiql/graphiql.min.css" rel="stylesheet" />
</head>
<body style="margin: 0;">
    <div id="graphiql" style="height: 100vh;"></div>
    <script crossorigin src="https://unpkg.com/react/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/graphiql/graphiql.min.js"></script>
    <script>
        const fetcher = GraphiQL.createFetcher({ url: '/graphql' });
        ReactDOM.render(
            React.createElement(GraphiQL, { fetcher: fetcher }),
            document.getElementById('graphiql'),
        );
    </script>
</body>
</html>
"""


def create_app(embeddings: WordEmbeddings | None = None) -> Flask:
    """Create Flask app with GraphQL endpoint.

    Args:
        embeddings: WordEmbeddings instance to use. If None, must call
            set_embeddings() before making queries.

    Returns:
        Flask application.
    """
    app = Flask(__name__)

    if embeddings is not None:
        set_embeddings(embeddings)

    @app.route("/graphql", methods=["GET"])
    def graphiql():
        """Serve GraphiQL interface."""
        return GRAPHIQL_HTML

    @app.route("/graphql", methods=["POST"])
    def graphql():
        """Handle GraphQL queries."""
        data = request.get_json()

        if not data:
            return jsonify({"errors": [{"message": "No query provided"}]}), 400

        query = data.get("query")
        variables = data.get("variables")
        operation_name = data.get("operationName")

        result = schema.execute(
            query,
            variables=variables,
            operation_name=operation_name,
        )

        response = {}
        if result.data:
            response["data"] = result.data
        if result.errors:
            response["errors"] = [
                {"message": str(e), "locations": e.locations, "path": e.path}
                for e in result.errors
            ]

        status = 200 if not result.errors else 400
        return jsonify(response), status

    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "ok"})

    @app.route("/")
    def index():
        """Root endpoint with API info."""
        return jsonify({
            "name": "NLP Pipeline GraphQL API",
            "version": "1.0.0",
            "endpoints": {
                "graphql": "/graphql",
                "graphiql": "/graphql (GET in browser)",
                "health": "/health",
            },
            "example_queries": {
                "info": "{ info { vocabSize dimension } }",
                "similarity": '{ similarity(word1: "king", word2: "queen") }',
                "most_similar": '{ mostSimilar(word: "king", topN: 5) { word similarity } }',
                "analogy": '{ analogy(positive: ["king", "woman"], negative: ["man"]) { word similarity } }',
            },
        })

    return app
