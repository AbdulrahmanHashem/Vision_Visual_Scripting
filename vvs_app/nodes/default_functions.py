from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QTreeWidgetItem, QListWidgetItem, QAbstractItemView
from qtpy.QtGui import *

from nodeeditor.node_socket import Socket, Socket_Types
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from textwrap import *

FontSize = 14
FontFamily = "Roboto"
mathOperators = "#70307030"
logicOperators = "#30000050"

L_P = "{"
R_P = "}"


def Indent(String):
    return indent(String, '     ')


# Process
class IfStatement(MasterNode):
    icon = "if.png"
    name = "IF Statement"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#90FF5733"
    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])
        self.set_input_label_text(0, "Action"),                 self.set_output_label_text(0, "True")
        self.set_input_label_text(1, "Condition"),              self.set_output_label_text(1, "False")

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        condition = self.get_my_input_code(1)
        true = self.get_other_socket_code(0)
        false = self.get_other_socket_code(1)
        if self.syntax == "Python":
            else_code = ''
            if self.isOutputConnected(1):
                else_code = f"""
else:
{Indent(false)}"""
            python_code = f"""
if {condition}:
{Indent(true)}
{else_code}"""

            raw_code = python_code
        elif self.syntax == "C++":
            else_code = ''
            if self.isOutputConnected(1):
                else_code = f"""
else
{L_P}
{Indent(false)}
{R_P}"""

            CPP_code = f"""
if ({condition})
{L_P}
{Indent(true)}
{R_P}
{else_code}"""

            raw_code = CPP_code
        elif self.syntax == "Rust":
            else_code = ''
            if self.isOutputConnected(1):
                else_code = f"""
else 
{L_P}
{Indent(false)}
{R_P}"""

            Rust_code = f"""
if {condition} 
{L_P}
{Indent(true)}
{R_P}
{else_code}"""

            raw_code = Rust_code
        return self.grNode.highlight_code(raw_code)


class ForLoop(MasterNode):
    icon = "Loop.png"
    name = "For Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        range = self.get_my_input_code(1)
        loopCode = self.get_other_socket_code(0)

        if self.syntax == "Python":

            python_code = f"""
for item in range({range}):
{Indent(loopCode)}"""
            raw_code = python_code
        elif self.syntax == "C++":
            CPP_code = f"""
for (int i=0;i&lt;{range};i++)
{L_P}
{Indent(loopCode)}
{R_P}"""
            raw_code = CPP_code
        elif self.syntax == "Rust":
            Rust_code = f"""
for index in 0..{range}
{L_P}
{Indent(loopCode)}
{R_P}"""
            raw_code = Rust_code

        return self.grNode.highlight_code(raw_code)


class ForEachLoop(MasterNode):
    icon = "Loop.png"
    name = "For Each Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5], outputs=[0, 6])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        array = self.get_my_input_code(1)
        loopCode = self.get_other_socket_code(0)
        self.outputs[1].socket_code = item_name = 'item'

        if self.syntax == "Python":
            python_code = f"""
for {item_name} in {array}:
{Indent(loopCode)}"""
            raw_code = python_code
        elif self.syntax == "C++":
            CPP_code = f"""
for (auto {item_name} : {array})
{L_P}
{Indent(loopCode)}
{R_P}"""
            raw_code = CPP_code
        elif self.syntax == "Rust":
            Rust_code = f"""
for {item_name} in &{array} 
{L_P}
{Indent(loopCode)}
{R_P}"""
            raw_code = Rust_code
        return self.grNode.highlight_code(raw_code)


class ConvertDataType(MasterNode):
    icon = "ConvertDataType.png"
    name = "Convert Data Type"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 6], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        inputName = self.get_my_input_code(1)

        other_input_name = ""
        type = ""
        if self.getInputs(2):
            other_input_name = self.get_my_input_code(2)
            current_syntax = self.scene.node_editor.return_types["Languages"].index(self.syntax)
            type = self.scene.node_editor.return_types[self.getInputs(2)[0].node_usage][current_syntax].replace(" -> ", "")
        equal = " = "
        if inputName == "" or inputName is None:
            equal = ''

        if self.syntax == "Python":
            python_code = f"""
{other_input_name}{equal} {type}({inputName})
{brotherCode}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
istringstream({inputName}) >> {other_input_name};
{brotherCode}"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
let {other_input_name}: {type} {equal} {inputName}.trim().parse().unwrap();
{brotherCode}"""
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)


