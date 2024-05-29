# Llama3 Email Processor

This project processes emails using agents in the CrewAI framework. It can classify emails into categories (important, casual, or spam) and generate appropriate responses. The project also supports optional human interaction to verify and modify the classification and response.

## Features

- **Email Classification**: Classify emails into important, casual, or spam.
- **Email Response**: Generate concise and appropriate responses based on the classification.
- **Human Interaction**: Optionally verify and modify the classification and response.

## Requirements

- Python 3.8+
- Virtual Environment (optional but recommended)

## Installation

1. **Clone the repository:**

```bash
   git clone https://github.com/yourusername/llama3-email-processor.git
   cd llama3-email-processor
```
2. **Create and activate a virtual environment (optional but recommended):**

```bash 
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required dependencies:**
```bash
pip install -r requirements.txt

```

4. **Enable or disable human interaction by setting the enable_human_interaction variable:**
```python
enable_human_interaction = True

```

