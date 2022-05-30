from PyQt5.QtGui import QBrush, QColor

from vvs_app.nodes.default_functions import FontSize, FontFamily
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode

FloatColor = "#7000FF10"
IntegerColor = "#aa0070FF"
BooleanColor = "#aaFF1010"
StringColor = "#70FF10FF"


class FloatVar(MasterNode):
    icon = ""
    name = "user_float"
    node_return = "float"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = FloatColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[1]) if not isSetter else super().__init__(scene, inputs=[0, 1], outputs=[0, 1])
        self.is_setter = isSetter

    def getNodeCode(self):
        if self.is_setter:
            self.showCode = not self.isInputConnected(0)
            self.outputs[1].socket_code = self.name
        else:
            self.showCode = False
            raw_code = self.outputs[0].socket_code = self.name
            return raw_code

        brotherCode = self.get_other_socket_code(0)
        setInput = self.get_my_input_code(1)

        syn = self.scene.node_editor.Languages["variable syntax"][self.node_structure][self.scene.node_editor.Languages["Languages"][self.syntax]]\
            .replace("name", self.name).replace("data type", self.get_datatype()).replace("content", str(setInput)).replace("next", f"\n{brotherCode}")

        raw_code = syn
        return self.grNode.highlight_code(raw_code)


class IntegerVar(MasterNode):
    icon = ""
    name = "user_integer"
    node_return = "integer"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = IntegerColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[2]) if not isSetter else super().__init__(scene, inputs=[0, 2], outputs=[0, 2])
        self.is_setter = isSetter

    def getNodeCode(self):
        if self.is_setter:
            self.showCode = not self.isInputConnected(0)
            self.outputs[1].socket_code = self.name
        else:
            self.showCode = False
            raw_code = self.outputs[0].socket_code = self.name
            return raw_code

        brotherCode = self.get_other_socket_code(0)
        setInput = self.get_my_input_code(1)

        syn = self.scene.node_editor.Languages["variable syntax"][self.node_structure][self.scene.node_editor.Languages["Languages"][self.syntax]] \
            .replace("name", self.name).replace("data type", self.get_datatype()).replace("content", str(setInput)).replace(
            "next", f"\n{brotherCode}")

        raw_code = syn
        return self.grNode.highlight_code(raw_code)


class BooleanVar(MasterNode):
    icon = ""
    name = "user_boolean"
    node_return = "boolean"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = BooleanColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[3]) if not isSetter else super().__init__(scene, inputs=[0, 3], outputs=[0, 3])
        self.is_setter = isSetter

    def getNodeCode(self):
        if self.is_setter:
            self.showCode = not self.isInputConnected(0)
            self.outputs[1].socket_code = self.name
        else:
            self.showCode = False
            raw_code = self.outputs[0].socket_code = self.name
            return raw_code

        brotherCode = self.get_other_socket_code(0)
        setInput = self.get_my_input_code(1)

        syn = self.scene.node_editor.Languages["variable syntax"][self.node_structure][self.scene.node_editor.Languages["Languages"][self.syntax]] \
            .replace("name", self.name).replace("data type", self.get_datatype()).replace("content", str(setInput)).replace(
            "next", f"\n{brotherCode}")

        raw_code = syn
        return self.grNode.highlight_code(raw_code)


class StringVar(MasterNode):
    icon = ""
    name = "user_string"
    node_return = "string"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = StringColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[4]) if not isSetter else super().__init__(scene, inputs=[0, 4], outputs=[0, 4])
        self.is_setter = isSetter

    def getNodeCode(self):
        if self.is_setter:
            self.showCode = not self.isInputConnected(0)
            self.outputs[1].socket_code = self.name
        else:
            self.showCode = False
            raw_code = self.outputs[0].socket_code = self.name
            return raw_code

        brotherCode = self.get_other_socket_code(0)
        setInput = f"{chr(34)}{self.get_my_input_code(1)}{chr(34)}"

        syn = self.scene.node_editor.Languages["variable syntax"][self.node_structure][self.scene.node_editor.Languages["Languages"][self.syntax]] \
            .replace("name", self.name).replace("data type", self.get_datatype()).replace("content", setInput).replace(
            "next", f"\n{brotherCode}")

        raw_code = syn
        return self.grNode.highlight_code(raw_code)

