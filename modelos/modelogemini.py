import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

class ModeloGemini:
    
    def __init__(self, api_key: str = None):
        # Cargar variables desde .env si existe
        load_dotenv()

        # Usar la clave pasada o leer del entorno
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("No se encontró GOOGLE_API_KEY o GEMINI_API_KEY en el entorno o en el archivo .env")

        # Configurar el modelo de Gemini con LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.7,
            google_api_key=api_key
        )

        # Plantilla base de prompt (puedes modificarla a gusto)
        self.prompt = PromptTemplate.from_template("{instruccion}")

    def generar(self, prompt: str) -> str:
        """Genera texto a partir del prompt usando Gemini"""
        prompt = (prompt or "").strip()
        if not prompt:
            return "⚠ Escribe un prompt válido."

        # Encadenar prompt y modelo (LCEL pipeline)
        chain = self.prompt | self.llm
        respuesta = chain.invoke({"instruccion": prompt})
        return getattr(respuesta, "content", str(respuesta))