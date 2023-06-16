from VoiceInput.voice_input import VoiceInput
from Conversation.conversation import Conversation
from TTS.text_to_speech import Text_To_Speech
from Conversation.conversation import read_initial_prompt
from VoiceRecord.voice_record import VoiceRecord
import requests

# The URL of the API endpoint
url = "http://localhost:5000/api"


def main():
    vinput = VoiceInput(
        whisper_model='small',
        non_english=False,
        energy_treshold=1000,
        # default_mic='Blue Snowball: USB Audio (hw:1,0)',
        default_mic="default",
        # record_timeout=2,
        # phrase_timeout=3,
        pause_threshold=2
    )
    print("Voice input ready")
    
    tts = Text_To_Speech()
    print('\n')
    decision = input("Record the voice sample [y] or use current one [n]: ")
    print('\n')
    if decision=='y':
        VoiceRecord(filename="sample.wav")
    else:
        tts.set_sample('./sample.wav')

    input("start the conversation? press enter.")
    i = 0
    while True:
        i += 1
        print("Your turn to speak")
        transcription = vinput.get_phrase()
        print(f"transcribed voice: {transcription}")
        #transcription = input("your response: ")
        #response = conversation.respond(transcription, max_tokens=40)

        # Send a POST request to the API
        response_data = requests.post(url=url, json={"response": transcription})
        response=response_data.json()["message"]
        # Check if the request was successful
        if response_data.status_code == 200:
            print('\nconnection succesfull')
            print(f"chatbot says: {response_data.json()}\n")
        else:
            print('request to chatbot failed with status code: ', response_data.status_code)
        

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