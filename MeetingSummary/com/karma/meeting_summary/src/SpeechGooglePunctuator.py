import argparse
import io

from google.cloud import speech_v1 as speech


# [START speech_transcribe_file_with_enhanced_model]
def transcribe_file_with_enhanced_model(path):
    """Transcribe the given audio file using an enhanced model."""
    client = speech.SpeechClient()

    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='phone_call')

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
# [END speech_transcribe_file_with_enhanced_model]


# [START speech_transcribe_file_with_metadata]
def transcribe_file_with_metadata(path):
    """Send a request that includes recognition metadata."""
    client = speech.SpeechClient()

    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()

    # Here we construct a recognition metadata object.
    # Most metadata fields are specified as enums that can be found
    # in speech.enums.RecognitionMetadata
    metadata = speech.types.RecognitionMetadata()
    metadata.interaction_type = (
        speech.enums.RecognitionMetadata.InteractionType.DISCUSSION)
    metadata.microphone_distance = (
        speech.enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD)
    metadata.recording_device_type = (
        speech.enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE)
    # Some metadata fields are free form strings
    metadata.recording_device_name = "Pixel 2 XL"
    # And some are integers, for instance the 6 digit NAICS code
    # https://www.naics.com/search/
    metadata.industry_naics_code_of_audio = 519190

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Add this in the request to send metadata.
        metadata=metadata)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
# [END speech_transcribe_file_with_metadata]


# [START speech_transcribe_file_with_auto_punctuation]
def transcribe_file_with_auto_punctuation(path):
    """Transcribe the given audio file with auto punctuation enabled."""
    client = speech.SpeechClient()

    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
# [END speech_transcribe_file_with_auto_punctuation]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command')
    parser.add_argument(
        'path', help='File for audio file to be recognized')

    args = parser.parse_args()

    if args.command == 'enhanced-model':
        transcribe_file_with_enhanced_model(args.path)
    elif args.command == 'metadata':
        transcribe_file_with_metadata(args.path)
    elif args.command == 'punctuation':
        transcribe_file_with_auto_punctuation(args.path)

