bl_info = {
    "name": "Vertex Weight Viewer",
    "author": "akiRAM2",
    "version": (1, 7, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item > Weight Viewer",
    "description": "Advanced vertex weight overlay with dual display and limit warnings.",
    "warning": "",
    "category": "3D View",
    "support": "COMMUNITY",
    "license": "GPL-3.0-or-later",
}

import bpy
import bpy_extras
from bpy.types import Panel, Operator
from bpy.props import BoolProperty, IntProperty, FloatVectorProperty
from bpy.app.handlers import persistent

# --- Module Checks ---
try:
    import blf
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False

# --- Core Logic ---
class VertexWeightViewerCore:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.draw_handle = None
        self.font_id = 0

    def start_session(self, context):
        if self.draw_handle is None:
            try:
                args = (None, bpy.context) if bpy.app.version < (5, 0, 0) else ()
                self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
                    draw_callback_wrapper, args, 'WINDOW', 'POST_PIXEL'
                )
                # Force redraw
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            except Exception as e:
                print(f"WeightViewer Error: {e}")

    def stop_session(self):
        if self.draw_handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
            self.draw_handle = None

    def draw(self, context=None):
        if not MODULES_AVAILABLE: 
            return
            
        ctx = context if context else bpy.context
        wm = ctx.window_manager
        
        if not getattr(wm, "show_weight_overlay", False):
            return

        # --- Settings ---
        show_total = getattr(wm, "show_total_weight", True)
        
        font_size_active = getattr(wm, "weight_overlay_font_size", 14)
        font_size_total = getattr(wm, "weight_overlay_total_font_size", 12)
        color_active = getattr(wm, "weight_overlay_color", (1, 1, 0, 1))
        color_total = getattr(wm, "weight_overlay_total_color", (0, 1, 1, 1))
        
        show_warning = getattr(wm, "show_weight_limit_warning", False)
        warning_thresh = getattr(wm, "weight_limit_threshold", 4)
        warning_color = getattr(wm, "weight_warning_color", (1, 0, 0, 1))

        # --- Object & Mesh ---
        obj = ctx.active_object
        if not obj or obj.type != 'MESH' or obj.mode not in {'EDIT', 'WEIGHT_PAINT'}:
            return
            
        try:
            # Determining the mesh to iterate
            depsgraph = ctx.evaluated_depsgraph_get()
            eval_obj = obj.evaluated_get(depsgraph)
            
            use_eval = len(eval_obj.data.vertices) == len(obj.data.vertices)
            
            if use_eval:
                mesh = eval_obj.data
                matrix_world = eval_obj.matrix_world
            else:
                mesh = obj.data
                matrix_world = obj.matrix_world

            if obj.mode == 'EDIT':
                mesh = obj.data
                matrix_world = obj.matrix_world

            vg_active = obj.vertex_groups.active
            vg_index = vg_active.index if vg_active else None
            
            region = ctx.region
            rv3d = ctx.region_data
        except:
            return

        # --- Iteration ---
        blf.size(self.font_id, font_size_active)
        
        for v in mesh.vertices:
            # 1. Project 3D -> 2D
            co_world = matrix_world @ v.co
            co_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(region, rv3d, co_world)
            if not co_2d:
                continue

            # 2. Weights
            active_w = 0.0
            total_w = 0.0
            influence_count = 0
            
            # Use original loop for groups as no simple way to map eval groups back without index matching
            for g in v.groups:
                w = g.weight
                total_w += w
                if vg_index is not None and g.group == vg_index:
                    active_w = w
                
                if w > 0.001:
                    influence_count += 1
            
            # --- Draw Overlay Numbers on Mesh ---
            has_active = (vg_index is not None and active_w > 0.0)
            has_total = (show_total and total_w > 0.0)
            
            if has_active or has_total:
                is_warn = show_warning and (influence_count >= warning_thresh)
                
                if has_active:
                    col = warning_color if is_warn else color_active
                    self.draw_text(co_2d.x, co_2d.y, f"{active_w:.2f}", font_size_active, col, is_warn)

                if has_total:
                    col = warning_color if is_warn else color_total
                    off_y = (-font_size_active - 2) if has_active else 0
                    self.draw_text(co_2d.x, co_2d.y + off_y, f"{total_w:.2f}", font_size_total, col, is_warn)

    def draw_text(self, x, y, text, size, color, bold=False):
        blf.size(self.font_id, size)
        blf.color(self.font_id, *color)
        if bold:
            # Multipass for thickness
            for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
                blf.position(self.font_id, x+ox, y+oy, 0)
                blf.draw(self.font_id, text)
        blf.position(self.font_id, x, y, 0)
        blf.draw(self.font_id, text)

