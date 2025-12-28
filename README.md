# Chat Template Detector

Detect chat template mismatches between training and inference in LLM fine-tuning.

## The Problem

You fine-tune an LLM with one chat template format. You run inference with a different format. The model outputs garbage. No error message. Hours wasted debugging.

This tool catches template mismatches before they waste your time and GPU credits.

## Installation

```bash
pip install chat-template-detector
```

## Usage

```bash
# Validate training data against inference config
chat-template-detector validate \
  --training-file train.jsonl \
  --inference-config config.yaml

# Validate against a specific model
chat-template-detector validate \
  --training-file train.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf

# Check a single formatted text file
chat-template-detector check samples/sample_chatml.txt
```

## Common Issues Detected

- ChatML vs Llama format mismatch
- Missing special tokens
- Incorrect token ordering
- BOS/EOS token mismatches
- Role name inconsistencies

## Examples

Training file uses ChatML:
```json
{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]}
```

Inference expects Llama format:
```
<s>[INST] Hello [/INST] Hi</s>
```

Detector catches this mismatch and shows exactly what's wrong.

## CI/CD Integration

Add to your training pipeline to catch template mismatches before training:

```yaml
# GitHub Actions
- name: Validate chat templates
  run: |
    pip install chat-template-detector
    chat-template-detector validate \
      --training-file data/train.jsonl \
      --model ${{ matrix.model }}
```

```bash
# GitLab CI / Jenkins / Any CI
pip install chat-template-detector
chat-template-detector validate \
  --training-file train.jsonl \
  --inference-config config.yaml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE) for details

## Author

Built by [ClarifyIntel](https://clarifyintel.com) - We clarify complex tech. Kubernetes, AI/ML, DevOps, Security — we write, we teach, we solve.