from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging

# --- Configuración de logging (igual que tu original) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModeloLLMChain:
    def __init__(self, model: str = "gemini-1.5-flash", temperature: float = 0.7): # Actualizado a un modelo más reciente
        self.model_name = model
        self.temperature = temperature
        self.llm = None
        self.chain = None
        self._configurar_entorno()
        self._inicializar_modelo()
        self._crear_cadena()

    def _configurar_entorno(self) -> None:
        os.environ["GRPC_VERBOSITY"] = "NONE"
        os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
        logging.getLogger("absl").setLevel(logging.ERROR)
        logging.getLogger("grpc").setLevel(logging.ERROR)
        
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("Variable GOOGLE_API_KEY o GEMINI_API_KEY no encontrada en .env")
            raise ValueError("Falta GOOGLE_API_KEY o GEMINI_API_KEY en el archivo .env")
        os.environ["GOOGLE_API_KEY"] = api_key

    def _inicializar_modelo(self) -> None:
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature
            )
        except Exception as e:
            raise ValueError(f"Error con Gemini API: {e}")

    def _crear_cadena(self) -> None:
        template = "Explícale a un estudiante universitario el tema {tema}."
        self.prompt_template = PromptTemplate.from_template(template)
        # -------------------------------
        self.chain = self.prompt_template | self.llm

    def generar(self, prompt_usuario: str) -> str:
        if not prompt_usuario or not prompt_usuario.strip():
            return "Por favor, introduce un prompt válido."
        try:
            respuesta = self.chain.invoke({"tema": prompt_usuario.strip()})
            
            return respuesta.content if hasattr(respuesta, "content") else str(respuesta)
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    try:
        print("Inicializando la cadena...")
        mi_cadena = ModeloLLMChain()
        print("Cadena lista.")
        
        tema_usuario = "el aprendizaje automático"
        print(f"\nPreguntando sobre: {tema_usuario}")
        
        respuesta = mi_cadena.generar(tema_usuario)
        print("\n--- Respuesta del Modelo (con contexto de estudiante) ---")
        print(respuesta)
        print("---------------------------------------------------------")
        
    except ValueError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"Un error inesperado ocurrió: {e}")