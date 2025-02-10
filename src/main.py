from search_ollama import OllamaSearchClient, OllamaSearchResult

import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
client = OllamaSearchClient()

@app.command()
def search(q: str):
    results : list[OllamaSearchResult] = client.search(q=q)
    if not results:
        return
    
    # we have some stuff to show-off
    tbl = Table(title='Ollama Model Catalog')
    tbl.add_column('Model Name', )
    tbl.add_column('Description', )
    tbl.add_column('Sizes', )
    tbl.add_column('Pulls', )
    tbl.add_column('Special', )

    for row in results:
        tbl.add_row(*row.display())
    
    console = Console()
    console.print(tbl)

if __name__ == '__main__':
    app()