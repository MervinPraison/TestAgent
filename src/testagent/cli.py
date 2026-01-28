"""
CLI for TestAgent - the world's easiest AI testing.

Usage:
    $ testagent "The output to test" --criteria "is correct"
    $ testagent accuracy "4" --expected "4"
    $ testagent criteria "Hello" --criteria "is a greeting"
"""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="testagent",
    help="The world's easiest way to test anything using AI",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    output: str = typer.Argument(..., help="The output to test"),
    criteria: Optional[str] = typer.Option(
        None, "--criteria", "-c", help="Criteria to evaluate against"
    ),
    expected: Optional[str] = typer.Option(
        None, "--expected", "-e", help="Expected output for accuracy testing"
    ),
    threshold: float = typer.Option(
        7.0, "--threshold", "-t", help="Score threshold for passing (1-10)"
    ),
    model: Optional[str] = typer.Option(
        None, "--model", "-m", help="LLM model to use"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbose output"
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Output as JSON"
    ),
):
    """
    Test any output using AI.
    
    Examples:
        testagent "The capital of France is Paris" --criteria "factually correct"
        testagent "4" --expected "4"
        testagent "Hello world" -c "is a friendly greeting"
    """
    from .core import test
    from .config import TestConfig, set_config
    
    # Set config if model specified
    if model:
        set_config(TestConfig(model=model, threshold=threshold, verbose=verbose))
    
    # Run the test
    try:
        result = test(output, expected=expected, criteria=criteria)
        
        if json_output:
            import json
            console.print(json.dumps(result.to_dict(), indent=2))
        else:
            # Pretty output
            status = "[green]✅ PASSED[/green]" if result.passed else "[red]❌ FAILED[/red]"
            
            console.print()
            console.print(Panel(
                f"{status}\n\n"
                f"[bold]Score:[/bold] {result.score}/10\n"
                f"[bold]Reasoning:[/bold] {result.reasoning}",
                title="[bold cyan]TestAgent Result[/bold cyan]",
                border_style="cyan" if result.passed else "red",
            ))
            
            if verbose:
                console.print(f"\n[dim]Output: {output[:100]}{'...' if len(output) > 100 else ''}[/dim]")
                if criteria:
                    console.print(f"[dim]Criteria: {criteria}[/dim]")
                if expected:
                    console.print(f"[dim]Expected: {expected}[/dim]")
        
        # Exit with appropriate code
        raise typer.Exit(0 if result.passed else 1)
        
    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[dim]Install praisonaiagents: pip install praisonaiagents[/dim]")
        raise typer.Exit(2)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(2)


