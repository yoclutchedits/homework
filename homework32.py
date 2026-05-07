import threading , sys , time , pyaudio , numpy as np , matplotlib.pyplot as plt , wave , speech_recognition as sr
from speech_recognition import AudioData
from colorama import init, Fore, Style
init(autoreset=True)
stop_event = threading.Event()
def wait_for_enter():
    input(f"{Fore.CYAN}Press Enter to stop recording...")
    stop_event.set()
def spinner():
    char=f'{Fore.MAGENTA}|/-\\{Style.RESET_ALL}'
    i=0
    while not stop_event.is_set():
        sys.stdout.write(f'{Fore.MAGENTA}\rRecording... {Style.RESET_ALL}' + char[i % 4])
        sys.stdout.flush()
        i+=1
        time.sleep(0.1)
    print(f"{Fore.GREEN}\nRecording stopped.{Style.RESET_ALL}")
def play_audio(data, rate, width):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(width),channels=1,rate=rate,output=True)
    print(f"{Fore.GREEN}Playing back recording...{Style.RESET_ALL}")
    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"{Fore.GREEN}Playback finished.{Style.RESET_ALL}")
def record_audio():
    p=pyaudio.PyAudio()
    try:
        stream=p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)
    except Exception as e:
        print(f"{Fore.RED}Error accessing microphone: {e}{Style.RESET_ALL}")
        sys.exit(1)
    frames=[]
    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()
    while not stop_event.is_set():
        frames.append(stream.read(1024))
    stream.stop_stream()
    stream.close()
    width=p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b''.join(frames), 16000, width
def save_audio(data, rate, width, filename="output.wav"):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Audio saved to {filename}")
def transcribe_audio(data, rate, width):
    recognizer = sr.Recognizer()
    audio=AudioData(data, rate, width)
    try:
        text=recognizer.recognize_google(audio)
        print(f"{Fore.YELLOW}Transcription: {text}{Style.RESET_ALL}")
    except sr.UnknownValueError:
        print(f"{Fore.RED}Could not understand audio{Style.RESET_ALL}")
    except sr.RequestError as e:
        print(f"{Fore.RED}Could not request results; {e}{Style.RESET_ALL}")
def transcribe_save(data, rate, width, name):
    recognizer = sr.Recognizer()
    audio=AudioData(data, rate, width)
    try:
        text=recognizer.recognize_google(audio)
        print(f"{Fore.YELLOW}Transcription: {text}{Style.RESET_ALL}")
        with open(name, "w") as f: f.write(text)
        print(f"{Fore.GREEN}Transcript saved → {name}")
    except sr.UnknownValueError:
        print(f"{Fore.RED}Could not understand audio{Style.RESET_ALL}")
    except sr.RequestError as e:
        print(f"{Fore.RED}Could not request results; {e}{Style.RESET_ALL}")
def plot_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color='blue')
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
def main():
    while True:
        stop_event.clear()
        print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Hello AI, can you hear me?{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}speak into your mic, and press Enter when you're done.{Style.RESET_ALL}")
        audio_data, rate, width = record_audio()
        time.sleep(0.2)
        n=input(f"{Fore.CYAN}Do you want to play back that audio? (y/N): {Style.RESET_ALL}").lower() or "n"
        if n.lower() == 'y':
            play_audio(audio_data, rate, width)
        y=input(f"{Fore.CYAN}Do you want to save that audio? (y/N): {Style.RESET_ALL}").lower() or "n"
        if y.lower() == 'y':
            filename = input(f"{Fore.CYAN}Enter the filename (without extension): {Style.RESET_ALL}") or "output"
            save_audio(audio_data, rate, width, filename + ".wav")
        transcribe_audio(audio_data, rate, width)
        if input(f"{Fore.CYAN}Do you want to save the transcription? (y/N): {Style.RESET_ALL}").lower() or "n" == 'y':
            name = input(f"{Fore.CYAN}Enter the filename for transcript (without extension): {Style.RESET_ALL}") or "transcript"
            transcribe_save(audio_data, rate, width, name + ".txt")
        plot_waveform(audio_data, rate)
        n=input(f"{Fore.CYAN}Do you want to record again? (y/N): {Style.RESET_ALL}").lower() or "n"
        if n.lower() == 'n':
            print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
if __name__ == "__main__":
    if input(f"{Fore.CYAN} ready to record? (Y/n): {Style.RESET_ALL}").lower() or "y" == 'y':
        main()
