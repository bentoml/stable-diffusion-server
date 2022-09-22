#!/bin/bash
echo -n "enter prompt (e.g. a bento box): "
while read PROMPT && [ -z "$PROMPT" ]; do echo -n "enter prompt (e.g. a bento box): "; done
if [[ -n "$PROMPT" ]];
then
    curl -X POST http://127.0.0.1:3000/txt2img -H 'Content-Type: application/json' -d "{\"prompt\":\"$PROMPT\"}" --output output.jpg
else
    echo "No input"
fi
