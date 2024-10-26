import os
import time
from groq import Groq

def chat(messages) -> str:
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content

client = Groq(
    api_key="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",
)

description = "A group of friends decided to play Bean Battles."
chunker_limit = 2000#4500

chunks = []
num_chunks = 0
with open("transcript2.txt", "r") as file:
    video_captions = file.read()

words = video_captions.split()
for i in range(0, len(words), chunker_limit):
    num_chunks += 1
    chunks.append(" ".join(words[i : (i + chunker_limit)]))
    
summary = ""

if num_chunks == 1:
    # print(current)
    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Senior NYT Reporter tasked with writing a summary of a youtube video.
    #         You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  1. A short context of the video going in.  2. Pre-processed summaries from junior researchers. Carefully process the information and think about the contents
    #         2. Then generate a final New York Times worthy report in the <report_format> provided below.
    #         3. Make your report engaging, informative, and well-structured.
    #         4. Break the report into sections and provide key takeaways at the end.
    #         5. Make a title that is engaging and descriptive. Provides a good hook for readers.
    #         6. Give the section relevant titles and provide details/facts/processes in each section. REMEMBER: you are writing for the New York Times, so the quality of the report is important.
    #         7. Use markdown to format your answers.
    #         8. The current time is 2024-09-03 21:17:20.430953
    #         </instructions>

    #         <report_format>
    #         ## Video Title with Link
    #         {this is the markdown link to the video}

    #         ### Overview
    #         {give a brief introduction of the video and why the user should read this report}
    #         {make this section engaging and create a hook for the reader}

    #         ### Section 1
    #         {break the report into sections}
    #         {provide details/facts/processes in this section}

    #         ... more sections as necessary...

    #         ### Takeaways
    #         {provide key takeaways from the video}

    #         Report generated on: {Month Date, Year (hh:mm AM/PM)}
    #         </report_format>"""
    #         }
    # ]

    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Senior NYT Reporter tasked with writing a timeline of a youtube video. 
    #         You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  1. A short context of the video going in.  2. Pre-processed summaries from junior researchers. Carefully process the information and think about the contents.
    #         2. Then generate a final New York Times worthy timeline in the <report_format> provided below.
    #         3. Make your timeline engaging, informative, and well-structured.
    #         4. Break the timeline into sections. Each section should summarize a new goal or question created by the actions of the participants in the transcript.
    #         5. Make a title that is engaging and descriptive. Provides a good hook for readers.
    #         6. Give the section relevant titles and provide details/facts/processes in each section. REMEMBER: you are writing for the New York Times, so the quality of the report is important.
    #         7. Use markdown to format your answers.
    #         8. Ignore the timestamps.
    #         </instructions>

    #         <report_format>
    #         ## Video Title

    #         ### Overview
    #         {give a brief introduction of the video and why the user should read this timeline}
    #         {make this section engaging and create a hook for the reader}

    #         ### Section 1
    #         {break the report into sections}
    #         {provide details/facts that summarize one key event or goal pursued by a participant}

    #         ... more sections as necessary...

    #         </report_format>"""
    #         }
    # ]


    # messages.append({"role": "user", "content": " Context: " + description + "Transcript: " + chunks[0]})

    # summary1 = chat(messages)

    # with open("debug1.txt", "w") as file2:
    #     file2.write(summary1)
    # file2.close()

    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Senior NYT Reporter tasked with fact checking a timeline provided by a junior researcher.
    #          You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  1. A transcript of a youtube video with everything said. 2. Pre-processed timeline of events from junior researchers. Carefully process the information and think about the contents.
    #         2. Read the transcript carefully and compare it to events in the timeline provided. 
    #         3. Rewrite the timeline while correcting any factual errors or typos. Rewrite inaccurate summaries of events.
    #         4. Make your timeline engaging, informative, and well-structured.
    #         5. Ensure you follow the re <report_format> provided below as it is the same format used in the timeline.
    #         6. Ignore the timestamps.
    #         </instructions>

    #         <report_format>
    #         ## Video Title

    #         ### Overview
    #         {give a brief introduction of the video and why the user should read this timeline}
    #         {make this section engaging and create a hook for the reader}

    #         ### Section 1
    #         {break the report into sections}
    #         {provide details/facts that summarize one key event or goal pursued by a participant}

    #         ... more sections as necessary...

    #         </report_format>
    #         """
    #         }
    # ]


    # messages.append({"role": "user", "content": " Summary: " + summary + "Transcript: " + chunks[0]})

    # summary = chat(messages)


    # with open("debug2.txt", "w") as file2:
    #     file2.write(summary)
    # file2.close()

    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
    #          You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  1. A transcript of a youtube video with everything said. 2. Pre-processed timeline of events from junior editors. Carefully process the information and think about the contents.
    #         2. Read the transcript carefully and compare it to events in the timeline provided. 
    #         3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Do not attempt to rewrite the transcript, simply select excerpts that are important to following the timeline.
    #         4. Write the selected excerpts as clips that will be connected in chronological order. Follow <include_clips> format.
    #         5. Write each clip as a continous excerpt from the transcript. Do not include multiple clips in a section.
    #         6. Provide the line numbers used in each clip.
    #         </instructions>

    #         <include_clips>

    #         ### Clip 1: {Lines used}
    #         {Continous excerpt from the transcript}

    #         ... more sections as necessary...
            
    #         </include_clips>
    #         """
    #         }
    # ]

    # print(" Context: " + summary + "Transcript: " + summary)
    # messages.append({"role": "user", "content": " Summary: " + summary1 + "Transcript: " + chunks[0]})

    # summary = chat(messages)

    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Senior NYT Reporter tasked with writing a timeline of a youtube video. 
    #         You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  1. A short context of the video going in.  2. Pre-processed summaries from junior researchers. Carefully process the information and think about the contents.
    #         2. Then generate a final New York Times worthy timeline in the <report_format> provided below.
    #         3. Make your timeline engaging, informative, and well-structured.
    #         4. Break the timeline into sections. Each section should summarize a new goal or question created by the actions of the participants in the transcript.
    #         5. Make a title that is engaging and descriptive. Provides a good hook for readers.
    #         6. Give the section relevant titles and provide details/facts/processes in each section. REMEMBER: you are writing for the New York Times, so the quality of the report is important.
    #         7. Use markdown to format your answers.
    #         </instructions>

    #         <report_format>
    #         ## Video Title

    #         ### Overview
    #         {give a brief introduction of the video and why the user should read this timeline}
    #         {make this section engaging and create a hook for the reader}

    #         ### Section 1
    #         {break the report into sections}
    #         {provide details/facts that summarize one key event or goal pursued by a participant}

    #         ... more sections as necessary...

    #         </report_format>"""
    #         }
    # ]

    # messages.append({"role": "user", "content": " Context: " + description + "Transcript: " + summary})

    # summary = chat(messages)

    # messages = [
    #     {"role": "system", "content": 
    #         """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
    #          You must follow these instructions carefully:
    #         <instructions>
    #         1. You will be provided with:  a. A short bit of context for the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
    #         2. Read the transcript carefully and think about what parts will summarize the entire video.
    #         3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
    #         4. Write the selected excerpts as clips that will be connected in chronological order. Follow <include_clips> format.
    #         5. Write each clip as a continous excerpt from the transcript. Do not include multiple clips in a section.
    #         6. Provide the line numbers used in each clip.
    #         7. Add entertaining clips that add humor or intrest to the video.
    #         </instructions>

    #         <include_clips>

    #         ### Clip 1: {Lines used}

    #         ... more sections as necessary...
            
    #         </include_clips>"""
    #         }
    # ]

    messages = [
        {"role": "system", "content": 
            """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
             You must follow these instructions carefully:
            <instructions>
            1. You will be provided with:  a. A short bit of context for the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
            2. Read the transcript carefully and think about what parts will summarize the entire video.
            3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
            4. Add entertaining clips that add humor or intrest to the video.
            5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...

            """
            }
    ]
    messages.append({"role": "user", "content": " Summary1: " + description + "Summary2: " + chunks[0]})

    summary = chat(messages)
