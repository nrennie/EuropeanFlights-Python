// Shinylive 0.0.7
// Copyright 2022 RStudio, PBC

// src/parse-codeblock.ts
function parseCodeBlock(codeblock, defaultFilename) {
  if (!Array.isArray(codeblock)) {
    codeblock = codeblock.split("\n");
  }
  const { lines, quartoArgs } = processQuartoArgs(codeblock);
  const files = parseFileContents(lines, defaultFilename);
  return { files, quartoArgs };
}
function processQuartoArgs(lines) {
  const outLines = [...lines];
  const quartoArgs = {};
  let searchingForArgs = true;
  while (searchingForArgs && outLines.length > 0) {
    const argsFromLine = outLines[0].match(
      /^#\|\s(?<prop>\w+):\s*(?<val>\w+)$/
    );
    if (argsFromLine) {
      outLines.splice(0, 1);
      const { prop, val } = argsFromLine.groups;
      if (!prop || !val) {
        console.warn(
          "Invalid format of layout args. Ignoring...",
          argsFromLine.groups
        );
      } else {
        quartoArgs[prop] = val;
      }
    } else {
      searchingForArgs = false;
      if (Object.keys(quartoArgs).length !== 0 && outLines.length >= 1 && outLines[0] === "") {
        outLines.splice(0, 1);
      }
    }
  }
  return {
    lines: outLines,
    quartoArgs
  };
}
function parseFileContents(lines, defaultFilename) {
  const files = [];
  let currentFile = {
    name: defaultFilename,
    content: "",
    type: "text"
  };
  let state = "START";
  for (const line of lines) {
    if (state === "START") {
      if (line.match(/^##\s?file:/)) {
        state = "HEADER";
        currentFile = {
          name: line.replace(/^##\s?file:/, "").trim(),
          content: "",
          type: "text"
        };
      } else if (line === "") {
      } else {
        state = "FILE_CONTENT";
        currentFile.content += line;
      }
    } else if (state === "HEADER") {
      if (line.match(/^##\s?file:/)) {
        state = "HEADER";
        files.push(currentFile);
        currentFile = {
          name: line.replace(/^##\s?file:/, "").trim(),
          content: "",
          type: "text"
        };
      } else if (line.match(/^##\s?type:/)) {
        const fileType = line.replace(/^##\s?type:/, "").trim();
        if (fileType === "text" || fileType === "binary") {
          currentFile.type = fileType;
        } else {
          console.warn(`Invalid type string: "${line}".`);
        }
      } else {
        state = "FILE_CONTENT";
        currentFile.content += line;
      }
    } else if (state === "FILE_CONTENT") {
      if (line.match(/^##\s?file:/)) {
        state = "HEADER";
        files.push(currentFile);
        currentFile = {
          name: line.replace(/^##\s?file:/, "").trim(),
          content: "",
          type: "text"
        };
      } else {
        currentFile.content += "\n" + line;
      }
    }
  }
  files.push(currentFile);
  return files;
}

// src/run-python-blocks.ts
import { runApp } from "./shinylive.js";
var classToAppTypeMappings = [
  { class: "pyshiny", appMode: "editor-viewer", defaultFilename: "app.py" },
  { class: "pyshinyapp", appMode: "viewer", defaultFilename: "app.py" },
  {
    class: "pyterminal",
    appMode: "editor-terminal",
    defaultFilename: "code.py"
  },
  { class: "pycell", appMode: "editor-cell", defaultFilename: "code.py" }
];
var allClassesSelector = classToAppTypeMappings.map((x) => "." + x.class).join(", ");
var blocks = document.querySelectorAll(allClassesSelector);
blocks.forEach((block) => {
  let mapping = null;
  for (const m of classToAppTypeMappings) {
    if (block.className.split(" ").includes(m.class)) {
      mapping = m;
      break;
    }
  }
  if (!mapping) {
    console.log("No mapping found for block ", block);
    return;
  }
  const container = document.createElement("div");
  container.className = "pyshiny-container";
  container.style.cssText = block.style.cssText;
  block.parentNode.replaceChild(container, block);
  const { files, quartoArgs } = parseCodeBlock(
    block.innerText,
    mapping.defaultFilename
  );
  const opts = { startFiles: files, ...quartoArgs };
  runApp(container, mapping.appMode, opts);
});
