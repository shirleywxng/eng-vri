
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def truncate(text, max_length):
    """Truncate text to a maximum length, ensuring it ends at a word boundary."""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated if truncated else text[:max_length]

def complete_input(inputs, grammar):

    results = []
    for input in inputs:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are an assistant for developers to inspect and analyze inputs based on a given input ANTLR grammar. Given a truncated input, please complete it to match the grammar."},
                {"role": "user", "content": "Inputs: " + input + "\n\nGrammar: " + grammar + "\n\nWrap the completed input with '<answer></answer>'."},
            ],
            temperature=0.7,
        )

        print(response.choices[0].message.content)

        if "<answer>" in response.choices[0].message.content and "</answer>" in response.choices[0].message.content:
            completed_input = response.choices[0].message.content.split("<answer>")[1].split("</answer>")[0]
            print(f"Completed input: {completed_input}")
        else:
            print(f"Unexpected response for input '{input}': {response.choices[0].message.content}")

        results.append(completed_input)

    return results


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

    # for debugging
    inputs = inputs[:3]

    input_truncated_length = 5
    # first filter by length
    inputs = [input for input in inputs if len(input) <= input_truncated_length]

    truncated_inputs = [truncate(input, input_truncated_length) for input in inputs]

    # print number of truncated inputs
    print(f"Truncated {len(truncated_inputs)} inputs to a maximum length of {input_truncated_length} characters.")
    # check inputs against grammar
    completed_inputs = complete_input(truncated_inputs, grammar)

    # write completed inputs to a directory
    if not os.path.exists("completed_inputs"):
        os.makedirs("completed_inputs")

    for i, completed_input in enumerate(completed_inputs):
        with open(os.path.join("completed_inputs", f"completed_input_{i}.txt"), "w") as f:
            f.write(completed_input.strip())
