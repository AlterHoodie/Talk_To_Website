import { Config } from "./src/config";

export const defaultConfig: Config = {
  url: "https://pes.edu/",
  match: "https://pes.edu/**",
  maxPagesToCrawl: 5,
  selector:"",
  outputFileName: "../data/output1.json",
  maxTokens: 2000000,
};