# Logic
class And(MasterNode):
    icon = "and.png"
    name = "And"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)
        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A} and {B})"
            raw_code = python_code

        elif ["C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A} && {B})"
            raw_code = code

        return raw_code


class GreaterThan(MasterNode):
    icon = "more_than.png"
    name = "Greater Than"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}&gt;{B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


class LessThan(MasterNode):
    icon = "less_than.png"
    name = "Less Than"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}&lt;{B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


class Equal(MasterNode):
    icon = "equal.png"
    name = "Equal"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}=={B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


# Math
class Add(MasterNode):
    icon = "add.png"
    name = "Add"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[6])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}+{B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


class Sub(MasterNode):
    icon = "sub.png"
    name = "Subtract"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[6])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}-{B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


class Mul(MasterNode):
    icon = "mul.png"
    name = "Multiply"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[6])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}*{B})"
            raw_code = code

        return self.grNode.highlight_code(raw_code)


class Div(MasterNode):
    icon = "divide.png"
    name = "Divide"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[6])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if ["Python", "C++", "Rust"].__contains__(self.syntax):
            code = self.outputs[0].socket_code = f"({A}/{B})"
            raw_code = code


        return self.grNode.highlight_code(raw_code)


# Input
class UserInput(MasterNode):
    icon = "user input.png"
    name = "User Input"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#505050"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 4], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        inputName = self.get_my_input_code(1)
        inputCode = self.get_my_input_code(2)

        equal = " = "
        rr = f'\nprintln!("{inputCode}");'
        if inputName == "" or inputName is None:
            equal = ''
        if inputCode == "" or inputCode is None:
            rr = ''


        if self.syntax == "Python":
            python_code = f"""
{inputName}{equal}input("{inputCode}")
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
cout &lt;&lt; "{inputCode}", cin >> {inputName};
{brotherCode}"""

            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
let mut {inputName} = String::new();{rr}
stdin().read_line(&mut {inputName}).unwrap();
let {inputName}: &str = &{inputName}[..];
{brotherCode}"""

            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)


class RawCode(MasterNode):
    icon = "Row Code.png"
    name = "Raw Code"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#303030"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        inputCode = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = CPP_code
        elif self.syntax == "Rust":
            Rust_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = Rust_code
        return self.grNode.highlight_code(raw_code)


# Output
class Print(MasterNode):
    icon = "print.png"
    name = "Print"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        printCode = self.get_my_input_code(1)

        if not self.isInputConnected(1): printCode = f'"{printCode}"'
        if self.syntax == "Python":
            python_code = f"""
print({printCode})
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
cout &lt;&lt; {printCode};
{brotherCode}"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            connected = self.isInputConnected(1)
            if connected: printCode = '"{}", ' + printCode
            rust_code = f"""
println!({printCode});
{brotherCode}"""
            raw_code = rust_code

        return self.grNode.highlight_code(raw_code)


class Return(MasterNode):
    icon = "return.png"
    name = "Return"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        return_code = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = f"""
return {return_code}
"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
return {return_code};
"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
return {return_code};
"""
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)


# List Operators
class MakeList(MasterNode):
    icon = ""
    name = "Make List"
    category = "FUNCTION"
    sub_category = "List Operator"

    def __init__(self, scene):
        super().__init__(scene, inputs=[6], outputs=['array'])
        self.inputs[0].is_multi_edges = True
        self.list = []

    def input_output_symmetry(self):
        if self.NodeAtOutput(0) and self.NodeAtOutput(0).node_usage:
            if self.inputs[0].socket_type != Socket_Types[self.NodeAtOutput(0).node_usage]:
                for edge in self.inputs[0].socketEdges:
                    edge.remove()
                self.remove_socket(self.inputs[0])
                socket = Socket(node=self, index=len(self.inputs), position=self.input_socket_position,
                                socket_type=Socket_Types[self.NodeAtOutput(0).node_usage], multi_edges=True,
                                count_on_this_node_side=len(self.inputs), is_input=True)
                self.inputs.append(socket)

    def properties(self):
        self.nodes_list = QListWidget()
        self.nodes_list.setDragDropMode(QAbstractItemView.InternalMove)

        self.scene.masterRef.proprietiesWdg.clear_properties()
        self.scene.masterRef.proprietiesWdg.create_properties_widget("List Items", self.nodes_list)
        if self.getInputs(0):
            for node in [edge.getOtherSocket(self.inputs[0]).node for edge in self.inputs[0].socketEdges]:
                item = QListWidgetItem(node.name, self.nodes_list)
                item.setData(50, node.id)
        self.nodes_list.model().rowsMoved.connect(self.change_order)
        self.change_order()

    def change_order(self):
        list1 = []
        for i in range(self.nodes_list.count()):
            list1.append(self.nodes_list.item(i).data(50))

        dic = {}
        for edge in self.inputs[0].socketEdges:
            dic[edge.getOtherSocket(self.inputs[0]).node.id] = edge

        self.inputs[0].socketEdges = [dic[index] for index in list1]

        self.getNodeCode()
        self.scene.node_editor.UpdateTextCode()

    def getNodeCode(self):
        self.input_output_symmetry()
        self.list.clear()
        for edge in self.inputs[0].socketEdges:
            self.list.append(edge.getOtherSocket(self.inputs[0]).node.name)

        raw_code = "Empty"
        self.showCode = False
        return_code = ''
        for socket in self.list:
            socket_code = socket

            if socket_code != '':
                socket_code = str(socket_code) + ', '
            return_code = return_code + socket_code

        if return_code.endswith(', '):
            return_code = return_code[:-2]
        code = f'{return_code}'
        raw_code = code
        self.outputs[0].socket_code = code
        return self.grNode.highlight_code(raw_code)


