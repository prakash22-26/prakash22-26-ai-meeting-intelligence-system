import os
import json

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models import Meeting

from schemas import MeetingCreate

from services.openai_service import (
    generate_summary
)

from services.transcription_service import (
    transcribe_file
)

router = APIRouter()


# -----------------------------------
# NORMALIZE AI RESPONSE
# -----------------------------------

def normalize_response(parsed):

    parsed.setdefault(
        "meeting_overview",
        {}
    )

    parsed.setdefault(
        "participants_detected",
        []
    )

    parsed.setdefault(
        "chronological_flow",
        []
    )

    parsed.setdefault(
        "important_points",
        []
    )

    parsed.setdefault(
        "detailed_discussions",
        []
    )

    parsed.setdefault(
        "technical_topics_discussed",
        []
    )

    parsed.setdefault(
        "business_topics_discussed",
        []
    )

    parsed.setdefault(
        "frontend_discussions",
        []
    )

    parsed.setdefault(
        "backend_discussions",
        []
    )

    parsed.setdefault(
        "database_discussions",
        []
    )

    parsed.setdefault(
        "api_discussions",
        []
    )

    parsed.setdefault(
        "deployment_discussions",
        []
    )

    parsed.setdefault(
        "ai_or_ml_discussions",
        []
    )

    parsed.setdefault(
        "performance_scalability_discussions",
        []
    )

    parsed.setdefault(
        "security_discussions",
        []
    )

    parsed.setdefault(
        "testing_discussions",
        []
    )

    parsed.setdefault(
        "action_items",
        []
    )

    parsed.setdefault(
        "decisions_made",
        []
    )

    parsed.setdefault(
        "questions_and_answers",
        []
    )

    parsed.setdefault(
        "problems_or_risks",
        []
    )

    parsed.setdefault(
        "future_plans",
        []
    )

    parsed.setdefault(
        "important_notes",
        []
    )

    parsed.setdefault(
        "next_steps",
        []
    )

    parsed.setdefault(
        "final_conclusion",
        ""
    )

    return parsed


# -----------------------------------
# TEXT TRANSCRIPT ANALYSIS
# -----------------------------------

@router.post("/meetings")

def create_meeting(
    meeting: MeetingCreate
):

    db: Session = SessionLocal()

    try:

        parsed = generate_summary(
            meeting.transcript
        )

        parsed = normalize_response(
            parsed
        )

        new_meeting = Meeting(

            transcript=(
                meeting.transcript
            ),

            summary=(
                parsed[
                    "meeting_overview"
                ].get(
                    "overall_summary",
                    ""
                )
            ),

            action_items=json.dumps(
                parsed.get(
                    "action_items",
                    []
                )
            )
        )

        db.add(new_meeting)

        db.commit()

        db.refresh(new_meeting)

        return {

            "transcript":
                meeting.transcript,

            **parsed
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# -----------------------------------
# AUDIO / VIDEO ANALYSIS
# -----------------------------------

@router.post("/upload")

async def upload_meeting(
    file: UploadFile = File(...)
):

    allowed_extensions = [

        "mp3",
        "wav",
        "m4a",

        "mp4",
        "mov",
        "mkv"
    ]

    try:

        # -----------------------------------
        # VALIDATE FILE
        # -----------------------------------

        extension = (
            file.filename
            .split(".")[-1]
            .lower()
        )

        if extension not in allowed_extensions:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Unsupported file format"
                )
            )

        # -----------------------------------
        # SAVE TEMP FILE
        # -----------------------------------

        file_path = (
            f"temp_{file.filename}"
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

        # -----------------------------------
        # TRANSCRIBE FILE
        # -----------------------------------

        transcription_result = (
            transcribe_file(
                file_path
            )
        )

        # FULL RAW TEXT

        full_text = (
            transcription_result[
                "full_text"
            ]
        )

        # DETAILED TIMESTAMPED TEXT

        detailed_transcript = (
            transcription_result[
                "detailed_transcript"
            ]
        )

        # WHISPER SEGMENTS

        segments = (
            transcription_result[
                "segments"
            ]
        )

        # DEBUG

        print(
            detailed_transcript
        )

        # -----------------------------------
        # AI ANALYSIS
        # -----------------------------------

        parsed = generate_summary(
            detailed_transcript
        )

        parsed = normalize_response(
            parsed
        )

        print(parsed)

        # -----------------------------------
        # STORE IN DATABASE
        # -----------------------------------

        db: Session = SessionLocal()

        new_meeting = Meeting(

            transcript=(
                detailed_transcript
            ),

            summary=(
                parsed[
                    "meeting_overview"
                ].get(
                    "overall_summary",
                    ""
                )
            ),

            action_items=json.dumps(
                parsed.get(
                    "action_items",
                    []
                )
            )
        )

        db.add(new_meeting)

        db.commit()

        db.refresh(new_meeting)

        # -----------------------------------
        # CLEAN TEMP FILES
        # -----------------------------------

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )

        mp3_path = (
            file_path.split(".")[0]
            + ".mp3"
        )

        if os.path.exists(
            mp3_path
        ):

            os.remove(
                mp3_path
            )

        # -----------------------------------
        # FINAL RESPONSE
        # -----------------------------------

        return {

            # BASIC TRANSCRIPT

            "transcript":
                full_text,

            # TIMESTAMPED TRANSCRIPT

            "detailed_transcript":
                detailed_transcript,

            # WHISPER SEGMENTS

            "segments":
                segments,

            # AI ANALYSIS

            **parsed
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# -----------------------------------
# GET SAVED MEETINGS
# -----------------------------------

@router.get("/meetings")

def get_meetings():

    db: Session = SessionLocal()

    meetings = db.query(
        Meeting
    ).all()

    return meetings