# Yumi: Python AI Voice Assistant 🎙️

Yumi is a lightweight, local-first voice assistant written in Python. It bridges local speech recognition with cloud-based LLM generation to provide seamless, hands-free control over desktop environments, system applications, and Steam games.

## 🛠️ Architecture & Technologies
- **Speech-to-Text (STT):** Local voice recognition using `Vosk` and `sounddevice` to ensure zero-latency listening without constant cloud streaming.
- **Brain (LLM):** Integration with the new `google-genai` SDK (Gemini 1.5 Flash) for rapid, context-aware conversational responses.
- **Text-to-Speech (TTS):** Audio output generated via `gTTS` and handled by `pygame.mixer` for asynchronous audio playback.
- **OS Integration:** Direct interaction with the Windows filesystem and Steam URI protocols (`steam://`) to launch specific applications via voice commands.

## 🔒 Security Note
API keys are strictly managed via environment variables (`GEMINI_API_KEY`). No sensitive credentials are hardcoded into the source logic.

## 🚀 Use Cases for Business
This proof-of-concept demonstrates my ability to:
1. Integrate third-party LLM APIs (like Gemini or OpenAI) into custom desktop or web applications.
2. Build custom RAG (Retrieval-Augmented Generation) audio interfaces.
3. Automate routine desktop tasks using Python scripting.
