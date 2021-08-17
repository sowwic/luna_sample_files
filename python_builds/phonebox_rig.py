import pymel.core as pm
from luna import Logger
import luna_rig
from luna_rig.core import pybuild
from luna_rig import importexport


class RigBuild(pybuild.PyBuild):

    SPACE_MATRIX_METHOD = False

    def run(self):
        # Visibility attrs
        self.character.root_control.transform.addAttr("boxVisibility", at="bool", k=True, dv=True)
        self.character.root_control.transform.addAttr("phoneVisibility", at="bool", k=True, dv=True)
        self.character.root_control.transform.boxVisibility.connect("static_geo_grp.visibility")
        self.character.root_control.transform.phoneVisibility.connect("phone_box_grp.visibility")

        self.phone = luna_rig.components.SimpleComponent.create(character=self.character, side="c", name="phone")
        self.phone_hand_ctl = self.phone.add_control("c_phone_hand_00_loc", "hand", as_hook=True, delete_guide=False)
        self.phone_hand_ctl.constrain_geometry("Phone_lp")
        self.phone_base_ctl = self.phone.add_control("c_phone_hand_00_loc", "base", as_hook=True, delete_guide=True)

        self.cord = luna_rig.components.WireComponent.create(character=self.character,
                                                             side="c",
                                                             name="cord",
                                                             curve="c_cord_00_crv",
                                                             geometry="PhoneCable_lp")

        # Constrain static geo
        self.character.root_control.constrain_geometry("static_geo_grp")
        self.character.root_control.constrain_geometry("phone_box_grp")

        # Spaces
        self.cord.shape_controls[-1].add_space(self.phone_hand_ctl, "hand", via_matrix=self.SPACE_MATRIX_METHOD)
        self.phone_hand_ctl.add_world_space()
        self.phone_hand_ctl.add_space(self.cord.root_control, "Cord Root", via_matrix=self.SPACE_MATRIX_METHOD)
        self.phone_hand_ctl.add_space(self.phone_base_ctl, "Base", via_matrix=self.SPACE_MATRIX_METHOD)

        # Attach to skeleton
        for comp in self.character.meta_children:
            comp.attach_to_skeleton()

    def post(self):
        importexport.CtlShapeManager().import_asset_shapes()
        self.character.set_publish_mode(True)


if __name__ == "__main__":
    RigBuild("enviroment", "Phonebox")
