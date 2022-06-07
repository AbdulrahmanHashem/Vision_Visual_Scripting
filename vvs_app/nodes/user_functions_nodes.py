from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from nodeeditor.node_editor_widget import *


class UserFunction(MasterNode):
    icon = "event.png"
    name = "user_function"
    category = "User_Function"
    sub_category = "User_Function"
    node_usage = 'function'
    declaration = "function"

    def __init__(self, scene, isSetter, node_usage='function'):
        if not self.node_usage: self.node_usage = node_usage
        if isSetter:
            super().__init__(scene, inputs=[], outputs=[0])
            self.getNodeCode = self.write_function
        else:
            super().__init__(scene, inputs=[0], outputs=[0])
            self.getNodeCode = self.call_function

        self.is_setter = isSetter

    def write_function(self):
        childCode = self.get_other_socket_code(0)
        raw_code = "Empty"
        L_P = "{"
        R_P = "}"

        if self.syntax == "Python":
            python_code = f"""
def {self.name}(){self.get_return()}:
{Indent(childCode)}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
{self.get_return()} {self.name}()
{L_P}
{Indent(childCode)}
{R_P}"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
fn {self.name}(){self.get_return()}
{L_P}
{Indent(childCode)}
{R_P}"""
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)

    def call_function(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        raw_code = "Empty"

        if self.syntax == "Python":
            python_code = f"""
{self.name}()
{brotherCode}"""
            raw_code = python_code

        elif self.syntax == "C++":
            cpp_code = f"""
{self.name}();
{brotherCode}"""
            raw_code = cpp_code

        elif self.syntax == "Rust":
            rust_code = f"""
{self.name}();
{brotherCode}"""
            raw_code = rust_code

        return self.grNode.highlight_code(raw_code)

# class UserFunction(MasterNode):
#     icon = "event.png"
#     name = "user_function"
#     category = "User_Function"
#     sub_category = "User_Function"
#     node_color = "#90FF1010"
#
#     def __init__(self, scene, isSetter):
#         super().__init__(scene, inputs=[], outputs=[0]) if isSetter else super().__init__(scene, inputs=[0], outputs=[0])
#         self.is_setter = isSetter
#         self.user_node = True
#
#     def getNodeCode(self):
#         (set_get, self.showCode) = ("set", True) if self.is_setter else ("call", False)
#
#         syn = self.scene.node_editor.Languages["function syntax"][set_get][self.scene.node_editor.Languages["Languages"][self.syntax]].\
#             replace("name", self.name).replace("return", self.get_datatype(True)).replace("content", f"\n{Indent(self.get_other_socket_code(0))}").replace("{", "\n{").replace("}", "\n}")
#
#         raw_code = syn
#         return self.grNode.highlight_code(raw_code)