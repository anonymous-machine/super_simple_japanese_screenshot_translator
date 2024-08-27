import os
from pathlib import Path
from typing import Union

import ollama
import torch

from dotenv import load_dotenv
from PIL import Image
from transformers import pipeline

class OllamaManager:
	def __init__(self, host: str, model_name: str, base_model: str) -> None:
		modelfile = f"""
	FROM {base_model}
	SYSTEM You are an embedded translation assistant. The user is a program which gives you Japanese text. Your output will be a correct, idiomatic translation of that text into English. Do not ask any questions. The input may be a snippet or extract from a longer work. Translate what you are given. """
		ollama.create(model=model_name, modelfile=modelfile)
		self.host = host
		self.model_name = model_name

	def connect(self) -> None:
		self.client = ollama.Client(host=self.host)

	def disconnect(self) -> None:
		self.client = None

	def translate(self, text:str) -> str:
		message = {"role": "user", "content": text}

		response = self.client.chat(model=self.model_name, messages=[message])
		translated_text = response['message']['content']
		return translated_text

class OCRManager:
	def __init__(self, model_name:str, device:int):
		self.pipeline = pipeline("image-to-text", model=model_name, device=device)

	def run(self, path: Union[str, Path]):
		with Image.open(path) as image:
			result = self.pipeline(image)
			text = result[0]['generated_text']
		return text

def get_ocr_manager():
	device = "cuda" if torch.cuda.is_available() else "cpu"
	ocr_model_name = os.environ.get("OCR_MODEL")
	client = OCRManager(
		model_name=ocr_model_name, 
		device=device)
	return client

def get_ollama_manager() -> OllamaManager:
	ollama_host = os.environ.get("OLLAMA_HOST")
	ollama_port = os.environ.get("OLLAMA_PORT")
	ollama_base_model = os.environ.get("OLLAMA_BASE_MODEL")
	translation_model_name = os.environ.get("OLLAMA_TRANSLATION_MODEL_NAME")

	ollama_url = f"http://{ollama_host}:{ollama_port}/api/generate"
	
	client = OllamaManager(
		host=ollama_url, 
		model_name=translation_model_name,
		base_model=ollama_base_model)
	return client

def get_files_by_recency(path: Path) -> list[Path]:
	files = [f for f in path.glob("*") if f.is_file()]
	files = sorted(files, key=lambda x: os.path.getmtime(x), reverse=True)
	return files

def main_loop():
	# Loading configuration variables
	watched_path = Path(os.environ.get("WATCHED_PATH"))
	loop_delay = os.environ.get("LOOP_DELAY", 1)
	if type(loop_delay) is str:
		try:
			loop_delay = float(loop_delay)
		except Exception as e:
			print(f"Error loading environment variables: {e}")
	# getting the managers/clients
	ollama_manager = get_ollama_manager()
	ollama_manager.connect()
	ocr_manager = get_ocr_manager()

	last_seen_file=None
	print("Ready")
	while True:
		time.sleep(loop_delay)

		# This block checks to see if a new most-recent file has appeared in the watched_path
		files = get_files_by_recency(watch_path)
		if len(files) == 0:
			continue	# I.e., if the folder is empty, do nothing
		most_recent_file = files[0]
		if last_seen_file is None:
			last_seen_file = most_recent_file	# This runs on the first loop and sets the last_seen_file to the most recent file in the watched_path
		if last_seen_file == most_recent_file:
			continue	# I.e., if no new file, do nothing

		last_seen_file = most_recent_file
		ocr_text = ocr_manager.run(most_recent_file)
		translation = ollama_manager.translate(ocr_test)
		print(f"{ocr_text}: {translation}")

if __name__ == '__main__':
	load_dotenv()
	main_loop()
