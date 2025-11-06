import json
import datetime
import zoneinfo
from openai import OpenAI

# --- Tools ---
def write_message_to_file(message: str):
    try:
        with open("messages.log", "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
        return "Message was created successfully!"
    except Exception as e:
        return f"Error: {e}"

def create_html_template(message: str):
    try:
        with open("templates/example-code-agent.html", "w", encoding="utf-8") as f:
            f.write(f"{message}\n")
        return "Template was updated"
    except Exception as e:
        return f"Error: {e}"

def generate_trip_price(message: str):
    try:
        with open("rag.txt", "r", encoding="utf-8") as f:
            return f"Prices: {f.read()}, Request: {message}"
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    ####
    # Method get time by timezone
    ####
    "get_time": lambda timezone: {
        "time": datetime.datetime.now(zoneinfo.ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timezone": timezone
    },

    ####
    # Group of methods that works with messages
    ####
    "say_hello": lambda name: {"message": f"Hello, {name}!"},
    "get_firstname_lastname": lambda firstname, lastname: {"message": f"First name {firstname}, Last name: {lastname}."},

    # "strange_message": lambda message: {"message": f"It's wrong {message}!"},
    "strange_message": lambda message: {"message": f"It's wrong message! Provide user with polite response."},
    # "strange_message": lambda message: {"message": f"It's wrong message! Don't reply. Provide user with polite response."},

    ####
    # Method work with file system
    ####
    "write_message": lambda message: { "message": write_message_to_file(message)},
    "create_template": lambda message: { "message": create_html_template(message) },

    ####
    # Retrieval Augmented Generation method
    ####
    # "get_trip_price": lambda message: { "message": generate_trip_price(message) }
    "get_trip_price": lambda message: { "message": f"Prices: { generate_trip_price(message) }, Request: { message }" }

}

# --- OpenAI client ---
api_key = ''
client = OpenAI(api_key=api_key)

rpc_id = 1

def generate_rpc(user_input, rpc_id):
    prompt = f"""
    You are an AI agent. The user query is:
    \"\"\"{user_input}\"\"\"

    Available tools:
    1. get_time(timezone: str)
    2. say_hello(name: str)
    3. strange_message(message: str)
    4. get_firstname_lastname(firstname: str, lastname: str)
    5. write_message(message: str)
    6. create_template(message: str)
    7. get_trip_price(message: str)

    Instructions:
    - If the user query explicitly requests HTML code, your JSON-RPC must call the "create_template" tool, and the resulting output should contain only the HTML code in the "message" argument. Do not add any extra text outside the HTML.
    - Otherwise, return a valid JSON-RPC dictionary for the appropriate tool.

    Return a valid JSON-RPC dictionary:
    {{"jsonrpc":"2.0","id":{rpc_id},"method":"call_tool","params":{{"name": "<tool_name>", "arguments":{{...}}}}}}
    Only JSON, no extra text.



    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    rpc_json = response.choices[0].message.content.strip()
    return json.loads(rpc_json)

def execute_rpc(rpc_instruction):
    try:
        params = rpc_instruction["params"]
        tool_name = params["name"]
        arguments = params.get("arguments", {})
        if tool_name not in TOOLS:
            return {"error": f"Unknown tool {tool_name}"}
        return {"result": TOOLS[tool_name](**arguments)}
    except Exception as e:
        return {"error": str(e)}

def format_response(user_input, tool_result):
    prompt = f"""
The user asked: "{user_input}"
The tool returned: {tool_result}
Return helpful natural language answer.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
