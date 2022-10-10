import json
from typing import List


class File:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_json_file(self) -> List[dict]:
        data = []
        try:
            with open(self.file_path) as json_file:
                print(f'=> Reading json file {self.file_path}')
                count = 0
                for row in json_file:
                    count += 1
                    if count % 100 == 0:
                        print(f'==> Reading line {count}')
                    data.append(json.loads(row))
        except Exception as err:
            print(f"error while reading json file: {err}")

        return data

    def read_and_exec_json_file(self, function) -> None:
        try:
            with open(self.file_path) as json_file:
                print(f'=> Reading json file {self.file_path}')
                count = 0
                for row in json_file:
                    count += 1
                    if count % 100 == 0:
                        print(f'==> Reading line {count}')

        except Exception as err:
            print(f"error while reading json file: {err}")
