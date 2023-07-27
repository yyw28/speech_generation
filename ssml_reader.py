from contextlib import closing
from io import TextIOWrapper
import sys
from typing import Dict, Text, Tuple, NewType

from aws_handler import AWSHandler

FileName: NewType = NewType("FileName", str)

class SsmlReader:
    file_contents: Dict[FileName, Text] = {}
    
    def extract_file_ssml(self, file_name: FileName) -> bool:
        file: TextIOWrapper
        
        try:
            file = open(file_name, "r")
        except IOError:
            print(f"{file_name} could not be opened. Please double check the file name or path.")
            return False 
        
        in_ssml_block: bool = False
        current_file: FileName = None 
        
        for line in file:
            line = line.strip() 
            
            if not line:
                continue 
            
            if not in_ssml_block:
                if line != "<speak>":
                    current_file = line 
                    self.file_contents[current_file] = ""
                else:
                    if not current_file:
                        print("File formatting is incorrect")  
                        return False 
                    self.file_contents[current_file] += line + "\n"  
                    in_ssml_block = True  
            else:
                if line != "</speak>":
                    if not current_file:
                        print("File formatting is incorrect")
                        return False 
                    self.file_contents[current_file] += line + "\n"
                else:
                    self.file_contents[current_file] += line + "\n"
                    
                    in_ssml_block = False 
                    current_file = False 
        
        return True
    
    def save_file_contents_as_speech(self) -> bool:
        aws_handler: AWSHandler = AWSHandler()
        polly_client = aws_handler.get_polly_client()
        
        for file_name, text in self.file_contents.items():
            response = aws_handler.generate_speech(polly_client, text)
            if response is None:
                continue
            
            self._save_response(file_name, response)
            print("Saved", file_name)
                    
                
            
    def _save_response(self, file_name: FileName, response: any) -> bool:
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                # output = os.path.join(gettempdir(), save_file)

                try:
                    # Open a file for writing the output as a binary stream
                        with open(f"saved_audio_files/{file_name}", "wb") as file:
                            file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # # Play the audio using the platform's default player
        # if sys.platform == "win32":
        #     os.startfile(output)
        # else:
        #     # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        #     opener = "open" if sys.platform == "darwin" else "xdg-open"
        #     subprocess.call([opener, output])
        