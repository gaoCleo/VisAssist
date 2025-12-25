# VisAssist: A Visually Impaired-Captured Video Question Answering Benchmark
![VisAssist Logo](pics/logo.png)

## Project Overview
VisAssist is the first large-scale video question answering (Video QA) dataset consisting of real-world videos captured by visually impaired users. It addresses a critical gap in assistive vision research by providing authentic first-person perspective data that reflects the unique challenges of blind photography—including unconventional framing, motion artifacts, and frequent information omission.

An example in the dataset:
![example.png](pics%2Fexample.png)

## Key Features
### 1. Authentic First-Person Perspective Data
- All videos are recorded by visually impaired volunteers (including individuals who meet legal blindness criteria), using screen readers to operate mobile devices.
- Each video has a resolution of 448×448 pixels and a duration of 4–15 seconds (average: 10.26 seconds).
- Covers core visual needs of visually impaired users, such as object search, navigation, and text reading, across both indoor and outdoor scenarios.

### 2. Comprehensive Annotation System
Each video includes the following structured annotations:
- Bilingual (Chinese-English) open-ended QA pairs.
- Multi-label tags for required visual information (8 categories: color, text, object, icon, depth, human, environment, direction).
- Indicator of answer completeness (whether the video contains sufficient information to answer the question).
- Shooting adjustment suggestions (e.g., "Adjust the angle to shoot the back of the packaging bag").
- Categorization of adjustment suggestions (e.g., stabilize camera, adjust angle).

### 3. Benchmark-Specific Challenges
The dataset inherently incorporates three core challenges tailored to assistive system requirements:
- High variance in frame utility (single-frame answerable vs. multi-frame dependent questions).
- Extreme diversity in video quality (motion blur, low light, glare, etc.).
- Contextual understanding of text and space (prioritizing relationships between elements over simple object detection).

## Dataset Statistics
| Metric | Value |
|--------|-------|
| Total Videos | 13,413 |
| Total Duration | 137,554.64 seconds (~38.2 hours) |
| Average Video Duration | 10.26 seconds |
| Average Frames per Video | 407.5 |
| Percentage of Videos with Shooting Adjustments | 17.25% |
| Percentage of Videos with Visible Answers | 90% |

## Dataset Structure
```
VisAssist/
├── video/
│   ├── video_xxx.mp4     # Video file
│   ├── video_yyy.mp4     # Video file
│   └── ...
├── train.json            # Training set (8,037 videos)
└── test.json             # Test set (5,376 videos)
```

### Annotation File Example
In the “answer” and “instruction” fields, there are annotations from multiple people. If the information contained in the video captured by the visually impaired person is sufficient to answer the question and there is no instruction, an empty string will be filled in the list of this field to align the length of the instruction list with that of the answer list.
```json
{
  "taskID": 10416, 
  "videoID": 10749, 
  "filename": "2210c599-0fb1-1737802591466-96a3.mp4", 
  "question": "这个空调的开关在哪里？我手指要怎么移动才能按到它？", 
  "answer": [
    "光线比较暗，而且距离稍远，看不太清楚。能看到您摸着的这一块区域上面约一个手掌的长度是按钮的位置。", 
    "视频中的字难以辨认。"
  ], 
  "has_answer": "2", 
  "visual_inform_type": "3", 
  "instruction": [
    "请稍微改善灯光环境，并且把镜头往右边移动一点点，并且近一点重新拍摄", 
    "请提供充足光线。"
  ], 
  "instruct_type": "1,2,3", 
  "question_en": "Where is the switch for this air conditioner? How should I move my fingers to press it?", 
  "answer_en": [
    "The light is relatively dim and the distance is a bit far, making it hard to see clearly. You can roughly make out where the buttons are about a palm's length away from the area you are touching.", 
    "The text in the video is difficult to recognize."
  ], 
  "instruction_en": [
    "Please slightly improve the lighting environment, move the lens a bit to the right, and re-capture it a bit closer.", 
    "Please provide adequate lighting."
  ]
}
```

Types of Visual Information Required to Answer Questions

| INDEX | LABEL |
| ---- | ---- |
| 1 | Color |
| 2 | Text |
| 3 | Objects (including object categories, states, features, etc.) |
| 4 | Images, icons, charts |
| 5 | Depth, distance, size |
| 6 | People (actions, states, etc.) |
| 7 | Overall environmental information |
| 8 | Position and orientation |
| 9 | Other |

