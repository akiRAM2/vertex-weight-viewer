# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2025-10-30

### 🎉 Major Features
- **Dual Display System**: Shows both active vertex group weight (large, top) and total weight (small, bottom) simultaneously
- **Multi-Mode Support**: Works seamlessly in both Weight Paint and Edit modes
- **Individual Customization**: Separate font sizes and colors for each display type
- **Auto-Display**: Automatically shows overlay when Blender starts or files are loaded

### 🎨 Display & UI
- **Smart Layout**: Active Vertex Group (14px, yellow) prioritized above Total Weight (12px, cyan)  
- **Item Tab Integration**: Located in standard "Item" tab for better Blender workflow integration
- **Smart Panel Visibility**: Appears only when mesh objects with vertex groups are selected
- **Organized Controls**: Dedicated sections for Font Sizes and Colors with clear labels

### 🔧 Technical Improvements
- **Robust Auto-Activation**: Multiple handlers ensure reliable display across Blender sessions
- **Enhanced Edit Mode**: Improved mesh data access for seamless compatibility
- **Performance Optimized**: Shows only non-zero values for clean visualization
- **Blender Standards**: Follows UI conventions for object-specific tools

### 📋 Requirements
- Blender 4.0 or later
- Mesh objects with vertex groups

### 🚀 Quick Start
1. Install addon and enable in Preferences
2. Select mesh with vertex groups → Enter Weight Paint or Edit mode
3. Find "Weight Viewer" panel in N-panel → Item tab
4. Customize colors and font sizes as needed

## [1.1.2] - 2025-10-30

### Changed
- Renamed addon from "Weight Paint Vertex Group Weight Overlay" to "Vertex Weight Viewer"
- Updated panel category to "Weight Viewer"
- Changed license to MIT
- Added comprehensive bl_info metadata

### Added
- Support level indication (COMMUNITY)
- License specification in bl_info

## [1.1.1] - Previous
- Bug fixes and improvements

## [1.1.0] - Previous
- Initial release with weight overlay functionality