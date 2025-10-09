# Test Directory

This directory contains test files and temporary data for the Audio PsyChat application.

## Files

### `do_not_delete_please.wav`
- **Purpose**: Test audio file used for ASR model warm-up
- **Usage**: Loaded during application startup to initialize the ASR model
- **Format**: WAV audio file
- **Important**: Required for proper application startup - do not delete

## Temporary Files

The application will create temporary files in this directory during operation:

- `input_audio.webm` - Temporary uploaded audio from web interface
- `input_audio.wav` - Converted audio file for ASR processing
- `output.wav` - Test output from TTS warm-up

These temporary files are automatically created and cleaned up by the application.

## Directory Structure

```
test/
├── README.md                 # This documentation
├── do_not_delete_please.wav  # Test audio for ASR warm-up
├── input_audio.webm          # Temporary upload (auto-created)
├── input_audio.wav           # Temporary converted audio (auto-created)
└── output.wav                # Temporary TTS output (auto-created)
```

## Notes

- This directory is automatically created by the application if it doesn't exist
- Temporary files are safe to delete manually if needed
- The `do_not_delete_please.wav` file should be preserved for proper application function
