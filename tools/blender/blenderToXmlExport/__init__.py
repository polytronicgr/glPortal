#!BPY
bl_info = {
    "name":         "GlPortal XML Format",
    "author":       "Henry Hirsch",
    "blender":      (2, 6, 3),
    "version":      (0, 0, 1),
    "location":     "File > Import-Export",
    "description":  "GlPortal XML Format",
    "category":     "Import-Export"
}

import bpy
from bpy_extras.io_utils import ExportHelper
import xml.etree.cElementTree as tree
import xml.dom.minidom as minidom
import os
import mathutils
import string
from mathutils import Vector

class ExportMyFormat(bpy.types.Operator, ExportHelper):
    bl_idname = "export_glportal_xml.xml"
    bl_label = "GlPortal XML Format"
    bl_options = {'PRESET'}
    filename_ext = ".xml"

    def execute(self, context):
       dir = os.path.dirname(self.filepath)
       objects = context.scene.objects
       root = tree.Element("map")
       textureElement = tree.SubElement(root, "texture")
       textureElement.set("source", "tiles.png")
       for object in objects:
           object.select = False
       for object in objects:
           if "." in object.name:
               mapObjectType = object.name.split(".")[0]
           else:
               mapObjectType = object.name
           if mapObjectType == "Lamp":
               lightElement = tree.SubElement(root, "light")
               lightElement.set("r", str(1))
               lightElement.set("g", str(1))
               lightElement.set("b", str(1))
               lightVectorElement = tree.SubElement(lightElement, "vector")
               matrix = object.matrix_world
               vector = Vector((object.location[0],object.location[1],object.location[2]))
               globalVector = matrix * vector
               lightVectorElement.set("x", str(globalVector.x))
               lightVectorElement.set("y", str(globalVector.y))
               lightVectorElement.set("z", str(globalVector.z))
           elif mapObjectType == "Camera":
               matrix = object.matrix_world
               vector = Vector((object.location[0],object.location[1],object.location[2]))
               globalVector = matrix * vector
               cameraElement = tree.SubElement(root, "spawn")
               spawnVectorElement = tree.SubElement(cameraElement, "vector")               
               spawnVectorElement.set("x", str(globalVector.x))
               spawnVectorElement.set("y", str(globalVector.y))
               spawnVectorElement.set("z", str(globalVector.z))               
           elif mapObjectType == "Cube":
               matrix = object.matrix_world
               boundingBox = object.bound_box
               
               boundingBoxBeginVector = Vector((boundingBox[0][0], boundingBox[0][1], boundingBox[0][2]))
               boundingBoxEndVector   = Vector((boundingBox[6][0], boundingBox[6][1], boundingBox[6][2]))
               transBoundingBoxBeginVector = matrix * boundingBoxBeginVector
               transBoundingBoxEndVector   = matrix * boundingBoxEndVector
               object.select = True
               boxElement = tree.SubElement(textureElement, "box")
               boundingBox = object.bound_box
               vectorElement = tree.SubElement(boxElement, "vector")
               vectorElement.set("x", str(transBoundingBoxBeginVector.x))
               vectorElement.set("y", str(transBoundingBoxBeginVector.y))
               vectorElement.set("z", str(transBoundingBoxBeginVector.z))
               endVectorElement = tree.SubElement(boxElement, "vector")
               endVectorElement.set("x", str(transBoundingBoxEndVector.x))
               endVectorElement.set("y", str(transBoundingBoxEndVector.y))
               endVectorElement.set("z", str(transBoundingBoxEndVector.z))
               object.select = False
               
       xml = minidom.parseString(tree.tostring(root))

       file = open(self.filepath, "w")
       file.write(xml.toprettyxml())
       file.close()

       return {'FINISHED'}

    
def menu_func(self, context):
    self.layout.operator(ExportMyFormat.bl_idname, text="GlPortal Map Format(.xml)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
