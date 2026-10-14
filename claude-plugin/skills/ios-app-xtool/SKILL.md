---
name: ios-app-xtool
description: Build, sign, install, and run iOS applications using SwiftPM on Linux, Windows (WSL), and macOS without needing Xcode.
---

# xtool — Cross-Platform iOS App Builder

`xtool` is a modern Xcode replacement enabling full-cycle iOS development using SwiftPM across Linux, Windows (WSL), and macOS.

## Core Capabilities
- **Create Projects**: Scaffold new iOS apps using standard SwiftPM packages (`Package.swift`).
- **Build & Run**: Compile Swift packages into signed iOS app bundles and IPAs (`xtool dev`).
- **Device Deployment**: Detect connected iPhones and iPads, install IPAs over USB or Wi-Fi, and launch apps.
- **Apple Developer Integration**: Programmatically interact with Apple Developer Services for code signing and provisioning profiles.

## Available MCP Tools

### `xtool_new_project`
Scaffold a new iOS SwiftPM app project.
- `name` (required): Application name
- `bundle_id` (optional): App Bundle Identifier (e.g. `com.example.myapp`)
- `path` (optional): Target directory path

### `xtool_build_app`
Build a SwiftPM package into an iOS application bundle / IPA.
- `project_path` (optional): Path to the SwiftPM project directory
- `configuration` (optional): Build configuration (`debug` or `release`)
- `sdk` (optional): Target SDK (e.g. `iphoneos`)

### `xtool_dev_run`
Build, sign, install, and launch the app in one command with continuous live feedback.
- `project_path` (optional): Project root path
- `device_id` (optional): Target device identifier if multiple devices are connected

### `xtool_list_devices`
List all connected physical iOS devices (iPhone, iPad) and simulators.

### `xtool_install_app`
Install an IPA file onto a connected device.
- `ipa_path` (required): Path to the `.ipa` or `.app` bundle
- `device_id` (optional): Specific device to target

### `xtool_launch_app`
Launch an installed application on a device.
- `bundle_id` (required): Bundle identifier of the app to launch (e.g. `com.example.myapp`)
- `device_id` (optional): Specific device to target

### `xtool_uninstall_app`
Remove an installed app from a device.
- `bundle_id` (required): Bundle identifier of the app to remove

### `xtool_setup_status`
Check toolchain readiness: verifies Swift compiler, Darwin SDK, and device connection drivers.
