import streamlit as st
from utils import extract_python_code, execute_code, write_count, retrieve_count
from labeling import run_labeling_pipeline, OptimizationLabeler
from llm_handler import OptimizationLLMHandler


class OptimizationApp:
    """Main application class for the optimization problem solver."""
    
    def __init__(self):
        self.llm_handler = OptimizationLLMHandler()
        self.labeler = OptimizationLabeler()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "latest_output" not in st.session_state:
            st.session_state.latest_output = ""
    
    def setup_ui(self):
        """Set up the main UI components."""
        st.set_page_config(
            page_title="Optimization Problem Solver",
            page_icon="🎯",
            layout="wide"
        )
        
        st.title("🎯 Optimization Problem Solver & Labeler")
        st.markdown("---")
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💬 Chat Interface")
            self.display_chat_interface()
        
        with col2:
            st.subheader("🏷️ Labeling Results")
            self.display_labeling_sidebar()
    
    def display_labeling_sidebar(self):
        """Display the labeling results in the sidebar."""
        latest_output = st.session_state.get("latest_output", "")
        
        # Add a refresh button
        if st.button("🔄 Refresh Labels"):
            st.session_state.latest_output = run_labeling_pipeline()
            st.rerun()
        
        # Text input for custom labeling
        st.subheader("Custom Text Labeling")
        custom_text = st.text_area(
            "Enter text to label:",
            height=100,
            placeholder="Enter your optimization problem text here..."
        )
        
        if st.button("🏷️ Label Custom Text") and custom_text:
            with st.spinner("Labeling text..."):
                result = run_labeling_pipeline(custom_text)
                st.session_state.latest_output = result
                st.rerun()
        
        # Display results
        st.text_area(
            "Labeling Output:",
            value=latest_output,
            height=400,
            disabled=True
        )
    
    def display_chat_interface(self):
        """Display the chat interface."""
        # Chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        self.handle_user_input()
    
    def handle_user_input(self):
        """Handle user input and generate responses."""
        if prompt := st.chat_input("Describe your optimization problem..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing problem..."):
                    # Generate solution
                    output = self.llm_handler.generate_solution(prompt)
                    st.markdown("**Problem Analysis:**")
                    st.markdown(output)
                    
                    # Extract and execute code
                    code = extract_python_code(str(output))
                    if code:
                        st.markdown("**Code Execution:**")
                        code_output = execute_code(code)
                        st.code(code_output, language="text")
                        
                        response = f"{output}\n\n**Code Output:**\n{code_output}"
                    else:
                        response = output
                    
                    # Add labeling
                    st.markdown("**Labeling Analysis:**")
                    with st.spinner("Generating labels..."):
                        labeling_result = run_labeling_pipeline(prompt)
                        st.session_state.latest_output = labeling_result
                        st.success("Labels updated!")
            
            # Store assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    def run(self):
        """Run the main application."""
        self.setup_ui()


def main():
    """Main application entry point."""
    app = OptimizationApp()
    app.run()


if __name__ == "__main__":
    main()