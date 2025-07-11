from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class OptimizationLLMHandler:
    """Handler for LLM-based optimization problem solving."""
    
    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name
        self.template = """ Task: {question}
        Output: Let's analyze the provided optimization function, then generate the equation and rewrite it as python code making sure to keep the answers concise and logical i.e avoiding answers like 0.5 phones, people. etc..
        """
        self.prompt_template = ChatPromptTemplate.from_template(self.template)
        self.model = self._configure_model()
        self.chain = self.prompt_template | self.model
    
    def _configure_model(self):
        """Configure the Ollama LLM model."""
        return OllamaLLM(
            model=self.model_name,
            stop=["question:"],
            temperature=0.4,
            num_predict=-2,
            seed=1786
        )
    
    def generate_solution(self, prompt: str) -> str:
        """
        Generate an optimization solution from a natural language prompt.
        
        Args:
            prompt (str): The optimization problem description
            
        Returns:
            str: Generated solution with Python code
        """
        context_text = f"""The task at hand is understanding the following optimization problem and transforming it into an optimization equation as python code which utilizes the pulp library, the problem is as follows:
        {prompt}
        """
        
        return self.chain.invoke({"question": context_text})
    
    def generate_with_callback(self, prompt: str) -> str:
        """Generate solution with streaming callback for real-time output."""
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        # Create a new model instance with callback for this generation
        model_with_callback = OllamaLLM(
            model=self.model_name,
            stop=["question:"],
            temperature=0.4,
            num_predict=-2,
            seed=1786,
            callback_manager=callback_manager
        )
        
        chain_with_callback = self.prompt_template | model_with_callback
        
        context_text = f"""The task at hand is understanding the following optimization problem and transforming it into an optimization equation as python code which utilizes the pulp library, the problem is as follows:
        {prompt}
        """
        
        return chain_with_callback.invoke({"question": context_text})