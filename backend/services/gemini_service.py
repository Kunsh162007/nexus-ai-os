"""
Google Gemini AI Service for Nexus AI OS
"""
import google.generativeai as genai
from typing import Optional, Dict, Any, List
from loguru import logger
import asyncio
from functools import lru_cache

from core.config import settings


class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self._configure_api()
        self.pro_model = None
        self.flash_model = None
        
    def _configure_api(self):
        """Configure Gemini API"""
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise
    
    def _get_pro_model(self):
        """Get Gemini Pro model (lazy loading)"""
        if not self.pro_model:
            self.pro_model = genai.GenerativeModel(settings.GEMINI_MODEL_PRO)
        return self.pro_model
    
    def _get_flash_model(self):
        """Get Gemini Flash model (lazy loading)"""
        if not self.flash_model:
            self.flash_model = genai.GenerativeModel(settings.GEMINI_MODEL_FLASH)
        return self.flash_model
    
    async def generate_response(
        self,
        prompt: str,
        use_flash: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate response from Gemini
        
        Args:
            prompt: Input prompt
            use_flash: Use Flash model for faster responses
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            system_instruction: System instruction for the model
            
        Returns:
            Generated text response
        """
        try:
            model = self._get_flash_model() if use_flash else self._get_pro_model()
            
            generation_config = {
                "temperature": temperature or settings.TEMPERATURE,
                "max_output_tokens": max_tokens or settings.MAX_TOKENS,
            }
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise
    
    async def generate_structured_response(
        self,
        prompt: str,
        schema: Dict[str, Any],
        use_flash: bool = False
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response from Gemini
        
        Args:
            prompt: Input prompt
            schema: Expected JSON schema
            use_flash: Use Flash model
            
        Returns:
            Structured response as dictionary
        """
        try:
            # Add schema to prompt
            structured_prompt = f"""
{prompt}

Please respond with a valid JSON object matching this schema:
{schema}

Response (JSON only):
"""
            
            response_text = await self.generate_response(
                structured_prompt,
                use_flash=use_flash,
                temperature=0.3  # Lower temperature for structured output
            )
            
            # Parse JSON response
            import json
            # Extract JSON from markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logger.error(f"Error generating structured response: {e}")
            raise
    
    async def analyze_multimodal(
        self,
        prompt: str,
        files: List[Dict[str, Any]],
        use_flash: bool = False
    ) -> str:
        """
        Analyze multimodal content (text, images, documents)
        
        Args:
            prompt: Analysis prompt
            files: List of files with 'type' and 'content' keys
            use_flash: Use Flash model
            
        Returns:
            Analysis result
        """
        try:
            model = self._get_flash_model() if use_flash else self._get_pro_model()
            
            # Prepare multimodal content
            content_parts = [prompt]
            
            for file in files:
                if file['type'] == 'image':
                    # Add image data
                    content_parts.append(file['content'])
                elif file['type'] == 'document':
                    # Add document text
                    content_parts.append(f"\n\nDocument content:\n{file['content']}")
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(content_parts)
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing multimodal content: {e}")
            raise
    
    async def extract_entities(
        self,
        text: str,
        entity_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract entities from text
        
        Args:
            text: Input text
            entity_types: Types of entities to extract
            
        Returns:
            List of extracted entities
        """
        try:
            entity_types_str = ", ".join(entity_types) if entity_types else "all relevant entities"
            
            prompt = f"""
Extract {entity_types_str} from the following text.
Return a JSON array of entities with 'type', 'value', and 'context' fields.

Text:
{text}

Entities (JSON array):
"""
            
            response = await self.generate_structured_response(
                prompt,
                schema={"entities": [{"type": "string", "value": "string", "context": "string"}]},
                use_flash=True
            )
            
            return response.get('entities', [])
            
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            raise
    
    async def summarize_long_context(
        self,
        text: str,
        max_length: int = 500,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        Summarize long-context text using Gemini's 1M token context
        
        Args:
            text: Long text to summarize
            max_length: Maximum summary length in words
            focus_areas: Specific areas to focus on
            
        Returns:
            Summary text
        """
        try:
            focus_str = ""
            if focus_areas:
                focus_str = f"\nFocus particularly on: {', '.join(focus_areas)}"
            
            prompt = f"""
Provide a comprehensive summary of the following text in approximately {max_length} words.
{focus_str}

Text:
{text}

Summary:
"""
            
            return await self.generate_response(
                prompt,
                use_flash=False,  # Use Pro for better quality
                temperature=0.5
            )
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            raise
    
    async def generate_embeddings(
        self,
        texts: List[str],
        task_type: str = "retrieval_document"
    ) -> List[List[float]]:
        """
        Generate embeddings for texts
        
        Args:
            texts: List of texts to embed
            task_type: Task type for embeddings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = []
            
            for text in texts:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: genai.embed_content(
                        model="models/embedding-001",
                        content=text,
                        task_type=task_type
                    )
                )
                embeddings.append(result['embedding'])
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    async def chat_conversation(
        self,
        messages: List[Dict[str, str]],
        use_flash: bool = True
    ) -> str:
        """
        Handle multi-turn conversation
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            use_flash: Use Flash model for faster responses
            
        Returns:
            Assistant response
        """
        try:
            model = self._get_flash_model() if use_flash else self._get_pro_model()
            
            # Start chat session
            chat = model.start_chat(history=[])
            
            # Add previous messages to history
            for msg in messages[:-1]:
                if msg['role'] == 'user':
                    chat.send_message(msg['content'])
            
            # Send final message and get response
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: chat.send_message(messages[-1]['content'])
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in chat conversation: {e}")
            raise


# Global service instance
@lru_cache()
def get_gemini_service() -> GeminiService:
    """Get Gemini service instance"""
    return GeminiService()

# Made with Bob
