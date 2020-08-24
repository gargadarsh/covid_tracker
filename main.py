from speech import speak, getAudio
from patterns import TOTAL_PATT, COUNTRY_PATT, UPDATE_PATT, data


def main():
    print("Starting COVID-19 Tracker and Predictor Voice Assistant :]")
    print("NOTE: Say STOP to stop the program!")

    countries = data.getListOfCountries()

    while True:
        print("\nListening: ")
        text = getAudio()
        print(text)
        result = None


        #for outputting country specific data
        for pattern, func in COUNTRY_PATT.items():
            if pattern.match(text):
                words = list(text.split(" "))
                for country in countries:
                    if country in words:
                        result = func(country)
                        break


        #for outputting total
        for pattern, func in TOTAL_PATT.items():
            if pattern.match(text):
                result = func()
                break

        #to update data
        if text.find(UPDATE_PATT) != -1:
            print("Data is being updated... This may take a while...")
            speak("Data is being updated... This may take a while...")
            data.updateData()
            print("Data is up to date!")
            speak("Data is up to date")

        if(text == "hello"):
            result = "Hello"

        if result:
            print(result)
            speak(result)

        if text.find("stop") != -1:
            print("Program has stopped")
            break

main()
