// Learn more https://docs.expo.io/guides/customizing-metro
const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// Fix for Node.js 24 compatibility issues with node:sea and other node: protocol imports
config.resolver.unstable_enablePackageExports = false;
config.resolver.unstable_conditionNames = ['require', 'import'];

// Block node: protocol imports that cause issues
config.resolver.blockList = [
    /node:sea/,
    /node:diagnostics_channel/,
    /node:async_hooks/,
];

// Provide empty implementations for problematic modules
config.resolver.extraNodeModules = {
    'node:sea': require.resolve('stream'),
    'node:diagnostics_channel': require.resolve('events'),
    'node:async_hooks': require.resolve('events'),
};

module.exports = config;
