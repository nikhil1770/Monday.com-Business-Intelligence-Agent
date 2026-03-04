"""
AI Agent with OpenAI Integration
Handles query understanding and Monday.com data retrieval
"""

import os
import sys

# Clear ALL proxy settings
for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
            'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']:
    os.environ.pop(var, None)

# Create a custom httpx client that ignores proxies
import httpx

def create_http_client():
    """Create HTTP client without proxy support"""
    return httpx.Client(
        timeout=httpx.Timeout(timeout=600.0, connect=60.0),
        follow_redirects=True,
        limits=httpx.Limits(max_connections=1000, max_keepalive_connections=100)
    )

import json
from openai import OpenAI
from config import OPENAI_API_KEY
import monday_api

# Define tools for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_deals",
            "description": "Query deals from Monday.com Deals board. Returns deal information including deal name, status, sector, value, etc. Can filter by sector (e.g., 'Renewables', 'Mining', 'Railways') and status (e.g., 'Won', 'Open', 'Dead').",
            "parameters": {
                "type": "object",
                "properties": {
                    "sector": {
                        "type": "string",
                        "description": "Filter by sector/industry (e.g., 'Renewables', 'Mining', 'Railways', 'Powerline')"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by deal status (e.g., 'Won', 'Open', 'Dead', 'On Hold')"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_work_orders",
            "description": "Query work orders from Monday.com Work Orders board. Returns project execution data. Can filter by sector and execution status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sector": {
                        "type": "string",
                        "description": "Filter by sector"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by execution status (e.g., 'Completed', 'Ongoing', 'Not Started')"
                    }
                }
            }
        }
    }
]


def process_query(user_question):
    """
    Process user question using OpenAI with Monday.com tools
    
    Args:
        user_question: The user's business intelligence query
    
    Returns:
        tuple: (answer_text, action_log_list)
    """
    action_log = []
    action_log.append(f"📝 User question: {user_question}")
    
    try:
        # Initialize OpenAI client with custom HTTP client
        action_log.append("🤖 Initializing OpenAI API...")
        
        # Create custom HTTP client without proxy support
        http_client = create_http_client()
        
        # Create OpenAI client pointing to Cerebras
        client = OpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=OPENAI_API_KEY,
            http_client=http_client
        )
        
        action_log.append("🤖 Analyzing question with gpt-oss-120b...")
        
        messages = [
            {"role": "system", "content": "You are a data analysis assistant. You have access to tools that return arrays of records. When asked to count records, ALWAYS look at the exact length of the JSON array returned by the tool. DO NOT guess or hallucinate numbers. Be exact."},
            {"role": "user", "content": user_question}
        ]
        
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=messages,
            tools=tools
        )
        
        # Process tool calls
        tool_call_count = 0
        while response.choices and response.choices[0].message.tool_calls:
            assistant_message = response.choices[0].message
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                    for tool_call in assistant_message.tool_calls
                ]
            })
            
            for tool_call in assistant_message.tool_calls:
                tool_call_count += 1
                
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}
                    
                action_log.append(f"\n🔧 Tool Call #{tool_call_count}: {tool_call.function.name}")
                action_log.append(f"   Parameters: {json.dumps(tool_args, indent=6)}")
                
                # Execute tool
                if tool_call.function.name == "query_deals":
                    action_log.append(f"    Querying Deals board (ID: {monday_api.DEALS_BOARD_ID})...")
                    raw_result = monday_api.get_deals(**tool_args)
                    
                    if isinstance(raw_result, list):
                        action_log.append(f"   ✅ Retrieved {len(raw_result)} deals")
                        if len(raw_result) > 10:
                            result = {"count": len(raw_result), "deals_sample": raw_result[:10], "notice": "Data truncated to save tokens. Use 'count' for totals."}
                        else:
                            result = {"count": len(raw_result), "deals": raw_result}
                    else:
                        action_log.append(f"   ❌ Error: {raw_result.get('error', 'Unknown error')}")
                        result = raw_result
                        
                elif tool_call.function.name == "query_work_orders":
                    action_log.append(f"   🔧 Querying Work Orders board (ID: {monday_api.WORK_ORDERS_BOARD_ID})...")
                    raw_result = monday_api.get_work_orders(**tool_args)
                    
                    if isinstance(raw_result, list):
                        action_log.append(f"   ✅ Retrieved {len(raw_result)} work orders")
                        if len(raw_result) > 10:
                            result = {"count": len(raw_result), "work_orders_sample": raw_result[:10], "notice": "Data truncated to save tokens. Use 'count' for totals."}
                        else:
                            result = {"count": len(raw_result), "work_orders": raw_result}
                    else:
                        action_log.append(f"   ❌ Error: {raw_result.get('error', 'Unknown error')}")
                        result = raw_result
                else:
                    result = {"error": "Unknown tool call"}
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(result)
                })
            
            # Continue conversation with tool result
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=messages,
                tools=tools
            )
        
        # Extract final answer
        if response.choices:
            answer = response.choices[0].message.content or ""
        else:
            answer = ""
            
        action_log.append(f"\n✅ Generated response")
        
        return answer, action_log
    
    except Exception as e:
        error_msg = f"❌ Error processing query: {str(e)}"
        action_log.append(error_msg)
        
        # Add helpful debug info
        import traceback
        action_log.append(f"\nDebug info:\n{traceback.format_exc()}")
        
        return f"Sorry, I encountered an error: {str(e)}", action_log


if __name__ == "__main__":
    # Test the agent
    print("Testing agent with OpenAI integration...")
    
    test_question = "How many deals do we have?"
    print(f"\nTest question: {test_question}\n")
    
    answer, log = process_query(test_question)
    
    print("Action Log:")
    for action in log:
        print(action)
    
    print(f"\nAnswer:\n{answer}")