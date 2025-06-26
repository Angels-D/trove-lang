import os
import re
from translate import Translator


class Language():
    SKIP_FILE = []
    SKIP_TEXT = []

    CN_MIX = {}

    CN_MIX_PATH = 'lang-txt/cn-mix'
    EN_BASE_PATH = 'lang-txt/en-base'
    CN_TRANSLATE_PATH = 'lang-txt/cn-translate'
    CN_BASE_PATH = 'lang-txt/cn-base'
    CN_LLF_PATH = 'lang-txt/cn-liulianf'
    CN_PATH = 'lang-txt/cn'

    SHOW_UPDATE = True
    UPDATE_TRANSLATE = True

    def __init__(self, path: str, showLog=False):
        self.path = path
        self.files = os.listdir(self.path)
        self.fileWriter = {}
        self.data = {file: self.Read(file) for file in self.files}
        self.use = 0
        self.update = 0
        self.showLog = showLog

    def Read(self, fileName: str):
        data = {}
        CN_MIX_DATA: dict = self.CN_MIX.setdefault(fileName, {})
        if os.path.exists(os.path.join(self.path, fileName)):
            with open(os.path.join(self.path, fileName), 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    key, value = line.split('»')
                    data[key] = value.rstrip('\n')
                    CN_MIX_DATA.setdefault(key, '')
        return data

    def Write(self, fileName, key, value):
        if not fileName in self.fileWriter:
            self.fileWriter[fileName] = open(
                os.path.join(self.path, file), 'wb', buffering=0)
        self.fileWriter[fileName].write(f'{key}»{value}\n'.encode('utf-8'))
        return self.fileWriter[fileName]

    def Use(self, fileName, key, value=None):
        self.use += 1
        file = self.data.setdefault(fileName, {})
        update = False
        if value:
            update = True
            self.update += 1
            file[key] = value
        else:
            value = file.get(key, '')
        try:
            index = list(file.keys()).index(key)
        except Exception:
            index = -1
        if (self.showLog or (self.SHOW_UPDATE and update)):
            print(
                f'{'↑' if update else '+'} {os.path.join(self.path, fileName)} {index}: {key}')
        self.CN_MIX.setdefault(fileName, {})[key] = value
        return value

    @classmethod
    def Translate(cls, file: str, key: str, value: str):
        def t(value: re.Match[str]):
            result = Translator(to_lang="zh").translate(value.group(2))
            if "MYMEMORY WARNING" in result:
                raise Exception(result)
            if (result == value.group(2)):
                return value.group(0)
            elif key.endswith('_description') and not key.endswith('_pack_description') and "welcome.txt" not in file:
                return f'{value.group(1) or ""}{result}\\n<font color="#cccccc">{value.group(2)}</font>{value.group(3) or ""}'
            else:
                return f'{value.group(1) or ""}{result}({value.group(2)}){value.group(3) or ""}'
        return re.sub(r'\[\s*[Hh]\s*[Kk]\s*:\s*([A-Za-z0-9\s]*)\]',
                      lambda value: f"[HK:{re.sub(r'\s+', '', value.group(1)).capitalize()}]",
                      re.sub(r'\s+(?=[《》！？；（）【】，。、])|(?<=[《》！？；（）【】，。、])\s+', '',
                             r'\n'.join(re.sub(r'(<font.*>)?(.+)(</font>)?', t, i)
                                        for i in value.split(r'\n'))))


EN_BASE = Language(Language.EN_BASE_PATH)
CN_TRANSLATE = Language(Language.CN_TRANSLATE_PATH)
CN_BASE = Language(Language.CN_BASE_PATH)
CN_LLF = Language(Language.CN_LLF_PATH)
CN = Language(Language.CN_PATH)

for file in Language.CN_MIX:
    # try:
    EN_BASE_FILE = EN_BASE.data.get(file, {})
    CN_TRANSLATE_FILE = CN_TRANSLATE.data.get(file, {})
    CN_BASE_FILE = CN_BASE.data.get(file, {})
    CN_LLF_FILE = CN_LLF.data.get(file, {})
    CN_FILE = CN.data.get(file, {})

    with open(os.path.join(Language.CN_MIX_PATH, file), 'wb', buffering=0) as CN_MIX:
        for key in Language.CN_MIX.get(file):
            value = EN_BASE_FILE.get(key, '')
            if key in CN_FILE:
                value = CN.Use(file, key)
            elif key in CN_LLF_FILE:
                value = CN_LLF.Use(file, key)
            elif key in CN_BASE_FILE:
                value = CN_BASE.Use(file, key)
            elif key in CN_TRANSLATE_FILE:
                value = CN_TRANSLATE.Use(file, key)
                CN_TRANSLATE.Write(file, key, value)
            elif Language.UPDATE_TRANSLATE:
                value = CN_TRANSLATE.Use(
                    file, key, Language.Translate(file, key, value))
                CN_TRANSLATE.Write(file, key, value)
            CN_MIX.write(f'{key}»{value}\n'.encode('utf-8'))

    # except Exception as e:
    #     print(f'''Error {e.__traceback__.tb_frame.f_globals["__file__"]} {e.__traceback__.tb_lineno}:
    # {e}''')

print(f'''
Total: {CN.use + CN_LLF.use + CN_BASE.use +
        CN_TRANSLATE.use}(↑{CN.update + CN_LLF.update + CN_BASE.update + CN_TRANSLATE.update})
  -> CN: {CN.use}(↑{CN.update})
  -> CN_LLF: {CN_LLF.use}(↑{CN_LLF.update})
  -> CN_BASE: {CN_BASE.use}(↑{CN_BASE.update})
  -> CN_TRANSLATE: {CN_TRANSLATE.use}(↑{CN_TRANSLATE.update})''')
