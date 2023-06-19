from VoiceInput.voice_input import VoiceInput
from Conversation.conversation import Conversation
from TTS.text_to_speech import Text_To_Speech
from Conversation.conversation import read_initial_prompt
from VoiceRecord.voice_record import VoiceRecord
# right now, there are some issues/warnings with microphone integration

def main():
    vinput = VoiceInput(
        whisper_model='small',
        non_english=False,
        energy_treshold=1000,
        default_mic='Blue Snowball: USB Audio (hw:1,0)',
        # default_mic="default",
        # record_timeout=2,
        # phrase_timeout=3,
        pause_threshold=2
    )
    print("Voice input ready")
    
    conversation = Conversation(initial_prompt = read_initial_prompt(), model_path = "../models/koala-7B.ggmlv3.q4_0.bin")

    tts = Text_To_Speech()
    print('\n')
    decision = input("Record the voice sample [y] or use current one [n]: ")
    print('\n')
    if decision=='y':
        VoiceRecord(filename="sample.wav")
    else:
        tts.set_sample('./sample.mp3')

    input("start the conversation? press enter.")
    # tts.vocalize("This is a test of the text-to-speech model. Here is a simple 2 sentences to test if it works and how well it works.")
    # tts.play_audio()
    # tts.save_audio()
    i = 0
    while True:
        i += 1
        print("Your turn to speak")
        transcription = vinput.get_phrase()
        print(f"transcribed voice: {transcription}")
        #transcription = input("your response: ")
        # response = conversation.respond(transcription, max_tokens=40)
        response = "This is an example response. Conversation model is not working right now."
        print(f"chatbot says: {response}")
        tts.vocalize(response) #response is saved inside tts object, I figured it might be more convenient. I implemented playback and write-to-file methods specific for tts already, second one working, first one has troubles specific to my system
        try: 
            tts.play_audio()
            tts.save_audio()
        except:
            tts.save_audio()
        input("continue the conversation? ")
        #print(f"{i}: {transcription}")
        #print("Response: {:}".format(response))


if __name__ == "__main__":
    main()


"""
Parameters on CPU:
llama_print_timings:        load time = 32865.04 ms
llama_print_timings:      sample time = 0.84 ms per token
llama_print_timings: prompt eval time = 139.85 ms per token
llama_print_timings:        eval time = 3425.51 ms per token
"""

"""
text to read:
The word penguin first appears in literature at the end of the 16th century. When European explorers discovered what are today known as penguins in the Southern Hemisphere, they noticed their similar appearance to the great auk of the Northern Hemisphere, and named them after this bird, although they are not closely related.

The etymology of the word penguin is still debated. The English word is not apparently of French, Breton or Spanish origin (the latter two are attributed to the French word pingouin), but first appears in English or Dutch.
"""