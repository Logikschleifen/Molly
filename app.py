
import Molly
import gradio as gr

def edit_video(description, output_folder, file_path, chunking):
    try:
        editor = Molly.molly()
        print("Description: " + description)
        print("Output Folder: " + output_folder)
        print("File Path: " + file_path)
        print("Chunking Size: " + str(chunking))
        print("")
        editor.create_Timeline(video_path=file_path, output_folder=output_folder, chunking_size=chunking, description=description)
        return "Video edited successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred during video editing."


# Define the Gradio interface layout
with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("<h1 style='text-align: center; font-size: 4em; font-weight: bold;'>Molly, the AI Video Editor</h1>")


    with gr.Row():
        video = gr.Textbox(label=f"Input Video")
        out = gr.Textbox(label=f"Output Folder", value="./output")

    with gr.Row():
        description = gr.Textbox(label=f"Initial Video description", value="A simple gaming video.")
        chunking = gr.Number(label=f"Chunk Size", value=500)

    # Add a large button at the bottom
    with gr.Row():
        button = gr.Button("One Click Edit", elem_classes="large-button", variant="primary")
        button.click(edit_video, inputs=[description, out, video, chunking])


demo.launch()
