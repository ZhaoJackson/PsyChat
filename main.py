from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from api.ffmpeg_api import convert_opus_to_wav
from pydantic import BaseModel
from api.psy_chat_api import PsyChatModel
from paddlespeech.cli.tts.infer import TTSExecutor
from pathlib import Path as P
from paddlespeech.cli.asr.infer import ASRExecutor
from fastapi.staticfiles import StaticFiles
import os
import logging
# from fastapi.middleware.cors import CORSMiddleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure required directories exist
os.makedirs('./test', exist_ok=True)
os.makedirs('./web/wavs', exist_ok=True)


app = FastAPI()

# # 2、声明一个 源 列表；重点：要包含跨域的客户端 源
# origins = ["*"]
#
# # 3、配置 CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # 允许访问的源
#     allow_credentials=True,  # 支持 cookie
#     allow_methods=["*"],  # 允许使用的请求方法
#     allow_headers=["*"]  # 允许携带的 Headers
# )

app.mount("/static", StaticFiles(directory="web", html=True), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "models_loaded": True,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


# When user uploads audio file, this method is used to receive and process the uploaded audio file
# TODO
@app.post('/api/audio_to_audio')
async def audio_to_audio(audio: UploadFile = File(...), history: str = Form(...)):
    if audio.filename == '':
        raise HTTPException(status_code=400, detail="No audio part")
    if not history:
        raise HTTPException(status_code=400, detail="No history part")

    try:
        # 读取音频文件
        contents = await audio.read()

        webm_path = './test/input_audio.webm'
        wav_path = './test/input_audio.wav'
        try:
            with open(webm_path, 'wb') as file:
                # 将字节流写入文件
                file.write(contents)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error writing webm file: {e}")
        convert_opus_to_wav(webm_path, wav_path)

        try:
            # Call Automatic Speech Recognition (ASR) interface
            logger.info("Starting ASR processing...")
            asr_text = call_asr_api(wav_path)
            logger.info(f"ASR result: {asr_text[:100]}...")
            
            # Use ASR recognition result to call Large Language Model (LLM)
            history += "\n" + "Visitor: " + asr_text
            logger.info("Starting LLM processing...")
            llm_response = call_llm_api(history)
            logger.info(f"LLM response: {llm_response[:100]}...")
            
            # Use LLM output to call Text-to-Speech (TTS) interface
            logger.info("Starting TTS processing...")
            tts_audio_path = call_tts_api(llm_response)
            logger.info(f"TTS output saved to: {tts_audio_path}")
            
        except Exception as e:
            logger.error(f"Error in processing pipeline: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in processing with ASR, LLM, or TTS APIs: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    # Temporary data
    # asr_text = "This is ASR output"
    # llm_response = "This is LLM response"
    # tts_audio_path = "tmp_0005.wav"

    # Return ASR and TTS results
    return JSONResponse(content={"asrText": asr_text, "llm_response": llm_response, "ttsAudio": tts_audio_path})


class TextItem(BaseModel):
    text: str


@app.post('/api/text_to_audio')
async def text_to_audio(item: TextItem):
    text = item.text
    if not text:
        raise HTTPException(status_code=400, detail="No text part")

    llm_response = call_llm_api(text)
    tts_audio = call_tts_api(llm_response)
    return JSONResponse(content={"llm_response": llm_response, "ttsAudio": tts_audio})


# When user clicks "Play Audio", if there's no local cache for that audio, it will search from server, if server has no cache, then call TTS
# TODO
@app.get("/api/text_converte_audio")
async def text_converte_audio():
    # print("Current Working Directory:", os.getcwd())
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(dir_path, "tmp_0006.wav")
    # llm_response = "This is LLM response"
    # return JSONResponse(content={"llm_response": llm_response, "file_url123": file_path})

    # text = item.text
    # if not text:
    #     raise HTTPException(status_code=400, detail="No text part")

    # tts_audio = call_tts_api(llm_response)
    # return JSONResponse(content={"llm_response": llm_response, "ttsAudio": tts_audio})
    return JSONResponse(content={"temp_response": "This feature is temporarily incomplete, please wait for development"})


# Initialize models with error handling
logger.info("Initializing models...")
try:
    logger.info("Loading ASR model...")
    asr = ASRExecutor()
    
    logger.info("Loading TTS model...")
    tts = TTSExecutor()
    
    logger.info("Loading PsyChat LLM model...")
    llm = PsyChatModel()
    
    # Run ASR+TTS once first to speed up inference (warm-up)
    logger.info("Warming up models...")
    if os.path.exists('./test/do_not_delete_please.wav'):
        asr(P('./test/do_not_delete_please.wav'))
    else:
        logger.warning("Test audio file not found, skipping ASR warm-up")
        
    tts(text="Hello, this is a test audio", output="./test/output.wav",
        am="fastspeech2_male", voc="pwgan_male")
    
    logger.info("All models loaded and warmed up successfully!")
    
except Exception as e:
    logger.error(f"Failed to initialize models: {e}")
    raise RuntimeError(f"Model initialization failed: {e}")


# Simulated ASR API call function
def call_asr_api(audio_path: str):
    # This should be code for calling external ASR service
    return asr(P(audio_path), force_yes=True)  # "Converted text"


# Simulated LLM API call function
def call_llm_api(text: str):
    # This should be code for calling external LLM service
    return llm.new_line_with_history(text)


# Simulated TTS API call function
def call_tts_api(text: str):
    # Code for calling external TTS service
    output_wav_path = './web/wavs/tts.wav'
    tts(text=text, output=output_wav_path, am="fastspeech2_male", voc="pwgan_male")
    return output_wav_path


# Run FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8086)
