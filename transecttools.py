import os
import glob
import sys
import shutil
import generate_transects as gt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        sizeObject = QDesktopWidget().screenGeometry(-1)
        global screenWidth
        screenWidth = sizeObject.width()
        global screenHeight
        screenHeight = sizeObject.height()
        global bw1
        bw1 = int(screenWidth/15)
        global bw2
        bw2 = int(screenWidth/50)
        global bh1
        bh1 = int(screenHeight/15)
        global bh2
        bh2 = int(screenHeight/20)

        self.setWindowTitle("TransectToolz")
        self.home()

    def make_transects_action(self, subregion_bool, spacing, length, G, C, RR, SSS, version_name):
        if subregion_bool == False:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if home_dir:
                ref_shoreline_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_shoreline.geojson')
                ref_area_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_polygon.geojson')
                transects_path_final = os.path.join(home_dir, G+C+RR+SSS+'_transects.geojson')
                gt.main(ref_shoreline_path,
                        ref_area_path,
                        transects_path_final,
                        G,
                        C,
                        RR,
                        SSS,
                        version_name,
                        spacing,
                        length
                        )
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if home_dir:
                gt.make_and_merge_transects_for_region(home_dir,
                                                       G,
                                                       C,
                                                       RR,
                                                       version_name,
                                                       transect_spacing=spacing,
                                                       transect_length=length)

    def qc_action(self, subregion_bool, G, C, RR, SSS, version_name):
        if subregion_bool == False:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if home_dir:
                ref_shoreline_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_shoreline.geojson')
                transects_path_final = os.path.join(home_dir, G+C+RR+SSS+'_transects.geojson')
                gt.re_index_with_ref_shoreline(transects_path_final,
                                               ref_shore_path,
                                               G,
                                               C,
                                               RR,
                                               SSS,
                                               version_name,
                                               tolerance=10,
                                               dist_int=50)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if home_dir:
                gt.qc(home_dir,
                      G,
                      C,
                      RR,
                      SSS,
                      version_name,
                      tolerance=10,
                      dist_int=50)

                
    def flip_transects_action(self, subregion_bool, G, C, RR, SSS, version_name):
##        if subregion_bool == False:
##            options = QFileDialog.Options()
##            options |= QFileDialog.DontUseNativeDialog
##            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
##            if home_dir:
##                ref_shoreline_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_shoreline.geojson')
##                ref_area_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_polygon.geojson')
##                transects_path_final = os.path.join(home_dir, G+C+RR+SSS+'_transects.geojson'))
##                gt.main(ref_shoreline_path,
##                        ref_area_path,
##                        transects_path_final,
##                        G,
##                        C,
##                        RR,
##                        SSS,
##                        version_name,
##                        spacing,
##                        length
##                        )
##        else:
##            options = QFileDialog.Options()
##            options |= QFileDialog.DontUseNativeDialog
##            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
##            if home_dir:
##                gt.make_and_merge_transects_for_region(home_dir,
##                                                       G,
##                                                       C,
##                                                       RR,
##                                                       version_name,
##                                                       transect_spacing=spacing,
##                                                       transect_length=length)
        return None
                
    def extend_transects_action(self, subregion_bool, seaward_val, landward_val, G, C, RR, SSS, version_name):
