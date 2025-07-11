# Google API Configuration
GOOGLE_API_KEY = "your-api-key-here"  # Replace with your actual API key

# Model Configuration
MODEL_NAME = "models/gemini-1.5-flash"
SYSTEM_INSTRUCTION = (
    "You are a helpful, smart and respectful assistant who always answers based on "
    "the provided information while thinking logically step by step"
)

# Generation Configuration
GENERATION_CONFIG = {
    "candidate_count": 1,
    "temperature": 1.5,
    "top_p": 0.95,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# File paths
LABELS_FILE = "labels.txt"
COUNTER_FILE = "counter_file.txt"

# Label categories and their descriptions
LABEL_CATEGORIES = {
    "O": "general word",
    "B/I-CONST_DIR": "optimization_problem_constraint_description",
    "B/I-LIMIT": "numerical_limit",
    "B/I-VAR": "variable",
    "B/I-PARAM": "measurable_parameter",
    "B/I-OBJ_NAME": "objective",
    "B-OBJ_DIR": "action_towards_objective"
}

# Prompt template for classification
CLASSIFICATION_PROMPT_TEMPLATE = """
## USER: the following text is an example of a text description of a problem that requires optimization your role is to classify each word should be classified into one of the following: (general word refered to using the label 'O' , optimization_problem_constraint_description refered to using the label 'B/I-CONST_DIR', numerical_limit refered to using the label 'B/I-LIMIT',variable refered to using the label 'B/I-VAR', measurable_parameter refered to using the label 'B/I PARAM', objective refered to using the label 'B/I-OBJ_NAME' , action_towards_objective refered to using the label 'B-OBJ_DIR') answer in the format 'word _ _ classification label' for each word in the provided text
## provided text:
{example_text}
## Assistant:
{reply_text}
## USER: the following text is an example of a text description of a problem that requires optimization your role is to classify each word should be classified into one of the following: (general word refered to using the label 'O' , optimization_problem_constraint_description refered to using the label 'B/I-CONST_DIR', numerical_limit refered to using the label 'B/I-LIMIT',variable refered to using the label 'B/I-VAR', measurable_parameter refered to using the label 'B/I PARAM', objective refered to using the label 'B/I-OBJ_NAME' , action_towards_objective refered to using the label 'B-OBJ_DIR') answer in the format 'word _ _ classification label' for each word in the provided text
{prompt_text}
## Assistant:
"""