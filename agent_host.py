import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the secret API key from the .env file safely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found. Please check your .env file.")
    exit()

# 2. Configure the AI Brain
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') 

print("Initializing CogniSync Multi-Agent Orchestrator...")
print("Connecting to Gemini AI Engine...\n")

class SupervisorAgent:
    def __init__(self):
        self.role = "Academic Supervisor"
        print("[Supervisor]: Active. Ready to delegate tasks.")

    def delegate_task(self, task_type: str, file_context: str):
        print(f"\n[Supervisor]: Received localized context. Analyzing routing rules...")
        
        if "physics" in task_type.lower() or "study guide" in task_type.lower():
            tutor = TutorAgent("Physics Concept Expert")
            tutor.execute(file_context)
        elif "planner" in task_type.lower() or "schedule" in task_type.lower():
            scheduler = PlannerAgent("JEE Study Planner")
            scheduler.execute(file_context)
        else:
            print("[Supervisor]: No suitable agent found for this task.")

class TutorAgent:
    def __init__(self, specialty):
        self.specialty = specialty

    def execute(self, context):
        print(f"[Tutor Agent ({self.specialty})]: Analyzing sanitized educational materials...")
        print(f"[Tutor Agent]: Requesting deep conceptual query generation...\n")
        
        prompt = f"""
        You are an elite Tutor. 
        Based on the following sanitized syllabus material, generate 1 challenging conceptual practice question, followed by a step-by-step solution.
        
        Sanitized Local Data:
        {context}
        """
        response = model.generate_content(prompt)
        print("================ TUTOR AGENT OUTPUT ================")
        print(response.text)
        print("====================================================\n")

class PlannerAgent:
    def __init__(self, specialty):
        self.specialty = specialty

    def execute(self, context):
        print(f"[Planner Agent ({self.specialty})]: Parsing schedule constraints...")
        print(f"[Planner Agent]: Generating optimized countdown milestones...\n")
        
        prompt = f"""
        You are an elite Academic Planner. 
        Based on the following syllabus topics, generate an optimized, high-intensity weekly revision countdown schedule and milestone plan to master these concepts.
        
        Topics to schedule:
        {context}
        """
        response = model.generate_content(prompt)
        print("================ PLANNER AGENT OUTPUT ================")
        print(response.text)
        print("====================================================\n")

if __name__ == "__main__":
    supervisor = SupervisorAgent()
    
    # Context data from the local server
    mock_mcp_output = "Successfully extracted 1 page:\n\nPhysics Syllabus Chapter 1: Kinematics (Projectile motion) and Vectors (Dot and Cross products)."
    
    # Execution 1: Run the Tutor Pipeline
    supervisor.delegate_task(task_type="Physics Study Guide", file_context=mock_mcp_output)
    
    # Execution 2: Run the Planning Pipeline
    supervisor.delegate_task(task_type="Revision Planner Schedule", file_context=mock_mcp_output)