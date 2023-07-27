from ssml_reader import SsmlReader

if __name__ == '__main__':
    reader: SsmlReader = SsmlReader()
    reader.extract_file_ssml("/Users/ghaz/documents/research_speech/ssmls/speech_test.txt")
    
    reader.save_file_contents_as_speech()
    