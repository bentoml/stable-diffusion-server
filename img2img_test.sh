curl -X POST http://127.0.0.1:3000/img2img -H 'Content-Type: multipart/form-data' -F img="@input.jpg" -F data='{"prompt":"a black and white cat"}' --output output.jpg
