import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def convert_opus_to_wav(webm_file_path, wav_file_path):
    """Convert webm/opus audio to wav format using ffmpeg"""
    try:
        # Check if ffmpeg is available
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("ffmpeg not found in PATH")
        
        ffmpeg_path = result.stdout.strip()
        logger.info(f"Using ffmpeg at: {ffmpeg_path}")
        
        # Remove existing output file if it exists
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)
            
        # Build ffmpeg command
        command = [
            ffmpeg_path, '-i', webm_file_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # Audio codec
            '-f', 'wav',  # Output format
            '-ar', '16000',  # Sample rate
            '-ac', '1',  # Mono channel
            '-y',  # Overwrite output file
            wav_file_path
        ]
        
        # Execute command
        logger.info(f"Converting {webm_file_path} to {wav_file_path}")
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"FFmpeg conversion failed: {result.stderr}")
            
        if not os.path.exists(wav_file_path):
            raise RuntimeError("Output file was not created")
            
        logger.info("Audio conversion completed successfully")
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("FFmpeg conversion timed out")
    except Exception as e:
        logger.error(f"Error in audio conversion: {e}")
        raise RuntimeError(f"Audio conversion failed: {e}")


if __name__ == '__main__':
    # 示例使用
    webm_file = './test/input_audio.webm'
    wav_file = './test/input_audio.wav'
    convert_opus_to_wav(webm_file, wav_file)
