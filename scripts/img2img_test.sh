#!/bin/bash
echo -n "enter prompt (e.g. two robots standing): "
while read PROMPT && [ -z "$PROMPT" ]; do echo -n "enter prompt (e.g. two robots standing): "; done
if [[ -n "$PROMPT" ]];
then
    curl -X POST http://127.0.0.1:3000/img2img -H 'Content-Type: multipart/form-data' -F img="@input.jpg" -F data="{\"prompt\":\"$PROMPT\"}" --output output.jpg
else
    echo "No input"
fi
