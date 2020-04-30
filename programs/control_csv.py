import csv

# 配列の要素を１行ずつ（漫画ごとに）CSVファイルへ書き込む
def output_csv(path, output_array):
    # wで開くと上書きモードになり、元の内容は削除される
    with open(path, 'w', newline='', encoding='utf_8') as file:
        writer = csv.writer(file)
        for i in output_array:
            writer.writerow(i)

def input_csv(path):
    with open(path, 'r', encoding='utf_8', errors='', newline='') as file:
        f = csv.reader(file, delimiter=",", doublequote=True)
        list = [n for n in f]
        # print(list)
    return list
