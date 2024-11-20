import os
import sys

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from transf_class_extractor import extract_class_core


def llm_request(task_description: str, model_id: str, origin_csv_file: str, final_csv_file: str):
    """
    This method make a request to the LLM and generate script that apply changes to

    Args:
        task_description (str): Description of manipulations over dataframe
        model_name (str): The name of the model from HuggingFace
        origin_csv_file (str): Path to the file with original dataset
        final_csv_file (str): Path where new dataset will be saved
    """
    # Define model ID and load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Load model with configuration
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype="auto"
    )

    # Create a text-generation pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=500,
        top_k=20,
        temperature=0.3
    )

    # Wrap the HuggingFace pipeline with LangChain
    llm = HuggingFacePipeline(pipeline=pipe)

    print("HuggingFace pipeline generated.")

    code_template = """
    Lower will be defined class for manipulation over dataframe object, template class for result format, and task. 
    You should use this defined class for solving task of manipulation over dataframe, you can use only methods of class for doing it.
    Code template provide python code, where should be replaced comment to sequence of class methods.
    And task, that should be solved with usage of predefined class and output should be in form of template code.
    In the end of solution should be string "End of implementation".

    Class:
    {class_code}

    Code template:
    {code_template}

    Task:
    {task_description}

    Python Code:
    """

    # Set up the prompt templates
    code_prompt = PromptTemplate(template=code_template,
                                 input_variables=["class_code", "code_template", "task_description"])

    # Create chains for generating Python code using LangChain
    code_chain = LLMChain(llm=llm, prompt=code_prompt)

    print("Taking class core.")
    class_code = extract_class_core("DataFrameTransformer.py")

    print("Taking solution template code.")
    f = open("solution_template.py")
    code_template = f.read()
    f.close()

    print("Starting generate answer.")
    generated_code = code_chain.run(class_code=class_code, code_template=code_template,
                                    task_description=task_description)

    print("Taking answer.")
    start_index = generated_code.find("Python Code:")

    first_end_index = generated_code.find("End of implementation")

    if first_end_index != -1:
        end_index = generated_code.find("End of implementation", first_end_index + len("End of implementation"))
    else:
        end_index = -1

    python_code = generated_code[start_index + len("Python Code:"):end_index].strip()

    print(f"Saving result into file: solution.py")
    f = open("solution.py", "w")
    f.write(python_code)
    f.close()

    print(f"Execute generated file.")
    os.system(f"python solution.py {origin_csv_file} {final_csv_file}")

def main():
    """
    This is the main function that runs when this file is executed.

    There defines model, that will be used for code generation.
    """
    argv = sys.argv

    task_description = ""
    model_id = "codellama/CodeLlama-7b-hf"
    origin_csv_file = "../dataframes/Housing.csv"
    final_csv_file = "../dataframes/Housing_Modified.csv"

    if len(argv) == 2:
        task_description = argv[1]
    elif len(argv) == 3:
        task_description = argv[1]
        model_id = argv[2]
    elif len(argv) == 4:
        task_description = argv[1]
        model_id = argv[2]
        origin_csv_file = argv[3]
    elif len(argv) == 5:
        task_description = argv[1]
        model_id = argv[2]
        origin_csv_file = argv[3]
        final_csv_file = argv[4]
    else:
        print("Error: Incorrect number of arguments! There should be at least 1 and no more than 2 arguments!")

    llm_request(task_description, model_id, origin_csv_file, final_csv_file)

if __name__ == '__main__':
    main()
