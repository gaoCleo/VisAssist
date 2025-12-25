Save the prediction results as a JSON file with the same name as the video filename. 
Example format:
```
{
    "filename": "00b3ad2b-8b14-1738323431306-ac2e.mp4", 
    "pred_answer": "根据图片，这个保温杯的颜色看起来是金属银色。从图片上看，没有明显的花纹，表面比较光滑和平整。", 
    "pred_answer_en": "The thermos is metallic in color and appears to have a smooth, plain surface without any visible patterns or designs on it."
}
```

After modifying the api-key in `llm.py` to your own key, run the file. 
Each evaluation result will be saved as a single json file, with the filename matching the video filename. Example of saving:
```
{
    "cor": "0",
    "do": "0",
    "su": "0"
}
```