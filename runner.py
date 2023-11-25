from model import Model

model = Model()

while True:
    choice = input("'lf' to load a file, 'e' to exit, or 'q' to ask a question: ")

    if choice.lower() == 'lf':
        file_name = input("Enter a file name: ")
        # Process the file here

        try:
            model.read_file(file_name)
            print(f"File {file_name} loaded")
            


        except:
            print("failure reading file")

    if choice.lower() in ['e', 'exit']:
        break
    if choice.lower() in ['q', 'question']:
        question = input("What is your question?\nQuestion: ")

        print(model.ask_question(question))
