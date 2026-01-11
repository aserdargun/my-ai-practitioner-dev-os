"""Main Dash application for NLP Pipeline visualization."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html
from sklearn.manifold import TSNE

from nlp_pipeline.embeddings import WordEmbeddings


def create_app(embeddings: WordEmbeddings | None = None) -> Dash:
    """Create the Dash application.

    Args:
        embeddings: Pre-loaded word embeddings. If None, uses sample data.

    Returns:
        Configured Dash application.
    """
    app = Dash(__name__, title="NLP Pipeline Dashboard")

    # Store embeddings in app
    if embeddings is None:
        embeddings = _create_sample_embeddings()

    # Pre-compute t-SNE for visualization
    tsne_df = _compute_tsne(embeddings)

    app.layout = html.Div([
        # Header
        html.Div([
            html.H1("NLP Pipeline Dashboard"),
            html.P("Explore word embeddings and semantic relationships"),
        ], className="header", style={
            "textAlign": "center",
            "padding": "20px",
            "backgroundColor": "#f8f9fa",
            "marginBottom": "20px"
        }),

        # Main content
        html.Div([
            # Left panel: Embedding visualization
            html.Div([
                html.H3("Embedding Space (t-SNE)"),
                dcc.Graph(
                    id="tsne-plot",
                    figure=_create_tsne_figure(tsne_df),
                    style={"height": "500px"}
                ),
                html.P(
                    f"Showing {len(tsne_df)} words from vocabulary",
                    style={"textAlign": "center", "color": "#666"}
                ),
            ], style={
                "width": "60%",
                "display": "inline-block",
                "verticalAlign": "top",
                "padding": "10px"
            }),

            # Right panel: Similarity search
            html.Div([
                html.H3("Similarity Search"),
                html.Div([
                    html.Label("Enter a word:"),
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="e.g., king, computer, happy",
                        style={
                            "width": "100%",
                            "padding": "10px",
                            "marginBottom": "10px",
                            "fontSize": "16px"
                        }
                    ),
                    html.Button(
                        "Find Similar",
                        id="search-button",
                        style={
                            "width": "100%",
                            "padding": "10px",
                            "backgroundColor": "#007bff",
                            "color": "white",
                            "border": "none",
                            "cursor": "pointer",
                            "fontSize": "16px"
                        }
                    ),
                ]),
                html.Div(
                    id="search-results",
                    style={"marginTop": "20px"}
                ),

                html.Hr(style={"margin": "30px 0"}),

                # Analogy solver
                html.H3("Word Analogy"),
                html.P("A is to B as C is to ?", style={"color": "#666"}),
                html.Div([
                    dcc.Input(
                        id="analogy-a",
                        type="text",
                        placeholder="king",
                        style={"width": "30%", "padding": "8px", "marginRight": "5px"}
                    ),
                    html.Span(" - ", style={"fontSize": "20px"}),
                    dcc.Input(
                        id="analogy-b",
                        type="text",
                        placeholder="man",
                        style={"width": "30%", "padding": "8px", "margin": "0 5px"}
                    ),
                    html.Span(" + ", style={"fontSize": "20px"}),
                    dcc.Input(
                        id="analogy-c",
                        type="text",
                        placeholder="woman",
                        style={"width": "30%", "padding": "8px", "marginLeft": "5px"}
                    ),
                ], style={"marginBottom": "10px"}),
                html.Button(
                    "Solve Analogy",
                    id="analogy-button",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "backgroundColor": "#28a745",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                        "fontSize": "16px"
                    }
                ),
                html.Div(
                    id="analogy-results",
                    style={"marginTop": "20px"}
                ),
            ], style={
                "width": "35%",
                "display": "inline-block",
                "verticalAlign": "top",
                "padding": "10px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "8px"
            }),
        ], style={"display": "flex", "justifyContent": "space-between"}),

        # Hidden store for embeddings data
        dcc.Store(id="embeddings-store", data={
            "vocab": embeddings.vocab[:1000],  # Limit for performance
            "dimension": embeddings.dimension
        }),
    ], style={
        "maxWidth": "1400px",
        "margin": "0 auto",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    })

    # Register callbacks
    _register_callbacks(app, embeddings)

    return app


def _create_sample_embeddings() -> WordEmbeddings:
    """Create sample embeddings for demo."""
    # Semantic categories with rough embeddings
    words: dict[str, list[float] | np.ndarray] = {
        # Royalty
        "king": [0.9, 0.1, 0.8, 0.2],
        "queen": [0.85, 0.15, 0.75, 0.3],
        "prince": [0.8, 0.2, 0.7, 0.25],
        "princess": [0.75, 0.25, 0.65, 0.35],
        "royal": [0.7, 0.3, 0.6, 0.4],
        # Gender
        "man": [0.5, 0.5, 0.9, 0.1],
        "woman": [0.5, 0.5, 0.1, 0.9],
        "boy": [0.4, 0.6, 0.85, 0.15],
        "girl": [0.4, 0.6, 0.15, 0.85],
        # Positive sentiment
        "happy": [0.2, 0.9, 0.5, 0.5],
        "joy": [0.25, 0.85, 0.55, 0.45],
        "love": [0.3, 0.8, 0.6, 0.4],
        "great": [0.35, 0.75, 0.5, 0.5],
        "wonderful": [0.28, 0.82, 0.52, 0.48],
        # Negative sentiment
        "sad": [0.8, 0.2, 0.5, 0.5],
        "angry": [0.85, 0.15, 0.55, 0.45],
        "hate": [0.9, 0.1, 0.6, 0.4],
        "terrible": [0.88, 0.12, 0.5, 0.5],
        # Technology
        "computer": [0.1, 0.5, 0.5, 0.9],
        "software": [0.15, 0.45, 0.55, 0.85],
        "programming": [0.12, 0.48, 0.52, 0.88],
        "code": [0.18, 0.42, 0.58, 0.82],
        "algorithm": [0.14, 0.46, 0.54, 0.86],
        # Nature
        "tree": [0.5, 0.5, 0.1, 0.1],
        "flower": [0.45, 0.55, 0.15, 0.15],
        "forest": [0.55, 0.45, 0.08, 0.08],
        "river": [0.48, 0.52, 0.12, 0.12],
        "mountain": [0.52, 0.48, 0.05, 0.05],
    }
    return WordEmbeddings.from_dict(words)


def _compute_tsne(embeddings: WordEmbeddings, max_words: int = 500) -> pd.DataFrame:
    """Compute t-SNE projection of embeddings."""
    words = embeddings.vocab[:max_words]
    vectors = np.array([embeddings[w] for w in words])

    n_samples = len(words)

    # t-SNE requires perplexity < n_samples
    # For very small datasets, fall back to simple 2D projection
    if n_samples < 5:
        # Use first two dimensions or PCA-like projection
        if vectors.shape[1] >= 2:
            coords = vectors[:, :2]
        else:
            coords = np.column_stack([vectors[:, 0], np.zeros(n_samples)])
    else:
        # Perplexity must be < n_samples and typically 5-50
        perplexity = min(30, max(2, (n_samples - 1) // 2))
        tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
        coords = tsne.fit_transform(vectors)

    return pd.DataFrame({
        "word": words,
        "x": coords[:, 0],
        "y": coords[:, 1]
    })


def _create_tsne_figure(df: pd.DataFrame) -> go.Figure:
    """Create t-SNE scatter plot."""
    fig = px.scatter(
        df,
        x="x",
        y="y",
        text="word",
        title="Word Embeddings Visualization"
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(size=10, color="#007bff"),
        textfont=dict(size=10)
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="t-SNE dimension 1",
        yaxis_title="t-SNE dimension 2",
        hovermode="closest"
    )

    return fig


def _register_callbacks(app: Dash, embeddings: WordEmbeddings) -> None:
    """Register Dash callbacks."""

    @app.callback(
        Output("search-results", "children"),
        Input("search-button", "n_clicks"),
        State("search-input", "value"),
        prevent_initial_call=True
    )
    def search_similar(n_clicks: int, word: str):
        if not word or word.strip() == "":
            return html.P("Please enter a word", style={"color": "#666"})

        word = word.strip().lower()

        if word not in embeddings:
            return html.P(
                f"'{word}' not in vocabulary",
                style={"color": "#dc3545"}
            )

        similar = embeddings.most_similar(word, topn=10)

        return html.Div([
            html.H4(f"Words similar to '{word}':", style={"marginBottom": "10px"}),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Word", style={"textAlign": "left", "padding": "8px"}),
                    html.Th("Similarity", style={"textAlign": "right", "padding": "8px"})
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(w, style={"padding": "8px"}),
                        html.Td(
                            f"{sim:.3f}",
                            style={"textAlign": "right", "padding": "8px"}
                        )
                    ]) for w, sim in similar
                ])
            ], style={
                "width": "100%",
                "borderCollapse": "collapse",
                "backgroundColor": "white"
            })
        ])

    @app.callback(
        Output("analogy-results", "children"),
        Input("analogy-button", "n_clicks"),
        State("analogy-a", "value"),
        State("analogy-b", "value"),
        State("analogy-c", "value"),
        prevent_initial_call=True
    )
    def solve_analogy(n_clicks: int, word_a: str, word_b: str, word_c: str):
        if not all([word_a, word_b, word_c]):
            return html.P("Please fill in all fields", style={"color": "#666"})

        word_a = word_a.strip().lower()
        word_b = word_b.strip().lower()
        word_c = word_c.strip().lower()

        missing = [w for w in [word_a, word_b, word_c] if w not in embeddings]
        if missing:
            return html.P(
                f"Words not in vocabulary: {', '.join(missing)}",
                style={"color": "#dc3545"}
            )

        try:
            results = embeddings.analogy(
                positive=[word_a, word_c],
                negative=[word_b],
                topn=5
            )

            return html.Div([
                html.H4(
                    f"{word_a} - {word_b} + {word_c} = ?",
                    style={"marginBottom": "10px"}
                ),
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("Answer", style={"textAlign": "left", "padding": "8px"}),
                        html.Th("Score", style={"textAlign": "right", "padding": "8px"})
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td(
                                w,
                                style={
                                    "padding": "8px",
                                    "fontWeight": "bold" if i == 0 else "normal"
                                }
                            ),
                            html.Td(
                                f"{sim:.3f}",
                                style={"textAlign": "right", "padding": "8px"}
                            )
                        ]) for i, (w, sim) in enumerate(results)
                    ])
                ], style={
                    "width": "100%",
                    "borderCollapse": "collapse",
                    "backgroundColor": "white"
                })
            ])
        except Exception as e:
            return html.P(f"Error: {str(e)}", style={"color": "#dc3545"})


def run_dashboard(
    embeddings: WordEmbeddings | None = None,
    debug: bool = True,
    port: int = 8050
) -> None:
    """Run the dashboard server.

    Args:
        embeddings: Word embeddings to visualize.
        debug: Enable debug mode.
        port: Port to run server on.
    """
    app = create_app(embeddings)
    print(f"Starting dashboard at http://localhost:{port}")
    app.run(debug=debug, port=str(port))


if __name__ == "__main__":
    run_dashboard()
