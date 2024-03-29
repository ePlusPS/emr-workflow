from new_records_token_classification_infer import inference

def label_notes():
    in_file = open('new_records_all_note_lines.txt')
    lines = in_file.readlines()
    total_length = len(lines)
    for i in range(0, len(lines), 100000):
        end_index = i + 100000
        if end_index < total_length:
            sub_lines = lines[i:end_index]
        else:
            sub_lines = lines[i:total_length]
        inference(sub_lines)
        print(str(end_index/total_length*100)+"% lines labeled")

