import json
from pyvi import ViTokenizer

with open('E:\Sources\Kaggle\zalo ai\zalo-ai-text-summarization\data\\train.jsonl', 'r', encoding='utf-8') as json_file:
    json_list = list(json_file)

samples = []
for json_str in json_list:
    sample = json.loads(json_str)
    samples.append(sample)
print()


def extract_key(sample):
    paragraphs = []
    list_sentences = [body['text'] for body in sample['original_doc']['_source']['body']]
    match_sumamary = sample['match_summary']
    team1 = match_sumamary['players']['team1']
    team2 = match_sumamary['players']['team2']
    score_board = [match_sumamary['score_board']['score1'] + '-' + match_sumamary['score_board']['score2'],
                   match_sumamary['score_board']['score2'] + '-' + match_sumamary['score_board']['score1']]
    scores = []
    score_list = match_sumamary['score_list']

    for sent in list_sentences:
        if sent.find(team1) > -1 and sent.find(team2) > -1:
            qas = [{'question': 'team1',
                    'answers': [{'answer_start': sent.find(team1),
                                 'text': team1}]},
                   {'question': 'team2',
                    'answers': [{'answer_start': sent.find(team2),
                                 'text': team2}]}]
            paragraphs.append({'qas': qas,
                               'context': sent})
            break

    for sent in list_sentences:
        for score_board_ in score_board:
            if sent.find(score_board_) > -1:
                qas = [{'question': 'score board',
                        'answers': [{'answer_start': sent.find(score_board_),
                                     'text': score_board_}]}]
                paragraphs.append({'qas': qas,
                                   'context': sent})
                break
            break

    for score_list_ in score_list:
        for sent in list_sentences:
            time = score_list_['time']
            player_name = score_list_['player_name']
            if sent.find(time) > -1 and sent.find(player_name) > -1:
                qas = [{'question': 'time',
                            'answers': [{'answer_start': sent.find(time),
                                         'text': time}]},
                        {'question': 'player_name',
                            'answers': [{'answer_start': sent.find(player_name),
                                         'text': player_name}]}]
                paragraphs.append({'qas': qas,
                                   'context': sent})
                break
    return paragraphs


for sample in samples:
    qas = extract_key(sample)
    print()
