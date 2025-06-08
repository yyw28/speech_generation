from collections import deque
from os import getcwd, path
from typing import Deque, Dict, Final, List, Tuple

from ssml_tag import Tag

TAGS_FILE: Final[str] = path.join(getcwd(), "ssml_tags.txt")

class SsmlCreator:
    ssml_stack: Deque[Tuple[str, str or None]] = deque()
    tags: Dict[str, Tag] = {}
    
    
    """
        How this deque works 
        if ssml_queue contains = [("<speak>", "</speak>"), ("I like cookies", None)]
        Using this stack we will obtain the ssml
            <speak>
                I like cookies
            </speak>
            
        A more complex que would be [("<speak>", "</speak>"), ("I like ", None), (<"emphasis level = 'strong'>, "</emphasis"), cookies]
        We would obtain 
            <speak>
                I like <"emphasis level = 'strong'>cookies</emphasis>
            </speak> 

        Skipped the faollowing in ssml_tags.txt
        Did not add anything for phonetic pronunciation as of now.
        Skipped amazon:breath, amazon:domain, amazon:effect name, amazon:effect phonation, amazon:effect vocal-tract-length, amazon effect name, 
    """
    
    def __init__(self):
        tags_stream = open(TAGS_FILE, 'r')

        for line in tags_stream:
            line = line.strip()
            
            if not line:
                continue
            
            features: List[str] = line.split(" : ")
            self.tags[features[0]] = Tag(features[1].split(", "), features[2], features[3:])
            
        self.ssml_stack.append(("<speak>", "</speak>"))


    
    def add_string(self, text: str) -> None:
        self.ssml_stack.append([(text, None)])
        
    def add_tag_to_string(self, tag_string: str, param_values: List[Tuple[int, any]]):
        tag_start: str = self.tags[tag_string].create_tag_start(param_values)
        tag_end: str = self.tags[tag_string].get_end_tag()
        
        previous = self.ssml_stack.pop()
        updated_previous = [(tag_start, tag_end)] + previous 
        self.ssml_stack.append(updated_previous)

    
    def add_tag(self, tag_string: str, param_values: List[Tuple[int, any]]):
        tag_start: str = self.tags[tag_string].create_tag_start(param_values)
        tag_end: str = self.tags[tag_string].get_end_tag()
        
        self.ssml_stack.append((tag_start, tag_end))


    def get_number_of_required_params(self, tag_string: str) -> int:
        tag = self.tags[tag_string]

        return 1 if tag.is_or_params else len(tag.params)
    
    def create_ssml(self, file_name: str):
        ssml_string: str = ""
        print()
        
        while self.ssml_stack:
            current = self.ssml_stack.pop()
            
            print(current)
            
            if type(current) is list:
                print("TEST 1")

                text_string: str = current.pop()[0]
                
                while len(current) > 0:
                    tag_start, tag_end = current.pop()
                    text_string = tag_start + text_string + tag_end
                
                ssml_string = text_string + ssml_string
            else:
                ssml_string = current[0] + ssml_string + current[1]
                
        with open(file_name, "w") as ssml_file:
            ssml_file.write(ssml_string)
                
    
    
        


     