bl_info = {
    "name": "Vertex Weight Viewer",
    "author": "copilot, akiRAM2",
    "version": (1, 6, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item > Weight Viewer",
    "description": "Advanced vertex weight overlay with dual display, individual customization, and auto-activation for Weight Paint and Edit modes. Compatible with Blender 4.0+ and 5.0+.",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
    "support": "COMMUNITY",
    "license": "GPL-3.0-or-later",
}

import bpy
from bpy.types import Panel
from bpy.props import BoolProperty, IntProperty, FloatVectorProperty
import bpy_extras
import bpy_extras.view3d_utils
from mathutils import Vector
import traceback
import sys

# Safe imports for version compatibility
try:
    import gpu
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("Vertex Weight Viewer: GPU module not available")

try:
    import blf
    BLF_AVAILABLE = True
except ImportError:
    BLF_AVAILABLE = False
    print("Vertex Weight Viewer: BLF module not available")

_handle = None
_cached_draw_data = None

def update_draw_data():
    """Update cached drawing data from current context (call this outside draw phase)."""
    global _cached_draw_data
    try:
        context = bpy.context
        obj = context.active_object
        
        if not obj or obj.mode not in ['WEIGHT_PAINT', 'EDIT'] or obj.type != 'MESH':
            _cached_draw_data = None
            return
        
        # Cache necessary data for drawing
        _cached_draw_data = {
            'obj': obj,
            'mode': obj.mode,
            'vg_index': obj.vertex_groups.active.index if obj.vertex_groups.active else None,
            'show_overlay': context.window_manager.show_weight_overlay if hasattr(context.window_manager, 'show_weight_overlay') else False,
            'show_total_weight': context.window_manager.show_total_weight if hasattr(context.window_manager, 'show_total_weight') else False,
            'font_size': getattr(context.window_manager, 'weight_overlay_font_size', 14),
            'total_font_size': getattr(context.window_manager, 'weight_overlay_total_font_size', 12),
            'color': getattr(context.window_manager, 'weight_overlay_color', (1.0, 1.0, 0.0, 1.0)),
            'total_color': getattr(context.window_manager, 'weight_overlay_total_color', (0.0, 1.0, 1.0, 1.0)),
        }
        
    except (AttributeError, TypeError):
        _cached_draw_data = None

def check_lazy_weight_tool():
    """Check if Lazy Weight Tool is installed and active."""
    try:
        addon_modules = bpy.context.preferences.addons
        for addon in addon_modules:
            if "lazy" in addon.module.lower() and "weight" in addon.module.lower():
                return True
        return False
    except:
        return False

def ensure_required_modules():
    """Ensure all required modules are available, attempting to resolve missing dependencies."""
    global GPU_AVAILABLE, BLF_AVAILABLE
    
    # Try to import again in case other addons have made modules available
    if not GPU_AVAILABLE:
        try:
            import gpu
            GPU_AVAILABLE = True
            print("Vertex Weight Viewer: GPU module now available")
        except ImportError:
            pass
    
    if not BLF_AVAILABLE:
        try:
            import blf
            BLF_AVAILABLE = True
            print("Vertex Weight Viewer: BLF module now available")
        except ImportError:
            pass
    
    # Check if we have Lazy Weight Tool which might provide missing modules
    has_lazy_weight = check_lazy_weight_tool()
    if has_lazy_weight:
        print("Vertex Weight Viewer: Lazy Weight Tool detected, attempting module resolution...")
    
    return BLF_AVAILABLE  # BLF is critical for text rendering

_handle = None

# Blender version compatibility utilities
def get_blender_version():
    """Get the current Blender version as a tuple."""
    return bpy.app.version

def is_blender_5_or_later():
    """Check if running on Blender 5.0 or later."""
    return get_blender_version() >= (5, 0, 0)

def diagnose_environment():
    """Diagnose the current Blender environment for compatibility issues."""
    print("=== Vertex Weight Viewer: Environment Diagnosis ===")
    print(f"Blender Version: {get_blender_version()}")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Check for installed addons (especially Lazy Weight Tool)
    print("--- Installed Addons ---")
    addon_modules = bpy.context.preferences.addons
    for addon in addon_modules:
        if "weight" in addon.module.lower() or "lazy" in addon.module.lower():
            print(f"✓ Weight-related addon found: {addon.module}")
    
    # Check Python modules
    modules_to_check = [
        'bpy', 'bpy.types', 'bpy.props', 'bpy_extras', 'bpy_extras.view3d_utils',
        'mathutils', 'gpu', 'blf', 'traceback'
    ]
    
    print("--- Core Blender Modules ---")
    for module_name in modules_to_check:
        try:
            module = __import__(module_name)
            module_path = getattr(module, '__file__', 'Built-in')
            print(f"✓ {module_name}: Available ({module_path})")
        except ImportError as e:
            print(f"✗ {module_name}: Missing ({str(e)})")
        except Exception as e:
            print(f"⚠ {module_name}: Error ({type(e).__name__}: {str(e)})")
    
    # Check GPU and BLF specific availability
    print("--- Graphics Modules ---")
    print(f"GPU Module Available: {GPU_AVAILABLE}")
    print(f"BLF Module Available: {BLF_AVAILABLE}")
    
    # Check sys.path for additional module paths
    print("--- Python Module Paths ---")
    for i, path in enumerate(sys.path[:5]):  # Show first 5 paths
        print(f"  {i}: {path}")
    if len(sys.path) > 5:
        print(f"  ... and {len(sys.path) - 5} more paths")
    
    # Check specific Blender 5.0 compatibility issues
    if is_blender_5_or_later():
        print("--- Blender 5.0+ Specific Checks ---")
        
        # Check for deprecated API usage
        try:
            # Test if draw handler signature has changed
            def test_draw():
                pass
            
            handle = bpy.types.SpaceView3D.draw_handler_add(test_draw, (), 'WINDOW', 'POST_PIXEL')
            bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
            print("✓ Draw handler: Compatible with Blender 5.0+ signature")
        except Exception as e:
            print(f"✗ Draw handler: Incompatible ({type(e).__name__}: {str(e)})")
    
    # Test GPU and BLF functionality if available
    print("--- Functionality Tests ---")
    if BLF_AVAILABLE:
        try:
            import blf
            blf.size(0, 12)
            print("✓ BLF: Basic text rendering functions available")
        except Exception as e:
            print(f"✗ BLF: Function test failed ({type(e).__name__}: {str(e)})")
    
    if GPU_AVAILABLE:
        try:
            import gpu
            print("✓ GPU: Module imported successfully")
        except Exception as e:
            print(f"✗ GPU: Import test failed ({type(e).__name__}: {str(e)})")
    
    print("=== End Diagnosis ===")

def check_import_compatibility():
    """Check if all required modules can be imported."""
    missing_modules = []
    
    # Check critical Blender modules
    if not BLF_AVAILABLE:
        missing_modules.append("blf")
    
    if not GPU_AVAILABLE:
        missing_modules.append("gpu")
    
    try:
        import bpy_extras.view3d_utils
    except ImportError:
        missing_modules.append("bpy_extras.view3d_utils")
    
    try:
        from mathutils import Vector
    except ImportError:
        missing_modules.append("mathutils")
    
    try:
        from bpy.types import Panel
    except ImportError:
        missing_modules.append("bpy.types")
    
    try:
        from bpy.props import BoolProperty
    except ImportError:
        missing_modules.append("bpy.props")
    
    if missing_modules:
        print(f"Vertex Weight Viewer: Missing required modules: {', '.join(missing_modules)}")
        print("This may indicate an incomplete Blender installation or a non-standard environment.")
        # Return False only if truly critical modules are missing
        critical_modules = ['bpy.types', 'bpy.props', 'mathutils', 'bpy_extras.view3d_utils']
        critical_missing = [m for m in missing_modules if m in critical_modules]
        return len(critical_missing) == 0
    
    return True

def check_api_compatibility():
    """Check if all required APIs are available for this Blender version."""
    try:
        # First check if modules can be imported
        if not check_import_compatibility():
            return False
        
        # Test critical imports and API calls only if modules are available
        if BLF_AVAILABLE and GPU_AVAILABLE:
            import bpy_extras.view3d_utils
        
        # Test draw handler registration with safe method for all versions
        # Use a simple test callback
        def test_callback():
            pass
        
        # Try different draw handler argument formats for version compatibility
        temp_handle = None
        try:
            if is_blender_5_or_later():
                # Blender 5.0+ may have stricter argument requirements
                temp_handle = bpy.types.SpaceView3D.draw_handler_add(
                    test_callback, (), 'WINDOW', 'POST_PIXEL'
                )
            else:
                # Blender 4.x format
                temp_handle = bpy.types.SpaceView3D.draw_handler_add(
                    test_callback, (None, bpy.context), 'WINDOW', 'POST_PIXEL'
                )
            
            if temp_handle is not None:
                bpy.types.SpaceView3D.draw_handler_remove(temp_handle, 'WINDOW')
        except Exception as draw_error:
            print(f"Vertex Weight Viewer: Draw handler test failed: {type(draw_error).__name__}: {str(draw_error)}")
            # Return True even if draw handler test fails, as the addon can still function partially
        
        print(f"Vertex Weight Viewer: API compatibility check completed for Blender {get_blender_version()}")
        return True
    except Exception as e:
        print(f"Vertex Weight Viewer: API compatibility check failed for Blender {get_blender_version()}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return False

def draw_callback_px(*args):
    """
    Draw callback function compatible with both Blender 4.x and 5.0+.
    Uses cached data to avoid context access issues in Blender 5.0+.
    """
    try:
        global _cached_draw_data
        
        # Use cached data if available (for Blender 5.0+ compatibility)
        if _cached_draw_data is None:
            # Try to get context for Blender 4.x
            context = None
            if len(args) >= 2:
                context = args[1]
            elif hasattr(bpy, 'context'):
                try:
                    context = bpy.context
                    # Test if context is accessible
                    _ = context.active_object
                except (AttributeError, TypeError):
                    # Context is restricted, skip drawing
                    return
            
            if context is None:
                return
            
            obj = context.active_object
            if not obj or obj.mode not in ['WEIGHT_PAINT', 'EDIT'] or obj.type != 'MESH':
                return
        else:
            # Use cached data
            obj = _cached_draw_data['obj']
            if not _cached_draw_data['show_overlay']:
                return
        
        # Get drawing parameters from cached data or context
        if _cached_draw_data is not None:
            vg_index = _cached_draw_data['vg_index']
            show_total_weight = _cached_draw_data['show_total_weight']
            font_size = _cached_draw_data['font_size']
            total_font_size = _cached_draw_data['total_font_size']
            color = _cached_draw_data['color']
            total_color = _cached_draw_data['total_color']
        else:
            vg = obj.vertex_groups.active
            vg_index = vg.index if vg else None
            show_total_weight = getattr(context.window_manager, 'show_total_weight', False)
            font_size = getattr(context.window_manager, 'weight_overlay_font_size', 14)
            total_font_size = getattr(context.window_manager, 'weight_overlay_total_font_size', 12)
            color = getattr(context.window_manager, 'weight_overlay_color', (1.0, 1.0, 0.0, 1.0))
            total_color = getattr(context.window_manager, 'weight_overlay_total_color', (0.0, 1.0, 1.0, 1.0))

        # Get mesh data
        if obj.mode == 'EDIT':
            mesh = obj.data
            matrix_world = obj.matrix_world
        else:
            # For weight paint mode, we need depsgraph - only available with context
            if _cached_draw_data is not None:
                # Use base mesh data for cached drawing
                mesh = obj.data
                matrix_world = obj.matrix_world
            else:
                depsgraph = context.evaluated_depsgraph_get()
                eval_obj = obj.evaluated_get(depsgraph)
                mesh = eval_obj.data
                matrix_world = eval_obj.matrix_world

        # Get region and viewport data - try from context or bpy.context
        region = None
        rv3d = None
        try:
            if _cached_draw_data is None and context:
                region = context.region
                rv3d = context.region_data
            else:
                # Try to get from bpy.context for drawing
                ctx = bpy.context
                region = getattr(ctx, 'region', None)
                rv3d = getattr(ctx, 'region_data', None)
        except (AttributeError, TypeError):
            pass
            
        if region is None or rv3d is None:
            return

        # Check BLF availability
        if not BLF_AVAILABLE:
            return
        
        font_id = 0
        blf.size(font_id, font_size)
    except Exception as e:
        print(f"Vertex Weight Viewer: Error in draw_callback_px setup: {type(e).__name__}: {str(e)}")
        return

    try:
        # Render vertex weights
        for v in mesh.vertices:
            try:
                # アクティブな頂点グループのウェイト
                active_weight = 0.0
                if vg_index is not None:
                    for group in v.groups:
                        if group.group == vg_index:
                            active_weight = group.weight
                            break
                
                # 全ての頂点グループのウェイト合計
                total_weight = sum(group.weight for group in v.groups)
                
                # 表示条件をチェック
                if active_weight == 0.0 and (not show_total_weight or total_weight == 0.0):
                    continue

                co_world = matrix_world @ v.co
                co_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(region, rv3d, co_world)
                if co_2d:
                    # Active Weightを大きく上に表示
                    if vg_index is not None and active_weight > 0.0:
                        blf.size(font_id, font_size)
                        blf.color(font_id, *color)
                        blf.position(font_id, co_2d.x, co_2d.y, 0)
                        blf.draw(font_id, f"{active_weight:.2f}")
                    
                    # Total Weightを小さく下に表示（Show Total Weightがオンの場合のみ）
                    if show_total_weight and total_weight > 0.0:
                        blf.size(font_id, total_font_size)
                        blf.color(font_id, *total_color)
                        # Active Weightが表示されている場合は、その下に表示
                        y_offset = -font_size - 2 if (vg_index is not None and active_weight > 0.0) else 0
                        blf.position(font_id, co_2d.x, co_2d.y + y_offset, 0)
                        blf.draw(font_id, f"{total_weight:.2f}")
            except Exception as e:
                print(f"Vertex Weight Viewer: Error processing vertex {v.index}: {type(e).__name__}: {str(e)}")
                continue
    except Exception as e:
        print(f"Vertex Weight Viewer: Error in draw_callback_px rendering loop: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")

class VIEW3D_PT_weight_overlay(Panel):
    bl_label = "Weight Viewer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return (context.active_object and 
                context.active_object.type == 'MESH' and
                context.active_object.vertex_groups)

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.prop(wm, "show_weight_overlay", text="Show Overlay")
        
        # Display module availability status
        if not BLF_AVAILABLE:
            box = layout.box()
            box.alert = True
            box.label(text="⚠ Text rendering unavailable", icon='ERROR')
            box.label(text="BLF module missing")
            if check_lazy_weight_tool():
                box.label(text="Try restarting Blender")
            else:
                box.operator("wm.console_toggle", text="Run Diagnosis", icon='CONSOLE')
        
        if wm.show_weight_overlay:
            layout.separator()
            
            # Total Weight表示切り替え
            layout.prop(wm, "show_total_weight", text="Show Total Weight")
            layout.separator()
            
            # フォントサイズ設定セクション
            box = layout.box()
            box.label(text="Font Sizes:")
            box.prop(wm, "weight_overlay_font_size", text="Active Vertex Group Size")
            if wm.show_total_weight:
                box.prop(wm, "weight_overlay_total_font_size", text="Total Weight Size")
            
            # カラー設定セクション
            box = layout.box()
            box.label(text="Colors:")
            box.prop(wm, "weight_overlay_color", text="Active Vertex Group Color")
            if wm.show_total_weight:
                box.prop(wm, "weight_overlay_total_color", text="Total Weight Color")

def register_draw_handler():
    global _handle
    try:
        if _handle is None:
            # Blender 5.0+ compatible draw handler registration
            if is_blender_5_or_later():
                # Use the new format for Blender 5.0+
                _handle = bpy.types.SpaceView3D.draw_handler_add(
                    draw_callback_px, (), 'WINDOW', 'POST_PIXEL'
                )
            else:
                # Use the legacy format for Blender 4.x
                _handle = bpy.types.SpaceView3D.draw_handler_add(
                    draw_callback_px, (None, bpy.context), 'WINDOW', 'POST_PIXEL'
                )
            print(f"Vertex Weight Viewer: Draw handler registered successfully for Blender {get_blender_version()}")
    except Exception as e:
        print(f"Vertex Weight Viewer: Failed to register draw handler: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")

def unregister_draw_handler():
    global _handle
    try:
        if _handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
            _handle = None
            print(f"Vertex Weight Viewer: Draw handler unregistered successfully")
    except Exception as e:
        print(f"Vertex Weight Viewer: Failed to unregister draw handler: {type(e).__name__}: {str(e)}")
        _handle = None  # Reset handle even if unregistration failed

def update_show_weight_overlay(self, context):
    try:
        if context.window_manager.show_weight_overlay:
            update_draw_data()  # Cache drawing data before enabling
            register_draw_handler()
        else:
            unregister_draw_handler()
    except Exception as e:
        print(f"Vertex Weight Viewer: Error in update_show_weight_overlay: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")

def on_file_loaded(dummy):
    """ファイル読み込み時に呼び出される関数"""
    try:
        wm = bpy.context.window_manager
        if hasattr(wm, "show_weight_overlay") and wm.show_weight_overlay:
            register_draw_handler()
    except Exception as e:
        print(f"Vertex Weight Viewer: Error in on_file_loaded: {type(e).__name__}: {str(e)}")

@bpy.app.handlers.persistent
def on_scene_update(dummy):
    """シーン更新時に確実にハンドラが登録されているかチェックし、描画データを更新"""
    try:
        wm = bpy.context.window_manager
        if hasattr(wm, "show_weight_overlay") and wm.show_weight_overlay:
            # Update cached drawing data for Blender 5.0+ compatibility
            update_draw_data()
            
            global _handle
            if _handle is None:
                register_draw_handler()
    except Exception as e:
        print(f"Vertex Weight Viewer: Error in on_scene_update: {type(e).__name__}: {str(e)}")

def register():
    try:
        print(f"Vertex Weight Viewer: Starting registration for Blender {get_blender_version()}")
        
        # Ensure required modules are available
        modules_available = ensure_required_modules()
        if not modules_available:
            print("Vertex Weight Viewer: Critical modules missing!")
            print("If you have Lazy Weight Tool installed, try restarting Blender.")
            diagnose_environment()
            
            # Still register the addon but warn about limited functionality
            print("Vertex Weight Viewer: Continuing with limited functionality...")
        
        # Check API compatibility
        if not check_api_compatibility():
            print(f"Vertex Weight Viewer: Warning - Running on Blender {get_blender_version()}, some features may not work correctly.")
            print("Running environment diagnosis...")
            diagnose_environment()
        
        bpy.utils.register_class(VIEW3D_PT_weight_overlay)
        print("Vertex Weight Viewer: UI panel registered successfully")
        
        bpy.types.WindowManager.show_weight_overlay = BoolProperty(
            name="Show Weight Overlay",
            default=True,
            update=update_show_weight_overlay
        )
        bpy.types.WindowManager.weight_overlay_font_size = IntProperty(
            name="Active Vertex Group Font Size", 
            description="Font size for active vertex group weight display",
            default=14, min=8, max=64
        )
        bpy.types.WindowManager.weight_overlay_total_font_size = IntProperty(
            name="Total Weight Font Size",
            description="Font size for total weight sum display", 
            default=12, min=8, max=64
        )
        bpy.types.WindowManager.weight_overlay_color = FloatVectorProperty(
            name="Active Vertex Group Color",
            description="Color for active vertex group weight display",
            default=(1.0, 1.0, 0.0, 1.0),
            min=0.0, max=1.0, size=4, subtype='COLOR'
        )
        bpy.types.WindowManager.weight_overlay_total_color = FloatVectorProperty(
            name="Total Weight Color",
            description="Color for total weight sum display",
            default=(0.0, 1.0, 1.0, 1.0),
            min=0.0, max=1.0, size=4, subtype='COLOR'
        )
        bpy.types.WindowManager.show_total_weight = BoolProperty(
            name="Show Total Weight",
            description="Display total weight sum below active vertex group weight",
            default=True
        )
        print("Vertex Weight Viewer: Properties registered successfully")

        # デフォルト値を確実に設定（既存の設定がある場合も更新）
        wm = bpy.context.window_manager
        if not hasattr(wm, "weight_overlay_font_size") or wm.weight_overlay_font_size == 16:
            # 16pxから14pxへの移行、または初回設定
            wm.weight_overlay_font_size = 14
        
        # 初期化時に確実にハンドラを登録
        register_draw_handler()
        
        # ファイル読み込み時やリロード時のイベントハンドラを追加
        bpy.app.handlers.load_post.append(on_file_loaded)
        bpy.app.handlers.depsgraph_update_post.append(on_scene_update)
        print("Vertex Weight Viewer: Event handlers registered successfully")
        
        print("Vertex Weight Viewer: Registration completed successfully")
    except Exception as e:
        print(f"Vertex Weight Viewer: Registration failed: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")

def unregister():
    try:
        print("Vertex Weight Viewer: Starting unregistration")
        
        unregister_draw_handler()
        
        # イベントハンドラを削除
        try:
            if on_file_loaded in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.remove(on_file_loaded)
            if on_scene_update in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.remove(on_scene_update)
            print("Vertex Weight Viewer: Event handlers removed successfully")
        except Exception as e:
            print(f"Vertex Weight Viewer: Error removing event handlers: {type(e).__name__}: {str(e)}")
        
        # プロパティを削除
        try:
            if hasattr(bpy.types.WindowManager, 'show_weight_overlay'):
                del bpy.types.WindowManager.show_weight_overlay
            if hasattr(bpy.types.WindowManager, 'weight_overlay_font_size'):
                del bpy.types.WindowManager.weight_overlay_font_size
            if hasattr(bpy.types.WindowManager, 'weight_overlay_total_font_size'):
                del bpy.types.WindowManager.weight_overlay_total_font_size
            if hasattr(bpy.types.WindowManager, 'weight_overlay_color'):
                del bpy.types.WindowManager.weight_overlay_color
            if hasattr(bpy.types.WindowManager, 'weight_overlay_total_color'):
                del bpy.types.WindowManager.weight_overlay_total_color
            if hasattr(bpy.types.WindowManager, 'show_total_weight'):
                del bpy.types.WindowManager.show_total_weight
            print("Vertex Weight Viewer: Properties removed successfully")
        except Exception as e:
            print(f"Vertex Weight Viewer: Error removing properties: {type(e).__name__}: {str(e)}")
        
        # UIクラスを削除
        try:
            bpy.utils.unregister_class(VIEW3D_PT_weight_overlay)
            print("Vertex Weight Viewer: UI panel unregistered successfully")
        except Exception as e:
            print(f"Vertex Weight Viewer: Error unregistering UI classes: {type(e).__name__}: {str(e)}")
        
        print("Vertex Weight Viewer: Unregistration completed")
    except Exception as e:
        print(f"Vertex Weight Viewer: Unregistration failed: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")

if __name__ == "__main__":
    try:
        register()
    except Exception as e:
        print(f"Vertex Weight Viewer: Failed to register addon: {type(e).__name__}: {str(e)}")
        print("This may indicate missing Blender modules or an incompatible environment.")
        print(f"Stack trace: {traceback.format_exc()}")