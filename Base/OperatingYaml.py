import yaml,os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
def readyaml(path):
    try:
        with open(path,  encoding='utf-8') as f:
            yamlstr = yaml.load(f)
            return yamlstr
    except FileNotFoundError:
        print('yaml 文件不存在')

