from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from typing import Text


class AWSHandler:
    def __init__(self):
        self.session = Session(profile_name="default")
    
    def get_polly_client(self) -> Session.client:
        return self.session.client("polly") 
    
    def generate_speech(self, polly: Session.client, text: Text) -> any:
        response = None 

        try:
            response = polly.synthesize_speech(
                VoiceId='Joanna',
                OutputFormat='mp3',
                TextType='ssml',
                Text=text
            )
        except (BotoCoreError, ClientError) as error:
            print(error)

        return response 