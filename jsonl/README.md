# Test Data - JSONL Files

## Available Training Files

- `train_chatml.jsonl` - ChatML format
- `train_llama2.jsonl` - Llama-2 format
- `train_mistral.jsonl` - Mistral format
- `train_alpaca.jsonl` - Alpaca format
- `train_vicuna.jsonl` - Vicuna format

## Available Config Files

- `config_chatml.yaml` - ChatML config
- `config_llama2.yaml` - Llama-2 config
- `config_mistral.yaml` - Mistral config

## Test Scenarios

### Scenario 1: Mismatch (FAIL)

Training uses ChatML, inference expects Llama-2:
```bash
chat-template-detector validate \
  --training-file jsonl/train_chatml.jsonl \
  --inference-config jsonl/config_llama2.yaml
```
Expected: ERROR - Template mismatch

### Scenario 2: Match (PASS)
Training uses Llama-2, inference expects Llama-2:
```bash
chat-template-detector validate \
  --training-file jsonl/train_llama2.jsonl \
  --inference-config jsonl/config_llama2.yaml
```
Expected: INFO - Templates match

### Scenario 3: Model Name Detection
Use model name instead of config:
```bash
chat-template-detector validate \
  --training-file jsonl/train_llama2.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
```
Expected: INFO - Templates match

### Scenario 4: Wrong Model for Training Data
```bash
chat-template-detector validate \
  --training-file jsonl/train_chatml.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
```
Expected: ERROR - Template mismatch

## Quick Test All Formats

```bash
# Test each format detection
for format in chatml llama2 mistral alpaca vicuna; do
  echo "Testing $format..."
  chat-template-detector check ../samples/sample_$format.txt
done
```
