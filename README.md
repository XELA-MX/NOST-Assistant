# NOST - Personal Assistant

NOST is a personal assistant powered by artificial intelligence, designed to interact with users through text and voice. This project utilizes the OpenAI GPT-4 API to generate intelligent and functional responses, as well as voice recognition technologies to activate and process spoken commands.

## Current Features

- **Intelligent Response Generation:** Uses the OpenAI GPT-4 API to provide responses based on conversation history.
- **Intuitive User Interface:** Graphical window developed with `customtkinter` to display messages and allow text input.
- **Markdown Support:** Processes Markdown-formatted text, such as lists and bold, for readable content.
- **Multilanguage Support:** Configured for Spanish voice recognition ("es-ES").

## Prerequisites

Before using NOST, ensure you have installed the following dependencies:

```bash
pip install customtkinter openai tiktoken pyttsx3 SpeechRecognition markdown-it pyaudio
```

Additionally, you need a valid OpenAI API key. You can obtain one [here](https://platform.openai.com/signup/).

## Usage

1. Run the project's main script.
2. You can also interact with the graphical interface to send messages.

## Configuration

### Configuration Variables

- **OpenAI API Key:** Set your key in the project file:
  ```python
  openai.api_key = "your_api_key_here"
  ```

## Future Versions

1. **Advanced Voice Control:**
   - Integration of commands to control applications and connected devices.
   - Activation via configurable keywords.

2. **System Automation:**
   - Open programs, manage files, and control tasks on the computer.

3. **IoT Integration:**
   - Control smart devices like lights, thermostats, and more.

4. **Cross-Platform Compatibility:**
   - Optimization for Windows, macOS, and Linux.

5. **Custom Command Support:**
   - Users will be able to define specific commands based on their needs.

6. **Custom GPT-4 Training:**
   - Personalization of the model to adapt it to specific contexts.

## Contributions

Contributions are welcome! If you have ideas, improvements, or encounter bugs, feel free to create an issue or a pull request in this repository.

## License

This project is licensed under the [MIT License](LICENSE).

---

_Developed with ❤️ by the NOST team._
