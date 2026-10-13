# DysLingo: Smart Reading for Dyslexia

A student final-year project prototype for accessible reading support. It includes:
- A student dashboard
- Smart Reader with adjustable font size, letter spacing and line spacing
- Browser text-to-speech with English, Tamil and Hindi language selections
- Optional OCR for uploaded page images (requires Tesseract OCR and language packs)
- Speech practice using browser speech recognition where available, with manual transcript entry as fallback
- Text comparison feedback and a local SQLite practice history
- An informal reading check-in questionnaire
- Progress chart and teacher/parent demo view

## Important limitations
This is a functional prototype, not a clinically validated dyslexia screening or diagnosis system. The screening questionnaire is illustrative and must not be presented as a validated instrument. The practice comparison is a simple word-matching baseline, not a trained ML model or clinical assessment. WPM is an estimate using a one-minute default, and actual pauses/phonemes are not measured. Browser speech recognition and voices vary by browser, operating system, language pack and network connection. The teacher/parent page has no authentication and is for local demonstration only.

## Requirements
- Python 3.10+
- A modern browser
- Internet connection for Bootstrap/Chart.js CDN assets (or download those assets locally for offline use)

## Run on Windows
1. Extract `DysLingo.zip`.
2. Open the `DysLingo` folder in VS Code.
3. Open Terminal in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install packages:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Start the application:
   ```bash
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

## Optional OCR setup
The Python `pytesseract` package is only a bridge; the Tesseract OCR program must also be installed separately.
- Install Tesseract OCR for your OS.
- Ensure the Tesseract executable is on PATH.
- Install language data for English (`eng`), Tamil (`tam`) and Hindi (`hin`) as needed.
- Restart the terminal and try OCR from the Smart Reader.

If OCR is not configured, all other features can still be used.

## Suggested demo checklist
1. Open Smart Reader and paste a paragraph.
2. Change font size and letter/line spacing.
3. Choose English, Tamil or Hindi and try Read aloud (voice availability varies).
4. Open Practice, enter a short passage and transcript, then save the session.
5. Open Progress to see the saved session and chart.
6. Complete the Reading Check-in and discuss the result as a non-diagnostic prompt.
7. Show the Teacher/Parent overview and explain the prototype's privacy limitations.

## Next steps for a research-grade project
- Use a validated screening instrument only with appropriate permission, expert supervision and consent.
- Collect ethically approved, consented data before training/evaluating an ML model.
- Add timed recordings and reliable pause/fluency extraction.
- Evaluate multilingual OCR and speech recognition separately for English, Tamil and Hindi.
- Add authentication, authorization, encryption, retention controls and accessibility testing before deployment.
- Add automated tests and report metrics on a held-out dataset.
