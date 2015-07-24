# parlare
language learning app

Given a csv file with the Google language codes for headers (ie "en, it" for english and italian)
and rows with two words/phrases apiece (ie first word is the english word and the second is the italian translation)

makeWordDoubles 
  1.  uses the Google Text To Speech API to make audio files of each word with its translation
  2.  Combines these word+translation audios with an image of the text into a video
MakeMediaFile 
  1.  Combines many of these word doubles in random order into a video or audio file