Types of Labels Indicating Whether the Video Contains the Answer

| INDEX | LABEL |
| ---- | ---- |
| 1 | Answer is visible in the frame |
| 2 | Blurriness primarily due to motion or camera shake |
| 3 | Reflection obscuring the answer area |
| 4 | Partial information loss (e.g., target out of frame, unrecorded angles) |
| 5 | Too far away |
| 6 | Too close |
| 7 | Occlusion |
| 8 | Other |

Types of Shooting Adjustment Recommendations

| INDEX | LABEL |
| ---- | ---- |
| 0 | No shooting recommendation |
| 1 | Shoot farther/closer |
| 2 | Shoot a little up/down/left/right |
| 3 | Stabilized camera |
| 4 | Adjust the shooting Angle | 

## Dataset Download
[Hugging face](https://huggingface.co/datasets/gaoCleo/VisAssist)

## Benchmark Results
We evaluated the performance of state-of-the-art (SOTA) multimodal large language models (MLLMs) on VisAssist, with key findings including:
1. All models perform best on color recognition tasks but exhibit significant deficiencies in spatial reasoning (e.g., depth estimation, directional queries).
2. Open-source models generally struggle with text understanding in blurry scenarios, especially for non-Latin scripts.
3. Strong vision models (e.g., Gemini-Pro) can maintain high accuracy while reducing computational costs through keyframe selection strategies.

### Metrics
The evaluation metrics used are COR (Correctness of Information), DO (Detail Orientation), and SU (Spatial Understanding). The assessment was conducted using an LLM (DeepSeek), with the code in `evaluation/llm.py`.

### Zero-Shot Performance
| Model               | Color | Text | Object | Icon | Depth | Human | Env  | Direction | COR  | DO   | SU   | Avg  |
|---------------------|-------|------|--------|------|-------|-------|------|-----------|------|------|------|------|
| TimeChat            | 1.11  | 0.93 | 1.06   | 1.09 | 1.08  | 1.24  | 1.28 | 0.97      | 1.21 | 0.99 | 0.93 | 1.04 |
| VideoChat2(vicuna)  | 1.73  | 1.02 | 1.34   | 1.32 | 1.26  | 1.79  | 1.53 | 1.22      | 1.34 | 1.24 | 1.27 | 1.28 |
| VideoChat2(mistral) | 1.79  | 0.93 | 1.22   | 1.27 | 0.82  | 1.29  | 1.14 | 1.00      | 1.27 | 1.07 | 1.15 | 1.16 |
| VideoChatGPT        | 1.46  | 0.94 | 1.18   | 1.15 | 1.25  | 1.35  | 1.23 | 1.17      | 1.21 | 1.07 | 1.11 | 1.13 |
| VideoLLaMA2         | 2.11  | 1.47 | 1.72   | 1.74 | 1.36  | 1.52  | 1.68 | 1.56      | 1.87 | 1.55 | 1.59 | 1.67 |
| Qwen-2-VL(OCR)      | 2.55  | 2.15 | 2.18   | 2.22 | 1.77  | 2.26  | 2.03 | 1.93      | 2.31 | 2.07 | 2.18 | 2.19 |
| Qwen-2.5-VL         | 2.58  | 2.36 | 2.37   | 2.44 | 1.88  | 2.05  | 2.20 | 2.00      | 2.54 | 2.29 | 2.29 | 2.37 |
| Gemini-flash        | 3.13  | 2.88 | 2.85   | 2.96 | 2.18  | 2.68  | 2.74 | 2.42      | 3.04 | 2.73 | 2.80 | 2.86 |
| Gemini-pro          | 3.45  | 3.37 | 3.29   | 3.35 | 2.54  | 3.23  | 3.13 | 2.88      | 3.47 | 3.14 | 3.30 | 3.30 |
| ChatGPT-4o          | 3.13  | 2.54 | 2.81   | 2.85 | 2.61  | 3.04  | 2.78 | 2.46      | 2.93 | 2.68 | 2.67 | 2.76 |

The scores for each category (e.g., color) and the "Avg" column at the end are all the mean values of the three scores: COR, DO, and SU. For full experimental results, refer to Tables 2–6 in the original paper.

An example of predictions in the dataset (Score is the average score of COR, DO, and SU):
![predictions.png](pics%2Fpredictions.png)

## Citation
If you use this dataset in your research, please cite:
```bibtex

```
