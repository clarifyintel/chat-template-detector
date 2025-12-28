"""Command-line interface for chat template detection."""

import json
import sys
from pathlib import Path
from typing import Optional

import click
import yaml

from .detector import TemplateDetector
from .templates import KNOWN_TEMPLATES


@click.group()
@click.version_option()
def main():
    """Detect chat template mismatches in LLM fine-tuning."""
    pass


@main.command()
@click.option(
    "--training-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to training data file (JSONL format)"
)
@click.option(
    "--inference-config",
    type=click.Path(exists=True),
    help="Path to inference config file (YAML/JSON)"
)
@click.option(
    "--model",
    type=str,
    help="Model name to check against"
)
@click.option(
    "--format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format"
)
def validate(training_file: str, inference_config: Optional[str], model: Optional[str], format: str):
    """Validate training data against inference configuration."""
    detector = TemplateDetector()
    
    # Analyze training file
    click.echo("Analyzing training file...")
    try:
        training_template = detector.validate_training_file(training_file)
        if training_template:
            click.echo(f"Detected training template: {training_template}")
        else:
            click.echo("Warning: Could not auto-detect training template")
    except Exception as e:
        click.echo(f"Error analyzing training file: {e}", err=True)
        sys.exit(1)
    
    # Analyze inference config
    inference_template = None
    if inference_config:
        click.echo("Analyzing inference config...")
        try:
            with open(inference_config, 'r', encoding='utf-8') as f:
                if inference_config.endswith('.yaml') or inference_config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            if config is None:
                click.echo("Error: Config file is empty", err=True)
                sys.exit(1)
            
            inference_template = detector.validate_inference_config(config)
            if inference_template:
                click.echo(f"Detected inference template: {inference_template}")
            else:
                click.echo("Warning: Could not auto-detect inference template")
        except FileNotFoundError:
            click.echo(f"Error: Config file not found: {inference_config}", err=True)
            sys.exit(1)
        except yaml.YAMLError as e:
            click.echo(f"Error: Invalid YAML format: {e}", err=True)
            sys.exit(1)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON format: {e}", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"Error analyzing inference config: {e}", err=True)
            sys.exit(1)
    elif model:
        click.echo(f"Checking model: {model}")
        from .templates import detect_template_from_model_name
        inference_template = detect_template_from_model_name(model)
        if inference_template:
            click.echo(f"Detected model template: {inference_template}")
    
    # Compare templates
    click.echo("\nValidating template consistency...")
    mismatches = detector.compare_templates(training_template, inference_template)
    
    # Output results
    if format == "json":
        output = {
            "training_template": training_template,
            "inference_template": inference_template,
            "mismatches": [
                {
                    "severity": m.severity,
                    "field": m.field,
                    "expected": m.expected,
                    "actual": m.actual,
                    "message": m.message
                }
                for m in mismatches
            ]
        }
        click.echo(json.dumps(output, indent=2))
    else:
        click.echo("\nResults:")
        click.echo("-" * 60)
        for mismatch in mismatches:
            color = {
                "error": "red",
                "warning": "yellow",
                "info": "green"
            }.get(mismatch.severity, "white")
            click.echo(click.style(str(mismatch), fg=color))
        click.echo("-" * 60)
        
        # Exit code
        has_errors = any(m.severity == "error" for m in mismatches)
        if has_errors:
            click.echo("\nValidation FAILED: Template mismatches detected")
            sys.exit(1)
        else:
            click.echo("\nValidation PASSED")
            sys.exit(0)


@main.command()
def list_templates():
    """List all known chat templates."""
    click.echo("Known chat templates:\n")
    for name, template in KNOWN_TEMPLATES.items():
        click.echo(f"{name}: {template.name}")
        click.echo(f"  BOS: {template.bos_token or 'None'}")
        click.echo(f"  EOS: {template.eos_token or 'None'}")
        click.echo(f"  User: {template.user_prefix}...{template.user_suffix}")
        click.echo(f"  Assistant: {template.assistant_prefix}...{template.assistant_suffix}")
        click.echo()


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--template",
    type=click.Choice(list(KNOWN_TEMPLATES.keys())),
    help="Expected template format"
)
def check(file_path: str, template: Optional[str]):
    """Check a single file for template issues."""
    detector = TemplateDetector()
    
    # Read file
    path = Path(file_path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        click.echo("Error: File encoding not supported. Please use UTF-8", err=True)
        sys.exit(1)
    except PermissionError:
        click.echo(f"Error: Permission denied reading file: {file_path}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        sys.exit(1)
    
    # Auto-detect if not specified
    if not template:
        from .templates import detect_template_from_text
        template = detect_template_from_text(content)
        if template:
            click.echo(f"Auto-detected template: {template}")
        else:
            click.echo("Could not auto-detect template. Please specify with --template")
            sys.exit(1)
    
    # Analyze
    mismatches = detector.analyze_formatted_text(content, template)
    
    # Output
    click.echo(f"\nAnalyzing file with template: {template}")
    click.echo("-" * 60)
    if not mismatches:
        click.echo(click.style("No issues found", fg="green"))
    else:
        for mismatch in mismatches:
            color = {
                "error": "red",
                "warning": "yellow",
                "info": "green"
            }.get(mismatch.severity, "white")
            click.echo(click.style(str(mismatch), fg=color))
    click.echo("-" * 60)


if __name__ == "__main__":
    main()
