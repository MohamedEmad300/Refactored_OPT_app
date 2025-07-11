import google.generativeai as genai
from config import (
    GOOGLE_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION, 
    GENERATION_CONFIG, CLASSIFICATION_PROMPT_TEMPLATE, LABELS_FILE
)
from utils import (
    extract_first_column, compare_columns_ignore_position, 
    load_labels_from_file, tokenize_text
)


class OptimizationLabeler:
    """Main class for handling optimization problem labeling."""
    
    def __init__(self):
        self.model = self._configure_model()
        self.reference_labels = load_labels_from_file(LABELS_FILE)
    
    def _configure_model(self):
        """Configure the generative AI model."""
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTION,
        )
    
    def _construct_prompt(self, example_text, reply_text, prompt_text):
        """Construct the prompt for the model."""
        return CLASSIFICATION_PROMPT_TEMPLATE.format(
            example_text=example_text,
            reply_text=reply_text,
            prompt_text=prompt_text
        )
    
    def label_text(self, input_text):
        """
        Label the input text using the AI model.
        
        Args:
            input_text (str): The text to be labeled, can be plain text or pre-tokenized
            
        Returns:
            dict: Results containing labeled text and accuracy metrics
        """
        # Check if input is already tokenized (contains tabs) or plain text
        if '\t' in input_text:
            # Already tokenized, extract first column
            tokenized_input = extract_first_column(input_text)
        else:
            # Plain text, need to tokenize
            tokenized_input = tokenize_text(input_text)
        
        # Use reference labels as both example and reply
        if self.reference_labels:
            example_text = extract_first_column(self.reference_labels)
            reply_text = self.reference_labels
        else:
            # Fallback if labels file is not available
            example_text = tokenized_input
            reply_text = self._create_dummy_labels(tokenized_input)
        
        # Construct prompt
        prompt = self._construct_prompt(example_text, reply_text, tokenized_input)
        
        # Generate response
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(**GENERATION_CONFIG),
        )
        
        generated_text = response.text.strip()
        
        # Compare with reference if available
        if self.reference_labels:
            accuracy_result = compare_columns_ignore_position(
                text1=self.reference_labels, 
                text2=generated_text
            )
        else:
            accuracy_result = {
                "match_percentage": 0,
                "common_words": [],
                "missing_in_text1": [],
                "missing_in_text2": []
            }
        
        return {
            "labeled_text": generated_text,
            "accuracy": accuracy_result,
            "input_text": input_text,
            "tokenized_input": tokenized_input
        }
    
    def _create_dummy_labels(self, tokenized_text):
        """Create dummy labels when reference is not available."""
        lines = tokenized_text.strip().split('\n')
        return '\n'.join([f"{line}\t_\t_\tO" for line in lines])
    
    def format_output(self, result):
        """Format the labeling result for display."""
        accuracy = result["accuracy"]
        
        output = f"""
=========== Labels ===========
{result["labeled_text"]}

=========== Accuracy ===========
Match Percentage: {accuracy['match_percentage']:.2f}%
Missing in Reference: {accuracy['missing_in_text1']}
Missing in Generated: {accuracy['missing_in_text2']}

=========== Input Processing ===========
Original Input: {result["input_text"][:100]}...
Tokenized Input: {result["tokenized_input"][:100]}...
""".strip()
        
        return output


def run_labeling_pipeline(input_text=None):
    """
    Run the complete labeling pipeline.
    
    Args:
        input_text (str): Optional input text. If not provided, uses reference labels.
        
    Returns:
        str: Formatted output with labels and accuracy metrics
    """
    labeler = OptimizationLabeler()
    
    # If no input provided, use reference labels for testing
    if input_text is None:
        input_text = labeler.reference_labels
    
    # Run labeling
    result = labeler.label_text(input_text)
    
    # Format and return output
    return labeler.format_output(result)


# For backward compatibility with existing code
def run_pipeline():
    """Legacy function for backward compatibility."""
    return run_labeling_pipeline()


def run_pipeline2():
    """Legacy function for backward compatibility."""
    return run_labeling_pipeline()