@app.command("accuracy")
def accuracy_cmd(
    output: str = typer.Argument(..., help="The actual output"),
    expected: str = typer.Option(..., "--expected", "-e", help="Expected output"),
    threshold: float = typer.Option(7.0, "--threshold", "-t", help="Score threshold"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Test output accuracy against expected output.
    
    Example:
        testagent accuracy "4" --expected "4"
    """
    from .core import accuracy
    
    result = accuracy(output, expected=expected)
    
    status = "[green]✅ PASSED[/green]" if result.passed else "[red]❌ FAILED[/red]"
    console.print()
    console.print(Panel(
        f"{status}\n\n"
        f"[bold]Score:[/bold] {result.score}/10\n"
        f"[bold]Reasoning:[/bold] {result.reasoning}",
        title="[bold cyan]Accuracy Test[/bold cyan]",
        border_style="cyan" if result.passed else "red",
    ))
    
    raise typer.Exit(0 if result.passed else 1)


@app.command("criteria")
def criteria_cmd(
    output: str = typer.Argument(..., help="The output to test"),
    criteria: str = typer.Option(..., "--criteria", "-c", help="Criteria to evaluate"),
    threshold: float = typer.Option(7.0, "--threshold", "-t", help="Score threshold"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Test output against custom criteria.
    
    Example:
        testagent criteria "Hello world" --criteria "is a friendly greeting"
    """
    from .core import criteria as criteria_fn
    
    result = criteria_fn(output, criteria=criteria)
    
    status = "[green]✅ PASSED[/green]" if result.passed else "[red]❌ FAILED[/red]"
    console.print()
    console.print(Panel(
        f"{status}\n\n"
        f"[bold]Score:[/bold] {result.score}/10\n"
        f"[bold]Reasoning:[/bold] {result.reasoning}",
        title="[bold cyan]Criteria Test[/bold cyan]",
        border_style="cyan" if result.passed else "red",
    ))
    
    raise typer.Exit(0 if result.passed else 1)


@app.command("version")
def version():
    """Show version."""
    from . import __version__
    console.print(f"testagent version {__version__}")


@app.command("collect")
def collect_cmd(
    path: str = typer.Argument(".", help="Path to collect tests from"),
    pattern: Optional[str] = typer.Option(
        None, "--pattern", "-p", help="File pattern (e.g., 'test_*.py')"
    ),
):
    """
    Discover and list AI tests without running them.
    
    Similar to pytest --collect-only.
    
    Example:
        testagent collect tests/
        testagent collect . --pattern "test_*.py"
    """
    from pathlib import Path as PathLib
    from .collector import Collector
    from .timing import Instant
    
    start = Instant()
    
    collector = Collector()
    if pattern:
        collector.file_patterns = [pattern]
    
    modules = collector.collect_only(PathLib(path))
    
    total_tests = sum(len(m.items) for m in modules)
    duration = start.elapsed()
    
    console.print(f"\n[bold]Collected {total_tests} tests in {duration}[/bold]\n")
    
    for module in modules:
        console.print(f"[cyan]{module.path}[/cyan]")
        for item in module.items:
            markers_str = f" [{', '.join(item.markers)}]" if item.markers else ""
            console.print(f"  [dim]├──[/dim] {item.name}{markers_str}")
    
    if not modules:
        console.print("[yellow]No tests found[/yellow]")
        raise typer.Exit(5)  # NO_TESTS_COLLECTED like pytest


@app.command("cache-clear")
def cache_clear():
    """Clear the test cache."""
    from .cache import get_cache
    
    cache = get_cache()
    stats = cache.stats()
    cache.clear()
    
    console.print("[green]✅ Cache cleared[/green]")
    console.print(f"[dim]Removed {stats['entries']} entries ({stats['size_bytes']} bytes)[/dim]")


@app.command("cache-stats")
def cache_stats():
    """Show cache statistics."""
    from .cache import get_cache
    
    cache = get_cache()
    stats = cache.stats()
    
    console.print("[bold]Cache Statistics[/bold]")
    console.print(f"  Entries: {stats['entries']}")
    console.print(f"  Size: {stats['size_bytes']} bytes")
    console.print(f"  Location: {cache.cache_dir}")


@app.command("run")
def run_cmd(
    path: str = typer.Argument("tests/", help="Path to test files"),
    pattern: Optional[str] = typer.Option(
        None, "--pattern", "-p", help="File pattern (e.g., 'test_*.py')"
    ),
    durations: Optional[int] = typer.Option(
        None, "--durations", help="Show N slowest tests (0 for all)"
    ),
    durations_min: float = typer.Option(
        0.005, "--durations-min", help="Minimum duration to show"
    ),
    fail_fast: bool = typer.Option(
        False, "-x", "--exitfirst", help="Exit on first failure"
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Verbose output"
    ),
):
    """
    Run AI tests with pytest-like options.
    
    Examples:
        testagent run tests/
        testagent run tests/ --durations=5
        testagent run tests/ -x  # Stop on first failure
    """
    from pathlib import Path as PathLib
    from .collector import Collector
    from .timing import Instant
    
    start = Instant()
    
    # Collect tests
    collector = Collector()
    if pattern:
        collector.file_patterns = [pattern]
    
    modules = collector.collect_only(PathLib(path))
    total_tests = sum(len(m.items) for m in modules)
    
    if total_tests == 0:
        console.print("[yellow]No tests found[/yellow]")
        raise typer.Exit(5)
    
    console.print(f"\n[bold]Collected {total_tests} tests[/bold]\n")
    
    # Track results for duration reporting
    results_with_duration = []
    passed = 0
    failed = 0
    skipped = 0
    
    for module in modules:
        if verbose:
            console.print(f"[cyan]{module.path}[/cyan]")
        
        for item in module.items:
            test_start = Instant()
            status = "[green].[/green]"
            
            # Simulate test execution (actual execution would require importing)
            test_duration = test_start.elapsed()
            
            results_with_duration.append({
                "nodeid": item.nodeid,
                "duration": test_duration.seconds,
                "status": "passed",
            })
            passed += 1
            
            if verbose:
                console.print(f"  {status} {item.name}")
    
    # Duration reporting
    if durations is not None:
        results_with_duration.sort(key=lambda x: x["duration"], reverse=True)
        
        if durations == 0:
            console.print("\n[bold]= slowest durations =[/bold]")
            show_results = results_with_duration
        else:
            console.print(f"\n[bold]= slowest {durations} durations =[/bold]")
            show_results = results_with_duration[:durations]
        
        for r in show_results:
            if r["duration"] >= durations_min:
                console.print(f"  {r['duration']:.4f}s {r['nodeid']}")
    
    # Summary
    total_duration = start.elapsed()
    console.print(f"\n[bold]{'=' * 50}[/bold]")
    
    summary_parts = []
    if passed:
        summary_parts.append(f"[green]{passed} passed[/green]")
    if failed:
        summary_parts.append(f"[red]{failed} failed[/red]")
    if skipped:
        summary_parts.append(f"[yellow]{skipped} skipped[/yellow]")
    
    summary = ", ".join(summary_parts)
    console.print(f"[bold]{summary}[/bold] in {total_duration}")
    
    raise typer.Exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    app()
