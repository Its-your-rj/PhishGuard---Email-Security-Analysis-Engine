#!/usr/bin/env python3
"""
Email Security Analysis Engine
Main CLI Interface
"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime

console = Console()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """[Shield] Email Security Analysis Engine - Detect Spam & Phishing"""
    pass

@cli.command()
@click.argument('email_file', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text', help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(email_file, format, output, verbose):
    """Analyze a single email file for spam/phishing"""
    from email_parser import EmailParser
    from classifier import EmailClassifier
    
    console.print(f"\n[cyan]Analyzing email: {email_file}[/cyan]\n")
    
    try:
        # Parse email
        parser = EmailParser()
        parsed_data = parser.parse_file(email_file)
        
        # Classify email
        classifier = EmailClassifier()
        result = classifier.classify(parsed_data)
        
        # Display results
        if format == 'text':
            display_results(result, parsed_data, verbose)
        elif format == 'json':
            json_output = json.dumps(result, indent=2)
            if output:
                Path(output).write_text(json_output)
                console.print(f"[green]✓ Results saved to {output}[/green]")
            else:
                console.print(json_output)
        elif format == 'html':
            html_output = generate_html_report(result, parsed_data)
            if output:
                Path(output).write_text(html_output)
                console.print(f"[green]✓ HTML report saved to {output}[/green]")
            else:
                console.print(html_output)
                
    except Exception as e:
        console.print(f"[red]✗ Error analyzing email: {str(e)}[/red]")
        raise click.Abort()

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('--output', '-o', default='batch_report.json', help='Output report file')
@click.option('--recursive', '-r', is_flag=True, help='Process subdirectories')
def batch(input_dir, output, recursive):
    """Batch process multiple email files"""
    from email_parser import EmailParser
    from classifier import EmailClassifier
    
    input_path = Path(input_dir)
    pattern = '**/*.eml' if recursive else '*.eml'
    email_files = list(input_path.glob(pattern))
    
    if not email_files:
        console.print("[yellow]⚠ No .eml files found[/yellow]")
        return
    
    console.print(f"\n[cyan]Processing {len(email_files)} email(s)...[/cyan]\n")
    
    parser = EmailParser()
    classifier = EmailClassifier()
    results = []
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing...", total=len(email_files))
        
        for email_file in email_files:
            try:
                parsed = parser.parse_file(str(email_file))
                result = classifier.classify(parsed)
                result['file'] = str(email_file)
                results.append(result)
            except Exception as e:
                console.print(f"[red]✗ Error processing {email_file}: {e}[/red]")
            
            progress.update(task, advance=1)
    
    # Save results
    Path(output).write_text(json.dumps(results, indent=2))
    
    # Display summary
    display_batch_summary(results)
    console.print(f"\n[green]✓ Batch report saved to {output}[/green]")

@cli.command()
@click.argument('dataset_dir', type=click.Path(exists=True))
@click.option('--model-output', '-m', default='models/trained_model.pkl', help='Model output path')
@click.option('--epochs', '-e', default=10, help='Training epochs')
def train(dataset_dir, model_output, epochs):
    """Train classifier on custom dataset"""
    from model_trainer import ModelTrainer
    
    console.print(f"\n[cyan]Training model on dataset: {dataset_dir}[/cyan]\n")
    
    trainer = ModelTrainer()
    metrics = trainer.train(dataset_dir, model_output, epochs)
    
    console.print("\n[green]Training complete![/green]")
    console.print(f"\nAccuracy: {metrics['accuracy']:.2%}")
    console.print(f"Precision: {metrics['precision']:.2%}")
    console.print(f"Recall: {metrics['recall']:.2%}")
    console.print(f"F1 Score: {metrics['f1']:.2%}")

def display_results(result, parsed_data, verbose):
    """Display analysis results in rich format"""
    
    # Classification result
    classification = result['classification']
    confidence = result['confidence']
    
    if classification == 'PHISHING':
        color = 'red'
        icon = '[PHISHING]'
    elif classification == 'SPAM':
        color = 'yellow'
        icon = '[SPAM]'
    else:
        color = 'green'
        icon = '[SAFE]'
    
    console.print(Panel(
        f"[{color} bold]{icon} {classification}[/{color} bold]\nConfidence: {confidence:.1%}",
        title="Classification Result",
        border_style=color
    ))
    
    # Email details
    console.print("\n[bold]Email Details:[/bold]")
    table = Table(show_header=False, box=None)
    table.add_row("From:", parsed_data['from'])
    table.add_row("To:", parsed_data['to'])
    table.add_row("Subject:", parsed_data['subject'])
    table.add_row("Date:", parsed_data['date'])
    console.print(table)
    
    # Threat indicators
    if result['threat_indicators']:
        console.print("\n[bold red]Threat Indicators:[/bold red]")
        for indicator in result['threat_indicators']:
            console.print(f"  {indicator}")
    
    # Header analysis
    if verbose and 'header_analysis' in result:
        console.print("\n[bold]Header Analysis:[/bold]")
        for key, value in result['header_analysis'].items():
            console.print(f"  {key}: {value}")
    
    # Recommendation
    console.print(f"\n[bold]Recommendation:[/bold] {result['recommendation']}")

def display_batch_summary(results):
    """Display summary of batch processing"""
    total = len(results)
    phishing = sum(1 for r in results if r['classification'] == 'PHISHING')
    spam = sum(1 for r in results if r['classification'] == 'SPAM')
    ham = sum(1 for r in results if r['classification'] == 'HAM')
    
    table = Table(title="Batch Analysis Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Percentage", style="green")
    
    table.add_row("Total Emails", str(total), "100%")
    table.add_row("Phishing", str(phishing), f"{phishing/total*100:.1f}%")
    table.add_row("Spam", str(spam), f"{spam/total*100:.1f}%")
    table.add_row("Ham (Safe)", str(ham), f"{ham/total*100:.1f}%")
    
    console.print("\n")
    console.print(table)

def generate_html_report(result, parsed_data):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Security Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }}
            .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .classification {{ padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .phishing {{ background: #ffe6e6; border-left: 5px solid #ff0000; }}
            .spam {{ background: #fff9e6; border-left: 5px solid #ffaa00; }}
            .ham {{ background: #e6ffe6; border-left: 5px solid #00aa00; }}
            .indicators {{ background: #fff; padding: 15px; border: 1px solid #ddd; }}
            table {{ width: 100%; border-collapse: collapse; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
            td:first-child {{ font-weight: bold; width: 150px; }}
        </style>
    </head>
    <body>
        <h1>Email Security Analysis Report</h1>
        <div class="header">
            <h2>Email Details</h2>
            <table>
                <tr><td>From:</td><td>{parsed_data['from']}</td></tr>
                <tr><td>To:</td><td>{parsed_data['to']}</td></tr>
                <tr><td>Subject:</td><td>{parsed_data['subject']}</td></tr>
                <tr><td>Date:</td><td>{parsed_data['date']}</td></tr>
            </table>
        </div>
        <div class="classification {result['classification'].lower()}">
            <h2>Classification: {result['classification']}</h2>
            <p>Confidence: {result['confidence']:.1%}</p>
        </div>
        <div class="indicators">
            <h3>Threat Indicators</h3>
            <ul>
                {''.join(f'<li>{ind}</li>' for ind in result['threat_indicators'])}
            </ul>
        </div>
        <p><strong>Recommendation:</strong> {result['recommendation']}</p>
        <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    cli()