core = VertexWeightViewerCore.get_instance()

# --- Callbacks ---
def draw_callback_wrapper(*args):
    context = args[1] if len(args) > 1 else bpy.context
    core.draw(context)

@persistent
def on_load(dummy):
    wm = bpy.context.window_manager
    if hasattr(wm, "show_weight_overlay") and wm.show_weight_overlay:
        core.start_session(bpy.context)

# --- UI ---
class VIEW3D_PT_weight_overlay(Panel):
    bl_label = "Weight Viewer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    @classmethod
    def poll(cls, c): 
        return c.active_object and c.active_object.type=='MESH'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        layout.prop(wm, "show_weight_overlay", text="Show Overlay")
        if not wm.show_weight_overlay: return
        
        layout.separator()
        layout.prop(wm, "show_total_weight", text="Show Total Weight")
        
        layout.separator()
        
        col = layout.column(align=True)
        col.label(text="Display Settings")
        col.prop(wm, "weight_overlay_font_size", text="Active Weight")
        col.prop(wm, "weight_overlay_color", text="Active Color")
        if wm.show_total_weight:
            col.prop(wm, "weight_overlay_total_font_size", text="Total Weight")
            col.prop(wm, "weight_overlay_total_color", text="Total Color")
        
        layout.separator()
        layout.prop(wm, "show_weight_limit_warning", text="Influence Limit Warning")
        if wm.show_weight_limit_warning:
            col = layout.column(align=True)
            col.prop(wm, "weight_limit_threshold", text="Max Bones")
            col.prop(wm, "weight_warning_color", text="")

# --- Reg ---
def update_toggle(self, context):
    if self.show_weight_overlay: core.start_session(context)
    else: core.stop_session()

def register():
    wm = bpy.types.WindowManager
    wm.show_weight_overlay = BoolProperty(name="Show", default=True, update=update_toggle)
    wm.show_total_weight = BoolProperty(name="Total", default=True)
    
    wm.weight_overlay_font_size = IntProperty(name="FSize", default=14)
    wm.weight_overlay_total_font_size = IntProperty(name="TSize", default=12)
    wm.weight_overlay_color = FloatVectorProperty(name="C", default=(1,1,0,1), subtype='COLOR', size=4)
    wm.weight_overlay_total_color = FloatVectorProperty(name="TC", default=(0,1,1,1), subtype='COLOR', size=4)
    
    wm.show_weight_limit_warning = BoolProperty(name="Warn", default=False)
    wm.weight_limit_threshold = IntProperty(name="Thresh", default=4, min=1)
    wm.weight_warning_color = FloatVectorProperty(name="WCol", default=(1,0,0,1), subtype='COLOR', size=4)

    bpy.utils.register_class(VIEW3D_PT_weight_overlay)
    bpy.app.handlers.load_post.append(on_load)
    
    # Init
    try:
        if hasattr(bpy.context.window_manager, "show_weight_overlay") and bpy.context.window_manager.show_weight_overlay:
            core.start_session(bpy.context)
    except: pass

def unregister():
    core.stop_session()
    if on_load in bpy.app.handlers.load_post: bpy.app.handlers.load_post.remove(on_load)
    bpy.utils.unregister_class(VIEW3D_PT_weight_overlay)
    
    wm = bpy.types.WindowManager
    del wm.show_weight_overlay
    # ... cleanup ...

if __name__ == "__main__":
    register()