# Optimization Problem Solver & Labeler

A modular Streamlit application for solving optimization problems and labeling text with optimization-related entities.

## Features

  - **LLM-based Problem Solving**: Uses Ollama to generate Python code solutions for optimization problems
  - **Automated Text Labeling**: Classifies words in optimization problems using Google's Gemini API
  - **Interactive Chat Interface**: Natural language interaction for problem solving
  - **Accuracy Metrics**: Compares generated labels with reference labels
  - **Modular Architecture**: Clean separation of concerns across multiple modules

## Project Structure

```
├── main.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── labeling.py            # Unified labeling module
├── llm_handler.py         # LLM integration
├── labels.txt             # Reference labels file
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Setup Instructions

1.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys**

      - Edit `config.py` and replace `"your-api-key-here"` with your actual Google API key
      - Make sure you have Ollama installed and running with the qwen3:8b model

3.  **Prepare Labels File**

      - The `labels.txt` file contains reference labels for comparison
      - You can modify this file to use your own reference labels

4.  **Run the Application**

    ```bash
    streamlit run main.py
    ```

## Usage

### Chat Interface

  - Enter optimization problems in natural language
  - The system will generate Python code using PuLP library
  - Code execution results are displayed automatically

### Text Labeling

  - Labels are automatically generated for chat inputs
  - Use the custom text labeling feature for standalone text analysis
  - View accuracy metrics comparing generated labels with reference labels

### Label Categories

  - **O**: General words
  - **B/I-CONST\_DIR**: Constraint descriptions
  - **B/I-LIMIT**: Numerical limits
  - **B/I-VAR**: Variables
  - **B/I-PARAM**: Measurable parameters
  - **B/I-OBJ\_NAME**: Objectives
  - **B-OBJ\_DIR**: Actions towards objectives

## Key Improvements

1.  **Modular Design**: Separated concerns into distinct modules
2.  **Unified Labeling**: Single labeling module handles all text processing
3.  **Better UI**: Improved layout with side-by-side chat and labeling panels
4.  **Custom Text Support**: Ability to label any input text
5.  **Error Handling**: Robust error handling throughout the application
6.  **Configuration Management**: Centralized configuration in config.py

## API Requirements

  - **Google Gemini API**: For text labeling functionality
