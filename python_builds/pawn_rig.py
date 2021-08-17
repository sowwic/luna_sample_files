import luna_rig
from luna_rig.core import pybuild
from luna_rig import importexport


class RigBuild(pybuild.PyBuild):

    SPACE_MATRIX_METHOD = False

    def run(self):
        self.base = luna_rig.components.SimpleComponent.create(name="body")
        self.root_ctl = self.base.add_control("c_body_00_jnt", "root", as_hook=True, bind_joint="c_body_00_jnt", orient_axis="y")
        self.barel_ctl = self.base.add_control("c_barel_00_jnt",
                                               "barel",
                                               bind_joint="c_barel_00_jnt",
                                               parent=self.root_ctl,
                                               shape="arrow",
                                               orient_axis="y")
        self.muzzle_ctl = self.base.add_control("c_barel_01_jnt",
                                                "muzzle",
                                                bind_joint="c_barel_01_jnt",
                                                parent=self.barel_ctl,
                                                attributes=["tx"])
        self.barel_ctl.add_orient_switch(self.character.world_locator, local_parent=self.root_ctl)
        self.left_front_leg = luna_rig.components.FKIKComponent.create(name="front_leg",
                                                                       side="l",
                                                                       start_joint="l_front_leg_00_jnt",
                                                                       end_joint="l_front_leg_02_jnt",
                                                                       ik_world_orient=True,
                                                                       meta_parent=self.base,
                                                                       hook=0)
        self.right_front_leg = luna_rig.components.FKIKComponent.create(name="front_leg",
                                                                        side="r",
                                                                        start_joint="r_front_leg_00_jnt",
                                                                        end_joint="r_front_leg_02_jnt",
                                                                        ik_world_orient=True,
                                                                        meta_parent=self.base,
                                                                        hook=0)
        self.left_back_leg = luna_rig.components.FKIKComponent.create(name="front_leg",
                                                                      side="l",
                                                                      start_joint="l_back_leg_00_jnt",
                                                                      end_joint="l_back_leg_02_jnt",
                                                                      ik_world_orient=True,
                                                                      meta_parent=self.base,
                                                                      hook=0)
        self.right_back_leg = luna_rig.components.FKIKComponent.create(name="front_leg",
                                                                       side="r",
                                                                       start_joint="r_back_leg_00_jnt",
                                                                       end_joint="r_back_leg_02_jnt",
                                                                       ik_world_orient=True,
                                                                       meta_parent=self.base,
                                                                       hook=0)
        for leg_comp in self.character.get_meta_children(of_type=luna_rig.components.FKIKComponent):
            leg_comp.fk_controls[-1].group.hide()

        # Spaces
        for leg_comp in self.character.get_meta_children(of_type=luna_rig.components.FKIKComponent):
            # Pole vector
            leg_comp.pv_control.add_world_space(via_matrix=self.SPACE_MATRIX_METHOD)
            leg_comp.pv_control.add_space(leg_comp.ik_control, "IK", via_matrix=self.SPACE_MATRIX_METHOD)
            leg_comp.pv_control.add_space(self.root_ctl, "Body", via_matrix=self.SPACE_MATRIX_METHOD)
            # IK
            leg_comp.ik_control.add_world_space(via_matrix=self.SPACE_MATRIX_METHOD)
            leg_comp.ik_control.add_space(self.root_ctl, "Body", via_matrix=self.SPACE_MATRIX_METHOD)
            leg_comp.fk_controls[0].add_orient_switch(self.character.world_locator)

        self.character.add_root_motion(self.root_ctl, root_joint="c_root_00_jnt")
        for comp in self.character.meta_children:
            comp.attach_to_skeleton()

    def post(self):
        importexport.CtlShapeManager().import_asset_shapes()
        importexport.SkinManager().import_all()
        # importexport.NgLayersManager.import_all()
        self.character.set_publish_mode(True)


if __name__ == "__main__":
    RigBuild("character", "Pawn")
