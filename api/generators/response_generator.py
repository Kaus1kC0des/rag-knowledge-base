"""
AI Response Generator using Google Gemini via LangChain
Generates contextual responses based on retrieved chunks
"""

import os
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import asyncio

load_dotenv()

class GeminiResponseGenerator:
    """
    Generates AI responses using Google Gemini with retrieved context
    """
    
    def __init__(self, model_name: str = "gemini-1.5-pro", temperature: float = 0.3):
        """
        Initialize the Gemini response generator
        
        Args:
            model_name: Gemini model to use (gemini-1.5-pro, gemini-1.5-flash, etc.)
            temperature: Creativity level (0.0 = deterministic, 1.0 = creative)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        self.chain = None
        
    async def initialize(self):
        """Initialize the LangChain components"""
        try:
            # Initialize Gemini model
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                max_tokens=2048,
                timeout=30,
            )
            
            # Prompt template
            self.chain = self._create_response_chain()

        except Exception as e:
            print(f"Failed to initialize Gemini Response Generator: {e}")
            raise
    
    def _create_response_chain(self):
        """Create the LangChain response generation chain"""
        
        # System prompt for RAG
        system_template = """
        You are an expert educational assistant helping students understand complex topics.
        
        Use the following retrieved information to answer the student's question accurately and comprehensively.
        
        Retrieved Context:
        {context}
        
        Guidelines:
        - Answer based primarily on the provided context
        - If the context doesn't fully answer the question, say so clearly
        - Provide clear, step-by-step explanations when appropriate
        - Use examples from the context when available
        - Keep responses focused and relevant
        - Be encouraging and supportive in your tone
        
        Question: {question}
        
        Subject: {subject}
        """
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(system_template)
        
        # Create the chain: prompt -> LLM -> string output
        chain = (
            RunnablePassthrough()
            | prompt
            | self.llm
            | StrOutputParser()  # Convert to string
        )
        
        return chain
    
    async def generate_response(
        self, 
        question: str,
        context_chunks: List[Dict[str, Any]],
        subject: str,
        unit: str,
        max_chunks: int = 5
    ) -> str:
        """
        Generate an AI response using retrieved context
        
        Args:
            question: The user's question
            context_chunks: List of retrieved chunks with content
            subject: Subject name
            unit: Unit name
            max_chunks: Maximum number of chunks to include in context
            
        Returns:
            Generated AI response
        """
        if not self.chain:
            raise RuntimeError("Response generator not initialized. Call initialize() first.")
        
        try:
            # Format context from chunks
            context = self._format_context(context_chunks, max_chunks)
            
            # Prepare inputs for the chain
            inputs = {
                "question": question,
                "context": context,
                "subject": subject,
                "unit": unit
            }
            
            # Generate response
            response = await self.chain.ainvoke(inputs)
            
            return response.strip()
            
        except Exception as e:
            print(f"Error generating response: {e.with_traceback()}")
            return f"I apologize, but I encountered an error while generating a response. Please try again. Error: {str(e)}"
    
    def _format_context(self, chunks: List[Dict[str, Any]], max_chunks: int = -1) -> str:
        """
        Format retrieved chunks into a readable context string
        
        Args:
            chunks: List of chunk dictionaries
            max_chunks: Maximum number to include
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant information found in the knowledge base."
        
        # Take top chunks
        top_chunks = chunks[:max_chunks]
        
        # Format each chunk
        formatted_chunks = []
        for i, chunk in enumerate(top_chunks, 1):
            content = chunk.get("content", "").strip()
            if content:
                formatted_chunks.append(f"[Chunk {i}]\n{content}")
        
        # Join with separators
        context = "\n\n".join(formatted_chunks)
        
        return context
    
    async def generate_fallback_response(
        self, 
        question: str,
        subject: str,
        unit: str,
        error_message: str = ""
    ) -> str:
        """
        Generate a fallback response when no context is available
        
        Args:
            question: The user's question
            subject: Subject name
            unit: Unit name
            error_message: Any error that occurred
            
        Returns:
            Fallback response
        """
        fallback_template = """
        I apologize, but I couldn't find specific information about "{question}" 
        in the {subject} - {unit} materials.
        
        This could mean:
        1. The topic might not be covered in the available materials
        2. The question might need to be rephrased
        3. There might be an issue with the search system
        
        Please try:
        - Rephrasing your question
        - Asking about a specific concept from the unit
        - Checking if the topic is covered in the unit materials
        
        {error_info}
        """
        
        error_info = f"\nTechnical details: {error_message}" if error_message else ""
        
        return fallback_template.format(
            question=question,
            subject=subject,
            unit=unit,
            error_info=error_info
        ).strip()

# Global instance for singleton pattern
_response_generator_instance: Optional[GeminiResponseGenerator] = None
_response_lock = asyncio.Lock()

async def get_response_generator() -> GeminiResponseGenerator:
    """
    Get the global response generator instance
    """
    global _response_generator_instance
    
    async with _response_lock:
        if _response_generator_instance is None:
            _response_generator_instance = GeminiResponseGenerator()
            await _response_generator_instance.initialize()
    
    return _response_generator_instance

# FastAPI Dependenc
async def get_ai_response_dependency() -> GeminiResponseGenerator:
    """FastAPI dependency for AI response generator"""
    return await get_response_generator()

async def generate_ai_response(
    question: str,
    chunks: List[Dict[str, Any]],
    subject: str,
    unit: str
) -> str:
    """
    Convenience function to generate AI responses
    
    Usage:
    response = await generate_ai_response(
        "What is machine learning?",
        retrieved_chunks,
        "Generative AI", 
        "Unit 1"
    )
    """
    generator = await get_response_generator()
    return await generator.generate_response(question, chunks, subject, unit)