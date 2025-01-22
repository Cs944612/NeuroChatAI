# 🧠 NeuroChatAI

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24.0-red.svg)](https://streamlit.io)

A streamlined interface for interacting with local Large Language Models

[Getting Started](#getting-started) •
[Features](#features) •
[Installation](#installation) •
[Usage](#usage) •
[Configuration](#configuration)

</div>

## 🚀 Getting Started

NeuroChatAI provides a user-friendly web interface for interacting with local Large Language Models (LLMs). Built with Streamlit, it offers a seamless experience for testing and using your local LLM implementations.

### Prerequisites

-   Python 3.8 or higher
-   A local LLM server (e.g., LM Studio) running on your machine
-   Git (for version control)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Cs944612/NeuroChatAI.git
cd NeuroChatAI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
✨ Features
💬 Interactive chat interface
⚙️ Configurable model parameters
💾 Chat history management
📤 Export conversations
⚡ Predefined prompts for quick testing
🛡️ Built-in error handling and rate limiting
🔍 API health monitoring
🎨 Modern, responsive UI
🛠️ Installation
Ensure you have Python 3.8+ installed:
bash
python --version
Clone the repository:
bash
git clone https://github.com/Cs944612/NeuroChatAI.git
cd NeuroChatAI
Create and activate a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install required dependencies:
bash
pip install -r requirements.txt
🎮 Usage
Start your local LLM server (e.g., LM Studio)

Configure your environment variables in .env file:

env
API_URL=http://127.0.0.1:1234/v1/completions
MODEL_NAME=your-model-name
Launch NeuroChatAI:
bash
streamlit run streamlit_app.py
Open your web browser and navigate to:
Code
http://localhost:8501
⚙️ Configuration
Environment Variables
Create a .env file in the project root:

env
API_URL=http://127.0.0.1:1234/v1/completions
MODEL_NAME=your-model-name
MAX_HISTORY_MESSAGES=5
RATE_LIMIT_SECONDS=1.0
Available Settings
API_URL	LLM API endpoint	http://127.0.0.1:1234/v1/completions
MODEL_NAME	Name of the model	your-model-name
MAX_HISTORY_MESSAGES	Number of messages to keep in context	5
RATE_LIMIT_SECONDS	Minimum time between requests	1.0
📁 Project Structure
Code
NeuroChatAI/
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── streamlit_app.py
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Streamlit for their amazing framework
The LLM community for their continuous support
📞 Support
If you encounter any issues or have questions:

Check the Issues page
Create a new issue if your problem isn't already listed
Provide as much detail as possible in bug reports
🔄 Updates and Versioning
Current Version: 1.0.0
Last Updated: 2025-01-22 16:17:17 UTC
Author: Cs944612

Made with ❤️ by Cs944612
```