else:
    output = ""
    summaries = []
    print(len(chunks))
    for chunk in chunks:
        messages = [
        {"role": "system", "content": 
            """You are a Senior NYT Reporter tasked with fact checking a timeline provided by a junior researcher.
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
            }
        ]
        messages.append({"role": "user", "content": " Context: " + description + "Transcript: " + chunk})
        summary = chat(messages)
        # print(summary)

        messages = [
            {"role": "system", "content": 
                """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
                You must follow these instructions carefully:
                <instructions>
                1. You will be provided with:  a. A short summary of the video. b. A transcript of everything said in the video. Carefully process the information and think about the contents.
                2. Read the description carefully and think about what parts of the transcript would summarize the entire video.
                3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
                4. Add entertaining clips that add humor or intrest to the video.
                5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1, L7, etc...

                """
                }
        ]
        messages.append({"role": "user", "content": " Context: " + summary + "Summary2: " + chunk})

        summary = chat(messages)
        output = output + "/n" + summary

    summary = output
    

    # messages = [
    # {"role": "system", "content": 
    #     """You are a Famous Youtube Editor tasked with creating an entertaining video from a streaming vod.
    #         You must follow these instructions carefully:
    #     <instructions>
    #     1. You will be provided with summaries from junior researchers that cover the whole video in parts. Carefully process the information and think about the contents.
    #     2. Read the transcript carefully and think about what parts will summarize the entire video.
    #     3. Select excerpts from the transcript that will convey the main points of the timeline while being as entertaining as possible. REMEMBER: Simply select excerpts that are important to following the timeline. Provide the lines that are from the sections you selected.
    #     4. Add entertaining clips that add humor or intrest to the video.
    #     5. Write the line numbers for each line you choose to add to the video. This will make up your response, a list going L1:, L7:, etc...

    #     """
    #     }
    # ]
    # messages.append({"role": "user", "content": "Summary: " + summary})

    # summary = chat(messages)
    
    

count = 0
current = ""
# print("Summary: " + summary)

with open("summary2.txt", "w") as file2:
    file2.write(summary)
