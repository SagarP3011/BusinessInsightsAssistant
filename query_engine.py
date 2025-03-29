import google.generativeai as genai
import os

class QueryEngine:
    def __init__(self):
        self.business_categories = ["finance", "marketing", "operations", "sales", "strategy"]
        self.setup_gemini()

    def setup_gemini(self):
        """Set up Google Gemini API key."""
        API_KEY = "Your_API_Key"  
        os.environ["GOOGLE_API_KEY"] = API_KEY
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def extract_business_context(self, query: str):
        """Extracts business context from user queries."""
        for category in self.business_categories:
            if category in query.lower():
                return category
        return "general"

    def generate_gemini_response(self, query: str):
        """Generates AI-powered recommendations using Google Gemini."""
        category = self.extract_business_context(query)
        prompt = f"""
        You are an AI business consultant. A user has asked about {category}. Provide a structured response with:
        1. Key challenges related to the query.
        2. Data-driven insights.
        3. Industry best practices.
        4. Strategic recommendations.
        
        User Query: {query}
        """

        response = self.model.generate_content(prompt)
        return response.text

# Testing
if __name__ == "__main__":
    engine = QueryEngine()
    user_query = "How can we improve our digital marketing strategy?"
    response = engine.generate_gemini_response(user_query)
    print(response)
