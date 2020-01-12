from django.test import TestCase
import numpy as np


# Create your tests here.
def process_gov_dataset(name):
    dataset_file = open('static/files/' + name, "r", encoding='utf-8')
    _lines = dataset_file.read().split("\n")
    first_line = _lines[0].split(",")
    lines = list(map(lambda x: x.split(","), _lines[1:]))
    dataset_file.close()
    dataset_file = open('static/files/' + "gov.data", "w", encoding='utf-8')
    row, col = np.array(lines).shape
    new_lines = np.empty([row, col], dtype=int)
    for i in range(col):
        if i == 0:
            for j in range(row):
                new_lines[j][col - 1] = lines[j][i]
            continue
        count = []
        for j in range(row):
            if not lines[j][i] in count:
                count.append(lines[j][i])
            # print(count)
            # print(np.where(np.array(count) == lines[j][i])[0][0])
            new_lines[j][i - 1] = str(np.where(np.array(count) == lines[j][i])[0][0])
    #dataset_file.write(",".join(first_line[1:]) + "," + first_line[0] + ",\n")
    for line in new_lines:
        print(line)
        dataset_file.write(",".join(list(map(lambda x: str(x), line))) + "\n")
    dataset_file.flush()
    dataset_file.close()


if __name__ == "__main__":
    process_gov_dataset("gov.csv")
