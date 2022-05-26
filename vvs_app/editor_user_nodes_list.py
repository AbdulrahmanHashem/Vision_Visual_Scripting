from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from nodeeditor.node_scene import NodeScene
from vvs_app.editor_properties_list import PropertiesList
from vvs_app.nodes.default_functions import *
from vvs_app.nodes.event_nodes import UserFunction
from vvs_app.nodes.nodes_configuration import VARIABLES, get_node_by_type, LISTBOX_MIMETYPE
from nodeeditor.utils import dumpException
from vvs_app.nodes.variables_nodes import *


class UserNodesList(QTabWidget):

    def __init__(self, parent=None, scene: NodeScene = None, propertiesWdg: PropertiesList = None):
        super().__init__(parent)
        self.all_return_types = ['mutable', 'float', 'integer', 'boolean', 'string', 'list', 'dictionary', 'tuple']
        self.user_nodes_data = []
        self.USER_NODES = {}

        self.scene = scene
        self.proprietiesWdg = propertiesWdg
        self.InitUI()

    def InitUI(self):
        # Add QTabWidget and add Both Variables Tab and Events Tab
        tab1 = QWidget()
        tab2 = QWidget()

        self.addTab(tab1, "Variables")
        self.addTab(tab2, "Functions")

        # Create Variables List
        self.VarList = QListWidget()
        self.EventList = QListWidget()

        # Create Variables and Events WNDs layout
        self.varLayout = QVBoxLayout()
        self.varLayout.setContentsMargins(0, 0, 0, 0)

        self.eventLayout = QVBoxLayout()
        self.eventLayout.setContentsMargins(0, 0, 0, 0)

        # Set Layouts For both
        tab1.setLayout(self.varLayout)
        tab2.setLayout(self.eventLayout)

        ## Setup CompoBox and add Button For Vars
        self.varCompoBox = QComboBox()
        self.varAddBtn = QPushButton("Add Variable")
        self.varHlayout = QHBoxLayout()
        self.varCompoBox.setMinimumHeight(28)
        self.varAddBtn.setMinimumHeight(28)
        self.VarList.setIconSize(QSize(28, 28))
        self.varHlayout.setContentsMargins(2, 2, 2, 2)
        self.varHlayout.addWidget(self.varCompoBox)
        self.varHlayout.addWidget(self.varAddBtn)
        self.varLayout.addLayout(self.varHlayout)
        self.varLayout.addWidget(self.VarList)
        self.VarList.setDragEnabled(True)

        # Setup CompoBox and add Button For Vars
        self.eventCompoBox = QComboBox()
        self.eventAddBtn = QPushButton("Add Event")
        self.eventHlayout = QHBoxLayout()
        self.eventCompoBox.setMinimumHeight(28)
        self.eventAddBtn.setMinimumHeight(28)
        self.EventList.setIconSize(QSize(28, 28))
        self.eventHlayout.setContentsMargins(2, 2, 2, 2)
        self.eventHlayout.addWidget(self.eventCompoBox)
        self.eventHlayout.addWidget(self.eventAddBtn)
        self.eventLayout.addLayout(self.eventHlayout)
        self.eventLayout.addWidget(self.EventList)
        self.EventList.setDragEnabled(True)

        self.VarList.startDrag = self.VarStartDrag
        self.EventList.startDrag = self.EventStartDrag

        # self.VarList.startDrag.connect()

        self.VarList.itemClicked.connect(lambda: self.list_selection_changed(var=True))
        self.EventList.itemClicked.connect(lambda: self.list_selection_changed(var=False))

        # self.VarList.itemSelectionChanged.connect(lambda : self.list_selection_changed(var=True))
        # self.EventList.itemSelectionChanged.connect(lambda : self.list_selection_changed(var=False))

        self.InitList()

    def set_user_node_Id_now(self, class_reference):
        id = 0
        while id in self.USER_NODES:
            id = id+1
        else:
            self.USER_NODES[id] = class_reference
            return id

    def get_user_node_by_id(self, node_id):
        if node_id not in self.USER_NODES:
            raise NodeTypeNotRegistered("node_type '%d' is not registered" % node_id)
        else:
            return self.USER_NODES[node_id]

    def MakeCopyOfClass(self, node):
        class NewNode(node):
            pass
        return NewNode

    def InitList(self):
        Events = list(EVENTS.keys())
        Events.sort()
        for node_type in Events:
            node = get_node_by_type(node_type)
            self.eventCompoBox.addItem(node.name, userData=node.node_type)

        Vars = list(VARIABLES.keys())
        Vars.sort()
        for node_type in Vars:
            node = get_node_by_type(node_type)
            self.varCompoBox.addItem(node.name, userData=node.node_type)

        # self.loadVars(self.userData.LoadData())
        self.varAddBtn.clicked.connect(lambda: self.add_new_node(var=True))
        self.eventAddBtn.clicked.connect(lambda: self.add_new_node(var=False))

    def add_new_node(self, var):
        if var:
            name = self.varCompoBox.currentText()
            type = self.varCompoBox.itemData(self.varCompoBox.currentIndex())

        else:
            name = self.eventCompoBox.currentText()
            type = self.eventCompoBox.itemData(self.eventCompoBox.currentIndex())

        self.create_user_node(self.autoNodeRename(name), node_id=None, type=type, user=True, node_return='mutable')

    def create_user_node(self, name, node_id, type, node_return, user=False):

        # Get new Variable type and construct new Variable object
        node = get_node_by_type(type)
        new_node = self.MakeCopyOfClass(node)
        new_node.node_return = node_return
        node_data = [name, node_id, type, node_return]

        # Add new copy of Var class Info to Dict of USER_VARS
        new_id = self.set_user_node_Id_now(new_node)
        new_node.nodeID = node_data[1] = new_id
        new_node.name = name

        # Save new Var to list of vars with [Type, ID, Name, Value]
        self.user_nodes_data.append(node_data)

        if new_node.node_type == UserFunction.node_type:
            A_list = self.EventList
        else:
            A_list = self.VarList

        # Add new QListItem to the UI List using Init Data
        self.addMyItem(new_node.name, new_node.icon, new_id, node.node_type, A_list)

        if user:
            self.scene.history.storeHistory("Created User Node ", setModified=True)
        self.scene.node_editor.UpdateTextCode()

    def addMyItem(self, name, icon=None, new_node_ID=int, node_type=int, List=QListWidget):
        item = QListWidgetItem(name, List)  # can be (icon, text, parent, <int>type)

        pixmap = QPixmap(icon if icon is not None else "")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(28, 28))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)

        item.setData(80, node_type)

        item.setData(90, new_node_ID)

        item.setData(91, name)

    def list_selection_changed(self, var, *args, **kwargs):
        # Name line edite setup
        if var:
            item = self.VarList.currentItem()
        else:
            item = self.EventList.currentItem()

        self.node_name_input = QLineEdit()
        self.node_name_input.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9_]+")))
        self.node_name_input.setText(f"{item.data(91)}")
        self.node_name_input.returnPressed.connect(lambda: self.update_node_name(var))

        self.proprietiesWdg.clear_properties()
        self.proprietiesWdg.detailsUpdate("Node Name", self.node_name_input)

        if item.data(80) == UserFunction.node_type or item.data(80) == ListVar.node_type:
            self.return_type = QComboBox()
            self.return_type.addItems(self.all_return_types)

            self.return_type.setCurrentText(self.get_user_node_by_id(item.data(90)).node_return)
            self.return_type.currentIndexChanged.connect(lambda: self.update_node_return(item.data(91), item.data(90)))

            self.proprietiesWdg.detailsUpdate("Return Type", self.return_type)

        self.delete_btn = QPushButton(f"Delete {item.data(91)}")
        self.delete_btn.clicked.connect(lambda: self.delete_node(item.data(91), user=True))
        self.delete_btn.setShortcut(
            QKeySequence(f"Shift+{self.scene.masterRef.global_switches.switches_Dict['Key Mapping']['Delete']}"))
        self.proprietiesWdg.detailsUpdate("Delete Node", self.delete_btn)

    def update_node_return(self, node_name, node_id):
        for item in self.user_nodes_data:
            if item[0] == node_name:
                item[3] = self.return_type.currentText()

        for node in self.scene.nodes:
            if node.name == node_name:
                node.node_return = self.return_type.currentText()

        node_ref = self.get_user_node_by_id(node_id)
        node_ref.node_return = self.return_type.currentText()

        self.scene.node_editor.UpdateTextCode()

    def VarStartDrag(self, *args, **kwargs):
        try:
            self.list_selection_changed(True)
            item = self.VarList.currentItem()
            var_ID = item.data(90)

            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            mimeData = QMimeData()
            drag = QDrag(self)

            dataStream << pixmap
            dataStream.writeInt(var_ID)
            dataStream.writeQString(item.text())
            dataStream.writeQStringList(["V"])

            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

    def EventStartDrag(self, *args, **kwargs):
        try:
            self.list_selection_changed(False)
            item = self.EventList.currentItem()
            event_ID = item.data(90)
            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            mimeData = QMimeData()
            drag = QDrag(self)

            dataStream << pixmap
            dataStream.writeInt(event_ID)
            dataStream.writeQString(item.text())
            dataStream.writeQStringList(["E"])

            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

    def update_node_name(self, var):
        if var:
            item = self.VarList.currentItem()
        else:
            item = self.EventList.currentItem()

        oldName = item.data(91)
        tryName = self.node_name_input.text()
        newName = self.userRename(oldName=oldName, tryName=tryName)
        if newName == None:
            return
        else:
          
            # get ref to user variable copy
            node_ref = self.get_user_node_by_id(item.data(90))

            # set item text to new name
            item.setText(newName)
            item.setData(91, newName)

            # set name of parent var
            node_ref.name = newName

            # rename all children grNode vars that have the old name
            for node in self.scene.nodes:
                if node.name == oldName:
                    node.name = newName
                    node.grNode.name = newName

            self.scene.node_editor.UpdateTextCode()

    def findListItem(self, selectedNodes: 'Nodes'):
        if selectedNodes != []:
            for item in range(self.VarList.count()):
                Litem = self.VarList.item(item)
                if Litem.text() == selectedNodes[0].name:
                    self.VarList.setCurrentItem(Litem)
                    self.list_selection_changed(var=True)
                    self.setCurrentIndex(0)
                    return Litem

            for item in range(self.EventList.count()):
                Litem = self.EventList.item(item)
                if Litem.text() == selectedNodes[0].name:
                    self.EventList.setCurrentItem(Litem)
                    self.list_selection_changed(var=False)
                    self.setCurrentIndex(1)
                    return Litem

            self.proprietiesWdg.clear_properties()
        else:
            self.proprietiesWdg.clear_properties()

