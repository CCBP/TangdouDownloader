import json
import os

def get_vid_set(json_dir):
    vid_set = set()
    for json_file in os.listdir(json_dir):
        print(json_file)
        if json_file.endswith(".json"):
            with open(os.path.join(json_dir, json_file), encoding="utf-8") as f:
                content = json.load(f)
                datas = content["datas"]
                if json_file == "download.json":
                    for item in datas:
                        vid_set.add(int(item))
                else:
                    for item in datas:
                        vid_set.add(item["vid"])
    return vid_set


if __name__ == "__main__":
    vid_set = get_vid_set()
    print(vid_set)
    print(len(vid_set))
