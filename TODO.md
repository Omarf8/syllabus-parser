# Items to Revisit

## Error Handling
* Gemini returning a 503 or other server error
* JSON parsing failing if Gemini returns unexpected output
* Scanned PDFs (non-extractable text)
* User uploading non-PDF files

## Async
* Currently, Gemini blocks execution until it finishes responding so we might need a way to do it async

## Concerns
* What will happen if a very large PDF is uploaded?
* What if there are no dates to extract?