from textwrap import indent

from vvs_app.master_node import MasterNode

data_types_symbols = \
                    {
                        "primary":
                            {
                                "empty": ["", "void", ""],
                                "float": ["float", "float", "f64"],
                                "integer": ["int", "int", "i64"],
                                "boolean": ["bool", "boolean", "bool"],
                                "string": ["str", "string", "&str"],
                                "character": ["chr", "char", "char"]
                            },
                        "complex":
                            {
                                "list": ["list", "list", "list"],
                                "array": ["array", "array", "array"],
                                "dictionary": ["dict", "dictionary", "dict"],
                                "tuple": ["tuple", "tuple", "tuple"]
                            }
                    }

Languages = \
            {
                "Languages": {"Python": 1, "C++": 2, "Rust": 3},
                "extensions": ['.py', '.CPP', '.rs'],
                "return_syntax": [" -> ", "", " -> "],
                "data type":
                    {
                        "primary":
                            {
                                "initialize":
                                    {
                                        "single_value": [[[0], [0]],
                                                         "name = data type(content)\nnext",
                                                         "data type name = content;\nnext",
                                                         "let name: data type = content;\nnext"],
                                        "vector": [[[], []],
                                                   "name = numpy.array([content], data type)\nnext",
                                                   "vector &lt;data type&gt; name = {content};\nnext",
                                                   "let name: Vec&lt;data type&gt; = vec![content];\nnext"],
                                        "array": [[[0, 6], [0]],
                                                  "name array(data type, [content])\nnext",
                                                  "data type name[] = {content};\nnext",
                                                  "let name = [content];\nnext"]
                                    },
                                "use":
                                    [
                                        [[[0], [0]],
                                         "name",
                                         "name",
                                         "name"]
                                    ]
                            },
                        "complex":
                            {
                                "initialize":
                                    {
                                        "list": [[[], []],
                                                 "",
                                                 "",
                                                 ""],
                                        "dictionary": [[[], []],
                                                       "",
                                                       "",
                                                       ""],
                                        "tuple": [[[], []],
                                                  "tuple",
                                                  "tuple",
                                                  "tuple"]
                                    },
                                "use":
                                    {

                                    }
                            }
                    },
                "entity":
                    {
                        "function":
                            {
                                "initialize": [[[], [0]],
                                               "def name()return:\ncontent\n",
                                               "data type name() \n{\ncontent\n}",
                                               "fn name()return: \n{\ncontent\n}"],
                                "use": [[[0], [0]],
                                        "name()",
                                        "name();",
                                        "name();"]
                            },
                        "class":
                            {
                                "initialize": [[[], []],
                                               "",
                                               "",
                                               ""],
                                "use": [[[], []],
                                        "",
                                        "",
                                        ""]
                            }
                    },
                "statement":
                    {
                        "Process":
                            {
                                "If": [[[0, 3], [0, 0]],
                                       "\nif input1:\noutput1\noutput0",
                                       "\nif (input1)\n{output1\n}\noutput0",
                                       "\nif input1\n{output1\n}\noutput0",
                                       "#90FF5733"],
                                "While loop": [[[0, 3], [0, 0]],
                                               "\nwhile input1:\noutput1\noutput0",
                                               "\nwhile (input1)\n{output1\n}\noutput0",
                                               "\nwhile input1\n{output1\n}\noutput0",
                                               "#905050FF"],
                                "For loop": [[[0, 2], [0, 0]],
                                             "\nfor item in range(input1):\noutput1\noutput0",
                                             "\nfor (int i=0;i&lt;input1;i++)\n{output1\n}\noutput0",
                                             "\nfor index in 0..input1\n{output1\n}\noutput0",
                                             "#905050FF"],
                                "For each loop": [[[0, 5, 4], [0, 0, 6]],
                                                  "\nfor input2 in input1:\noutput1\noutput0",
                                                  "\nfor (auto input2 : input1)\n{output1\n}\noutput0",
                                                  "\nfor input2 in &input1\n{output1\n}\noutput0",
                                                  "#905050FF"],
                                "Else": [[[0], [0, 0]],
                                         "\nelse:\noutput1\noutput0",
                                         "\nelse \n{output1\n}\noutput0",
                                         "\nelse \n{output1\n}\noutput0",
                                         "#90FF5733"],
                                "Elif": [[[0, 3], [0, 0]],
                                         "\nelif input1:\noutput1\noutput0",
                                         "\nelse if (input1)\n{output1\n}\noutput0",
                                         "\nelse if (input1)\n{output1\n}\noutput0",
                                         "#90FF5733"],
                                "ConvertDataType": [[[0, 6, 6], [0]],
                                                    "\ninput2 = input_type2(input1)\noutput0",
                                                    "\nistringstream(input1) >> input2;\noutput0",
                                                    "\nlet input2: input_type2 = input1.trim().parse().unwrap();\noutput0",
                                                    "#90FF5000"]
                            },
                        "Logic":
                            {
                                "And": [[[6, 6], [3]],
                                        "input0 and input1",
                                        "input0 and input1",
                                        "input0 && input1",
                                        "#30000050"],
                                "Or": [[[6, 6], [3]],
                                       "input0 or input1",
                                       "input0 or input1",
                                       "input0 | input1",
                                       "#30000050"],
                                "Less than": [[[6, 6], [3]],
                                              "input0 &lt; input1",
                                              "input0 &lt; input1",
                                              "input0 &lt; input1",
                                              "#30000050"],
                                "Greater than": [[[6, 6], [3]],
                                                 "input0 &gt;  input1",
                                                 "input0 &gt;  input1",
                                                 "input0 &gt;  input1",
                                                 "#30000050"],
                                "Equal": [[[6, 6], [3]],
                                          "input0 = input1",
                                          "input0 = input1",
                                          "input0 = input1",
                                          "#30000050"]
                            },
                        "Math":
                            {
                                "Add": [[[6, 6], [6]],
                                        "input0 + input1",
                                        "input0 + input1",
                                        "input0 + input1",
                                        "#70307030"],
                                "Subtract": [[[6, 6], [6]],
                                             "input0 - input1",
                                             "input0 - input1",
                                             "input0 - input1",
                                             "#70307030"],
                                "Multiply": [[[6, 6], [6]],
                                             "input0 * input1",
                                             "input0 * input1",
                                             "input0 * input1",
                                             "#70307030"],
                                "Divide": [[[6, 6], [6]],
                                           "input0 / input1",
                                           "input0 / input1",
                                           "input0 / input1",
                                           "#70307030"]
                            },
                        "Input":
                            {
                                "Raw code": [[[0, 4], [0]],
                                             "\ninput1\noutput0",
                                             "\ninput1\noutput0",
                                             "\ninput1\noutput0",
                                             "#505050"],
                                "User input": [[[0, 6, 4], [0]],
                                               "\ninput1 = input(input2)\noutput0",
                                               "\ncout &lt;&lt; input1, cin >> input2;\noutput0",
                                               "\nlet mut input1 = String::new();\nprintln!(input2);\nstdin().read_line(&mut input1).unwrap();\noutput0",
                                               "#303030"]
                            },
                        "Output":
                            {
                                "Return": [[[0, 6], []],
                                           "\nreturn input1",
                                           "\nreturn input1;",
                                           "\nreturn input1;",
                                           "#90702070"],
                                "Break": [[[0], []],
                                          "\nbreak",
                                          "\nbreak;",
                                          "\nbreak;",
                                          "#90702070"],
                                "Print": [[[0, 6], [0]],
                                          "\nprint(input1)\noutput0",
                                          "\ncout &gt;&gt;  input1;\noutput0",
                                          "\nprintln!(input1);\noutput0",
                                          "#90702070"]
                            }
                    }
            }

