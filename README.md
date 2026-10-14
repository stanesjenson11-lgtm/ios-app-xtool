# xtool

Cross-platform Xcode replacement. Build and deploy iOS apps with SwiftPM on Linux, Windows, and macOS.

## Overview

xtool is a cross-platform (Linux/WSL/macOS) tool that replicates Xcode functionality with open standards.

✅ Build a SwiftPM package into an iOS app

✅ Sign and install iOS apps

✅ Interact with Apple Developer Services programmatically

## Getting Started

1. Follow the guide to install `xtool`
    - [Installation (Linux/Windows)](https://xtool.sh/documentation/xtooldocs/installation-linux)
    - [Installation (macOS)](https://xtool.sh/documentation/xtooldocs/installation-macos)
2. Create and run your first xtool-powered app by following the [tutorial](https://xtool.sh/tutorials/xtooldocs/first-app)!

## Examples

### Screenshot

![A screenshot of xtool being invoked from VSCode](Documentation/xtool.docc/Resources/Cover.png)

### Command line interface

```bash
$ xtool --help
OVERVIEW: Cross-platform Xcode replacement

USAGE: xtool <subcommand>

OPTIONS:
  -h, --help              Show help information.

CONFIGURATION SUBCOMMANDS:
  setup                   Set up xtool for iOS development
  auth                    Manage Apple Developer Services authentication
  sdk                     Manage the Darwin Swift SDK

DEVELOPMENT SUBCOMMANDS:
  new                     Create a new xtool SwiftPM project
  dev                     Build and run an xtool SwiftPM project
  ds                      Interact with Apple Developer Services

DEVICE SUBCOMMANDS:
  devices                 List devices
  install                 Install an ipa file to your device
  uninstall               Uninstall an installed app
  launch                  Launch an installed app

  See 'xtool help <subcommand>' for detailed help.
```

### Library

xtool includes a library that you can use to interact with Apple Developer Services, iOS devices, and more from your own app. You can use this by adding `XKit` as a SwiftPM dependency.

```swift
// package dependency:
.package(url: "https://github.com/xtool-org/xtool", .upToNextMinor(from: "1.2.0"))
// target dependency:
.product(name: "XKit", package: "xtool")
```

---

## 🔌 Claude Plugin (MCP)

`xtool` is available as a **Claude Code Plugin** powered by the Model Context Protocol (MCP). Build, test, sign, install, and launch iOS apps directly from your Claude Code conversations without Xcode.

### Install via Claude Code Marketplace

```bash
# 1. Add the marketplace
/plugin marketplace add stanesjenson11-lgtm/ios-app-xtool

# 2. Install the plugin
/plugin install ios-app-xtool@ios-app-xtool-marketplace
```

### Available Tools
- `xtool_new_project`: Scaffold a new iOS SwiftPM app project.
- `xtool_build_app`: Compile a Swift package into an iOS application bundle.
- `xtool_dev_run`: Live build, sign, and launch app loop on device.
- `xtool_list_devices`: List connected physical iPhones, iPads, and simulators.
- `xtool_install_app`: Install an IPA onto a connected device.
- `xtool_launch_app`: Launch an installed app on device by bundle ID.
- `xtool_uninstall_app`: Remove an app from a device.
- `xtool_setup_status`: Verify Swift compiler, xtool CLI, and SDK readiness.

