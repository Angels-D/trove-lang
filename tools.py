import os, re
from translate import Translator

BASE_EN = 'lang-txt\en-base'
BASE_CN = 'lang-txt\cn-base'
BASE_LLF = 'lang-txt\cn-liulianf'
USE_CN = 'lang-txt\cn'
MIX_CN = 'lang-txt\mix-cn'

GO_Translate = True
GO_UseBase = True

SHOW_USEBASE = False
SHOW_TRANSLATE = True

SKIP = []

files = os.listdir(BASE_EN)

usebase_log = {}
translate_log = {}

def translate(value: str):
    if not value or not GO_Translate:
        return value
    translate_log[file].append(key)
    if SHOW_TRANSLATE:
        print(f'[Translate] {os.path.join(MIX_CN, file)} {index}: {key}')
    data_cn[key]= r'\n'.join(re.sub(r'(<font.*>)?(.+)(</font>)?', lambda x: 
                             f'{x.group(1) or ""}{Translator(to_lang="zh").translate(x.group(2))}({x.group(2)}){x.group(3) or ""}' if key.endswith('name') else 
                             f'{x.group(1) or ""}{Translator(to_lang="zh").translate(x.group(2))}\\n<font color="#cccccc">{x.group(2)}</font>{x.group(3) or ""}', i) 
                             for i in value.split(r'\n'))
    return data_cn[key]

def base(value: str):
    if not value or not GO_UseBase:
        return None
    usebase_log[file].append(key)
    if SHOW_USEBASE:
        print(f'[UseBase] {os.path.join(MIX_CN, file)} {index}: {key}')
    data_cn[key] = value
    return data_cn[key]

for file in files:
    try:
        if file in SKIP:
            continue

        usebase_log[file] = []
        translate_log[file] = []
        
        en = open(os.path.join(BASE_EN, file), 'r', encoding='utf-8').readlines()
        
        cn_base = open(os.path.join(BASE_CN, file), 'r', encoding='utf-8').readlines() if os.path.exists(os.path.join(BASE_CN, file)) else []
        cn_llf = open(os.path.join(BASE_LLF, file), 'r', encoding='utf-8').readlines() if os.path.exists(os.path.join(BASE_LLF, file)) else []
        cn = open(os.path.join(USE_CN, file), 'r', encoding='utf-8').readlines() if os.path.exists(os.path.join(USE_CN, file)) else []

        data_en,data_cn_base,data_cn_llf,data_cn  = [{},{},{},{}]

        cn_mix = open(os.path.join(MIX_CN, file), 'w', encoding='utf-8')
        
        for line in en:
            key,value = line.split('»')
            data_en[key] = value.rstrip('\n')
        for line in cn_base:
            key,value = line.split('»')
            data_cn_base[key] = value.rstrip('\n')
        for line in cn_llf:
            key,value = line.split('»')
            data_cn_llf[key] = value.rstrip('\n')
        for line in cn:
            key,value = line.split('»')
            data_cn[key] = value.rstrip('\n')
        
        index = 0
        for key in data_en:
            index += 1
            value = data_cn.get(key) \
                or data_cn_llf.get(key) \
                or base(data_cn_base.get(key)) \
                or translate(data_en.get(key))
            
            cn_mix.write(f'{key}»{value}\n')

    except Exception as e:
        print('Error: ',e)

    finally:
        if data_cn:
            cn_new = open(os.path.join(USE_CN, file), 'w', encoding='utf-8')
            for key,value in data_cn.items():
                cn_new.write(f'{key}»{value}\n')


print(f'''
Total UseBase: {sum([len(value) for value in usebase_log.values()])}
Total Translate: {sum([len(value) for value in translate_log.values()])}''')