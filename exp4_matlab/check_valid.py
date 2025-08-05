import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def check_inputs_against_grammar(inputs, grammar):
    valid_inputs = []
    invalid_inputs = []
    unrecognized_responses = []

    for idx, input_str in enumerate(inputs):
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are an assistant for developers to inspect and analyze inputs based on a given input ANTLR grammar."
                },
                {
                    "role": "user", 
                    "content": (
                        "Please analyze the following inputs against the provided grammar:\n\n"
                        f"Input: {input_str}\n\n"
                        f"Grammar: {grammar}\n\n"
                        "End your response with '<answer>VALID</answer>' or '<answer>INVALID</answer>' "
                        "depending on whether the input matched the grammar."
                    )
                },
            ],
            temperature=1,
        )

        response_content = response.choices[0].message.content
        
        if "<answer>VALID</answer>" in response_content:
            valid_inputs.append(input_str)
        elif "<answer>INVALID</answer>" in response_content:
            invalid_inputs.append(input_str)
        else:
            unrecognized_responses.append((idx, input_str, response_content))
    
    # Write valid inputs to file
    with open("valid_inputs.txt", "w") as valid_file:
        for input_str in valid_inputs:
            valid_file.write(f"{input_str}\n")
            valid_file.write("-" * 40 + "\n")  # Separator
    
    # Write invalid inputs to file
    with open("invalid_inputs.txt", "w") as invalid_file:
        for input_str in invalid_inputs:
            invalid_file.write(f"{input_str}\n")
            invalid_file.write("-" * 40 + "\n")  # Separator
    
    # Write unrecognized responses for debugging
    if unrecognized_responses:
        with open("unrecognized_responses.txt", "w") as debug_file:
            for idx, input_str, response_content in unrecognized_responses:
                debug_file.write(f"Input #{idx}: {input_str}\n")
                debug_file.write(f"Response: {response_content}\n")
                debug_file.write("=" * 80 + "\n")
    
    # Print summary
    print(f"Total inputs processed: {len(inputs)}")
    print(f"Valid inputs: {len(valid_inputs)} (saved to valid_inputs.txt)")
    print(f"Invalid inputs: {len(invalid_inputs)} (saved to invalid_inputs.txt)")
    if unrecognized_responses:
        print(f"Unrecognized responses: {len(unrecognized_responses)} (saved to unrecognized_responses.txt)")

if __name__ == "__main__":
    # Read inputs from 'tests' directory
    inputs = []
    test_dir = "tests"
    for filename in os.listdir(test_dir):
        filepath = os.path.join(test_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                inputs.append(f.read().strip())
    
    # Deduplicate and limit
    inputs = list(set(inputs))[:200]  # Remove duplicates and limit to 500
    
    print(f"Found {len(inputs)} inputs in tests directory.")
    
    # Read grammar
    grammar_path = "matlab.g4"
    if os.path.exists(grammar_path):
        with open(grammar_path, "r") as f:
            grammar = f.read().strip()
    else:
        raise FileNotFoundError(f"Grammar file not found: {grammar_path}")
    
    # Process inputs
    check_inputs_against_grammar(inputs, grammar)