import sys
sys.path.insert(0,'../..')
sys.path.append('..')
import autosar
import PortInterfaces
import Signals

class GaugeHandler(autosar.Template):
   @classmethod
   def apply(cls, ws):
      componentName = cls.__name__
      package = ws.getComponentTypePackage()
      if package.find(componentName) is None:
         swc = package.createApplicationSoftwareComponent(componentName)
         cls.addPorts(swc)
         cls.addBehavior(swc)
   
   @classmethod
   def addPorts(cls, swc):
      componentName = cls.__name__
      swc.apply(Signals.VehicleSpeed.Receive)
      swc.apply(Signals.EngineSpeed.Receive)
   
   @classmethod
   def addBehavior(cls, swc):
      componentName = cls.__name__
      swc.behavior.createRunnable(componentName+'_Init')
      swc.behavior.createRunnable(componentName+'_Exit')
      swc.behavior.createRunnable(componentName+'_Run', portAccess=[x.name for x in swc.requirePorts+swc.providePorts])
      swc.behavior.createTimerEvent(componentName+'_Run', 20)

if __name__ == '__main__':
   ws = autosar.workspace()
   ws.apply(GaugeHandler)
   ws.saveXML('GaugeHandler.arxml')
