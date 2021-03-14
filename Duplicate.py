# Copyright (c) 2020 5@xes
#
# The Duplicate plugin is released under the terms of the AGPLv3 or higher.
# Release V1.0.2  Update  "resolution","shell","infill","material","speed","travel","cooling","dual"
# Release V1.0.3  Update   "experimental","blackmagic","meshfix" 
# Release V1.0.4  Limit the plugin to release 4.5 -> 4.7
#

from UM.Extension import Extension
from cura.CuraApplication import CuraApplication
from cura.CuraVersion import CuraVersion  

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
       
    def acTion1(self) -> None:
        self.CopyExtrud(0)

    def acTion2(self) -> None:
        self.CopyExtrud(1)

    def acTion3(self) -> None:
        self.CopyExtrud(2)
        
    # Copy parameter form the ExtruderNb (Reference to the Other Extruder)
    def CopyExtrud(self,ExtruderNb) -> None:
 
        VersC=1.0

        # Test version for futur release 4.9
        if "master" in CuraVersion or "beta" in CuraVersion or "BETA" in CuraVersion:
            #Logger.log('d', "Info CuraVersion --> " + str(CuraVersion))
            VersC=4.9  # Master is always a developement version.
        else:
            try:
                VersC = int(CuraVersion.split(".")[0])+int(CuraVersion.split(".")[1])/10
            except:
                pass
                
        machine_manager = CuraApplication.getInstance().getMachineManager()        
        stack = CuraApplication.getInstance().getGlobalContainerStack()

        global_stack = machine_manager.activeMachine

        #Get extruder count
        extruder_count=stack.getProperty("machine_extruder_count", "value")

        Refer=stack.extruderList[int(extruder_count-1)]
        # Modification from global_stack to extruders[0]
        
        for Extrud in list(global_stack.extruders.values()):
            PosE = int(Extrud.getMetaDataEntry("position"))
            if PosE == ExtruderNb:
                Refer=Extrud
        
        for Extrud in list(global_stack.extruders.values()):
            PosE = int(Extrud.getMetaDataEntry("position"))
            #Logger.log("d", "Extruder = %s %s", str(PosE), str(ExtruderNb))            
            if PosE != ExtruderNb:
                self._doTree(Refer,Extrud,"resolution")
                self._doTree(Refer,Extrud,"shell")
                # New section Arachne and 4.9 ?
                if VersC > 4.8:
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
