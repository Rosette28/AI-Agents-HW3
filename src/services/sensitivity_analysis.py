import time
import matplotlib.pyplot as plt
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

def run_sensitivity_analysis():
    print("Running LLM Temperature Sensitivity Analysis...")
    temperatures = [0.1, 0.5, 0.9]
    response_times = []

    for temp in temperatures:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=temp, 
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        start_time = time.time()
        # Simulated test prompt
        llm.invoke("Write a detailed 500-word essay on the architecture of Agentic AI.")
        end_time = time.time()
        
        elapsed = end_time - start_time
        response_times.append(elapsed)
        print(f"Temperature {temp}: {elapsed:.2f} seconds")

    # Plot the results
    os.makedirs('notebooks', exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(temperatures, response_times, marker='o', linestyle='-', color='purple')
    plt.title('Sensitivity Analysis: API Latency vs. Temperature')
    plt.xlabel('LLM Temperature')
    plt.ylabel('Response Time (seconds)')
    plt.grid(True)
    plt.savefig('notebooks/sensitivity_analysis.png')
    print("Analysis complete. Graph saved to notebooks/sensitivity_analysis.png")

if __name__ == '__main__':
    run_sensitivity_analysis()