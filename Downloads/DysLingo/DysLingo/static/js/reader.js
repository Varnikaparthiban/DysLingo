(() => {
  const $ = (id) => document.getElementById(id);
  function updatePreview() {
    const source = $('sourceText'), preview = $('readingPreview');
    if (!source || !preview) return;
    preview.textContent = source.value || "Your reading passage will appear here.";
  }
  document.addEventListener('DOMContentLoaded', () => {
    const source = $('sourceText'), preview = $('readingPreview');
    if (source && preview) {
      source.addEventListener('input', updatePreview);
      $('fontSize')?.addEventListener('input', e => preview.style.fontSize = `${e.target.value}px`);
      $('letterSpacing')?.addEventListener('input', e => preview.style.letterSpacing = `${e.target.value}px`);
      $('lineSpacing')?.addEventListener('input', e => preview.style.lineHeight = e.target.value);
      $('speakBtn')?.addEventListener('click', () => {
        if (!('speechSynthesis' in window)) { alert('Text-to-speech is not supported in this browser.'); return; }
        const text = source.value.trim();
        if (!text) { alert('Paste or load a passage first.'); return; }
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = $('readerLanguage')?.value || 'en-US';
        utterance.rate = 0.85;
        window.speechSynthesis.speak(utterance);
      });
      $('stopBtn')?.addEventListener('click', () => window.speechSynthesis?.cancel());
    }
    const listen = $('listenPractice'), target = $('targetText'), lang = $('language');
    listen?.addEventListener('click', () => {
      if (!('speechSynthesis' in window)) { alert('Text-to-speech is not supported in this browser.'); return; }
      if (!target.value.trim()) { alert('Enter a passage first.'); return; }
      speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(target.value);
      u.lang = lang.value; u.rate = .85; speechSynthesis.speak(u);
    });
    let recognition = null;
    const start = $('startRecognition'), stop = $('stopRecognition'), status = $('speechStatus');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (start && !SpeechRecognition) {
      start.disabled = true;
      if (status) status.textContent = 'Speech recognition is not supported in this browser. Enter the transcript manually or try a compatible browser.';
    }
    start?.addEventListener('click', () => {
      if (!SpeechRecognition) return;
      recognition = new SpeechRecognition();
      recognition.lang = lang.value; recognition.continuous = true; recognition.interimResults = true;
      recognition.onresult = event => {
        let transcript = '';
        for (let i = 0; i < event.results.length; i++) transcript += event.results[i][0].transcript + ' ';
        $('spokenText').value = transcript.trim();
      };
      recognition.onerror = event => { if (status) status.textContent = `Speech recognition message: ${event.error}. You can type the transcript manually.`; };
      recognition.onend = () => { if (status) status.textContent = 'Speech recognition stopped. Review the transcript before analyzing.'; };
      recognition.start();
      if (status) status.textContent = 'Listening… Read the passage clearly. Browser microphone permission may be requested.';
    });
    stop?.addEventListener('click', () => { recognition?.stop(); if (status) status.textContent = 'Microphone stopped.'; });
    lang?.addEventListener('change', () => { if (recognition) recognition.lang = lang.value; });
  });
})();
