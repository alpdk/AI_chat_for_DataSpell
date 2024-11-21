# AI chat for DataSpell

## Preparations

### Python packages

For proper work of the code required packages:

1. langchain
2. langchain_huggingface
3. pandas
4. transformers

For that, you can run script below:

```pip install requirements.txt```

## Python files

### DataFrameTransformer.py

This file contain class that helps to manipulate over pandas dataframe.
Inside of the file you can find methods for selecting columns and filtering rows.
This file will be used for definition what methods should be used over pandas dataframe.

### transf_class_extractor.py

This file contain method, that takes from the fail: 

1. Definition of class
2. Definition of methods inside of the class
3. Doc string of classes and methods

### solution_template.py

This file contain code, that provide template, where implemented code for manipulation
over pandas dataframe object, with usage of the class DataFrameTransformer.
This template have a comment string signifying, where should be written part with manipulation over dataframe.

Result of generated code from LLM should have the same structure.

This code require count of arguments between 0 and 2:

1. Path to the file for modification. (default: `../dataframes/Housing.csv`)
2. Path to the file for saving modified first file. (default: `../dataframes/Housing_Modified.csv`)

### llm_request.py

This is the main fail of the repository. This file implement request to the llm, that will 
finish code from `solution_template.py` with requested changes, that should made with usage of class
from `DataFrameTransformer.py`
This code require count of arguments between 1 and 4:

1. Request describing manipulation over dataframe.
2. Path to the file for modification. (default: `../dataframes/Housing.csv`)
3. Path to the file for saving modified first file. (default: `../dataframes/Housing_Modified.csv`)
4. Model id from huggingface. (default: `codellama/CodeLlama-7b-hf`)

As a result it will create file `solution.py`, that transform dataset and run it with defined path of 
original and modified file. 

For running this test with default files and model run script bellow:

```python llm_request.py "Take columns with names: price, bedrooms, mainroad, and parking, and rows, where count of bedrooms are smaller or equal to 3."```

## What can be improved?

This implementation has several limitations, and some aspect can be change for better work:

1. Implement full chat with LLM. Current solution implement 1-shot request, that can generate 
result that do not satisfy request, or do not work at all.
2. Experiment with more models. I tried several models, and decided that model `codellama/CodeLlama-7b-hf`
generate best result among the others, but it is not objective estimation.