def Indent(String):
    return indent(String, '     ')

def make_nodes():
    for categori in Languages["statement"]:
        for statement in Languages["statement"][categori]:
            class node(MasterNode):
                icon = f"{statement}.png"
                name = statement
                category = "statement"
                sub_category = categori
                node_name = statement
                node_color = Languages["statement"][sub_category][node_name][4]

                def __init__(self, scene):
                    super().__init__(scene, inputs=Languages["statement"][self.sub_category][self.node_name][0][0],
                                     outputs=Languages["statement"][self.sub_category][self.node_name][0][1])

                def getNodeCode(self):
                    self.showCode = not self.isInputConnected(0)
                    current_language = Languages["Languages"][self.syntax]
                    raw_code = Languages["statement"][self.sub_category][self.node_name][current_language]

                    # putting all inputs in the proper place and order
                    if self.inputs:
                        for input in self.inputs[1:]:
                            new = str(self.get_my_input_code(self.inputs.index(input)))
                            raw_code = raw_code.replace(f"input{str(self.inputs.index(input))}", new)

                    # putting all outputs in the proper place and order
                    if self.outputs:
                        for output in self.outputs:
                            new = str(self.get_other_socket_code(self.outputs.index(output)))

                            if output.socket_type == 0 and self.outputs.index(output) > 0:
                                new = Indent(str(self.get_other_socket_code(self.outputs.index(output))))

                            raw_code = raw_code.replace(f"output{str(self.outputs.index(output))}", new)

                            # as a rule if you have only one output and it's not of the type 0 (executable) then
                            # the node's code only is useful inside another and it shouldn't show as an independent code
                            if output.socket_type != 0 and len(self.outputs) == 1:
                                self.showCode = False

                    if raw_code.__contains__("input_type"):
                        for input in self.inputs[1:]:
                            type = ""
                            if self.isInputConnected(self.inputs.index(input)):
                                type = self.scene.node_editor.return_types[self.getInput(self.inputs.index(input)).node_usage][current_language].replace(" -> ", "")
                            raw_code = raw_code.replace(f"input_type{str(self.inputs.index(input))}", type)

                        #     raw_code = self.outputs[0].socket_code = raw_code
                        # if raw_code.__contains__("next"):
                        #     nextCode = self.get_other_socket_code(0)
                        #     raw_code = raw_code.replace("next", f"{Indent(nextCode)}")
                        #
                        #     if len(self.outputs) > 1:
                        #         brotherCode = self.get_other_socket_code(1)
                        #         if self.outputs[1].socket_type != 0:
                        #             self.outputs[1].socket_code = self.get_my_input_code(2)
                        #         raw_code = raw_code.replace("order", f"{brotherCode}")
                        # else:
                        #     self.showCode = False

                    return self.grNode.highlight_code(raw_code)
