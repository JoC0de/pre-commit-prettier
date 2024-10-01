#!/usr/bin/env node

"use strict";

import { run as runPrettier } from "prettier/internal/cli.mjs";
import { createRequire } from "module";

const require = createRequire(import.meta.url);

// Helper function to resolve the plugin path using require.resolve
function resolvePlugin(pluginName) {
  try {
    // Use Node's standard module resolution to resolve the plugin path
    return require.resolve(pluginName);
  } catch (error) {
    console.error(`Could not resolve plugin: ${pluginName} ${error}`);
    return null;
  }
}

// Check for plugins passed through command line arguments
let plugins = [];
for (let argumentIndex = process.argv.length - 1; argumentIndex >= 0; argumentIndex--) {
  const argument = process.argv[argumentIndex];
  if (!argument.startsWith("--plugin=")) {
    continue;
  }

  const pluginName = argument.slice("--plugin=".length);
  const pluginPath = resolvePlugin(pluginName);

  if (pluginPath) {
    // Remove the plugin argument from process.argv
    process.argv.splice(argumentIndex, 1);
    plugins.push(pluginPath);
  }
}

// Use the resolved plugin paths directly without trying to open package.json
const additionalArguments = plugins.flatMap((pluginPath) => {
  return ["--plugin", pluginPath];
});

// Insert additional arguments into process.argv (after node and script paths)
process.argv.splice(2, 0, ...additionalArguments);

// Override stdout.write to filter messages that end with "(unchanged)"
const originalWrite = process.stdout.write;
process.stdout.write = function (message, ...optionalParams) {
  if (typeof message === "string" && message.includes(" (unchanged)")) {
    return;
  }

  originalWrite.apply(process.stdout, [message, ...optionalParams]);
};

runPrettier();
