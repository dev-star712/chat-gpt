import re 


# Basic Arithmetic Operators

async def execute_command(argument: list, group_room_code: str):
    to_eval = ''.join(argument).replace("x","*").replace(":","/")
    if not to_eval:
        return "/do_math 1+1"
    if re.findall("[A-Za-z]", to_eval):
        return f"{to_eval} is not valid arithmetic operators!"
    try:
        result = eval(to_eval)
    except Exception as e:
        return str(e)
    return f"{''.join(argument)}=<b>{result}</b>"