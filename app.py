from zenml import pipeline, step

@step
def step_1() -> str:
    """ step 1"""
    return "hello"

@step(enable_cache=False)
def step_2(input_one:str, input_two:str) -> None:
    """ step 2"""
    print(f"{input_one} {input_two}")

@pipeline
def my_pipeline():
    var1 = step_1()
    print(step_2(input_one=var1, input_two="world"))

if __name__ == "__main__":
    my_pipeline()