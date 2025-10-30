bl_info = {
    "name": "Vertex Weight Viewer",
    "author": "copilot, akiRAM2",
    "version": (1, 3, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item > Weight Viewer",
    "description": "Advanced vertex weight overlay with dual display, individual customization, and auto-activation for Weight Paint and Edit modes.",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
    "support": "COMMUNITY",
    "license": "GPL-3.0-or-later",
}

import bpy
import bpy_extras
import gpu
from mathutils import Vector

_handle = None

def draw_callback_px(self, context):
    obj = context.active_object
    if not obj or obj.mode not in ['WEIGHT_PAINT', 'EDIT'] or obj.type != 'MESH':
        return
    
    vg = obj.vertex_groups.active

    # Editモードとウェイトペイントモードで異なるアプローチ
    if obj.mode == 'EDIT':
        # Editモードでは元のメッシュデータを直接使用
        mesh = obj.data
        matrix_world = obj.matrix_world
    else:
        # ウェイトペイントモードでは評価されたメッシュを使用
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.data
        matrix_world = eval_obj.matrix_world

    region = context.region
    rv3d = context.region_data
    if region is None or rv3d is None:
        return

    import blf
    font_id = 0
    blf.size(font_id, context.window_manager.weight_overlay_font_size)

    # 表示モードの設定
    vg_index = vg.index if vg else None
    
    for v in mesh.vertices:
        # アクティブな頂点グループのウェイト
        active_weight = 0.0
        if vg_index is not None:
            for group in v.groups:
                if group.group == vg_index:
                    active_weight = group.weight
                    break
        
        # 全ての頂点グループのウェイト合計
        total_weight = sum(group.weight for group in v.groups)
        
        # 少なくとも一つが0より大きい場合のみ表示
        if total_weight == 0.0 and active_weight == 0.0:
            continue

        co_world = matrix_world @ v.co
        co_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(region, rv3d, co_world)
        if co_2d:
            # Active Weightを大きく上に表示
            if vg_index is not None and active_weight > 0.0:
                active_font_size = context.window_manager.weight_overlay_font_size
                blf.size(font_id, active_font_size)
                blf.color(font_id, *context.window_manager.weight_overlay_color)
                blf.position(font_id, co_2d.x, co_2d.y, 0)
                blf.draw(font_id, f"{active_weight:.2f}")
            
            # Total Weightを小さく下に表示
            if total_weight > 0.0:
                total_font_size = context.window_manager.weight_overlay_total_font_size
                blf.size(font_id, total_font_size)
                blf.color(font_id, *context.window_manager.weight_overlay_total_color)
                # Active Weightが表示されている場合は、その下に表示
                y_offset = -active_font_size - 2 if (vg_index is not None and active_weight > 0.0) else 0
                blf.position(font_id, co_2d.x, co_2d.y + y_offset, 0)
                blf.draw(font_id, f"{total_weight:.2f}")

class VIEW3D_PT_weight_overlay(bpy.types.Panel):
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
        
        if wm.show_weight_overlay:
            layout.separator()
            
            # フォントサイズ設定セクション
            box = layout.box()
            box.label(text="Font Sizes:")
            box.prop(wm, "weight_overlay_font_size", text="Active Vertex Group Size")
            box.prop(wm, "weight_overlay_total_font_size", text="Total Weight Size")
            
            # カラー設定セクション
            box = layout.box()
            box.label(text="Colors:")
            box.prop(wm, "weight_overlay_color", text="Active Vertex Group Color")
            box.prop(wm, "weight_overlay_total_color", text="Total Weight Color")

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

def on_file_loaded(dummy):
    """ファイル読み込み時に呼び出される関数"""
    try:
        wm = bpy.context.window_manager
        if hasattr(wm, "show_weight_overlay") and wm.show_weight_overlay:
            register_draw_handler()
    except:
        pass

@bpy.app.handlers.persistent
def on_scene_update(dummy):
    """シーン更新時に確実にハンドラが登録されているかチェック"""
    try:
        wm = bpy.context.window_manager
        if hasattr(wm, "show_weight_overlay") and wm.show_weight_overlay:
            global _handle
            if _handle is None:
                register_draw_handler()
    except:
        pass

def register():
    bpy.utils.register_class(VIEW3D_PT_weight_overlay)
    bpy.types.WindowManager.show_weight_overlay = bpy.props.BoolProperty(
        name="Show Weight Overlay",
        default=True,
        update=update_show_weight_overlay
    )
    bpy.types.WindowManager.weight_overlay_font_size = bpy.props.IntProperty(
        name="Active Vertex Group Font Size", 
        description="Font size for active vertex group weight display",
        default=14, min=8, max=64
    )
    bpy.types.WindowManager.weight_overlay_total_font_size = bpy.props.IntProperty(
        name="Total Weight Font Size",
        description="Font size for total weight sum display", 
        default=12, min=8, max=64
    )
    bpy.types.WindowManager.weight_overlay_color = bpy.props.FloatVectorProperty(
        name="Active Vertex Group Color",
        description="Color for active vertex group weight display",
        default=(1.0, 1.0, 0.0, 1.0),
        min=0.0, max=1.0, size=4, subtype='COLOR'
    )
    bpy.types.WindowManager.weight_overlay_total_color = bpy.props.FloatVectorProperty(
        name="Total Weight Color",
        description="Color for total weight sum display",
        default=(0.0, 1.0, 1.0, 1.0),
        min=0.0, max=1.0, size=4, subtype='COLOR'
    )

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

def unregister():
    unregister_draw_handler()
    
    # イベントハンドラを削除
    if on_file_loaded in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_file_loaded)
    if on_scene_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(on_scene_update)
    
    del bpy.types.WindowManager.show_weight_overlay
    del bpy.types.WindowManager.weight_overlay_font_size
    del bpy.types.WindowManager.weight_overlay_total_font_size
    del bpy.types.WindowManager.weight_overlay_color
    del bpy.types.WindowManager.weight_overlay_total_color
    bpy.utils.unregister_class(VIEW3D_PT_weight_overlay)

if __name__ == "__main__":
    register()