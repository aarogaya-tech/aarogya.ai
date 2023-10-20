import requests
import io
from .models import Patient, Transcript
from celery import shared_task

@shared_task
def count_patients():
    print(f'# of patients: {Patient.objects.count()}')

@shared_task
def transcribe_audio(transcript_id):
    transcript = Transcript.objects.get(id=transcript_id)
    result = requests.get(
        "https://asr.naamii.org.np/predictions/Wav2Vec2",
        files={"data": transcript.audio_file_url.file},
        timeout=1000000
    )
    transcribed_text = result.content.decode(encoding="utf-8")
    transcript.generated_transcript = transcribed_text
    transcript.transcript_generation_in_progress = False
    transcript.save()
    print("done transcribing")
    print(result)
    return result
