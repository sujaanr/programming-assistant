import argparse
import os
import logging
from typing import Optional
from langchain.llms.ollama import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from termcolor import colored

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProgrammingAssistant:
    def __init__(self, model: str = "codellama", verbose: bool = False) -> None:
        logging.info("Initializing the Programming Assistant with model %s.", model)
        self.verbose = verbose
        self.system_prompt = ("You are a pair programming tool to help developers "
                              "debug, think through design, and write code. "
                              "Help the user think through their approach and provide feedback on the code.")
        self.llm = Ollama(model=model, callbacks=[StreamingStdOutCallbackHandler()], system=self.system_prompt)

    def call_llama(self, code: str = "", prompt: Optional[str] = None, chain: bool = False) -> None:
        prompt = prompt or "Review the code, find any issues if any, suggest cleanups if any: "
        prompt += code
        if self.verbose:
            logging.info("Sending prompt to the model: %s", prompt)
        self.llm(prompt)

        while chain:
            user_input = input(colored("\nWhat's on your mind? \n", 'green'))
            self.llm(user_input)

def read_files_from_dir(directory: str) -> str:
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        logging.error("The specified directory does not exist: %s", directory)
        return ""

    code = ""
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, 'r') as f:
                file_contents = f.read()
                code += file_contents
                if verbose:
                    logging.info("Read %d characters from %s", len(file_contents), file)
        except Exception as e:
            logging.error("Failed to read from file %s: %s", file, str(e))
            continue
    return code

def programmingFriend() -> None:
    parser = argparse.ArgumentParser(description="Tool to assist with coding tasks using the Ollama model.")
    parser.add_argument("--prompt", "-p", help="Custom prompt to be used", default=None)
    parser.add_argument("--file", "-f", help="The file to be processed", default=None)
    parser.add_argument("--directory", "-d", help="The directory to be processed", default=None)
    parser.add_argument("--chain", "-c", action="store_true", help="Continue interaction after initial command")
    parser.add_argument("--model", "-m", help="The model to be used", default="codellama")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    assistant = ProgrammingAssistant(model=args.model, verbose=args.verbose)

    if args.file:
        try:
            code = open(args.file).read()
        except FileNotFoundError:
            logging.error("The specified file does not exist: %s", args.file)
            return
        assistant.call_llama(code=code, prompt=args.prompt, chain=args.chain)
    elif args.directory:
        code = read_files_from_dir(args.directory)
        if code:
            assistant.call_llama(code=code, prompt=args.prompt, chain=args.chain)
    else:
        while True or args.chain:
            prompt = input(colored("\nWhat's on your mind? \n", 'green'))
            assistant.call_llama(prompt=prompt, chain=args.chain)

if __name__ == "__main__":
    programmingFriend()
