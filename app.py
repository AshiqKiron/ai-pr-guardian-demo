# VIOLATION: Hardcoded Secret
api_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"

# VIOLATION: Dangerous Function
def run_code():
    user_input = input("Enter code: ")
    eval(user_input) 
