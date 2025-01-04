import pyaudio
import numpy as np
from websocket_server import WebsocketServer
import threading
import json

# Configuration audio (default to 44.1 kHz, will adapt later)
CHUNK = 1024  # Taille du buffer
FORMAT = pyaudio.paInt16  # Format audio
DEFAULT_RATE = 44100  # Default sample rate (44.1 kHz)

# Fonction pour lister les périphériques d'entrée audio disponibles
def list_input_devices():
    p = pyaudio.PyAudio()
    print("Listing available audio input devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")
    p.terminate()

# Fonction pour vérifier les taux d'échantillonnage supportés par le périphérique
def get_supported_sample_rate(device_index):
    p = pyaudio.PyAudio()
    device_info = p.get_device_info_by_index(device_index)
    supported_rates = device_info.get('defaultSampleRate', DEFAULT_RATE)
    print(f"Supported Sample Rate for Device {device_index}: {supported_rates} Hz")
    p.terminate()
    return supported_rates

# Fonction pour capturer l'audio et envoyer les données via WebSocket
def audio_stream(server):
    # Initialisation de PyAudio
    p = pyaudio.PyAudio()

    # List available input devices and choose the correct one
    list_input_devices()
    device_index = 50  # Replace this with the correct index of your Realtek HD Output or preferred device

    # Get the number of input channels for the selected device
    device_info = p.get_device_info_by_index(device_index)
    input_channels = device_info['maxInputChannels']

    # Get the supported sample rate for the selected device
    sample_rate = get_supported_sample_rate(device_index)

    # Ensure mono (1 channel) or stereo (2 channels) depending on the device's capabilities
    if input_channels == 1:
        print("Mono input detected. Using 1 channel for capture.")
        channels = 1
    else:
        print("Stereo input detected or defaulting to stereo. Using 2 channels for capture.")
        channels = 2

    # Open the stream with the selected channel configuration and sample rate
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=int(sample_rate),  # Use the supported sample rate
                    input=True,
                    input_device_index=device_index,  # Specify the correct device index
                    frames_per_buffer=CHUNK)

    print(f"Démarrage de la capture audio avec un taux d'échantillonnage de {sample_rate} Hz...")
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            # Calcul FFT
            freq_data = np.fft.rfft(audio_data)
            freq_magnitude = np.abs(freq_data)  # Magnitude des fréquences

            # Normalisation des fréquences
            freq_magnitude = freq_magnitude / np.max(freq_magnitude)

            # Envoi des données audio et fréquences au client WebSocket
            server.send_message_to_all(json.dumps({
                "audio": audio_data.tolist(),
                "frequencies": freq_magnitude.tolist()
            }))
    except KeyboardInterrupt:
        print("Arrêt de la capture audio.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Configuration du serveur WebSocket
def start_websocket_server():
    server = WebsocketServer(host='0.0.0.0', port=8765)
    threading.Thread(target=audio_stream, args=(server,), daemon=True).start()
    print("Serveur WebSocket démarré sur ws://localhost:8765")
    server.run_forever()

if __name__ == "__main__":
    start_websocket_server()
