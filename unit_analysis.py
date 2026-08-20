import json
from openai import OpenAI
def analyze_text_for_units(text):
    try:
        with open("config.json") as f:
            config = json.load(f)
            apikey = config.get('APIKEY')
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json")
    api_key = apikey
    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"""
            Parse the following text about betting picks and only return True if there is a player with a stake strictly GREATER THAN 1.0 units, if there is a mention of a TOTAL unit count greater than 1.0, or if there is any mention of the word "streak". Units can appear in the form of unit, units, or u, capital or lowercase.  
            Ignore any numbers inside the angle brackets '<', '>'. 
            Return False otherwise. Do not give any sort of explanation. Just return either ONE (1) 'True' or 'False'.
    Text to analyze: {text}
    """
        }
    ]

    # Make the API call
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0,  # Keep it deterministic
            max_tokens=100
        )
        result = response.choices[0].message.content
        print(f"OpenAI response: {result}")  # Add this debug print
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error analyzing text: {str(e)}") #TODO Error analyzing text -> send a message maybe?
        return False
