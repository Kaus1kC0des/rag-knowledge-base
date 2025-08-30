"""
AI Response Generator using Google Gemini via LangChain
Generates contextual responses based on retrieved chunks
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

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
                max_tokens=2048,  # Limit response length
                timeout=30,  # Timeout for API calls
            )

            # Create the prompt template
            self.chain = self._create_response_chain()

            print(f"✅ Gemini Response Generator initialized with {self.model_name}")

        except Exception as e:
            print(f"❌ Failed to initialize Gemini Response Generator: {e}")
            raise

    def _create_response_chain(self):
        """Create the LangChain response generation chain"""

        # System prompt for RAG with Markdown formatting
        system_template = """
        You are an expert educational assistant helping students understand complex topics.
        Always respond in well-formatted Markdown for better readability.

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

        **Formatting Instructions:**
        - Use **bold** for important terms and concepts
        - Use *italics* for emphasis
        - Use `code blocks` for technical terms, formulas, or code snippets
        - Use numbered lists (1., 2., 3.) for steps or sequences
        - Use bullet points (-, *) for lists of items
        - Use ### headings for main sections
        - Use > blockquotes for important notes or definitions
        - Use tables when comparing concepts or showing data

        Question: {question}

        Subject: {subject}
        Unit: {unit}
        """

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(system_template)

        # Create the chain: prompt -> LLM -> string output
        chain = (
            RunnablePassthrough()  # Pass through all inputs
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
            print(f"❌ Error generating response: {e}")
            return f"I apologize, but I encountered an error while generating a response. Please try again. Error: {str(e)}"

    def _format_context(self, chunks: List[Dict[str, Any]], max_chunks: int) -> str:
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
        😔 **I apologize**, but I couldn't find specific information about *"{question}"* in the **{subject} - {unit}** materials.

        ### Possible Reasons:
        1. **Topic Coverage**: The topic might not be covered in the available materials
        2. **Question Phrasing**: The question might need to be rephrased differently
        3. **Search System**: There might be an issue with the search system

        ### Suggestions:
        - Try rephrasing your question
        - Ask about a specific concept from the unit
        - Check if the topic is covered in the unit materials

        {error_info}
        """

        error_info = f"\n\n**Technical Details:**\n```\n{error_message}\n```" if error_message else ""

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
    Get the global response generator instance (singleton pattern)
    """
    global _response_generator_instance

    async with _response_lock:
        if _response_generator_instance is None:
            _response_generator_instance = GeminiResponseGenerator()
            await _response_generator_instance.initialize()

    return _response_generator_instance

# FastAPI Dependency
async def get_ai_response_dependency() -> GeminiResponseGenerator:
    """FastAPI dependency for AI response generator"""
    return await get_response_generator()

# Example usage function
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

if __name__ == "__main__":
    # Example usage
    async def test_generator():
        print("🤖 Gemini Response Generator ready for integration!")

        # Test with mock data
        mock_chunks = [
            {
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
                "score": 0.95
            },
            {
                "content": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.",
                "score": 0.89
            }
        ]

        generator = GeminiResponseGenerator()
        await generator.initialize()

        response = await generator.generate_response(
            "What is machine learning?",
            mock_chunks,
            "Generative AI",
            "Unit 1"
        )

        print("Generated Response:")
        print(response)

    asyncio.run(test_generator())