###################################
    # Data
###################################


    def userRename(self, oldName, tryName: str):
        names = []
        for item in self.user_nodes_data:
            names.append(item[0])

        if names.__contains__(tryName):
            return None
        else:
            for item in self.user_nodes_data:
                if item[0] == oldName:
                    item[0] = tryName
                    return tryName

    def autoNodeRename(self, name: 'Node'):
        x = 0
        newName = name

        # does a variable already has this name ?
        names = []
        for item in self.user_nodes_data:
            names.append(item[0])
        # print(names)
        while names.__contains__(newName):
            x += 1
            newName = f"{name}{x}"

        else:
            return newName

    def delete_node(self, item_name, user=False):
        item_ref = None
        if self.VarList.findItems(item_name, Qt.MatchExactly):
            list_ref = self.VarList
            item_ref = self.VarList.findItems(item_name, Qt.MatchExactly)[0]
        else:
            list_ref = self.EventList
            item_ref = self.EventList.findItems(item_name, Qt.MatchExactly)[0]

        if item_ref:

            self.USER_NODES.pop(item_ref.data(90))
            selected = []
            for item in self.user_nodes_data:
                if item[0] == item_name:
                    self.user_nodes_data.remove(item)

            for node in self.scene.nodes:
                if node.name == item_name:
                    selected.append(node)

            # This is split into two loops to prevent bugs that happen while deleting nodes
            for node in selected:
                node.remove()

            list_ref.setCurrentItem(item_ref)

            list_ref.takeItem(list_ref.currentRow())
            list_ref.clearSelection()
            self.proprietiesWdg.clear_properties()
            self.scene.node_editor.UpdateTextCode()

            if user:
                self.scene.history.storeHistory("Delete User Node ", setModified=True)

            self.scene.node_editor.UpdateTextCode()

        else:
            print("List Item Doesn't Exist")