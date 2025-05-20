from random import sample as random_sample
import os
import re
import yaml


def get_filters(greenlist):
    return [re.compile(check) for check in greenlist]


def all_files(location):
    for pwd, _, files in os.walk(location):
        for file in files:
            yield os.path.join(pwd, file)


def get_samples(config):
    samples = {}
    for k, v in config.items():
        files = set()
        greenlist = get_filters(v["greenlist"])
        extractor = re.compile(v["extractor"])
        for location in v["locations"]:
            for file in all_files(location):
                if any(check.match(file) for check in greenlist):
                    if match := extractor.match(file):
                        files.add(match.groupdict()["Recipe"])
        if len(files) > int(v["samples"]):
            samples[k] = random_sample(list(files), int(v["samples"]))
        elif len(files) > 0:
            samples[k] = list(files)
            samples[k] = [" ** Fewer recipes than requested samples **"] + samples[k]
        else:
            samples[k] = [" ** No recipes match Greenlist **"]
    return samples


def main():
    with open("config.yaml") as in_file:
        config = yaml.load(in_file, yaml.Loader)
    samples = get_samples(config)
    for category, samplelist in samples.items():
        print(category)
        for sample in samplelist:
            if "**" in sample:
                print(sample)
            else:
                print(f"  - {sample}")
        print()


if __name__ == "__main__":
    main()
