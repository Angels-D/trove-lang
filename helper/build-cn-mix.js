"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = require("fs");
const path_1 = __importDefault(require("path"));
const trove_lang_tool_1 = require("@thestarweb/trove-lang-tool");
const common_1 = require("./common");
const config_1 = __importDefault(require("./common/config"));
(async () => {
    const BASE_DIR = "lang-txt/mix-cn";
    (0, common_1.mapDir)(BASE_DIR, (filename) => {
        const base = (0, common_1.readTxtFile)(path_1.default.join(BASE_DIR, filename));
        const newData = base.map(({ key, value }) => ({ key, value: value.replace(/[\n\r]/g, "").replace(/\\n/g, "\n") }));
        if (newData.length > 0) {
            (0, fs_1.writeFileSync)(path_1.default.join(config_1.default.buildOutputDir, filename.substr(0, filename.lastIndexOf(".")) + ".binfab"), (0, trove_lang_tool_1.write)(newData));
        }
    });
})();
