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
        # default_mic='Blue Snowball: USB Audio (hw:1,0)',
        default_mic="default",
        # record_timeout=2,
        # phrase_timeout=3
    )
    print("Voice input ready")
    
    conversation = Conversation(initial_prompt = read_initial_prompt(), model_path = "../models/ggml-vicuna-13B-1.1-q4_0.bin")

    tts = Text_To_Speech()
    print('\n')
    input("nagrać? ")
    VoiceRecord(filename="sample.wav")
    print('\n')
    tts.set_sample('./sample_woman.wav')

    i = 0
    while True:
        i += 1
        transcription = vinput.get_phrase()
        print(f"transcribed voice: {transcription}")
        #transcription = input("your response: ")
        response = conversation.respond(transcription)
        print(f"chatbot says: {response}")
        tts.vocalize(response) #response is saved inside tts object, I figured it might be more convenient. I implemented playback and write-to-file methods specific for tts already, second one working, first one has troubles specific to my system
        try: 
            tts.play_audio()
            tts.save_audio()
        except:
            tts.save_audio()
        input("kontynuować7? ")

            
        print(f"{i}: {transcription}")
        print("Response: {:}".format(response))


if __name__ == "__main__":
    main()
