from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


def create_client() -> Session.client:
    """
    Create AWS session and return polly client
    """
    session : Session = Session(profile_name="default")
    polly_client : Session.client = session.client("polly") 
    
    return polly_client

def get_ssml_text(ssml_file_name = "./ssmls/speech_rev.ssml") -> str:
    ssml_file = open(ssml_file_name)
    text: str = ""
    
    for line in ssml_file:
        text += line 

    return text 
    

def create_speech(polly: Session.client, text: str) -> any:
    """
    Create speech from text a string and instantiated polly client

    Returns:
        any: Returns a response which represents the speech generated from the text string
    """
    response = None 

    try:
        response = polly.synthesize_speech(
            VoiceId='Matthew',
            OutputFormat='mp3',
            TextType='ssml',
            Text=text
        )
    except (BotoCoreError, ClientError) as error:
        print(error)

    return response 

temp_dir = gettempdir()
print("Temporary directory:", temp_dir)

def save_response(save_file: str, response: any) -> bool:
    """
        Saves audio file as an mp3
    """
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
           output = os.path.join(gettempdir(), save_file)

           try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                   file.write(stream.read())
           except IOError as error:
              # Could not write to file, exit gracefully
              print(error)
              sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])
        


if __name__ == '__main__':
    polly_client: Session.client = create_client()
    text = get_ssml_text()
    #response = create_speech(polly_client, text)
    
    #if not response:
       #print("Failed to generate speech, exiting")
       #sys.exit(-1)
        
    #save_response("different_settings.mp3", response)
        
        
