
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def check_inputs_against_grammar(inputs, grammar):

    num_valid = 0
    num_invalid = 0

    for input in inputs:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are an assistant for developers to inspect and analyze inputs based on a given input ANTLR grammar."},
                {"role": "user", "content": "Please analyze the following inputs against the provided grammar:\n\nInputs: " + input + "\n\nGrammar: " + grammar + "\n\nEnd your response with '<answer>VALID</answer>' or '<answer>INVALID</answer>' depending on whether the input matched the grammar."},
            ],
            temperature=0.7,
        )

        print(response.choices[0].message.content)

        

        if "<answer>VALID</answer>" in response.choices[0].message.content:
            print(f"Input '{input}' is VALID according to the grammar.")
            num_valid += 1
        elif "<answer>INVALID</answer>" in response.choices[0].message.content:
            print(f"Input '{input}' is INVALID according to the grammar.")
            num_invalid += 1
        else:
            print(f"Unexpected response for input '{input}': {response.choices[0].message.content}")

    print(f"Total valid inputs: {num_valid}")
    print(f"Total invalid inputs: {num_invalid}")

if __name__ == "__main__":
    # read inputs in `tests`
    inputs = []
    for filename in os.listdir("tests"):
    
        with open(os.path.join("tests", filename), "r") as f:
            inputs.append(f.read().strip())

    print(f"Found {len(inputs)} inputs in tests directory.")
    # read grammar
    with open("JSON.g4", "r") as f:
        grammar = f.read().strip()

    # check inputs against grammar
    check_inputs_against_grammar(inputs, grammar)
