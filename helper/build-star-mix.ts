import { writeFileSync } from "fs";
import path from "path";
import { write } from '@thestarweb/trove-lang-tool';
import { mapDir, readTxtFile } from "./common";
import config from "./common/config";

(async () => {
    const LANG_DIR = "lang-txt/mix-star";
    const BASE_DIR = "./lang-txt/en-base";
    mapDir(BASE_DIR,(filename) => {
        const baseEN = readTxtFile(path.join(BASE_DIR, filename));
        const mixMap = new Map();
        const cnMap = new Map();
        readTxtFile(path.join(LANG_DIR, filename)).forEach(item => mixMap.set(item.key,item.value));
        readTxtFile(path.join('./lang-txt/cn-liulianf', filename)).forEach(item => cnMap.set(item.key,item.value));
        const newData = baseEN.map((item) => {
            if(mixMap.get(item.key)){
                return {key: item.key, value: mixMap.get(item.key)};
            }
            if(item.value === cnMap.get(item.key) || !cnMap.has(item.key)) return item;
            const n = (cnMap.get(item.key).indexOf("\\n") != -1 || item.value.indexOf("\\n") != -1 || cnMap.get(item.key).length > 100 || item.value.length > 150) ? "\n" : "";
            return {key: item.key, value: `${cnMap.get(item.key)}${n}(${item.value})`};
        }).map(({key, value}) => ({key, value: value.replace(/[\n\r]/g, "").replace(/\\n/g, "\n")}));
        if(newData.length > 0){
            writeFileSync(path.join(config.buildOutputDir,filename.substr(0,filename.lastIndexOf("."))+".binfab"),write(newData));
        }
    });
})();