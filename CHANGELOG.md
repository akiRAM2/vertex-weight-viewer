# Changelog

All notable changes to this project will be documented in this file.

## [1.5.0] - 2025-11-01

### 🚀 Blender 5.0 Compatibility
- **Major Update**: Added full Blender 5.0 support while maintaining backward compatibility
- **Version Detection**: Added automatic Blender version checking system
- **API Validation**: Implements startup compatibility checks for critical APIs
- **Enhanced Error Handling**: Comprehensive error logging and exception handling throughout
- **Future-Proof**: Designed to adapt to API changes in Blender 5.x series

### 🛠️ Robust Error Handling
- **Detailed Logging**: Added comprehensive error messages with exception types and stack traces
- **Graceful Degradation**: Functions continue to work even when individual components fail
- **Debug Information**: Registration/unregistration process now provides detailed status messages
- **Safe Operations**: All critical operations wrapped in try-catch blocks with proper cleanup
- **Developer Tools**: Enhanced debugging information for troubleshooting compatibility issues

### 🔧 Import & Environment Fixes
- **Missing Module Detection**: Added comprehensive import compatibility checking
- **Explicit Imports**: Improved import statements for better compatibility across environments
- **Environment Diagnosis**: Added detailed environment diagnostic tool for troubleshooting
- **Safe Module Loading**: Graceful handling of missing or unavailable Blender modules
- **Cross-Platform Compatibility**: Enhanced support for different Blender installations and configurations

### 🔧 Technical Improvements
- **Smart Compatibility**: Automatic detection of Blender 4.0+ vs 5.0+ environments
- **Robust Initialization**: Enhanced startup sequence with compatibility validation
- **Developer Tools**: Added utility functions for version checking and API testing
- **Improved Logging**: Better error reporting for debugging compatibility issues

### 📋 Updated Requirements
- **Extended Support**: Blender 4.0 or later (including 5.0+)
- **Backward Compatibility**: Existing Blender 4.x installations continue to work seamlessly

## [1.4.0] - 2025-11-01

### 🎛️ Enhanced Control Options
- **Total Weight Toggle**: Added "Show Total Weight" checkbox to enable/disable total weight display
- **Smart UI Layout**: Total Weight options (font size and color) only appear when toggle is enabled
- **Flexible Display**: Can now show only Active Vertex Group weights or both displays simultaneously
- **Improved User Control**: Better customization for different workflow needs

## [1.3.1] - 2025-10-31

### 📄 License Compliance
- **GPL v3.0+ License**: Changed from MIT to GNU General Public License v3.0 or later
- **Updated Documentation**: License information updated in all relevant files

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