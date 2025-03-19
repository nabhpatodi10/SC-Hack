from dotenv import load_dotenv
load_dotenv()

import os
import av
import io
from google import genai
from google.genai import types

class AttachmentPreprocessing:

    def __init__(self):
        self.__client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY"),
        )

    def extract_audio(self, video_path):
        audio_output_path = f"{video_path.split(".")[0]}.mp3"
        # Open the video file
        input_container = av.open(video_path)
        input_stream = input_container.streams.get(audio=0)[0]

        # Create an output container for the audio
        output_container = av.open(audio_output_path, 'w')
        output_stream = output_container.add_stream('mp3')

        # Decode audio frames from the input and encode them to the output
        for frame in input_container.decode(input_stream):
            frame.pts = None  # Reset PTS to avoid timestamp issues
            for packet in output_stream.encode(frame):
                output_container.mux(packet)

        # Flush the encoder
        for packet in output_stream.encode(None):
            output_container.mux(packet)

        # Close the output container
        return audio_output_path

    def generate(self, file_path: str) -> str | None:

        __files = [
            # Make the file available in local system working directory
            self.__client.files.upload(file=file_path),
        ]
        __contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=__files[0].uri,
                        mime_type=__files[0].mime_type,
                    ),
                    types.Part.from_text(text="""Transcribe the entire audio line by line in the language the person is speaking in. If there are multiple languages, transcribe each line. Correct the \
                                        spellings and grammar as needed.
                                        
                                        If you get an image, give all the details which can be seen in the image point wise.""")
                ],
            ),
        ]
        __generate_content_config = types.GenerateContentConfig(
            temperature=0.5,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )

        __result = self.__client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=__contents,
            config=__generate_content_config,
        )

        return __result.text
    
# print(AttachmentPreprocessing().generate(AttachmentPreprocessing().extract_audio("Images/Video.mp4")))