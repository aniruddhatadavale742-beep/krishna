# KRISHNA

KRISHNA is a modular Python personal assistant for Windows. It includes voice input/output, online/offline AI routing, mathematics tools, Windows automation, and local-model power management. Check each feature's status in the source before assuming it is fully configured.

## System status command

While KRISHNA is running, say or type any of:

- `status`
- `KRISHNA status`
- `system check`
- `run diagnostics`

The report checks the configured AI mode, application sleep state, Ollama connectivity, whether the configured local model is installed, and how many Chrome profiles are detected. It uses Ollama's model-list endpoint and does not generate a response or load the local AI model.

## Local setup notes

- Keep API keys in a local `.env` file; do not commit secrets.
- Keep downloaded model assets (including Piper `.onnx` voice files) outside Git commits.
- Install project dependencies in a virtual environment.
- The assistant currently uses the configured Ollama model `qwen2.5:1.5b`; ensure that it is installed locally for offline AI responses.
