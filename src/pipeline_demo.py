from VoiceInput.voice_input import VoiceInput

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
    i = 0
    print("Loaded")
    while True:
        i = i+1
        transcription = vinput.get_phrase()
        print(f"{i}: {transcription}")

if __name__ == "__main__":
    main()