from VoiceInput.voice_input import VoiceInput
from Conversation.conversation import Conversation
from TTS.text_to_speech import Text_To_Speech
# right now, there are some issues/warnings with microphone integration

def main():
    vinput = VoiceInput(
        whisper_model='small',
        non_english=False,
        energy_treshold=1000,
        # default_mic='Blue Snowball: USB Audio (hw:1,0)',
        default_mic="pulse",
        # record_timeout=2,
        # phrase_timeout=3
    )
    print("Voice input ready")

    conversation = Conversation(initial_prompt = "You are a helpful and intelligent assistant. Your interlocutor is not. Be ready for anything.", api_key_path = "Change this")

    tts = Text_To_Speech()
    tts.set_sample('sample_wav_path')

    i = 0
    while True:
        i += 1
        transcription = vinput.get_phrase()
        response = conversation.respond(transcription)
        tts.vocalize(response) #response is saved inside tts object, I figured it might be more convenient. I implemented playback and write-to-file methods specific for tts already, second one working, first one has troubles specific to my system
        try: 
            tts.play_audio()
            tts.save_audio()
        except:
            tts.save_audio()

            
        print(f"{i}: {transcription}")
        print("Response: {:}".format(response))


if __name__ == "__main__":
    main()
