import json
import os
import re

from openai import OpenAI
from tqdm import tqdm

API_KEY = 'your-key'


def correctness_of_information(question, answer, pred):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content":
                    "You are a chatbot for evaluating factual accuracy in video-based Q&A. Compare the predicted answer with correct answers to ensure consistency. Instructions:"
                    "- Ensure the predicted answer is factually accurate and aligns with the video.\n"
                    "- Allow synonyms or paraphrases.\n"
                    "- Check for misinterpretations or misinformation."
            },
            {
                "role": "user",
                "content":
                    f"Evaluate this video-based QA pair:\n"
                    f"Question: {question}\n"
                    "Correct Answers:\n"
                        + "\n".join([f"{i+1}. {ans}" for i, ans in enumerate(answer)]) + "\n"
                    f"Predicted Answer: {pred}\n"
                    "Provide ONLY an integer score (0-5) for factual accuracy."
            }
        ],
        stream=False
    )

    return response.choices[0].message.content


def detail_orientation(question, answer, pred):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content":
                    "You are a chatbot for evaluating detail orientation in video-based Q&A. Compare the predicted answer with the correct answer to assess completeness and specificity. Instructions:"
                    "- Ensure the predicted answer covers all key points from the video.\n"
                    "- Check for specific details tied to the video content.\n"
                    "- Allow synonyms or paraphrases.\n"
                    "- Provide a single score reflecting detail orientation."
            },
            {
                "role": "user",
                "content":
                    f"Evaluate this video-based QA pair:\n"
                    f"Question: {question}\n"
                    "Correct Answers:\n"
                        + "\n".join([f"{i+1}. {ans}" for i, ans in enumerate(answer)]) + "\n"
                    f"Predicted Answer: {pred}\n"
                    "Provide ONLY an integer score (0-5) for factual accuracy."
            }
        ],
        stream=False
    )

    return response.choices[0].message.content


def spatial_understanding(question, answer, pred):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content":
                    "You are a chatbot for evaluating spatial understanding in video-based Q&A. Compare the predicted answer with the correct answer to ensure it accurately reflects spatial relationships or locations in the video. Instructions:"
                    "- Focus on whether the predicted answer correctly describes spatial elements (e.g., positions, directions, or layouts) in the video.\n"
                    "- Allow synonyms or paraphrases, but ensure spatial accuracy is maintained.\n"
                    "- Evaluate the spatial consistency of the prediction compared to the answer."
            },
            {
                "role": "user",
                "content":
                    f"Evaluate this video-based QA pair:\n"
                    f"Question: {question}\n"
                    "Correct Answers:\n"
                        + "\n".join([f"{i+1}. {ans}" for i, ans in enumerate(answer)]) + "\n"
                    f"Predicted Answer: {pred}\n"
                    "Provide ONLY an integer score (0-5) for factual accuracy."
            }
        ],
        stream=False
    )

    return response.choices[0].message.content


def contains_chinese(text):
    # Use regular expressions to match Chinese characters.
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(text))


if __name__ == '__main__':
    annotation_path = ''  # The path to the ground truth annotation file
    pred_res_dir = ''  # Folder for storing prediction results

    save_dir_zh = ''  # Folder for saving evaluation scores of Chinese prediction results
    save_dir_en = ''  # Folder for saving evaluation scores of English prediction results;
    if not os.path.exists(save_dir_zh):
        os.makedirs(save_dir_zh)
    if not os.path.exists(save_dir_en):
        os.makedirs(save_dir_en)

    with open(annotation_path, 'r', encoding='utf-8') as f:
        test_datas = json.load(f)

    for data in tqdm(test_datas):
        filename = data['filename']
        question = data['question']

        gt_answer = data['answer']
        gt_answer_en = data['answer_en']

        pred_path = os.path.join(pred_res_dir, filename.split('.')[0] + '.json')
        with open(pred_path, 'r', encoding='utf-8') as f:
            pred = json.load(f)

        pred_answer = pred['pred_answer']
        pred_answer_en = pred['pred_answer_en']

        if not os.path.exists(os.path.join(save_dir_zh, filename.split('.')[0] + '.json')):
            cor = correctness_of_information(question, gt_answer, pred_answer)
            do = detail_orientation(question, gt_answer, pred_answer)
            su = spatial_understanding(question, gt_answer, pred_answer)

            with open(os.path.join(save_dir_zh, filename.split('.')[0] + '.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'cor': cor,
                    'do': do,
                    'su': su
                }, f, ensure_ascii=False, indent=4)

        if not os.path.exists(os.path.join(save_dir_en, filename.split('.')[0] + '.json')):
            # If the output is purely in English, replace the ground truth with the English ground truth.
            if pred_answer is None:
                cor_en = 0
                do_en = 0
                su_en = 0
            else:
                if not contains_chinese(pred_answer):
                    gt_answer = gt_answer_en

                cor_en = correctness_of_information(question, gt_answer_en, pred_answer_en)
                do_en = detail_orientation(question, gt_answer_en, pred_answer_en)
                su_en = spatial_understanding(question, gt_answer_en, pred_answer_en)

            with open(os.path.join(save_dir_en, filename.split('.')[0] + '.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'cor': cor_en,
                    'do': do_en,
                    'su': su_en
                }, f, ensure_ascii=False, indent=4)
