import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .openai_server import *

rpc_id = 1

@csrf_exempt
def chat_view(request):
    global rpc_id

    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are supported"}, status=405)

    user_input = request.GET.get("q", "")
    if not user_input:
        return JsonResponse({"error": "Missing 'q' parameter"}, status=400)

    try:
        rpc_instruction = generate_rpc(user_input, rpc_id)
        rpc_id += 1
        tool_result = execute_rpc(rpc_instruction)
        final_answer = format_response(user_input, tool_result)

        return JsonResponse({
            "answer": final_answer,
            "raw_tool_result": tool_result,
            "rpc_instruction": rpc_instruction
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
