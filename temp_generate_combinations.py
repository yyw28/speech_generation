import os
import sys

from contextlib import closing
from typing import Set, List, Final
from boto3 import Session

from aws_handler import AWSHandler


SAVE_DIRECTORY: Final[str] = os.path.join(os.getcwd(), "test_audio_files")

base_string: Final[str] = "I am here to listen! How are you feeling?"

pitch_tags: Set[str] = {"low", "medium", "high"}
intensity_tags: Set[str] = {"low", "medium", "high"}
rate_tags: Set[str] = {"slow", "medium", "fast"}

aws_handler: AWSHandler = AWSHandler()
polly_client: Final[Session.client] = aws_handler.get_polly_client() 


def add_speak_tag(text: str) -> str:
    return f"<speak>{text}</speak>"

def save_and_generate_audio_file(text: str, name_stack: List[str]) -> None: 
    file_name = generate_file_name(name_stack)
    final_text: Final[str] = add_speak_tag(text)
    
    global aws_handler, polly_client 
    response = aws_handler.generate_speech(polly_client, final_text)
    
    save_response(file_name, response)
    
def save_response(file_name: str, response: any) -> bool:
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            # output = os.path.join(gettempdir(), save_file)

            try:
                global SAVE_DIRECTORY
                # Open a file for writing the output as a binary stream
                with open(f"{SAVE_DIRECTORY}/{file_name}", "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        # sys.exit(-1)

def generate_file_name(name_stack: List[str]) -> str:
    return "_".join(name_stack) + ".mp3"


name_stack: List[str] = []

for intensity in intensity_tags:
    edited_w_intensity_string: str = base_string
    name_stack.append(f"intensity_{intensity}")
    
    for pitch in pitch_tags:
        edited_w_pitch_string = f'<prosody pitch="{pitch}">{edited_w_intensity_string}</prosody>'
        name_stack.append(f"pitch_{pitch}")

        for rate in rate_tags:
            edited_w_rate_string = f'<prosody rate="{rate}">{edited_w_pitch_string}</prosody>'
            name_stack.append(f"rate_{rate}")
            
            save_and_generate_audio_file(edited_w_rate_string, name_stack)
            name_stack.pop()        
            
        save_and_generate_audio_file(edited_w_pitch_string, name_stack)
        name_stack.pop()
    
    save_and_generate_audio_file(edited_w_intensity_string, name_stack)
    name_stack.pop()
    
        
