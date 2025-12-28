#!/bin/bash

echo "======================================"
echo "Chat Template Detector - Full Test"
echo "======================================"
echo ""

echo "1. Testing MISMATCH scenarios (should FAIL)..."
echo "--------------------------------------"

echo ""
echo "Test 1.1: ChatML training vs Llama-2 config"
chat-template-detector validate \
  --training-file jsonl/train_chatml.jsonl \
  --inference-config jsonl/config_llama2.yaml
echo ""

echo "Test 1.2: Llama-2 training vs ChatML config"
chat-template-detector validate \
  --training-file jsonl/train_llama2.jsonl \
  --inference-config jsonl/config_chatml.yaml
echo ""

echo "Test 1.3: ChatML training vs Llama-2 model"
chat-template-detector validate \
  --training-file jsonl/train_chatml.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
echo ""

echo ""
echo "2. Testing MATCH scenarios (should PASS)..."
echo "--------------------------------------"

echo ""
echo "Test 2.1: Llama-2 training vs Llama-2 config"
chat-template-detector validate \
  --training-file jsonl/train_llama2.jsonl \
  --inference-config jsonl/config_llama2.yaml
echo ""

echo "Test 2.2: Mistral training vs Mistral config"
chat-template-detector validate \
  --training-file jsonl/train_mistral.jsonl \
  --inference-config jsonl/config_mistral.yaml
echo ""

echo "Test 2.3: Llama-2 training vs Llama-2 model"
chat-template-detector validate \
  --training-file jsonl/train_llama2.jsonl \
  --model meta-llama/Llama-2-7b-chat-hf
echo ""

echo ""
echo "3. Testing sample file detection..."
echo "--------------------------------------"

for format in chatml llama2 mistral alpaca vicuna; do
  echo ""
  echo "Test 3.$format: Auto-detect $format format"
  chat-template-detector check samples/sample_$format.txt
done

echo ""
echo "======================================"
echo "All tests completed!"
echo "======================================"
