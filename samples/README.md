# Sample Files

Formatted text examples for each chat template type.

## Files

- `sample_chatml.txt` - ChatML format example
- `sample_llama2.txt` - Llama-2 format example
- `sample_mistral.txt` - Mistral format example
- `sample_alpaca.txt` - Alpaca format example
- `sample_vicuna.txt` - Vicuna format example

## Usage

### Auto-detect template type
```bash
chat-template-detector check samples/sample_chatml.txt
```

### Validate against specific template
```bash
chat-template-detector check samples/sample_llama2.txt --template llama-2
```

### Wrong template (will show errors)
```bash
chat-template-detector check samples/sample_chatml.txt --template llama-2
```

## Template Characteristics

**ChatML:**
- Uses `<|im_start|>` and `<|im_end|>` tokens
- Roles: user, assistant, system

**Llama-2:**
- Uses `<s>`, `</s>`, `[INST]`, `[/INST]` tokens
- System prompt wrapped in `<<SYS>>` tags

**Mistral:**
- Similar to Llama-2
- Uses `[INST]` and `[/INST]` tokens

**Alpaca:**
- Uses markdown-style headers: `### Instruction:`, `### Response:`
- Clear section separation

**Vicuna:**
- Simple format: `USER:`, `ASSISTANT:`, `SYSTEM:`
- Conversational style