##        if subregion_bool == False:
##            options = QFileDialog.Options()
##            options |= QFileDialog.DontUseNativeDialog
##            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
##            if home_dir:
##                ref_shoreline_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_shoreline.geojson')
##                ref_area_path = os.path.join(home_dir, G+C+RR+SSS+'_reference_polygon.geojson')
##                transects_path_final = os.path.join(home_dir, G+C+RR+SSS+'_transects.geojson'))
##                gt.main(ref_shoreline_path,
##                        ref_area_path,
##                        transects_path_final,
##                        G,
##                        C,
##                        RR,
##                        SSS,
##                        version_name,
##                        spacing,
##                        length
##                        )
##        else:
##            options = QFileDialog.Options()
##            options |= QFileDialog.DontUseNativeDialog
##            home_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
##            if home_dir:
##                gt.make_and_merge_transects_for_region(home_dir,
##                                                       G,
##                                                       C,
##                                                       RR,
##                                                       version_name,
##                                                       transect_spacing=spacing,
##                                                       transect_length=length)
        return None
        
    def home(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QGridLayout()             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)


        ##Setting G, C, RR, SS, version_name
        G_lab = QLabel('G')
        self.vbox.addWidget(G_lab, 0, 1)
        G_text_box = QLineEdit()
        self.vbox.addWidget(G_text_box, 1, 1)

        C_lab = QLabel('C')
        self.vbox.addWidget(C_lab, 0, 2)
        C_text_box = QLineEdit()
        self.vbox.addWidget(C_text_box, 1, 2)

        RR_lab = QLabel('RR')
        self.vbox.addWidget(RR_lab, 0, 3)
        RR_text_box = QLineEdit()
        self.vbox.addWidget(RR_text_box, 1, 3)

        SSS_lab = QLabel('SSS')
        self.vbox.addWidget(SSS_lab, 0, 4)
        SSS_text_box = QLineEdit()
        self.vbox.addWidget(SSS_text_box, 1, 4)

        version_name_lab = QLabel('V')
        self.vbox.addWidget(version_name_lab, 0, 5)
        version_name_text_box = QLineEdit()
        self.vbox.addWidget(version_name_text_box, 1, 5)
        
        ##Make transects
        make_transects = QPushButton('Make Transects')
        self.vbox.addWidget(make_transects, 2, 1)
        make_subregion = QCheckBox(text='Entire Subregion')
        self.vbox.addWidget(make_subregion, 3, 1)

        ##transect length and spacing
        transect_length_lab = QLabel('Transect Length (m)')
        self.vbox.addWidget(transect_length_lab, 4, 1)
        transect_length = QDoubleSpinBox()
        self.vbox.addWidget(transect_length, 5, 1)
        transect_spacing_lab = QLabel('Transect Spacing (m)')
        self.vbox.addWidget(transect_spacing_lab, 6, 1)
        transect_spacing = QDoubleSpinBox()
        self.vbox.addWidget(transect_spacing, 7, 1)

        ##QC Transects
        qc = QPushButton('QC Transect Order')
        self.vbox.addWidget(qc, 2, 2)
        qc_subregion = QCheckBox(text='Entire Subregion')
        self.vbox.addWidget(qc_subregion, 3, 2)
        
        ##Flip Transects
        flip_transects = QPushButton('Flip Transects')
        self.vbox.addWidget(flip_transects, 2, 3)
        flip_subregion = QCheckBox(text='Entire Subregion')
        self.vbox.addWidget(flip_subregion, 3, 3)
        
        ##Extend Transects
        extend_transects = QPushButton('Extend Transects')
        self.vbox.addWidget(extend_transects, 2, 4)
        extend_subregion = QCheckBox(text='Entire Subregion')
        self.vbox.addWidget(extend_subregion, 3, 4)
        seaward_lab = QLabel('Seaward (m)')
        self.vbox.addWidget(seaward_lab, 4, 4)
        seaward = QDoubleSpinBox()
        self.vbox.addWidget(seaward, 5, 4)
        landward_lab = QLabel('Landward (m)')
        self.vbox.addWidget(landward_lab, 6, 4)
        landward = QDoubleSpinBox()
        self.vbox.addWidget(landward, 7, 4)

        ##setting maximums and minimums
        transect_spacing.setMaximum(500)
        transect_spacing.setMinimum(0)
        transect_length.setMaximum(10000)
        transect_length.setMinimum(0)
        seaward.setMaximum(1000)
        seaward.setMinimum(0)
        landward.setMaximum(1000)
        landward.setMinimum(0)

        ##actions
        make_transects.clicked.connect(lambda: self.make_transects_action(make_subregion.isChecked(),
                                                                          transect_spacing.value(),
                                                                          transect_length.value(),
                                                                          G_text_box.text(),
                                                                          C_text_box.text(),
                                                                          RR_text_box.text(),
                                                                          SSS_text_box.text(),
                                                                          version_name_text_box.text()
                                                                          )
                                       )
        qc.clicked.connect(lambda: self.qc_action(qc_subregion.isChecked(),
                                                  G_text_box.text(),
                                                  C_text_box.text(),
                                                  RR_text_box.text(),
                                                  SSS_text_box.text(),
                                                  version_name_text_box.text()
                                                  )
                           )
        flip_transects.clicked.connect(lambda: self.flip_transects_action(flip_subregion.isChecked(),
                                                                          G_text_box.text(),
                                                                          C_text_box.text(),
                                                                          RR_text_box.text(),
                                                                          SSS_text_box.text(),
                                                                          version_name_text_box.text()
                                                                          )
                                       )
        extend_transects.clicked.connect(lambda: self.extend_transects_action(extend_subregion.isChecked(),
                                                                              seaward.value(),
                                                                              landward.value(),
                                                                              G_text_box.text(),
                                                                              C_text_box.text(),
                                                                              RR_text_box.text(),
                                                                              SSS_text_box.text(),
                                                                              version_name_text_box.text()
                                                                              )
                                         )


        
        ##Scroll policies
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)


## Function outside of the class to run the app   
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

## Calling run to run the app
run()
