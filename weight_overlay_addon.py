bl_info = {
    "name": "Vertex Weight Viewer",
    "author": "copilot, akiRAM2",
    "version": (1, 1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Weight Viewer",
    "description": "Show active vertex group weights as overlay in weight paint mode. Toggle with UI panel.",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
    "support": "COMMUNITY",
    "license": "MIT",
}

import bpy
import bpy_extras
import gpu
from mathutils import Vector

_handle = None

def draw_callback_px(self, context):
    obj = context.active_object
    if not obj or obj.mode != 'WEIGHT_PAINT':
        return
    vg = obj.vertex_groups.active
    if not vg:
        return

    depsgraph = context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.data

    region = context.region
    rv3d = context.region_data
    if region is None or rv3d is None:
        return

    import blf
    font_id = 0
    blf.size(font_id, context.window_manager.weight_overlay_font_size)

    for v in mesh.vertices:
        try:
            w = vg.weight(v.index)
        except RuntimeError:
            w = 0.0
        if w == 0.0:
            continue

        co_world = eval_obj.matrix_world @ v.co
        co_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(region, rv3d, co_world)
        if co_2d:
            color = context.window_manager.weight_overlay_color
            blf.position(font_id, co_2d.x, co_2d.y, 0)
            blf.color(font_id, *color)
            blf.draw(font_id, f"{w:.2f}")

class VIEW3D_PT_weight_overlay(bpy.types.Panel):
    bl_label = "Weight Viewer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Weight Viewer"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.prop(wm, "show_weight_overlay", text="Show Overlay")
        layout.prop(wm, "weight_overlay_font_size", text="Font Size")
        layout.prop(wm, "weight_overlay_color", text="Font Color")

def register_draw_handler():
    global _handle
    if _handle is None:
        _handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback_px, (None, bpy.context), 'WINDOW', 'POST_PIXEL'
        )

def unregister_draw_handler():
    global _handle
    if _handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
        _handle = None

def update_show_weight_overlay(self, context):
    if context.window_manager.show_weight_overlay:
        register_draw_handler()
    else:
        unregister_draw_handler()

def register():
    bpy.utils.register_class(VIEW3D_PT_weight_overlay)
    bpy.types.WindowManager.show_weight_overlay = bpy.props.BoolProperty(
        name="Show Weight Overlay",
        default=True,
        update=update_show_weight_overlay
    )
    bpy.types.WindowManager.weight_overlay_font_size = bpy.props.IntProperty(
        name="Font Size", default=14, min=8, max=64
    )
    bpy.types.WindowManager.weight_overlay_color = bpy.props.FloatVectorProperty(
        name="Font Color",
        default=(1.0, 1.0, 0.0, 1.0),
        min=0.0, max=1.0, size=4, subtype='COLOR'
    )
    # ここで初期値がTrueならハンドラ登録
    wm = bpy.context.window_manager
    if not hasattr(wm, "show_weight_overlay") or wm.show_weight_overlay:
        register_draw_handler()

def unregister():
    unregister_draw_handler()
    del bpy.types.WindowManager.show_weight_overlay
    del bpy.types.WindowManager.weight_overlay_font_size
    del bpy.types.WindowManager.weight_overlay_color
    bpy.utils.unregister_class(VIEW3D_PT_weight_overlay)

if __name__ == "__main__":
    register()