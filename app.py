from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv, find_dotenv
import os
from werkzeug.utils import secure_filename
from os.path import splitext

app = Flask(__name__)

# Dummy document text for testing
documents = {
    "Objective": "Please generate an objective summary of the meeting transcript. Summarize the key points, decisions, and action items discussed during the meeting. Focus on providing a factual account without introducing any interpretation or bias. The objective is to capture the essence of the meeting in a concise and informative manner.",
    "Executive": "Generate an executive summary based on the meeting transcript tailored for senior leadership. Highlight critical decisions, key outcomes, and their strategic implications discussed during the meeting. Include recommendations and outline the subsequent steps or actions to be taken. The objective is to provide a concise yet comprehensive summary targeted at senior leadership, ensuring it captures the strategic importance and actionable insights derived from the meeting",
    "KeyTakeaways": "Please generate key takeaways from the meeting transcript. Summarize the main points and key insights discussed during the meeting. Focus specifically on distilling the essential information that team members or stakeholders need to grasp quickly. Highlight the most significant aspects, key decisions, and crucial insights derived from the meeting, ensuring the summary is concise and easily understandable",
    "ActionItem": "Create a list of all the action items, assigned responsibilities, and deadlines discussed and decided upon during the meeting. Present this information in a clear, organized format that highlights each action item, the responsible parties, and the associated deadlines. The objective is to compile a comprehensive and structured summary specifically focused on the actionable tasks arising from the meeting, ensuring clarity regarding responsibilities and timelines.",
    "ProblemSolution": "This document encapsulates the meeting's discussions on problems and their corresponding solutions or strategies. It highlights the challenges discussed and their resolutions.",
    "Training": "Generate a training summary based on the meeting transcript, designed for individuals who were absent. Summarize the main discussions, decisions, and important points covered during the meeting to ensure that absent team members can quickly catch up. Highlight key takeaways and essential information that will aid in their understanding. Additionally, provide specific notes or sections addressing the absence of certain individuals, ensuring the summary covers the topics crucial for their awareness and integration upon their return.",
    "MOMs": "Please generate detailed meeting minutes summarizing all discussions, decisions, attendees, and actions taken during the meeting. Organize the document systematically and include timestamps if available. Ensure the minutes encompass a comprehensive overview of the meeting, covering topics discussed, decisions made, attendees present, and actions assigned, in a detailed and structured format",
    "SpeakerNotes": "Provide speaker notes summarizing the key points made by each speaker during the meeting. Include the name of each speaker along with a brief summary of their contributions or the main ideas they presented. Ensure the notes capture the essence of each speaker's input, helping to highlight individual perspectives and key information shared during the meeting.",
}




@app.route("/")
def index():
    return render_template("index.html")

def read_file_and_chunk(file_path):
    with open(file_path, "r") as file:
        text = file.read()
        return text

instructions = "You are a document summarizer"  # Default instructions

_=load_dotenv(find_dotenv())
openai.api_key=os.getenv('OPENAI_API_KEY')

# Define the function for extracting keywords
# ...

@app.route("/get_summary", methods=["POST"])
def get_summary(model="gpt-3.5-turbo-16k", temperature=0):
    uploaded_file = request.files["file"]
    file_content = None  # Initialize file_content
    filename = secure_filename(uploaded_file.filename)
    selected_category = request.form.get("meeting-type")

    # Set default instructions
    instructions = "This is a meeting transcript and you need to create a list of items discussed during meeting so that absentees get an idea"

    if uploaded_file:

        print("Uploaded File:", uploaded_file)
        print("Selected Category:", selected_category)
        filename = secure_filename(uploaded_file.filename)

        # Extract the file extension
        _, file_extension = splitext(filename)

        if file_extension.lower() in {".txt", ".srt"}:
            uploaded_file.save(filename)
            file_content = read_file_and_chunk(filename)
            os.remove(filename)
        else:
            return jsonify({"error": "Invalid file type. Please upload a .txt or .srt file."})
    else:
        return jsonify({"error": "No file uploaded"})

    if file_content:
        # Fetch the selected category from the request
        print("Form Data:", request.form)  # Print the entire form data for inspection
        selected_category = request.form.get("meeting-type")

        # Update instructions based on the selected category
        if selected_category in documents:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            instructions = documents[selected_category]
        else:
            print("#############################")



        # Continue with generating the summary using the content of the uploaded file
        messages = [
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": file_content
            }
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        result = response.choices[0].message["content"]
        return jsonify({"summary": result})
    else:
        return jsonify({"error": "Failed to read the uploaded file."})

# ...


if __name__ == "__main__":
    app.run(debug=True)
