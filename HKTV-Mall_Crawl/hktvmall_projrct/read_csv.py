import csv


def read_urls_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader]
    return urls
