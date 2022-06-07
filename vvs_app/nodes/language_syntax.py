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
                    },
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
                                "if": [[[0, 3], [0, 0]],
                                       "\nif content1:\nnext\norder",
                                       "\nif (content1)\n{next\n}\norder",
                                       "\nif content1\n{next\n}\norder",
                                       "#90FF5733"],
                                "while loop": [[[0, 3], [0]],
                                               "\nwhile content1:\nnext",
                                               "\nwhile (content1)\n{next\n}",
                                               "\nwhile content1\n{next\n}",
                                               "#90FF5733"],
                                "for loop": [[[0, 2], [0]],
                                             "\nfor item in range(content1):\nnext",
                                             "\nfor (int i=0;i&lt;content1;i++)\n{next\n}",
                                             "\nfor index in 0..content1\n{next\n}",
                                             "#905050FF"],
                                "for each loop": [[[0, 5, 4], [0, 6]],
                                                  "\nfor content2 in content1:\nnext",
                                                  "\nfor (auto content2 : content1)\n{next\n}",
                                                  "\nfor content2 in &content1\n{next\n}",
                                                  "#905050FF"],
                                "else": [[[0], [0]],
                                         "\nelse:\nnext",
                                         "\nelse \n{next\n}",
                                         "\nelse \n{next\n}",
                                         "#90FF5733"],
                                "elif": [[[0, 3], [0]],
                                         "\nelif content1:\nnext",
                                         "\nelse if (content1)\n{next\n}",
                                         "\nelse if (content1)\n{next\n}",
                                         "#90FF5733"]
                            },
                        "Logic":
                            {
                                "and": [[[6, 6], [3]],
                                        "content0 and content1",
                                        "content0 and content1",
                                        "content0 && content1",
                                        "#30000050"],
                                "or": [[[6, 6], [3]],
                                       "content0 or content1",
                                       "content0 or content1",
                                       "content0 | content1",
                                       "#30000050"],
                                "Less than": [[[6, 6], [3]],
                                              "content0 &lt; content1",
                                              "content0 &lt; content1",
                                              "content0 &lt; content1",
                                              "#30000050"],
                                "greater than": [[[6, 6], [3]],
                                                 "content0 &gt;  content1",
                                                 "content0 &gt;  content1",
                                                 "content0 &gt;  content1",
                                                 "#30000050"],
                                "equal": [[[6, 6], [3]],
                                          "content0 = content1",
                                          "content0 = content1",
                                          "content0 = content1",
                                          "#30000050"]
                            },
                        "Math":
                            {
                                "add": [[[6, 6], [6]],
                                        "content0 + content1",
                                        "content0 + content1",
                                        "content0 + content1",
                                        "#70307030"],
                                "subtract": [[[6, 6], [6]],
                                             "content0 - content1",
                                             "content0 - content1",
                                             "content0 - content1",
                                             "#70307030"],
                                "multiply": [[[6, 6], [6]],
                                             "content0 * content1",
                                             "content0 * content1",
                                             "content0 * content1",
                                             "#70307030"],
                                "divide": [[[6, 6], [6]],
                                           "content0 / content1",
                                           "content0 / content1",
                                           "content0 / content1",
                                           "#70307030"]
                            },
                        "Input":
                            {
                                "raw code": [[[0, 4], [0]],
                                             "\ncontent1\nnext",
                                             "\ncontent1\nnext",
                                             "\ncontent1\nnext",
                                             "#505050"],
                                "user input": [[[0, 6, 4], [0]],
                                               "\ncontent1 = input(content2)\nnext",
                                               "\ncout &lt;&lt; content1, cin >> content2;\nnext",
                                               "\nlet mut content1 = String::new();\nprintln!(content2);\nstdin().read_line(&mut content1).unwrap();\nnext",
                                               "#303030"]
                            },
                        "Output":
                            {
                                "return": [[[0, 6], []],
                                           "\nreturn content1",
                                           "\nreturn content1;",
                                           "\nreturn content1;",
                                           "#90702070"],
                                "break": [[[0], []],
                                          "\nbreak",
                                          "\nbreak;",
                                          "\nbreak;",
                                          "#90702070"],
                                "print": [[[0, 6], [0]],
                                          "\nprint(content1)\nnext",
                                          "\ncout &gt;&gt;  content1;\nnext",
                                          "\nprintln!(content1);\nnext",
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

                    if self.inputs:
                        for input in self.inputs:
                            if input.socket_type != 0:
                                new = str(self.get_my_input_code(self.inputs.index(input)))
                                raw_code = raw_code.replace(f"content{str(self.inputs.index(input))}", new)

                    if self.outputs:
                        if raw_code.__contains__("next"):
                            nextCode = self.get_other_socket_code(0)
                            raw_code = raw_code.replace("next", f"{Indent(nextCode)}")

                            if len(self.outputs) > 1:
                                brotherCode = self.get_other_socket_code(1)
                                if self.outputs[1].socket_type != 0:
                                    self.outputs[1].socket_code = self.get_my_input_code(2)
                                raw_code = raw_code.replace("order", f"{brotherCode}")
                        else:
                            self.showCode = False
                            raw_code = self.outputs[0].socket_code = raw_code

                    return self.grNode.highlight_code(raw_code)

# def get_datatype_node(self, as_fun_return: bool = False):
#     return self.scene.node_editor.get_datatype(self.syntax, self.node_return, as_fun_return)
#
# def get_datatype(syntax, node_return, as_fun_return: bool = False):
#     lang_index = Languages["Languages"][syntax]
#     get_datatype = Languages["data types"][node_return][lang_index]
#     if as_fun_return:
#         if get_datatype != "":
#             return f"""{Languages["return_syntax"][lang_index]}{get_datatype}"""
#     return get_datatype