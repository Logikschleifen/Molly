# Molly
Molly is a video editing tool that uses a combination of whisper and llama (hosted by NIVIDIA NIMS) to help pear down long videos into clips. It does this by getting clips of when people are talking and then
sorting through what it thinks are the most interesting. I will likely return to this project in the future and work on how it makes the selection but for now it is a good start that is 
most effective on videos over an hour long. 

This is my submission to the LLamaIndex dev contest hosted by Nividia. Sup Nividia engineers? I hope you are having a good day.

# Setup
IMPORTANT, I have only tested this on one computer, my own. I used a NIVIDIA graphics card with cuda 12.1 + cudnn on python 3.10. Also I had a stuffed animal on my desk, not sure if that'll help.

### Prereqs
Some prerequisite include:

  1. [Cuda](https://developer.nvidia.com/cuda-toolkit)
  2. [Cudnn](https://developer.nvidia.com/cudnn)
  3. [NIMS](https://build.nvidia.com/explore/discover) account

### Step 1: Clone repo
Clone this repo, or download it as a zip if you like that better. 

### Step 2: Setup Python Environment
Not nessesarily critical but setting up a venv or conda environment is recommended. I used python 3.10.

### Step 3: Install pytorch library
Install [Pytorch](https://pytorch.org/get-started/locally/) for your version of cuda.

### Step 4: Run this command
Open a terminal in the cloned directory and use this to install the rest of the libraries.
...
pip install -r requirments.txt
...

### Step 5: Add your API key
Go into Molly.py and on line 64 add your NIMS Api key for a language model. I have it set to [llama3 70B](https://build.nvidia.com/meta/llama3-70b) but you 
could make it any on the service.

### Step 6: Your done!
To run just use:
...
python app.py
...

# How to use
It is pretty self explanatory but let me give a brief overview of the controls you have in the GUI. There are 4 inputs:

  1. Path to file. Where you can give the path to the video file you want to edit.
  2. Ouput folder. Path to the folder you want the transcript and final timeline to be put.
  3. Initial description. Injects a prompt into the start of the language model that helps it understand the content a bit before going in. Just more context for it to work with.
  4. Chunk size. The number of max number of words that are proccessed from the transcript at a time. Generally increasing will result in less clips being selected if the video is above a certain length. Don't expect much to happen if you change it for shorter videos. Since more api calls will be made at lower numbers (since it'll process only that many words) I recommend keeping it in the triple digits.

Hope its useful. Let me know if it isn't and if so what WOULD be. 
