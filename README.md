# Enhancing Trust in Intelligent Virtual Agents: The Role of Acoustic Cues, Lexical Style, and Listener Characteristics in the Perception of Synthesized Speech
This repository supports the research presented in our paper, which has been accepted for publication (details forthcoming).

## Speech stimuli
Question-based speech clips are saved under these three folders: 
1. question_humor_audio,
2. question_neutral_audio,
3. question_polite_audio.

Recommendation-based speech clips are saved under these three folders: 
1. recommendation_humor_audio,
2. recommendation_neutral_audio,
3. recommendation_polite_audio.

Note: The audio name: q10_F_saved_audio_files_wav corresponds to text 10, female speaker

## Code
temp_generate_combinations.py and aws_handler.py are main codes to generate speech stimuli
analysis_script folder has analysis.ipynb file to analysis code and results, you need to replace dataset to generate corresponding results

## Collected ratings
collected_ratings includes all collected ratings from 6 experiments; rec == recommendation, q == question, pol == polite, hum = humor.
1. csv file name started with 'processed_df_' has the average of trustworthy ratings from unique 5 raters for each audio clip.
2. csv file name started with 'speaker' has the rater info.
3. csv file name started with 'aggregated_df_tipi_' has the aggregated information for raters and their ratings info.
4. Pairwise_Preference_Test.csv has the data for Section 9: Pairwise Preference Test for Lexical Style Under Trustworthy Acoustic Conditions.


If you have any questions about data or code, please reach out to yyu4@gradcenter.cuny.edu
