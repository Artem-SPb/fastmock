import typer
import uvicorn

from fastmock.core.config import settings

app = typer.Typer(help="FastMock API Engine CLI")

@app.command()
def start(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Bind socket to this host."),
    port: int = typer.Option(8000, "--port", "-p", help="Bind socket to this port."),
    spec: str = typer.Option("openapi.yaml", "--spec", "-s", help="Path to the OpenAPI specification file."),
    persist: str = typer.Option(None, "--persist", help="Path to the JSON file for saving the database state (e.g. db.json)."),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development.")
):
    """
    Start the FastMock API Engine server.
    """
    # Update global settings based on CLI args
    settings.default_spec_path = spec
    settings.debug = reload
    if persist:
        settings.persist_path = persist

    typer.echo("=" * 50)
    typer.echo("Starting FastMock API Engine")
    typer.echo(f"➜  Local:   http://127.0.0.1:{port}/docs")
    if host == "0.0.0.0":
        typer.echo(f"➜  Network: http://<your-network-ip>:{port}/docs")
    else:
        typer.echo(f"➜  Bind:    http://{host}:{port}/docs")
    
    if persist:
        typer.echo(f"➜  Persist: {persist}")
    typer.echo("=" * 50)
        
    uvicorn.run(
        "fastmock.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    app()
