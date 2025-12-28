# Quick Start Guide

## Installation

```bash
pip install chat-template-detector
```

## Basic Usage

### List Available Templates

```bash
chat-template-detector list-templates
```

### Validate Training Data

You have a training file with ChatML format:

```json
{"text": "<|im_start|>user\nHello<|im_end|>\n<|im_start|>assistant\nHi<|im_end|>"}
```

And an inference config expecting Llama-2:

```yaml
model: meta-llama/Llama-2-7b-chat-hf
```

Check for mismatches:

```bash
chat-template-detector validate \
  --training-file train.jsonl \
  --inference-config config.yaml
```

Output:
```
Analyzing training file...
Detected training template: chatml
Analyzing inference config...
Detected inference template: llama-2

Validating template consistency...

Results:
------------------------------------------------------------
[ERROR] template: Template mismatch: training uses chatml, inference uses llama-2
------------------------------------------------------------

Validation FAILED: Template mismatches detected
```

### Check Model Compatibility

```bash
chat-template-detector validate \
  --training-file train.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
```

### Check Single File

```bash
chat-template-detector check formatted_text.txt
```

Auto-detects template and validates formatting.

### Specify Template

```bash
chat-template-detector check formatted_text.txt --template chatml
```

### JSON Output

```bash
chat-template-detector validate \
  --training-file train.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf \
  --format json
```

## Common Scenarios

### Scenario 1: You fine-tuned with ChatML, but inference uses Llama format

Problem: Model outputs garbage.

Solution:
```bash
chat-template-detector validate \
  --training-file train.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
```

The tool will catch the mismatch.

### Scenario 2: You're not sure what template your training data uses

Solution:
```bash
chat-template-detector check train.jsonl
```

Auto-detection will identify the template.

### Scenario 3: You want to verify template consistency before fine-tuning

Solution:
```bash
chat-template-detector validate \
  --training-file train.jsonl \
  --inference-config config.yaml
```

Run this before starting the fine-tuning job. Save GPU time.
