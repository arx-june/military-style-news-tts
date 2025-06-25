import boto3
import os
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
from botocore.exceptions import BotoCoreError, ClientError
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

def synthesize_speech(text, voice='Matthew'):
    
    print(f"DEBUG: AWS Region: {AWS_REGION}")
    print(f"DEBUG: Voice: {voice}")
    print(f"DEBUG: Text length: {len(text)}")
    
    if not AWS_ACCESS_KEY or AWS_ACCESS_KEY == 'your-aws-access-key-here':
        raise Exception("AWS credentials not configured properly")
    
    
    try:
        polly = boto3.client(
            "polly",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        response = polly.synthesize_speech(
            Engine="neural",
            LanguageCode="en-US",
            VoiceId=voice,
            OutputFormat="mp3",
            Text=text
        )
        return response["AudioStream"].read()
    except (BotoCoreError, ClientError) as e:
        logger.error(f"AWS Polly error: {e}")
        raise Exception(f"Speech synthesis failed: {str(e)}")
