from typing import Tuple, List, Set, Dict

class Tag: 
    def __init__(self, tag: Tuple[str, str or None], tag_description: str, tag_params: List[str]):
        self.tag_start: str = tag[0]
        self.tag_end: str = tag[1] if len(tag[1]) > 0 and tag[1].strip() != "None" else ""
        self.tag_description: str = tag_description 
        
        self.param_information: Dict[any, any] = {}

        param_string: str = tag_params[0]
        param_types: List[str] = tag_params[1:]
        self.params: List[str] = []
        self.is_or_params: bool = False 
        
        if param_string != "None":
            if " or " in param_string:
                self.is_or_params = True 
                self.params = param_string.split(" or ")
            else:         
                if " and "in param_string:
                    self.params = param_string.split(" and ")
                else:
                    self.params = [param_string]
                    self.is_or_params = True 

        else:
            param_types = []
            param_string = ""
            self.params = []
                    
        if len(param_types) != len(self.params):
            print("Please double check this tags data", tag)
            
        for i, param in enumerate(self.params):
            options = param_types[i].split(", ")
            
            self.param_information[i] = {
                "param": param,
                "options": set(options)
            }
            
    def _insert_parameter_value(self, param_values: Tuple[int, any]) -> str:
        REPLACE: Set[str] = {"X", "Y"}
                
        if param_values[0] not in self.param_information:
            print("The param index does not exist for this tag")
            return
        
        current_param_information = self.param_information[param_values[0]]
        param: str = current_param_information["param"]
        options: Set[str] = current_param_information["options"]
        
        type_of_replacements: List[str] = []
        
        for replacement in REPLACE:
            if replacement in param:
                type_of_replacements.append(replacement)
                
        if not type_of_replacements:
            print("There is no parameter to replace, please double check the tag text file")
        
        parameter_string: str = ""
               
        if not("Any" in options or param_values[1] in options):
            print("This parameter cannot be used for this tag, please double check the tag text file")
        else: 
            for replacement in type_of_replacements:
                parameter_string = param.replace(replacement, param_values[1])
    
        return parameter_string                               
        
        
    def create_tag_start(self, param_values: List[Tuple[int, any]]) -> str:
        tag: str = self.tag_start
        if self.param_information:
            parameter_string: str = ""
            
            if self.is_or_params and len(param_values) == 1:
                parameter_string = self._insert_parameter_value(param_values[0]) 
            elif not self.is_or_params and len(param_values) > 1:
                for param in param_values:
                    parameter_string += self._insert_parameter_value(param) 
            else:
                print("Please double check ")

            tag = f"{tag[:-1]}={parameter_string}>"
       
        return tag
    
    def get_end_tag(self) -> str:
        return self.tag_end
    
    def get_description(self) -> str:
        return self.tag_description
    
    def __str__(self) -> str:
        stringified: str = f"Start Tag: {self.tag_start},\nEnd Tag: {self.tag_end},\nDescription: {self.tag_description},\nParameter Information: {self.param_information}"
        return stringified
    
        
        
# print()
# test_one: Tag = Tag(["<speak>", "</speak>"], "Basic tag for instantiating a ssml script", ["None", "None"])
# print(test_one)
# print(test_one.create_tag_start([(None, None)])) 

# print()
# test_two: Tag = Tag(["<emphasis>","</emphasis>"], "Emphasizes words by altering the speaking rate and volume based on a param", ["X", "strong, moderate, reduced"])
# print(test_two, test_two.is_or_params)
# print(test_two.create_tag_start([(0, "strong")])) 

# print()
# test_three: Tag = Tag(["<prosody volume>", "</prosody>"], "Adjusts the volume of of a voice. Y in this case is an integer", ["X or +YdB or -YdB", "default, silent, x-soft, medium, loud, x-loud", "Any", "Any"])
# print(test_three)
# print(test_three.create_tag_start([(0, "default")])) 
# print(test_three.create_tag_start([(1, "10")])) 

# print()
# test_four: Tag = Tag(["<break time>", ""], "Tag for creating a pause. Xs meaning X number of units of Y (if seconds <= 10s, if milliseconds <= 1000ms). Where Y is a time unit.", ["X and Y", "Any", "s, ms"])
# print(test_four)
# print(test_four.create_tag_start([(0, "1000"), (1, "s")])) 

# Reminder: fix <break time=1000s/>, / is not acccountd for