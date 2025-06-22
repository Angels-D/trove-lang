import { writeFileSync } from "fs";
import path from "path";
import { write } from '@thestarweb/trove-lang-tool';
import { mapDir, readTxtFile } from "./common";
import config from "./common/config";

(async () => {
    const BASE_DIR = "lang-txt/cn-mix";
    mapDir(BASE_DIR,(filename) => {
        const base = readTxtFile(path.join(BASE_DIR, filename));
        const newData = base.map(({key, value}) => ({key, value: value.replace(/[\n\r]/g, "").replace(/\\n/g, "\n")}));
        if(newData.length > 0)
            writeFileSync(path.join(config.buildOutputDir,filename.slice(0,filename.lastIndexOf("."))+".binfab"),write(newData));
    });
})();