class ListAppend(MasterNode):
    icon = "add.png"
    name = "Append"
    category = "FUNCTION"
    sub_category = "List Operator"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5, 6], outputs=[0])

    def change_socket(self):
        if not self.inputs[2].socket_type == Socket_Types[self.getInput(1).node_usage]:
            self.remove_socket(self.inputs[2])
            for socket in self.inputs:
                socket.index = self.inputs.index(socket)
                socket.setSocketPosition()

            socket = Socket(node=self, index=2, position=self.input_socket_position,
                            socket_type=self.getInput(1).node_usage, multi_edges=self.input_multi_edged,
                            count_on_this_node_side=2, is_input=True)
            self.inputs.append(socket)
            self.grNode.AutoResizeGrNode()

    def getNodeCode(self):
        if self.getInput(1):
            self.change_socket()
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        o_list = self.get_my_input_code(1)
        new_value = self.get_my_input_code(2)

        next = self.get_other_socket_code(0)

        if self.syntax == "Python":
            L_SP = "["
            R_SP = "]"
            if self.isInputConnected(2):
                L_SP = ""
                R_SP = ""
            python_code = f"""
{o_list} = numpy.append({o_list}, {L_SP}{new_value}{R_SP})
{next}"""
            raw_code = python_code
        elif self.syntax == "C++":
            if self.getInputs(2):
                if self.getInputs(2)[0].node_structure == "single value":
                    new_value = f"1, {new_value}"
                else:
                    new_value = f"{new_value}.begin(),{new_value}.end()"
            CPP_code = f"""
{o_list}.assign(1, {new_value});
{next}"""
            raw_code = CPP_code
        elif self.syntax == "Rust":
            if self.getInputs(2):
                if self.getInputs(2)[0].node_structure == "single value":
                    rust_code = f"""
{o_list}.push({new_value});
{next}"""
                else:
                    rust_code = f"""
for item in &{new_value}
{L_P}
{Indent(f"{o_list}.push(item);")}
{R_P}
{next}"""
            else:
                rust_code = f"""
{o_list}.push({new_value});
{next}
                """
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)


class ListRemove(MasterNode):
    icon = "sub.png"
    name = "Remove"
    category = "FUNCTION"
    sub_category = "List Operator"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5, 6], outputs=[0])

    def change_socket(self):
        if not self.inputs[2].socket_type == Socket_Types[self.getInput(1).node_usage]:
            self.remove_socket(self.inputs[2])
            for socket in self.inputs:
                socket.index = self.inputs.index(socket)
                socket.setSocketPosition()

            socket = Socket(node=self, index=2, position=self.input_socket_position,
                            socket_type=self.getInput(1).node_usage, multi_edges=self.input_multi_edged,
                            count_on_this_node_side=2, is_input=True)
            self.inputs.append(socket)
            self.grNode.AutoResizeGrNode()

    def getNodeCode(self):
        if self.getInput(1):
            self.change_socket()
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        o_list = self.get_my_input_code(1)
        remove_value = self.get_my_input_code(2)
        next = self.get_other_socket_code(0)
        if self.syntax == "Python":
            python_code = f"""
index = numpy.where({o_list} == {remove_value})
{o_list} = numpy.delete({o_list}, index[0][0])
{next}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
{o_list}.remove({remove_value});
{next}"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
let index = {o_list}.iter().position(|x| *x == {remove_value}).unwrap();
{o_list}.remove(index);
{next}"""
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)



# Khyria Efforts
# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""
