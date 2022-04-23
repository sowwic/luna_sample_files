from luna import Logger
import pymel.core as pm
import luna_rig
from luna_rig.core import pybuild
from luna_rig import importexport
from luna_rig.functions import common_setup


class RigBuild(pybuild.PyBuild):

    MATRIX_SPACE_METHOD = False

    def run(self):
        importexport.BlendShapeManager.import_all()
        self.spine = luna_rig.components.FKIKSpineComponent.create(start_joint="c_pelvis_00_jnt",
                                                                   end_joint="c_spine_03_jnt",
                                                                   character=self.character,
                                                                   forward_axis="x",
                                                                   up_axis="y")
        self.spine_stretch = luna_rig.components.IKSplineStretchComponent.create(
            self.spine, switch_control=self.spine.root_control)

        self.left_clavicle = luna_rig.components.FKComponent.create(side="l",
                                                                    name="clavicle",
                                                                    start_joint="l_clavicle_00_jnt",
                                                                    end_joint="l_clavicle_00_jnt",
                                                                    add_end_ctl=True,
                                                                    lock_translate=False,
                                                                    meta_parent=self.spine,
                                                                    hook=self.spine.Hooks.CHEST,
                                                                    character=self.character)
        self.right_clavicle = luna_rig.components.FKComponent.create(side="r",
                                                                     name="clavicle",
                                                                     start_joint="r_clavicle_00_jnt",
                                                                     end_joint="r_clavicle_00_jnt",
                                                                     add_end_ctl=True,
                                                                     lock_translate=False,
                                                                     meta_parent=self.spine,
                                                                     hook=self.spine.Hooks.CHEST,
                                                                     character=self.character)
        self.left_arm = luna_rig.components.FKIKComponent.create(side="l",
                                                                 name="arm",
                                                                 start_joint="l_arm_00_jnt",
                                                                 end_joint="l_arm_02_jnt",
                                                                 meta_parent=self.left_clavicle,
                                                                 hook=-1,
                                                                 character=self.character)
        self.right_arm = luna_rig.components.FKIKComponent.create(side="r",
                                                                  name="arm",
                                                                  start_joint="r_arm_00_jnt",
                                                                  end_joint="r_arm_02_jnt",
                                                                  meta_parent=self.right_clavicle,
                                                                  hook=-1,
                                                                  character=self.character)
        self.left_leg = luna_rig.components.FKIKComponent.create(side="l",
                                                                 name="leg",
                                                                 start_joint="l_leg_00_jnt",
                                                                 end_joint="l_leg_02_jnt",
                                                                 ik_world_orient=True,
                                                                 meta_parent=self.spine,
                                                                 hook=self.spine.Hooks.HIPS,
                                                                 character=self.character)
        self.left_foot = luna_rig.components.FootComponent.create(meta_parent=self.left_leg,
                                                                  start_joint="l_foot_00_jnt",
                                                                  end_joint="l_foot_01_jnt",
                                                                  rv_chain="l_rv_foot_00_jnt",
                                                                  foot_locators_grp="l_foot_roll_00_grp")
        self.right_leg = luna_rig.components.FKIKComponent.create(side="r",
                                                                  name="leg",
                                                                  start_joint="r_leg_00_jnt",
                                                                  end_joint="r_leg_02_jnt",
                                                                  ik_world_orient=True,
                                                                  meta_parent=self.spine,
                                                                  hook=self.spine.Hooks.HIPS,
                                                                  character=self.character)
        self.right_foot = luna_rig.components.FootComponent.create(meta_parent=self.right_leg,
                                                                   start_joint="r_foot_00_jnt",
                                                                   end_joint="r_foot_01_jnt",
                                                                   rv_chain="r_rv_foot_00_jnt",
                                                                   foot_locators_grp="r_foot_roll_00_grp")

        self.head = luna_rig.components.HeadComponent.create(start_joint="c_neck_00_jnt",
                                                             end_joint="c_head_01_jnt",
                                                             head_joint_index=-2,
                                                             meta_parent=self.spine,
                                                             hook=self.spine.Hooks.CHEST,
                                                             character=self.character)

        # Twist components
        # Arms
        self.left_arm_upper_twist = luna_rig.components.TwistComponent.create(self.left_arm,
                                                                              name="upper_twist",
                                                                              start_joint=self.left_arm.ctl_chain[0],
                                                                              end_joint=self.left_arm.ctl_chain[1],
                                                                              start_object=self.left_arm.in_hook.transform)
        self.left_arm_lower_twist = luna_rig.components.TwistComponent.create(self.left_arm,
                                                                              name="lower_twist",
                                                                              start_joint=self.left_arm.ctl_chain[1],
                                                                              end_joint=self.left_arm.ctl_chain[-1])
        self.right_arm_upper_twist = luna_rig.components.TwistComponent.create(self.right_arm,
                                                                               name="upper_twist",
                                                                               start_joint=self.right_arm.ctl_chain[0],
                                                                               end_joint=self.right_arm.ctl_chain[1],
                                                                               start_object=self.right_arm.in_hook.transform)
        self.right_arm_lower_twist = luna_rig.components.TwistComponent.create(self.right_arm,
                                                                               name="lower_twist",
                                                                               start_joint=self.right_arm.ctl_chain[1],
                                                                               end_joint=self.right_arm.ctl_chain[-1])
        # Legs
        self.left_leg_upper_twist = luna_rig.components.TwistComponent.create(self.left_leg,
                                                                              name="upper_twist",
                                                                              start_joint=self.left_leg.ctl_chain[0],
                                                                              end_joint=self.left_leg.ctl_chain[1],
                                                                              start_object=self.left_leg.in_hook.transform)
        self.left_leg_lower_twist = luna_rig.components.TwistComponent.create(self.left_leg,
                                                                              name="lower_twist",
                                                                              start_joint=self.left_leg.ctl_chain[1],
                                                                              end_joint=self.left_leg.ctl_chain[-1])

        self.right_leg_upper_twist = luna_rig.components.TwistComponent.create(self.right_leg,
                                                                               name="upper_twist",
                                                                               start_joint=self.right_leg.ctl_chain[0],
                                                                               end_joint=self.right_leg.ctl_chain[1],
                                                                               start_object=self.right_leg.in_hook.transform,
                                                                               mirrored_chain=True)
        self.right_leg_lower_twist = luna_rig.components.TwistComponent.create(self.right_leg,
                                                                               name="lower_twist",
                                                                               start_joint=self.right_leg.ctl_chain[1],
                                                                               end_joint=self.right_leg.ctl_chain[-1],
                                                                               mirrored_chain=True)
        # Hands
        # Left
        self.left_hand = luna_rig.components.HandComponent.create(meta_parent=self.left_arm,
                                                                  hook=self.left_arm.Hooks.END_JNT,
                                                                  character=self.character)
        self.left_hand.add_fk_finger("l_thumb_finger_00_JNT", name="thumb")
        self.left_hand.add_fk_finger("l_index_finger_00_JNT", name="index")
        self.left_hand.add_fk_finger("l_middle_finger_00_JNT", name="middle")
        self.left_hand.add_fk_finger("l_ring_finger_00_JNT", name="ring")
        self.left_hand.add_fk_finger("l_pinky_finger_00_JNT", name="pinky")
        # Right
        self.right_hand = luna_rig.components.HandComponent.create(meta_parent=self.right_arm,
                                                                   hook=self.right_arm.Hooks.END_JNT,
                                                                   character=self.character)
        self.right_hand.add_fk_finger("r_thumb_finger_00_JNT", name="thumb")
        self.right_hand.add_fk_finger("r_index_finger_00_JNT", name="index")
        self.right_hand.add_fk_finger("r_middle_finger_00_JNT", name="middle")
        self.right_hand.add_fk_finger("r_ring_finger_00_JNT", name="ring")
        self.right_hand.add_fk_finger("r_pinky_finger_00_JNT", name="pinky")

        # Face
        self.face = luna_rig.components.SimpleComponent.create(side="c",
                                                               name="face",
                                                               meta_parent=self.head,
                                                               hook=self.head.Hooks.HEAD,
                                                               character=self.character)
        # self.face_base_ctl = self.face.add_control("c_face_ctls_loc", "base", delete_guide=True)
        self.jaw = luna_rig.components.FKComponent.create(name="jaw",
                                                          start_joint="c_jaw_00_JNT",
                                                          end_joint="c_jaw_01_JNT",
                                                          add_end_ctl=False,
                                                          lock_translate=False,
                                                          meta_parent=self.head,
                                                          hook=self.head.Hooks.HEAD)

        # Clavicle add-ons
        self.left_clavicle.add_auto_aim(self.left_arm.ik_control, default_value=5.0)
        self.right_clavicle.add_auto_aim(self.right_arm.ik_control, default_value=5.0)

        # Arms legs FK0 addons:
        self.left_arm.add_fk_orient_switch()
        self.right_arm.add_fk_orient_switch()
        self.left_leg.add_fk_orient_switch()
        self.right_leg.add_fk_orient_switch()

        # Head add-on
        self.head.add_orient_attr()

        # Body spaces
        # Arms
        common_setup.basic_limbs_spaces(arm_components=[self.left_arm, self.right_arm],
                                        leg_components=[self.left_leg, self.right_leg],
                                        spine=self.spine)

        # Attach to skeleton
        self.character.add_root_motion(self.spine.root_control, root_joint="c_root_00_jnt")
        for comp in self.character.meta_children:
            comp.attach_to_skeleton()

        # Data import
        importexport.DrivenPoseManager.import_all()
        importexport.SkinManager.import_all()
        # importexport.NgLayersManager.import_all()

    def post(self):
        importexport.CtlShapeManager.import_asset_shapes()
        self.character.set_publish_mode(True)


if __name__ == "__main__":
    RigBuild("character", "Ninja")
