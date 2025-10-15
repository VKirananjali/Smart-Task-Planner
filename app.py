import os
import time 
import json
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "google/gemma-3-1B-it-QAT"

app = Flask(__name__)

PLANS_DIRECTORY = 'saved_plans' 
os.makedirs(PLANS_DIRECTORY, exist_ok=True)

def get_goal_timeline(query):
    
    prompt= f"""
    You are an intelligent text analysis assistant. Your task is to extract the core 'goal' and the 'timeline' from the user's request and return it as a JSON object.

    Analyze the user request: "{query}"

    Extract the information into a valid JSON object with two keys: "goal" and "timeline".
    - The "goal" should be a clear, concise action phrase describing the main objective.
    - The "timeline" should be the duration or deadline mentioned.
    - If no specific timeline is meprint(query)ntioned, set the value of "timeline" to "unspecified".

    IMPORTANT: ONLY output the JSON object with goal and timeline. Do not include any other text, explanations, or markdown formatting like ```json.
    """

    try:    
        response = ask(prompt)
        cleaned_response = response.strip().replace("```json", "").replace("```", "")
        extracted_info = json.loads(cleaned_response)
        user_goal = extracted_info.get('goal', '')
        user_timeline = extracted_info.get('timeline', 'unspecified')
        status= 'OK'

    except json.JSONDecodeError:
        user_goal = ''
        user_timeline = 'unspecified'
        status= 'JSONDecodeError'

    except Exception as e:
        print(f"An error occurred: {e}")
        user_goal = ''
        user_timeline = 'unspecified'
        status= f'Error {e}'
    return user_goal, user_timeline, status


def get_planner_prompt(goal, timeline):
    
    prompt= f"""
    You are an expert project manager AI. Your task is to break down a user's goal into a complete, actionable plan.

    Goal: "{goal}"
    Timeline: "{timeline}"

    Generate a detailed project plan in a valid JSON format. The JSON should be an array of objects, where each object represents a major phase of the project.

    Each phase object must contain:
    - "phase_name": A string name for the phase (e.g., "Phase 1: Research and Planning").
    - "tasks": An array of task objects.

    Each task object must contain:
    - "task_id": A unique integer identifier for the task (e.g., 1, 2, 3).
    - "task_name": A concise string name for the task.
    - "description": A brief one-sentence description of the task.
    - "start_day": An integer representing the start day of the task.
    - "end_day": An integer representing the end day of the task.
    - "dependencies": An array of integers, listing the 'task_id's of tasks that must be completed before this one can start. An empty array [] means no dependencies.

    IMPORTANT RULES:
    1. The entire plan must logically fit within the given timeline.
    2. Ensure dependencies are logical. A task cannot depend on a task that starts later.
    3. Provide a complete breakdown covering all key aspects of the goal.
    4. ONLY output the JSON object. Do not include any other text, explanations, or markdown formatting like ```json.
    """
    return prompt

def ask(prompt):
    response = client.chat.completions.create(
        model=MODEL,   messages=[
            {"role": "user",
            "content":prompt}
            ]
    )
    reply = response.choices[0].message.content
    return reply


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def create_plan():
    
    user_msg = request.json.get('query', '')
    print(user_msg)
    user_goal, user_timeline, status= get_goal_timeline(user_msg)
    

    if status != 'OK':
        return jsonify({"error": status}), 400
    
    if not user_goal:
        return jsonify({"error": "Could not extract a valid goal from the user message."}), 400

    try:
        prompt = get_planner_prompt(user_goal, user_timeline)
        response = ask(prompt)
        print(response)

        cleaned_response = response.strip().replace("```json", "").replace("```", "")
        plan_json = json.loads(cleaned_response)
        print(plan_json)
        # enter intlo db.
        store(prompt, plan_json)
        return jsonify(plan_json), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse LLM response as JSON."}), 500
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    

def store(user_query,plan_json):
    filename = f"{int(time.time())}.json"
    filepath = os.path.join(PLANS_DIRECTORY, filename)

    data_to_save = {
        "user_query": user_query,
        "plan_data": plan_json
    }
    
    # Write the data to the file
    with open(filepath, 'w') as f:
        json.dump(data_to_save, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)