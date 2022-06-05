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
                                    {
                                        [[[0], [0]],
                                         "name",
                                         "name",
                                         "name"]
                                    }
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
                "entities":
                    {
                        "function":
                            {
                                "initialize": [[[], [0]],
                                               "def name()return:content",
                                               "data type name() {content}",
                                               "fn name()return: {content}"],
                                "use": [[[0], [0]],
                                        "name()content",
                                        "name();content",
                                        "name();content"]
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
                "statements":
                    {
                        "process":
                            {
                                "if": [[[0, 3], [0, 0]],
                                       "if content:\nnext",
                                       "if (content)\n{next}",
                                       "if content\n{next}"],
                                "while loop": [[[0, 3], [0]],
                                               "while content:\nnext",
                                               "while (content)\n{next}",
                                               "while content\n{next}"],
                                "for loop": [[[0, 2], [0]],
                                             "for item in content:\nnext",
                                             "for (auto item : content)\n{next}",
                                             "for index in 0..content\n{next}"],
                                "for each loop": [[[0, 5], [0, 6]],
                                                  "for item in range(content):\nnext",
                                                  "for (int i=0;i&lt;content;i++)\n{next}",
                                                  "for item in range(content):\nnext"],
                                "else": [[[0], [0, 0]],
                                         "else:\nnext",
                                         "else \n{next}",
                                         "else \n{next}"],
                                "elif": [[[0, 3], [0, 0]],
                                         "elif content:\nnext",
                                         "else if (content3)\n{next}",
                                         "else if (content1)\n{next}"]
                            },
                        "logic":
                            {
                                "and": [[[6, 6], [3]],
                                        "content and content",
                                        "content and content",
                                        "content && content"],
                                "or": [[[6, 6], [3]],
                                       "content or content",
                                       "content or content",
                                       "content | content"],
                                "Less than": [[[6, 6], [3]],
                                              "content &lt; content",
                                              "content &lt; content",
                                              "content &lt; content"],
                                "greater than": [[[6, 6], [3]],
                                                 "content &gt;  content",
                                                 "content &gt;  content",
                                                 "content &gt;  content"],
                                "equal": [[[6, 6], [3]],
                                          "content = content",
                                          "content = content",
                                          "content = content"]
                            },
                        "math":
                            {
                                "add": [[[6, 6], [6]],
                                        "content + content",
                                        "content + content",
                                        "content + content"],
                                "subtract": [[[6, 6], [6]],
                                             "content - content",
                                             "content - content",
                                             "content - content"],
                                "multyply": [[[6, 6], [6]],
                                             "content * content",
                                             "content * content",
                                             "content * content"],
                                "divide": [[[6, 6], [6]],
                                           "content / content", "content / content",
                                           "content / content"]
                            },
                        "input":
                            {
                                "raw code": [[[0, 4], [0]],
                                             "content",
                                             "content",
                                             "content"],
                                "user input": [[[], []],
                                               "content = input(content)\nnext",
                                               "cout &lt;&lt; content, cin >> content;\nnext",
                                               "stdin().read_line(&mut name.unwrap();\nnext"]
                            },

                        "output":
                            {
                                "return": [[[0, 6], []],
                                           "return content",
                                           "return content;",
                                           "return content;"],
                                "break": [[[0], []],
                                          "break",
                                          "break;",
                                          "break;"],
                                "print": [[[0, 6], [0]],
                                          "print(content)next",
                                          "cout &gt;&gt;  content;",
                                          "println!(content);"]
                            }
                    }
            }


# list &lt;data type&gt; name = {content};\nnext

#
#
#
#
#

def make_nodes():
    for statements in Languages["statements"]:
        class node(MasterNode):
            pass


def get_datatype_node(self, as_fun_return: bool = False):
    return self.scene.node_editor.get_datatype(self.syntax, self.node_return, as_fun_return)


def get_datatype(syntax, node_return, as_fun_return: bool = False):
    lang_index = Languages["Languages"][syntax]
    get_datatype = Languages["data types"][node_return][lang_index]
    if as_fun_return:
        if get_datatype != "":
            return f"""{Languages["return_syntax"][lang_index]}{get_datatype}"""
    return get_datatype
