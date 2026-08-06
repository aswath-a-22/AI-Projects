"""
This code creates a simple web app UI using Gradio. 
Users can enter a website URL, click submit, and see the AI-generated summary.
"""
import gradio as gr #gradio is a Python library that lets you turn Python functions into web applications with very little code. 
from summarizer import summarize

"""
Creates the Gradio interface for the website summarizer.
"""
gr.Interface( 
    fn=summarize, 
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"), 
    title="🔎 AI Website Summarizer",
).launch(share=True)   
