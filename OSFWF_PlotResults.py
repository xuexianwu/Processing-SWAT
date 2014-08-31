import os
from PyQt4 import QtGui
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.WrongHelpFileException import WrongHelpFileException
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterFile import ParameterFile
from processing.parameters.ParameterString import ParameterString
from processing.parameters.ParameterSelection import ParameterSelection
from processing.parameters.ParameterNumber import ParameterNumber
from datetime import date, timedelta, datetime
from read_SWAT_out import read_SWAT_time
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.pylab import *
import ASS_module4_Results
import ASS_module4_Results_weekly

class OSFWF_PlotResults(GeoAlgorithm):

    SRC_FOLDER = "SRC_FOLDER"
    ASS_MODE = "ASS_MODE"
    ASS_FOLDER = "ASS_FOLDER"
    STARTDATE = "STARTDATE"
    OBSFILE = "OBSFILE"
    REACH_ID = "REACH_ID"

    def defineCharacteristics(self):
        self.name = "5 - Plot results (OSFWF)"
        self.group = "Operational simulation and forecasting workflow (OSFWF)"
        self.addParameter(ParameterFile(OSFWF_PlotResults.ASS_FOLDER, "Select assimilation folder", True))
        self.addParameter(ParameterFile(OSFWF_PlotResults.SRC_FOLDER, "Select model source folder", True))
        self.addParameter(ParameterString(OSFWF_PlotResults.STARTDATE, "Issue date (yyyy-mm-dd)", str(date.today())))
        self.addParameter(ParameterFile(OSFWF_PlotResults.OBSFILE, "Select file with corresponding observations",False))
        self.addParameter(ParameterNumber(OSFWF_PlotResults.REACH_ID, "Reach ID", 1, 500, 1))

    def processAlgorithm(self, progress):
        SRC_FOLDER = self.getParameterValue(OSFWF_PlotResults.SRC_FOLDER)
        ASS_MODE = self.getParameterValue(OSFWF_PlotResults.ASS_MODE)
        ASS_FOLDER = self.getParameterValue(OSFWF_PlotResults.ASS_FOLDER)
        STARTDATE = self.getParameterValue(OSFWF_PlotResults.STARTDATE)
        OBSFILE = self.getParameterValue(OSFWF_PlotResults.OBSFILE)
        REACH_ID = self.getParameterValue(OSFWF_PlotResults.REACH_ID)

        SWAT_time_info = read_SWAT_time(SRC_FOLDER)
        SWAT_startdate = date2num(date(int(SWAT_time_info[1]),1,1) + timedelta(days=int(SWAT_time_info[2])-1))
        if SWAT_time_info[4] > 0: # Account for NYSKIP>0
            SWAT_startdate = date2num(date(int(SWAT_time_info[1]+SWAT_time_info[4]),1,1))
        SWAT_enddate = date2num(date(int(SWAT_time_info[0]+SWAT_time_info[1]-1),1,1)) + SWAT_time_info[3]-1

        # Assimilation startdate is 30 days prior to STARTDATE
        ASS_startdate = SWAT_startdate
        # Assimilation enddate is 8 days after STARTDATE
        ASS_enddate = SWAT_enddate
        ASS_module4_Results.Results(OBSFILE, str(STARTDATE), ASS_startdate, ASS_enddate, ASS_FOLDER, REACH_ID)
#        ASS_module4_Results.Results(OBSFILE, STARTDATE, ASS_startdate, ASS_enddate, ASS_FOLDER, REACH_ID)

    def getIcon(self):
        return  QtGui.QIcon(os.path.dirname(__file__) + "/images/tigerNET.png")

    def helpFile(self):
        [folder, filename] = os.path.split(__file__)
        [filename, _] = os.path.splitext(filename)
        helpfile = str(folder) + os.sep + "doc" + os.sep + filename + ".html"
        if os.path.exists(helpfile):
            return helpfile
        else:
            raise WrongHelpFileException("Sorry, no help is available for this algorithm.")
