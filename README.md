# How this program works

The program watches a given folder. When a new image arrives in the folder, it runs a Japanese-language OCR to extract the untranslated Japanese text, and then translates it using Ollama. The OCR'd text and the translation are printed to the terminal.

# How to use this code

1. Install Ollama. Instructions are at [here](https://ollama.com/download/)

2. Configure the program by editing the .env file. If you're using the default Ollama settings, the only thing you should need to change is the WATCHED\_PATH field. WATCHED\_PATH should be whatever folder the screenshots are saved to.
3. Install the required dependencies

```
pip install -r requirements.txt
```

4. Run the script:

```
python run.py
```

# Notes

I use ShareX to capture a screenshot of just the text I want to translate and save it to the folder being watched by this script. So this script is designed to look for new images in a specific, known directory, and it expects those images to only contain the text you want to translate.
