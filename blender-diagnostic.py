import bpy
import sys
import os

def diagnose_model():
    """Diagnose potential issues with the model and materials"""
    
    # Find the body mesh
    body = None
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and ('Man Body' in obj.name or '24_body' in obj.name):
            body = obj
            break
    
    if not body:
        print(f"ERROR: Body model not found in file")
        return
        
    print(f"\nDiagnostic Report for {bpy.data.filepath}")
    print("-" * 50)
    
    # Check mesh data
    print(f"\n1. Basic Mesh Information:")
    print(f"   Object name: {body.name}")
    print(f"   Number of vertices: {len(body.data.vertices)}")
    print(f"   Number of polygons: {len(body.data.polygons)}")
    
    # Check vertex groups
    print(f"\n2. Vertex Groups:")
    vg_names = [vg.name for vg in body.vertex_groups]
    print(f"   Total vertex groups: {len(vg_names)}")
    
    # Check for expected vertex group names
    expected_groups = ['Head', 'Neck', 'Spine', 'LeftShoulder', 'RightShoulder']
    for group in expected_groups:
        found = any(group in vg or f"mixamorig:{group}" in vg for vg in vg_names)
        print(f"   {group}: {'Found' if found else 'Missing'}")
    
    # Check materials
    print(f"\n3. Materials:")
    print(f"   Number of material slots: {len(body.material_slots)}")
    for i, slot in enumerate(body.material_slots):
        if slot.material:
            if slot.material.use_nodes:
                principled = next((node for node in slot.material.node_tree.nodes 
                                 if node.type == 'BSDF_PRINCIPLED'), None)
                if principled:
                    color = principled.inputs['Base Color'].default_value[:3]
                    print(f"   Slot {i}: {slot.material.name} (RGB: {[round(c, 3) for c in color]})")
                else:
                    print(f"   Slot {i}: {slot.material.name} (No Principled BSDF node)")
            else:
                print(f"   Slot {i}: {slot.material.name} (No nodes)")
        else:
            print(f"   Slot {i}: Empty")
    
    # Check material assignments
    print(f"\n4. Material Assignments:")
    material_counts = {i: 0 for i in range(len(body.material_slots))}
    for poly in body.data.polygons:
        material_counts[poly.material_index] = material_counts.get(poly.material_index, 0) + 1
    
    print("   Polygons per material index:")
    for idx, count in material_counts.items():
        print(f"   Material index {idx}: {count} polygons")
    
    # Check for potential issues
    print(f"\n5. Potential Issues:")
    issues = []
    
    if len(body.material_slots) == 0:
        issues.append("No material slots found")
    
    if not any(material_counts.values()):
        issues.append("No polygons have material assignments")
    
    if len(vg_names) < 10:  # Arbitrary threshold for minimum expected vertex groups
        issues.append("Very few vertex groups found - might be missing rigging")
    
    if not issues:
        print("   No major issues detected")
    else:
        for issue in issues:
            print(f"   ⚠️ {issue}")

# Run diagnostic
diagnose_model()
