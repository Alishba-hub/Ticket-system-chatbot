from State_of_node import State
from langgraph.graph import END
from graph_const import graph_compile
from langgraph.checkpoint.memory import MemorySaver
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


graph, _ = graph_compile({})
thread_id = 1

class SupportTicketBackend:
    def __init__(self):
        self.graph = graph
        self.thread_counter = 1
    
    def process_ticket(self, subject, description, thread_id=None):
        """
        Process a new ticket using your existing graph logic
        """
        if thread_id is None:
            self.thread_counter += 1
            thread_id = self.thread_counter
        
        
        state_dict = {
            "subject": subject,
            "description": description,
            "category": "",
            "context": "",
            "draft": "",
            "review_feedback": "",
            "status_of_feedback": "",
            "final_response": "",
            "no_of_try": 0,
        }
        
        
        result = self.graph.invoke(state_dict, config={"configurable": {"thread_id": thread_id}})
        state_dict = result  
        
        response = state_dict.get("final_response", "⚠️ No response generated.")
        return {
            "response": response,
            "thread_id": thread_id,
            "state": state_dict
        }
    
    def process_followup(self, follow_up_message, thread_id, current_state):
        """
        Process follow-up messages using your existing logic
        """
        current_state["description"] = follow_up_message
        
        result = self.graph.invoke(current_state, config={"configurable": {"thread_id": thread_id}})
        state_dict = result 
        
        followup_response = state_dict.get("final_response", "⚠️ No response generated.")
        return {
            "response": followup_response,
            "thread_id": thread_id,
            "state": state_dict
        }

# Initializing backend hereeeee
backend = SupportTicketBackend()

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve the CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """Serve the JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/api/process_ticket', methods=['POST'])
def api_process_ticket():
    """API endpoint to process new tickets"""
    try:
        data = request.json
        subject = data.get('subject', '').strip()
        description = data.get('description', '').strip()
        
        if not subject or not description:
            return jsonify({"error": "Subject and description are required"}), 400
        
        result = backend.process_ticket(subject, description)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/api/process_followup', methods=['POST'])
def api_process_followup():
    """API endpoint to process follow-up messages"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        thread_id = data.get('thread_id')
        current_state = data.get('current_state', {})
        
        if not message or not thread_id:
            return jsonify({"error": "Message and thread_id are required"}), 400
        
        result = backend.process_followup(message, thread_id, current_state)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    print("🎫 Starting Support Ticket System with Modular Frontend")
    print("📱 Frontend: http://localhost:5000")
    print("📁 Files Structure:")
    print("   - index.html (Main HTML structure)")
    print("   - styles.css (All CSS styles)")
    print("   - script.js (All JavaScript functionality)")
    print("🔧 API Endpoints:")
    print("   POST /api/process_ticket")
    print("   POST /api/process_followup")
    app.run(debug=True, host='0.0.0.0', port=5000)