#----------------------------------------------------------------------------------------------------
# Copyright (c) 2020-2022 5@xes
#
# The Duplicate plugin is released under the terms of the AGPLv3 or higher.
# Release V1.0.2  Update  "resolution","shell","infill","material","speed","travel","cooling","dual"
# Release V1.0.3  Update   "experimental","blackmagic","meshfix" 
# Release V1.0.4  Limit the plugin to release 4.5 -> 4.7
# Release V1.0.5  Ready for release Arachne or 4.9 ?
# Release V1.0.6  Bug correction and Nozzle diameter used as condition to duplicate resolution section
#
# Release V1.1.0  Update Cura 5.0
#----------------------------------------------------------------------------------------------------

from UM.Extension import Extension
from cura.CuraApplication import CuraApplication
from cura.CuraVersion import CuraVersion  
from UM.Version import Version

from UM.i18n import i18nCatalog
i18n_cura_catalog = i18nCatalog("cura")
i18n_catalog = i18nCatalog("fdmprinter.def.json")
i18n_extrud_catalog = i18nCatalog("fdmextruder.def.json")

from UM.Logger import Logger
from UM.Message import Message

class Duplicate(Extension):   

    def __init__(self, parent = None) -> None:
        Extension.__init__(self)
        
        # Add Plugin Menu
        self.addMenuItem(i18n_cura_catalog.i18nc("@item:inmenu", "Duplicate Extruder N°1"), self.acTion1)
        self.addMenuItem(i18n_cura_catalog.i18nc("@item:inmenu", "Duplicate Extruder N°2"), self.acTion2)
        self.addMenuItem(i18n_cura_catalog.i18nc("@item:inmenu", "Duplicate Extruder N°3"), self.acTion3)
        self.addMenuItem(i18n_cura_catalog.i18nc("@item:inmenu", "Duplicate Extruder N°4"), self.acTion4)
       
    def acTion1(self) -> None:
        self.CopyExtrud(0)

    def acTion2(self) -> None:
        self.CopyExtrud(1)

    def acTion3(self) -> None:
        self.CopyExtrud(2)
 
    def acTion4(self) -> None:
        self.CopyExtrud(3)
        
    # Copy parameter form the ExtruderNb (Reference to the Other Extruder)
    def CopyExtrud(self,ExtruderNb) -> None:
 
        self.Major=1
        self.Minor=0

        Logger.log('d', "Info CuraVersion --> " + str(CuraVersion))
        
        # Test version for Cura Master Release
        if "master" in CuraVersion :
            self.Major=4
            self.Minor=20  
        else:
            try:
                self.Major = int(CuraVersion.split(".")[0])
                self.Minor = int(CuraVersion.split(".")[1])
            except:
                pass
                
        machine_manager = CuraApplication.getInstance().getMachineManager()        
        stack = CuraApplication.getInstance().getGlobalContainerStack()

        global_stack = machine_manager.activeMachine

        #Get extruder count
        extruder_count=stack.getProperty("machine_extruder_count", "value")

        Refer=stack.extruderList[int(extruder_count-1)]
        # Modification from global_stack to extruders[0]
        self.NozzleSize=0
        extruder_stack = CuraApplication.getInstance().getExtruderManager().getActiveExtruderStacks()
        # for Extrud in list(global_stack.extruders.values()):
        for Extrud in extruder_stack:
            PosE = int(Extrud.getMetaDataEntry("position"))
            if PosE == ExtruderNb:
                Refer=Extrud  
 
        # Try to get the reference machine_nozzle_size
        try:
            extrd = stack.extruderList
            self.NozzleSize=float(extrd[ExtruderNb].getProperty("machine_nozzle_size","value"))               
        except:
            pass
                    

        # for Extrud in list(global_stack.extruders.values()):
        for Extrud in extruder_stack:
            PosE = int(Extrud.getMetaDataEntry("position"))
            #Logger.log("d", "Extruder = %s %s", str(PosE), str(ExtruderNb))            
            if PosE != ExtruderNb:
                C_NozzleSize=float(Extrud.getProperty("machine_nozzle_size","value"))
                if self.NozzleSize == C_NozzleSize :
                    self._doTree(Refer,Extrud,"resolution")
                
                # Shell before 4.9 and now walls
                self._doTree(Refer,Extrud,"shell")
                # New section Arachne and 4.9 ?
                if self.Major > 4 or ( self.Major == 4 and self.Minor >= 9 ) :
                    self._doTree(Refer,Extrud,"top_bottom")
                    
                self._doTree(Refer,Extrud,"infill")
                self._doTree(Refer,Extrud,"material")
                self._doTree(Refer,Extrud,"speed")
                self._doTree(Refer,Extrud,"travel")
                self._doTree(Refer,Extrud,"cooling")
                self._doTree(Refer,Extrud,"dual")
                
                self._doTree(Refer,Extrud,"experimental")
                self._doTree(Refer,Extrud,"blackmagic")
                self._doTree(Refer,Extrud,"meshfix")
               
    def _doTree(self,ref,stack,key):   
        
        if stack.getProperty(key,"type") != "category":                         
            # Value of the reference Extruder for the key parameter
            GetVal=ref.getProperty(key,"value")
            # Value of the current Extruder for the key parameter
            CurVal=stack.getProperty(key,"value")

            # If value is different change the value
            if GetVal!=CurVal :
                stack.setProperty(key,"value",GetVal)

        #look for children
        if len(CuraApplication.getInstance().getGlobalContainerStack().getSettingDefinition(key).children) > 0:
            for Child in CuraApplication.getInstance().getGlobalContainerStack().getSettingDefinition(key).children:       
                self._doTree(ref,stack,Child.key)        
