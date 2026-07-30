import os

from openai import OpenAI

from moviepy import VideoFileClip


# -----------------------------------
# LOAD MODEL
# -----------------------------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# -----------------------------------
# SUPPORTED FORMATS
# -----------------------------------

AUDIO_EXTENSIONS = [
    "mp3",
    "wav",
    "m4a"
]

VIDEO_EXTENSIONS = [
    "mp4",
    "mov",
    "mkv"
]


# -----------------------------------
# EXTRACT AUDIO FROM VIDEO
# -----------------------------------

def extract_audio(
    video_path
):

    try:

        audio_path = (

            os.path.splitext(
                video_path
            )[0]

            + ".mp3"
        )

        video = VideoFileClip(
            video_path
        )

        if video.audio is None:

            raise Exception(
                "Video contains no audio"
            )

        video.audio.write_audiofile(

            audio_path,

            logger=None
        )

        video.close()

        return audio_path

    except Exception as e:

        raise Exception(

            f"Audio extraction failed: {str(e)}"
        )


# -----------------------------------
# BUILD TIMELINE TRANSCRIPT
# -----------------------------------

def build_detailed_transcript(segments):

    transcript_parts = []

    for segment in segments:

        start = round(segment["start"], 2)
        end = round(segment["end"], 2)
        text = segment["text"].strip()

        transcript_parts.append(
            f"[START: {start}s - END: {end}s]\n\n{text}\n"
        )

    return "\n".join(transcript_parts)


# -----------------------------------
# TRANSCRIBE FILE
# -----------------------------------

def transcribe_file(
    file_path
):

    try:

        extension = (
            file_path
            .split(".")[-1]
            .lower()
        )

        temp_audio_path = None

        # VIDEO INPUT

        if extension in VIDEO_EXTENSIONS:

            temp_audio_path = (
                extract_audio(
                    file_path
                )
            )

            transcription_path = (
                temp_audio_path
            )

        # AUDIO INPUT

        elif extension in AUDIO_EXTENSIONS:

            transcription_path = (
                file_path
            )

        else:

            raise Exception(
                "Unsupported file format"
            )

        # -----------------------------------
        # TRANSCRIBE
        # -----------------------------------

        with open(transcription_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="verbose_json",
                language="en"
            )

        # CONVERT GENERATOR TO LIST

        segments = transcription.segments

        # FULL TEXT

        full_text = transcription.text

        # DETAILED TIMELINE

        detailed_transcript = (
            build_detailed_transcript(
                segments
            )
        )

        # CLEANUP TEMP AUDIO

        if (
            temp_audio_path
            and os.path.exists(
                temp_audio_path
            )
        ):

            os.remove(
                temp_audio_path
            )

        return {

            "full_text":
                full_text,

            "segments": [

                {
                    "start":
                        segment["start"],

                    "end":
                        segment["end"],

                    "text":
                        segment["text"]
                }

                for segment in segments
            ],

            "detailed_transcript":
                detailed_transcript
        }

    except Exception as e:

        raise Exception(

            f"Transcription failed: {str(e)}"
        )
