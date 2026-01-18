# Changelog

All notable changes to this project will be documented in this file.

## [1.7.0] - 2026-01-18

### ✨ New Features
- **Bone Weight Limit Warning**: Added a feature to warn when the number of vertex weights (influences) exceeds a specified threshold.
    - **Visual Warning**: Displays weight values in **bold color** (default: Red) for vertices exceeding the limit.
    - **Customizable Threshold**: Users can set the limit threshold (e.g., 4 for Unity/Game engines).
    - **Custom Color**: Warning color is fully customizable in the preferences.
- **Enhanced Overlay**:
    - Improved visibility options for Active and Total weights.
    - Cleaned up UI for better usability.

## [1.6.0] - 2025-11-01

### Critical Blender 5.0.0 Fixes
- Fixed context access issues in drawing callbacks for Blender 5.0+
- Implemented cached drawing data system
- Added robust environment diagnosis

### Dependency Handling
- Added lazy-loading for heavy modules
- Improved error handling for missing dependencies

## [1.5.0] - 2025-06-15

### 🚀 Major Improvements
- **Dual Weight Display**: Now shows both active group weight AND total weight sum per vertex
- **Smart Formatting**: Labels are positioned to avoid overlap
- **Performance**: Optimized drawing loop for high-count meshes

## [1.0.0] - 2024-01-20

### 🎉 Initial Release
- Basic vertex weight overlay
- Weight Paint and Edit Mode support
- Font size and color customization