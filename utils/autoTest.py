from subprocess import run, PIPE
import re
import json

def do_test(index:str, script_file: str, sample_file: str):
    with open(sample_file, "r") as file:
        sample_data = json.load(file)
    test_sample = sample_data[index]
    outputs = []
    for sample in test_sample:
        p = run(["python", script_file], input=sample["input"],
                stdout=PIPE, encoding='utf-8')
        sample["user_output"] = p.stdout
        sample["pass"] = p.stdout == sample["output"]
        outputs.append(sample)
    return outputs

def html_to_sample(index:str, data: str, file_path: str):
    result = re.findall(
        r"((?:sample )?input.*):?\n((?:.|\n[^\n])+)\n{2,}" +
        r"(?:sample )?output.*\n((?:.|\n[^\n])+)\n{2,}",
        data,
        flags=re.I)
    with open(file_path, 'w+') as file:
        try:
            sample_data = json.load(file)
        except json.decoder.JSONDecodeError:
            sample_data = dict()
        test_sample = []
        for x in result:
            name, _input, output = x
            test = {
                "name": name,
                "input": _input+'\n',
                "output": output+'\n',
            }
            test_sample.append(test)
        sample_data[index] = test_sample
        file.writelines(json.dumps(sample_data, indent=4))


def test():
    with open('050q.txt', 'r') as file:
        html_text = ''.join(file.readlines())
    #get
    html_to_sample('050', html_text, 'test_sample.json')
    result = do_test("050", './050-meeting.py', 'test_sample.json')
    print(result)
