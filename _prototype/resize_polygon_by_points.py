import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

# How to resize polygon by dragging its corners?
# https://www.pythonfixing.com/2021/12/fixed-how-to-resize-polygon-by-dragging.html

class Scene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.record_points = True
        self.selected = None  # the selected polygon
        self.points_lst = []  # points that are stored when recording
        self.corner_points = []  # This contains corner point and control point mapping
        self.selected_corner = None
        self.poly_points = [] # points that are stored when resizing (You could instead reuse points_lst)

    def record(self):
        self.record_points = True

    def removeControlPoints(self):
        """ removes the control points (i,e the ellipse)"""
        for ellipse, _ in self.corner_points:
            self.removeItem(ellipse)

        self.corner_points = []

    def mousePressEvent(self, event):
        super(Scene, self).mousePressEvent(event)

        if self.record_points:
            self.points_lst.append(event.scenePos())
            return

        for point in self.corner_points:
            if point[0].contains(event.scenePos()):
                self.selected_corner = point
                return

        if self.selectedItems():

            self.removeControlPoints()

            self.selected = self.selectedItems()[0]
            self.poly_points = [self.selected.mapToScene(x) for x in self.selected.polygon()]

            for index, point in enumerate(self.poly_points):
                x, y = point.x(), point.y()
                ellipse = self.addEllipse(QtCore.QRectF(x - 5, y - 5, 10, 10), brush=QtGui.QBrush(QtGui.QColor("red")))
                ellipse.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)

                self.corner_points.append((ellipse, index))

        else:
            self.selected = None
            self.removeControlPoints()
            self.corner_points = []
            self.poly_points = []
            self.selected_corner = None

    def mouseMoveEvent(self, event) -> None:
        super(Scene, self).mouseMoveEvent(event)

        if self.selected_corner:
            self.poly_points[self.selected_corner[1]] = QtCore.QPointF(event.scenePos())
            self.selected.setPolygon(QtGui.QPolygonF(self.poly_points))

    def mouseReleaseEvent(self, event) -> None:
        super(Scene, self).mouseReleaseEvent(event)
        self.selected_corner = None

    def addPoints(self):  # adds the polygon to the scene
        self.record_points = False
        polygon = self.addPolygon(QtGui.QPolygonF(self.points_lst))
        polygon.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.points_lst = []


class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        view = QtWidgets.QGraphicsView()
        scene = Scene()
        view.setScene(scene)

        record_btn = QtWidgets.QPushButton(text="Record", clicked=scene.record)
        finish_btn = QtWidgets.QPushButton(text="Finish", clicked=scene.addPoints)

        self.layout().addWidget(view)
        self.layout().addWidget(record_btn)
        self.layout().addWidget(finish_btn)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())