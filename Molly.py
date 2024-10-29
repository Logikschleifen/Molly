import TimelineMaker
import re
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.llms import ChatMessage, MessageRole
import os
import stable_whisper
import tkinter as tk

systempromt1 = """ You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
You must follow these instructions carefully:
<instructions>
1. You will be provided with:  a. A short bit of context for the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
2. Read the transcript carefully and think about what parts will summarize the entire video.
3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
4. Add entertaining clips that add humor or intrest to the video.
5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...
"""

systempromt2 = """You are a Senior NYT Reporter tasked with fact checking a timeline provided by a junior researcher.
You must follow these instructions carefully:
<instructions>
1. You will be provided with:  1. Short context of the video. 2. A transcript of a youtube video with everything said. Carefully process the information and think about the contents.
2. Read the transcript carefully and compare it to events in the timeline provided. 
3. Rewrite the timeline while correcting any factual errors or typos. Rewrite inaccurate summaries of events.
4. Make your timeline engaging, informative, and well-structured.
5. Ensure you follow the re <report_format> provided below as it is the same format used in the timeline.
6. Ignore the timestamps.
</instructions>

<report_format>
## Video Title

### Overview
{give a brief introduction of the video and why the user should read this timeline}
{make this section engaging and create a hook for the reader}

### Section 1
{break the report into sections}
{provide details/facts that summarize one key event or goal pursued by a participant}

... more sections as necessary...

</report_format>
"""

systempromt3 = """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
You must follow these instructions carefully:
<instructions>
1. You will be provided with:  a. A short summary of the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
2. Read the description carefully and think about what parts of the transcript would summarize the entire video.
3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
4. Add entertaining clips that add humor or intrest to the video.
5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...
"""

class molly:
    def __init__(self):

        self.transcriptPath = "./output/transcript.txt"
        self.summaryPath = "./output/summary.txt"
        self.timelinePath = "./output/final.otio"
        
        self.llm = NVIDIA(
             base_url="https://integrate.api.nvidia.com/v1", model="meta/llama3-70b-instruct", api_key="API_KEY_HERE"
        )
        
    def create_Timeline(self, video_path, output_folder, chunking_size, description, log):
        log.insert(tk.END, "Transcription: Transcribing...\n")
        log.see(tk.END)

        # Load the Stable Whisper model
        model = stable_whisper.load_faster_whisper("medium")  # Use "tiny", "small", "medium", or "large" depending on your needs

        # Transcribe the audio file with timestamps
        results = model.transcribe_stable(video_path, language="en", word_timestamps=True)
        segments = results.to_dict()["segments"]

        segmentList = []
        count = 0
        os.makedirs(output_folder, exist_ok=True)

        video_captions = ""
        with open(output_folder + "/transcript.txt", "w") as file: 
            for segment in segments:
                line = "[" + str(segment["start"]) + ", " + str(segment["end"])  + "] " + "L" + str(count) + ": " + segment["text"] + "\n"
                video_captions = video_captions + line
                segmentList.append(segment)
                file.write( line )
                count += 1
                file.flush()
        segments = {}

        log.insert(tk.END, "Transcription: Done\n")
        log.see(tk.END)

        log.insert(tk.END, "Chunking: Splitting text...\n")
        log.see(tk.END)
        chunker_limit = chunking_size
        
        chunks = []
        num_chunks = 0
        words = video_captions.split()
        for i in range(0, len(words), chunker_limit):
            num_chunks += 1
            chunks.append(" ".join(words[i : (i + chunker_limit)]))
        
        log.insert(tk.END, "Chunking: Done\n")
        log.see(tk.END)
        summary = ""
        if num_chunks == 1:
            log.insert(tk.END, "Summarizing: Processing...\n")
            log.see(tk.END)
            messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=(systempromt1)),  
                ChatMessage(role=MessageRole.USER, content= "Summary1: " + description + "Summary2: " + chunks[0])
            ]

            summary = str(self.llm.chat(messages))
        else:
            output = ""
            for i, chunk in enumerate(chunks):
                #f"Summarizing: {i}/{len(chunks)}", end='\r'
                log.insert(tk.END, f"Summarizing: {i}/{len(chunks)}\n")
                log.see(tk.END)

                messages = [
                    ChatMessage(role=MessageRole.SYSTEM, content=(systempromt2)),  
                    ChatMessage(role=MessageRole.USER, content= "Context: " + description + "Transcript: " + chunk)
                ]

                summary = str(self.llm.chat(messages))

                messages = [
                    ChatMessage(role=MessageRole.SYSTEM, content=(systempromt3)),  
                    ChatMessage(role=MessageRole.USER, content= "Context: " + summary + "Summary2: " + chunk)
                ]

                summary = str(self.llm.chat(messages))
                output = output + "/n" + summary
            summary = output

        log.insert(tk.END, "Summarizing: Done\n")
        log.see(tk.END)

        with open(output_folder + "/summary.txt", "w") as file2:
            file2.write(summary)

        log.insert(tk.END, "Generating Timeline: Finding lines...\n")
        log.see(tk.END)
        pattern = r'L(\d+):'

        matches = re.findall(pattern, summary)

        unique_matches = sorted(set(map(int, matches)))

        timeline = TimelineMaker.VideoTimelineResolveOTIO()

        for match in unique_matches:
            start = segmentList[match]["start"]
            end = segmentList[match]["end"]
            timeline.add_clip(video_path, start_time=start, duration=end - start)

        timeline.write_to_file(output_folder + "/final.otio")
        log.insert(tk.END, "Generating Timeline: Done\n")
        log.see(tk.END)