from dotenv import load_dotenv
load_dotenv()

import os
from google import genai
from google.genai import types

class AttachmentPreprocessing:

    def __init__(self):
        self.__client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    
    def generate(self, file_path: str):

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
    
# print(AttachmentPreprocessing().generate("Images/Agent-Architecture.png"))