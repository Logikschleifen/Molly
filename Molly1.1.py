from llama_index.llms.nvidia import NVIDIA
from llama_index.core.llms import ChatMessage, MessageRole

# connect to an chat NIM running at localhost:8080, spcecifying a specific model
llm = NVIDIA(
    base_url="https://integrate.api.nvidia.com/v1", model="meta/llama3-70b-instruct", api_key="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"
)

messages = [
    ChatMessage(
        role=MessageRole.SYSTEM, content=("You are a helpful assistant.")
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=("Hi, what's 1234124 + 2512?"),
    ),
]
response = llm.chat(messages)

print(str(response))

# import TimelineMaker
# from groq import Groq
# import re
# from faster_whisper import WhisperModel 
# import basicagent


# video_path = "podcast.mkv"

# segmentList = []
# count = 0
# with open("transcript2.txt", "r") as file: 
#     for line in file:
#         line = str(line.split(": "))
#         segmentList.append(line.strip())

# print(segmentList)

# def chat(messages) -> str:
#     chat_completion = client.chat.completions.create(
#         messages=messages,
#         model="llama-3.1-70b-versatile",
#     )

#     return chat_completion.choices[0].message.content

# client = Groq(
#     api_key="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",
# )

# description = "A group of friends decided to play Bean Battles."
# chunker_limit = 500#4500

# chunks = []
# num_chunks = 0
# with open("transcript2.txt", "r") as file:
#     video_captions = file.read()

# words = video_captions.split()
# for i in range(0, len(words), chunker_limit):
#     num_chunks += 1
#     chunks.append(" ".join(words[i : (i + chunker_limit)]))
    
# summary = ""

# if num_chunks == 1:
#     messages = [
#         {"role": "system", "content": 
#             """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
#              You must follow these instructions carefully:
#             <instructions>
#             1. You will be provided with:  a. A short bit of context for the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
#             2. Read the transcript carefully and think about what parts will summarize the entire video.
#             3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
#             4. Add entertaining clips that add humor or intrest to the video.
#             5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...

#             """
#             }
#     ]
#     messages.append({"role": "user", "content": " Summary1: " + description + "Summary2: " + chunks[0]})

#     summary = chat(messages)
# else:
#     output = ""
#     summaries = []
#     print(len(chunks))
#     for chunk in chunks:
#         messages = [
#         {"role": "system", "content": 
#             """You are a Senior NYT Reporter tasked with fact checking a timeline provided by a junior researcher.
#              You must follow these instructions carefully:
#             <instructions>
#             1. You will be provided with:  1. Short context of the video. 2. A transcript of a youtube video with everything said. Carefully process the information and think about the contents.
#             2. Read the transcript carefully and compare it to events in the timeline provided. 
#             3. Rewrite the timeline while correcting any factual errors or typos. Rewrite inaccurate summaries of events.
#             4. Make your timeline engaging, informative, and well-structured.
#             5. Ensure you follow the re <report_format> provided below as it is the same format used in the timeline.
#             6. Ignore the timestamps.
#             </instructions>

#             <report_format>
#             ## Video Title

#             ### Overview
#             {give a brief introduction of the video and why the user should read this timeline}
#             {make this section engaging and create a hook for the reader}

#             ### Section 1
#             {break the report into sections}
#             {provide details/facts that summarize one key event or goal pursued by a participant}

#             ... more sections as necessary...

#             </report_format>
#             """
#             }
#         ]
#         messages.append({"role": "user", "content": " Context: " + description + "Transcript: " + chunk})
#         summary = chat(messages)
#         # print(summary)

#         messages = [
#             {"role": "system", "content": 
#                 """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
#                 You must follow these instructions carefully:
#                 <instructions>
#                 1. You will be provided with:  a. A short summary of the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
#                 2. Read the description carefully and think about what parts of the transcript would summarize the entire video.
#                 3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
#                 4. Add entertaining clips that add humor or intrest to the video.
#                 5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...

#                 """
#                 }
#         ]
#         messages.append({"role": "user", "content": " Context: " + summary + "Summary2: " + chunk})

#         summary = chat(messages)
#         output = output + "/n" + summary

#     summary = output
    

# count = 0
# current = ""

# with open("summary2.txt", "w") as file2:
#     file2.write(summary)

# pattern = r'L(\d+):'

# matches = re.findall(pattern, summary)

# unique_matches = sorted(set(map(int, matches)))

# timeline = TimelineMaker.VideoTimelineResolveOTIO()

# for match in unique_matches:
#     start = segmentList[match].start
#     end = segmentList[match].end
#     # print(match)
#     timeline.add_clip(video_path, start_time=start, duration=end - start)

# timeline.write_to_file("testotio.otio")