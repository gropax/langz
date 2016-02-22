#!/bin/bash

anki="$1.anki"
media="$1.media"

# Generate flashcards
cmn-anki $1 -f "s@" -o $anki

# Ask for validation
vim $anki

# Record sound files
qrec $anki -an -o $media

for wav in `ls $1.media`
do
  wav="$media/$wav"
  mp3="${wav/wav/mp3}"
  lame -V6 $wav $mp3 >/dev/null 2>&1    

  rm $wav
done
