from text_to_speech import Text_To_Speech
import sys
sys.path.append('./Real-Time-Voice-Cloning')

if __name__ == "__main__":
    TTS = Text_To_Speech()
    while True:
        user_input = input("enter sample name or press enter to interpolate: ")
        user_int_input=[]
        alpha=0
        if user_input == "quit":
            print("Exiting program...")
            break
        elif user_input == "":
            user_int_input.append(input("provide first sample name: "))
            user_int_input.append(input("provide second sample name: "))
            alpha=float(input("provide 0-1 alpha: "))
        else:
            print("Unknown command, please try again.")

        sentence_input = input("enter text to vocalize: ")
        if sentence_input == "":
            print("loaded default sentence")
            #sentences long enough (~twice size of following one) start to deform on their own still using recognisable voice but with blurred and unintelligible words
            #sentence_input = 'I remember you was conflicted. Misusing your influence. Sometimes I did the same. Ar ar ar, ur ur ur, mom, mommm, while we were. Rough. Thou shall be glad, ye who misguides. Lord may have thee.'
            sentence_input = 'With war just around the corner the risk of identity fracture is back. The risk of losing our culture is experienced through the artificial synthesis of a personalised God in an AI driven multimedia installation.'




        if user_input != "":
            TTS.set_sample(user_input)
        else:
            TTS.interpolate_embeddings(*user_int_input, alpha)

        TTS.vocalize(sentence_input)
        try: 
            TTS.play_audio()
            TTS.save_audio()
        except:
            TTS.save_audio()
        #generating this on CPU takes around 10 seconds, length doesn't scale linearly, device is more efficient with longer text.