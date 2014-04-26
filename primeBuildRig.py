import maya.cmds as mc
import sys
import os
import json
import string
import re
import sys


#global lists


class NameSpaceCaller:
    def __init__(self):
        if mc.namespace(ex=':jsBuilder') == True:
            mc.namespace(set=':jsBuilder')
        elif mc.namespace(ex=':jsBuilder') == False:
            
            mc.namespace(add='jsBuilder')
            mc.namespace(set=':jsBuilder')
    
    
class LocatorSetup(object):
    def __init__(self):
        global LocatorList 
        LocatorList = []
        mc.namespace(set=':jsBuilder')
        if mc.objExists('jsBuilder:ct_Bind_Chest_bone_Locator') == True:
            mc.error('locators are already in the scene ')
        else:
            self.readXList = []
            self.readYList = []
            self.readZList = []
            self.newDefaultTrans= []
            self.newFloatY = []
            self.newFloatZ = []
            self.nameReadList = []
            self.defaultTransFileRead = []
            self.newDefaultTrans.extend(range(0,203))
            
            LocatorList.extend(range(0,203))
        
            self.readDefaultTrans = []
            self.readDefaultTrans.extend(range(0,203))
     
           
            
            self.fileJointNameOb = open('x:/jsMaya/jsPython/allJointNames.py','r')
            self.nameReadList = [i for i in self.fileJointNameOb.readlines()]
      
           
           
            
            self.defaultTransFileRead = open('x:/jsMaya/jsPython/LocatorDefaultTranslations.py','r')
            
            self.readDefaultTrans = [i for i in self.defaultTransFileRead.readlines()]
           
            for i in range(0,203,1):#need to hardcode list index range here still
                self.newDefaultTrans[i] = json.loads(self.readDefaultTrans[i])#this is how you use json to reinterepret strings to float list items 
            for i in range(0,203,1):
                mc.spaceLocator(a=True,n=self.nameReadList[i] + 'Locator',p=(self.newDefaultTrans[i]))
                LocatorList[i] = mc.ls(sl=True)
                
            mc.select(clear=True)
            
            self.influenceLen = []
            self.influenceLen = len(LocatorList)
           
            
            
            
            
            self.oldTransform = []
            self.oldTransform.extend(range(0,self.influenceLen))
            self.newtransformLocationX = []
            self.newtransformLocationY = []
            self.newtransformLocationZ = []
            self.newtransformLocationX.extend(range(0,self.influenceLen))
            self.newtransformLocationY.extend(range(0,self.influenceLen))
            self.newtransformLocationZ.extend(range(0,self.influenceLen))
            self.latestTransformX = []
            self.latestTransformY = []
            self.latestTransformZ = []
            self.latestTransformX.extend(range(0,self.influenceLen))
            self.latestTransformY.extend(range(0,self.influenceLen))
            self.latestTransformZ.extend(range(0,self.influenceLen))
            self.NewNameList = []
            self.newLocations = []
            self.newLocations.extend(range(0,self.influenceLen))
            for i in range(0,self.influenceLen,1):
                mc.select(LocatorList[i],add=True)
                
            
            self.TransformMenu = []
            
            
        
        
            self.TransformMenu = mc.ls(sl=True,type ='transform')
            mc.select(clear=True)
           
            
            
            if mc.getAttr(self.TransformMenu[0] + '.localPositionX' ) == 0:
                mc.error('Positions are already set move the locators to desired position and then hit build rig')
            else:
                for i in range(0,self.influenceLen,1):
            
                    #since wonderful maya locs are always made in local space regardless of flag via local is offset to match shapenodes loc need to switch attributes
                    self.newtransformLocationX[i] = mc.getAttr(self.TransformMenu[i] + '.localPositionX')
                    self.newtransformLocationY[i] = mc.getAttr(self.TransformMenu[i] + '.localPositionY')
                    self.newtransformLocationZ[i] = mc.getAttr(self.TransformMenu[i] + '.localPositionZ')
                for i in range(0,self.influenceLen,1):
                    mc.setAttr(self.TransformMenu[i] + '.translateX',self.newtransformLocationX[i])
                    mc.setAttr(self.TransformMenu[i] + '.translateY',self.newtransformLocationY[i])
                    mc.setAttr(self.TransformMenu[i] +  '.translateZ',self.newtransformLocationZ[i])
                    mc.setAttr(self.TransformMenu[i] + '.localPositionX',0)
                    mc.setAttr(self.TransformMenu[i] + '.localPositionY',0)
                    mc.setAttr(self.TransformMenu[i] + '.localPositionZ',0)
                for i in range(0,self.influenceLen,1):
            
            
                    self.latestTransformX[i] = mc.getAttr(self.TransformMenu[i] + '.translateX')
                    self.latestTransformY[i] = mc.getAttr(self.TransformMenu[i] + '.translateY')
                    self.latestTransformZ[i] = mc.getAttr(self.TransformMenu[i] + '.translateZ')
           
           
           #NEW STUFF WAS ADDED BELOW THIS LINE TO PARENT UP THE LOCATORS
                    self.currentNameList = open('x:/jsMaya/jsPython/allJointNames.py','r')
                    self.readFileList = [i for i in self.currentNameList.readlines()]
        
                    self.LocatorParentListFileOpen = []
                    self.locatorParentListRead = []
                    self.LocatorParentListFileOpen = open('x:/jsMaya/jsPython/ParentListcurrentforLocators.py','r')
                    self.locatorParentListRead = [i for i in self.LocatorParentListFileOpen.readlines()]
                    self.LocatorParentListFileOpen.close()
        
                    self.locatorChildListFileOpen = []
                    self.locatorChildListFileRead = []
                    self.locatorChildListFileOpen = open('x:/jsMaya/jsPython/ChildListLocators.py','r')
                    self.locatorChildListFileRead = [i for i in self.locatorChildListFileOpen.readlines()]
                    self.locatorChildListFileOpen.close()
        
                for i in range(0,202,1):
                    mc.parent(self.locatorChildListFileRead[i],self.locatorParentListRead[i])
                mc.select(clear=True)
                
#now to setup the parenting order of locators after all information has been setup 
        
#make lists that need to be passed to other classes without re initializing global such as list 


OriginalBindJoints = []

class BuildSkeletonRig:
    def __init__(self):
        global LocatorList
       
        
        global OriginalBindJoints
        
        OriginalBindJoints = []
        OriginalBindJoints.extend(range(0,203))
        self.influenceLen = []
        
        self.influenceLen = len(LocatorList)
        
        self.currentRotateOrderList = []
        self.currentRotateOrderList.extend(range(0,self.influenceLen,1))
        self.getrotateOrderFromFile = open('x:/jsMaya/jsPython/rotOrderTofile.py','r')
        self.NewRotateOrderList = [i for i in self.getrotateOrderFromFile.readlines()]
        self.RotListLen = len(self.NewRotateOrderList)
        self.getrotateOrderFromFile.close()
        
        self.NewRotateOrderListCleaner = []
        self.NewRotateOrderListCleaner.extend(range(0,self.RotListLen))
        for i in range(0,self.RotListLen,1):
            self.NewRotateOrderListCleaner[i] = str(self.NewRotateOrderList[i]).replace('\n','')
        
        mc.namespace(set=':jsBuilder')
        self.currentNameList = open('x:/jsMaya/jsPython/allJointNames.py','r')
        self.readFileList = [i for i in self.currentNameList.readlines()]
        self.currentNameList.close()
        self.newParentList = []
        self.currentChildList = []
        self.ParentList = open('x:/jsMaya/jsPython/ParentListcurrent.py','r')
        
        self.newParentList = [i for i in self.ParentList.readlines()]
        self.ParentList.close()
        
        self.ChildList = open('x:/jsMaya/jsPython/ChildList.py','r')
        
        self.currentChildList = [i for i in self.ChildList.readlines()]
        self.ChildList.close()
        self.latestTransformX = []
        self.latestTransformX.extend(range(0,self.influenceLen,1))
        self.latestTransformY = []
        self.latestTransformY.extend(range(0,self.influenceLen,1))
        self.latestTransformZ = []
        self.latestTransformZ.extend(range(0,self.influenceLen,1))
        
        for i in range(0,self.influenceLen,1):
            mc.select(LocatorList[i],add=True)
        self.TransformMenu = []
        self.TransformMenu = mc.ls(sl=True,type ='transform')
        mc.select(clear=True)
        self.LocatorTransformLocations = []
        self.LocatorTransformLocations.extend(range(0,self.influenceLen))
        for i in range(0,self.influenceLen,1):
            self.LocatorTransformLocations[i] = mc.xform(self.TransformMenu[i],q=True,ws=True,a=True,t=True)
            
        for i in range(0,self.influenceLen,1):
            self.latestTransformX[i] = mc.getAttr(self.TransformMenu[i] + '.translateX')
            self.latestTransformY[i] = mc.getAttr(self.TransformMenu[i] + '.translateY')
            self.latestTransformZ[i] = mc.getAttr(self.TransformMenu[i] + '.translateZ')
            
        
        for i in range(0,self.influenceLen,1):
            mc.joint(n=self.readFileList[i],p=(self.LocatorTransformLocations[i]))
            
            OriginalBindJoints[i]= mc.ls(sl=True)
            
            
            
            
            mc.select(clear=True)
            
        
        
        self.CurrentBindJointList = []
        
        self.CurrentLocatorList = []
        self.CurrentLocatorList.extend(range(0,self.influenceLen))
        self.CurrentBindJointList.extend(range(0,self.influenceLen))
        self.listCleaner = []
        self.listCleaner.extend(range(0,self.influenceLen))
        self.cleanedLocatorList= []
        self.cleanedLocatorList.extend(range(0,self.influenceLen))
        for i in range(0,self.influenceLen,1):
            self.cleanedLocatorList[i] = json.dumps(LocatorList[i],skipkeys=True,separators=(',', ': '))
        
        for i in range(0,self.influenceLen,1):
            self.CurrentLocatorList[i] = str(self.cleanedLocatorList[i]).replace('[','').replace(']','').replace("",'').replace('"','')
            
        
        for i in range(0,self.influenceLen,1):
            self.listCleaner[i] = json.dumps(OriginalBindJoints[i],skipkeys=True,separators=(',', ': '))
            
            
        for i in range(0,self.influenceLen,1):
            self.CurrentBindJointList[i] = str(self.listCleaner[i]).replace('[','').replace(']','').replace("",'').replace('"','')
            
            
        
        
        for i in range(0,self.influenceLen,1):
            mc.joint(self.CurrentBindJointList[i],e=True,roo=self.NewRotateOrderListCleaner[i])
        
       
       
        for i in range(0,202,1):
            mc.parent (self.currentChildList[i],self.newParentList[i])
        mc.select(clear=True)
        
        
        
            
        
        for i in range(0,self.influenceLen,1):
            mc.select(self.CurrentLocatorList[i],add=True)
        mc.delete()
        
            
        
        self.MyJointDictionary = {}
        
        self.MyJointDictionary = {self.readFileList[i]:self.CurrentBindJointList[i] for i in range(0,self.influenceLen) }
       
         
       
        mc.select(self.MyJointDictionary['lt_Bind_Elbow_bone\n'])
        mc.joint(e=True,roo='xyz')
        mc.select(self.MyJointDictionary['lt_Bind_Wrst_bone\n'])
        mc.joint(e=True,roo='yxz')
        mc.select(self.MyJointDictionary['rt_Bind_Wrst_bone\n'])
        mc.joint(e=True,roo='yxz')
        mc.select(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'])
        mc.joint(e=True,roo='xyz')
       
        #now to setup the Orienttion of all the joints 
        mc.select(self.MyJointDictionary['ct_bind_bodyroot_bone\n'])
        mc.makeIdentity(a=True,jo=True,)
        mc.select(self.MyJointDictionary['ct_Bind_spinebase_bone\n'])
        mc.joint(e=True,oj='xyz',sao='yup',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_spinea_bone\n'])
        mc.joint(e=True,oj='xyz',sao='yup',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_spinec_bone\n'])
        mc.joint(e=True,oj='xyz',sao='yup',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_spined_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_spinee_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_spinef_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False)
        
        
        
        mc.select(self.MyJointDictionary['lt_Bind_Femur_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=True)
        mc.select(self.MyJointDictionary['lt_Bind_Calf_bone\n'])
        mc.joint(e=True,oj='xyz',sao='yup',ch=True)
        mc.select(self.MyJointDictionary['lt_Bind_Ankle_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=True)
        mc.select(self.MyJointDictionary['lt_Bind_Clav_bone\n'])
        mc.joint(e=True,oj='xzy',sao='yup',ch=True)
        mc.select(self.MyJointDictionary['lt_Bind_Humerous_bone\n'])
        mc.joint(e=True,oj='xyz',sao='zdown',ch=True)#move down to the wrist, eblow should orient fine 
        mc.select(self.MyJointDictionary['lt_Bind_Wrst_bone\n'])
        mc.joint(e=True,oj='xyz',sao='xup',ch=True)#fingers are all set with this with Child influenced on including thumb
        mc.select(self.MyJointDictionary['ct_Bind_Head_base_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=True,roo='yzx')#jaw looks good as well may need to change
        #for now just copyand pasting to the other side 
        mc.select(self.MyJointDictionary['ct_Bind_chest_tip_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False)
        mc.select(self.MyJointDictionary['ct_Bind_Neck_a_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False,roo='yzx')
        mc.select(self.MyJointDictionary['ct_Bind_Neck_b_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False,roo='yzx')
        mc.select(self.MyJointDictionary['ct_Bind_Neck_c_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=False,roo='yzx')
        
       
        mc.select(self.MyJointDictionary['rt_Bind_Femur_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=True)
        mc.select(self.MyJointDictionary['rt_Bind_Calf_bone\n'])
        mc.joint(e=True,oj='xyz',sao='yup',ch=True)
        mc.select(self.MyJointDictionary['rt_Bind_Ankle_bone\n'])
        mc.joint(e=True,oj='xyz',sao='ydown',ch=True)
        mc.select(self.MyJointDictionary['rt_Bind_Clav_bone\n'])
        mc.joint(e=True,oj='xzy',sao='zdown',ch=False,zso=True)
        mc.select(self.MyJointDictionary['rt_Bind_Humerous_bone\n'])
        mc.joint(e=True,oj='xyz',sao='zdown',ch=True)#move down to the wrist, eblow should orient fine 
        mc.select(self.MyJointDictionary['rt_Bind_Wrst_bone\n'])
        mc.joint(e=True,oj='xyz',sao='xup',ch=True,zso=True)#fingers are all set with this with Child influenced on including thumb
        
        mc.select(self.MyJointDictionary['rt_Bind_Clav_bone\n'])
        mc.joint(e=True,oj='xyz',sao='zdown',ch=False,zso=True)
        self.jawPrimaryOffsetTranslation = []
       
        self.jawMainOffsetPrimary = []#newStuff here for jaw offset
        self.jawMainOffsetSecondary = []
        mc.select(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'])
        mc.group(r=True,n=self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] + 'primaryOffset')
        self.jawMainOffsetPrimary = mc.ls(sl=True)
        mc.group(r=True,n=self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] + 'secondaryOffset')
        mc.jawMainOffsetSecondary = mc.ls(sl=True)
        mc.select(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'])
        self.jawPrimaryOffsetTranslation = mc.joint(q=True,r=True,p=True)
        mc.select(self.jawMainOffsetPrimary[0])
        
        mc.xform(t=(self.jawPrimaryOffsetTranslation[0],self.jawPrimaryOffsetTranslation[1],self.jawPrimaryOffsetTranslation[2]))
        mc.select(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'])
        mc.setAttr((self.MyJointDictionary['ct_Bind_Jaw_main_bone\n']) + '.translateX',0)
        mc.setAttr((self.MyJointDictionary['ct_Bind_Jaw_main_bone\n']) + '.translateY',0)
        mc.setAttr((self.MyJointDictionary['ct_Bind_Jaw_main_bone\n']) + '.translateZ',0)
        
       
        
        self.influenceJointsList = []
        self.twistJointsList = []
        
        self.influenceJointsList = [ i for i in self.CurrentBindJointList if 'inf' in i]
        self.twistJointsList = [i for i in self.CurrentBindJointList if 'twist' in i]#grab anything in list with flagged string to put it in its own list
            
        self.twistAmnt = len(self.twistJointsList)
        self.inflAmnt = len(self.influenceJointsList)
        self.influenceprimaryOffsetList =[]
        self.influencesecondaryOffsetList = []
        self.twistOffsetPrimary = []
        self.twistOffsetSecondary = []
        self.twistOffsetPrimary.extend(range(0,self.twistAmnt))#this is how you create offsets in code for each item first step is selecting the object you want  to group
        self.twistOffsetSecondary.extend(range(0,self.twistAmnt))#second step is grouping that object and then selecting that group object and putting into a list
        self.influenceprimaryOffsetList.extend(range(0,self.inflAmnt))#third step would be to select the object that was grouped , set the attributes to zero
        self.influencesecondaryOffsetList.extend(range(0,self.inflAmnt))#fourth step would be
        for i in range(0,self.inflAmnt,1):
            mc.select(self.influenceJointsList[i])
            mc.group(r=True,n=self.influenceJointsList[i] + 'primaryOffset')#setting up the offsets for face influences
            self.influenceprimaryOffsetList[i] = mc.ls(sl=True)
            mc.group(r=True,n=self.influenceJointsList[i] + 'secondaryOffset')
            self.influencesecondaryOffsetList[i]=mc.ls(sl=True)#taket the offsets and place them in thier own list 
            mc.select(clear=True)
        
        
        self.InfOffsetLen = len(self.influenceprimaryOffsetList)
        self.localTransformOffset = []
        self.localTransformOffset.extend(range(0,self.inflAmnt))
        self.localTransformTwistOffset = []
        self.localTransformTwistOffset.extend(range(0,self.twistAmnt))
        self.influenceRelativeTransformX = []
        self.influenceRelativeTransformY = []
        self.influenceRelativeTransformZ = []
        self.influenceRelativeTransformX.extend(range(0,self.InfOffsetLen))
        self.influenceRelativeTransformY.extend(range(0,self.InfOffsetLen))
        self.influenceRelativeTransformZ.extend(range(0,self.InfOffsetLen))
        for i in range(0,self.inflAmnt,1):
            self.localTransformOffset[i] = mc.joint(self.influenceJointsList[i],q=True,r=True,p=True)
        for i in range(0,self.inflAmnt,1):
            mc.xform(self.influenceprimaryOffsetList[i],t=(self.localTransformOffset[i]))
            
            
            
            mc.setAttr(self.influenceJointsList[i] + '.translateX',0)
            mc.setAttr(self.influenceJointsList[i] + '.translateY',0)
            mc.setAttr(self.influenceJointsList[i] + '.translateZ',0)
            mc.setAttr(self.influenceJointsList[i] + '.jointOrientX',0)
            mc.setAttr(self.influenceJointsList[i] + '.jointOrientY',0)
            mc.setAttr(self.influenceJointsList[i] + '.jointOrientZ',0)
            mc.select(clear=True)
        for i in range(0,self.twistAmnt,1):#first phase just grabs the information and creates the offsets for the twist joints to prevent them from getting that connection thingy
            mc.select(self.twistJointsList[i])
            mc.group(r=True,n=self.twistJointsList[i] + 'PrimaryOffset')
            self.twistOffsetPrimary[i] = mc.ls(sl=True)
            mc.group(r=True,n=self.twistJointsList[i] + 'SecondaryOffset')
            self.twistOffsetSecondary[i] = mc.ls(sl=True)
            mc.select(clear=True)
        for i in range(0,self.twistAmnt,1):#first qeury the relative under parent pos of each joint
            self.localTransformTwistOffset[i] = mc.joint(self.twistJointsList[i],q=True,r=True,p=True)#set the offset to the joiints relative amount then zero out the joint
        for i in range(0,self.twistAmnt,1):
            mc.xform(self.twistOffsetPrimary[i],t=(self.localTransformTwistOffset[i]))
            mc.setAttr(self.twistJointsList[i] + '.translateX',0)
            mc.setAttr(self.twistJointsList[i] + '.translateY',0)
            mc.setAttr(self.twistJointsList[i] + '.translateZ',0)
            mc.setAttr(self.twistJointsList[i] + '.jointOrientX',0)
            mc.setAttr(self.twistJointsList[i] + '.jointOrientY',0)
            mc.setAttr(self.twistJointsList[i] + '.jointOrientZ',0)
            mc.select(clear=True)
        
        self.TwistMdivList = []
        self.TwistMdivList.extend(range(0,self.twistAmnt))
        self.TwistJointDict = {}
        self.TwistJointMDivDict = {}
            
        for i in range(0,self.twistAmnt,1):
            mc.shadingNode('multiplyDivide',n=self.twistJointsList[i] + 'Mdiv',au=True)
            self.TwistMdivList[i] = mc.ls(sl=True)
            mc.select(clear=True)
        self.TwistJointName = []
        self.TwistJointName.extend(range(self.twistAmnt))
        self.TwistJointCleaner = []
        self.TwistJointCleaner.extend(range(0,self.twistAmnt,1))
        self.TwistJointMdivCleaner = []
        self.TwistJointMdivCleaner.extend(range(0,self.twistAmnt))
        self.CurrentTwistJointMdivList = []
        self.CurrentTwistJointMdivList.extend(range(0,self.twistAmnt))
        self.CurrentTwistJointName = []
        self.CurrentTwistJointName.extend(range(0,self.twistAmnt))
        str(self.TwistMdivList)
        for i in range(0,self.twistAmnt,1):
            mc.select(self.twistJointsList[i])
            self.TwistJointName[i] = mc.ls(sl=True,sn=True)
            mc.select(clear=True)
        self.TwistJointNameCleaner = []
        self.TwistJointNameCleaner.extend(range(0,self.twistAmnt))
        for i in range(0,self.twistAmnt,1):
            self.TwistJointNameCleaner[i] =json.dumps(self.TwistJointName[i],skipkeys=True,separators=(',', ': '))
        for i in range(0,self.twistAmnt,1):
            self.CurrentTwistJointName[i] = str(self.TwistJointNameCleaner[i].replace('[','').replace(']','').replace("",'').replace('"',''))
            
        for i in range(0,self.twistAmnt,1):
            self.TwistJointMdivCleaner[i] = json.dumps(self.TwistMdivList[i],skipkeys=True,separators=(',', ': '))
        for i in range(0,self.twistAmnt,1):
            self.CurrentTwistJointMdivList[i] = str(self.TwistJointMdivCleaner[i].replace('[','').replace(']','').replace("",'').replace('"',''))
        
        #ommitting the connection between the twist joints to have an IKSPine drive their twist
        #for i in range(0,self.twistAmnt,1):
            #mc.connectAttr(self.CurrentTwistJointMdivList[i] + '.outputX',self.twistJointsList[i] + '.rotateX')
            #mc.connectAttr(self.CurrentTwistJointMdivList[i] + '.outputY',self.twistJointsList[i] + '.rotateY')
            #mc.connectAttr(self.CurrentTwistJointMdivList[i] + '.outputZ',self.twistJointsList[i] + '.rotateZ')
        
        self.TwistJointDict = {self.CurrentTwistJointName[i]:self.twistJointsList[i] for i in range(0,self.twistAmnt)}
        self.TwistJointMDivDict = {self.CurrentTwistJointName[i]:self.CurrentTwistJointMdivList[i] for i in range(0,self.twistAmnt)}
        
        self.InfluenceJointName = []
        self.InfluenceJointName.extend(range(0,self.inflAmnt))
        self.InfluenceMDiv = []
        self.InfluenceMDiv.extend(range(0,self.inflAmnt))
        self.InfluenceMdivCleaner = []
        self.InfluenceMdivCleaner.extend(range(0,self.inflAmnt))
        self.InfluenceMdivCurrent = []
        self.InfluenceMdivCurrent.extend(range(0,self.inflAmnt))
        self.InfluenceJointNameCurrent = []
        self.InfluenceJointNameCurrent.extend(range(0,self.inflAmnt))

        
        for i in range(0,self.inflAmnt,1):
            mc.select(self.influenceJointsList[i])
            self.InfluenceJointName[i]= mc.ls(sl=True)
            mc.select(clear=True)
        
        self.InfluenceJointNameCleaner = []
        self.InfluenceJointNameCleaner.extend(range(0,self.inflAmnt))
        
        for i in range(0,self.inflAmnt,1):
            mc.shadingNode('multiplyDivide',n=self.influenceJointsList[i] + 'Mdiv',au=True)
            self.InfluenceMDiv[i] = mc.ls(sl=True)
            mc.select(clear=True)
        for i in range(0,self.inflAmnt,1):
            self.InfluenceMdivCleaner[i] = json.dumps(self.InfluenceMDiv[i],skipkeys=True,separators=(',', ': '))
            
        for i in range(0,self.inflAmnt,1):
            self.InfluenceMdivCurrent[i] = str(self.InfluenceMdivCleaner[i].replace('[','').replace(']','').replace("",'').replace('"',''))
            
        self.InfluenceMdivJointDict= {}
        self.InfluenceJointDict = {}
        for i in range(0,self.inflAmnt,1):
            self.InfluenceJointNameCleaner[i] = json.dumps(self.InfluenceJointName[i],skipkeys=True,separators=(',', ': '))
        for i in range(0,self.inflAmnt,1):
            self.InfluenceJointNameCurrent[i] = str(self.InfluenceJointNameCleaner[i].replace('[','').replace(']','').replace("",'').replace('"',''))
            
        
        self.InfluenceJointDict = {self.InfluenceJointNameCurrent[i]:self.influenceJointsList[i] for i in range(0,self.inflAmnt)}
        
        self.InfluenceMDivJointDict = {self.InfluenceJointNameCurrent[i]:self.InfluenceMdivCurrent[i] for i in range(0,self.inflAmnt)}
        
         
        
        
       
         
         #self.TwistJointMDivDict = {self.CurrentTwistJointName[i]:self.CurrentTwistJointMdivList[i] for i in range(0,self.twistAmnt)}
         #now to connect the joints in the bind to the mdivs then to the influence joints from the mvdiv list 
        for i in range(0,self.inflAmnt,1):
            mc.connectAttr(self.InfluenceMdivCurrent[i] + '.outputX',self.influenceJointsList[i] + '.rotateX')
            mc.connectAttr(self.InfluenceMdivCurrent[i] + '.outputY',self.influenceJointsList[i] + '.rotateY')
            mc.connectAttr(self.InfluenceMdivCurrent[i] + '.outputZ',self.influenceJointsList[i] + '.rotateZ')
            
        self.MDivJawInfList = [i for i in self.InfluenceMdivCurrent if 'jaw' in i]
    
            
        self.jawinfluenceList = [i for i in self.influenceJointsList if 'jaw' in i]
        self.headinfluenceList = [i for i in self.influenceJointsList if 'head' in i]
        
        self.amntOfJawInf = len(self.jawinfluenceList)
        self.amntOfHeadInf = len(self.headinfluenceList)
        #print self.jawinfluenceList
        #print self.MDivJawInfList
        
        
        for i in range(0,self.amntOfJawInf,1):
            mc.connectAttr(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] + '.rotateX',self.MDivJawInfList[i] + '.input1X')
            mc.connectAttr(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] + '.rotateY',self.MDivJawInfList[i] + '.input1Y')
            mc.connectAttr(self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] + '.rotateZ',self.MDivJawInfList[i] + '.input1Z')
        
        
        #ref for json dump #turning off direct connection from body bind jointsto twist bind since an ik spline will be used for twist for now
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Clav_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_clavicle_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Clav_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_clavicle_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Humerous_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_shoulder_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Humerous_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_shoulder_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Elbow_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_elbow_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Elbow_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_elbow_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Femur_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_femur_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Femur_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_femur_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['lt_Bind_Calf_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:lt_calf_twist_b'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_a'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_a'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_a'] + '.input1Z')
        
        mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateX', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_b'] + '.input1X')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateY', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_b'] + '.input1Y')
        #mc.connectAttr(self.MyJointDictionary['rt_Bind_Calf_bone\n'] + '.rotateZ', self.TwistJointMDivDict['jsBuilder:rt_calf_twist_b'] + '.input1Z')
        
        #start building the fk control rig first 
        #delete all orientconstraints to the twist joints
        #mc.connectAttr(self.TwistJointMDivDict['jsBuilder:rt_calf_twist_b'] + '.outputX')
        
        mc.select(self.MyJointDictionary['ct_bind_bodyroot_bone\n'],hi=True)
        self.CurrentHiarchyBind = mc.ls(sl=True,type='joint')
        
        mc.duplicate(un=True,rc=True)
        mc.select(clear=True)
        mc.select('jsBuilder:ct_bind_bodyroot_bone1',hi=True)
        self.FkSkeletonBones = mc.ls(sl=True,type='joint')
        self.FkControlSkeletonList = mc.listConnections(c=True,s=True,d=True)
        #after duplication go through list and put orient constraints from the  fk skeleton to the bind skeleton
        
        
        self.FkSkeletonHi = mc.ls(sl=True,type='joint')
        
        
        self.LenOfFkDuped = []
        
        self.LenOfFkDuped = len(self.FkSkeletonHi)
        
        mc.select(self.CurrentBindJointList[0],hi=True)
        
        
        
        
        mc.container(n='FkControlSkeletonContainer')
        
        self.FkSkeletonLen = len(self.FkControlSkeletonList)
        
        #make two identical lists so that set same list of fk joints constrains all of the bind joints in an orient constraint
        
        for i in range(0,self.FkSkeletonLen,1):
            mc.container(e=True,an=self.FkControlSkeletonList,inc=True)
            
        #mc.select('jsBuilder:jsBuilder:rt_Bind_Wrst_bone1')
        #mc.delete()
        #mc.select('jsBuilder:jsBuilder:lt_Bind_Wrst_bone1')
        #mc.delete()
        for i in range(0,203,1):
            mc.orientConstraint(self.FkSkeletonHi[i],self.CurrentHiarchyBind[i],n=self.FkSkeletonHi[i] + 'FkOrientCst',mo=False)
        mc.select(clear=True)
        
        self.OrientsOfTwistJoints = [i for i in self.twistJointsList if 'FkOrientCst' in i]
        self.LenOfOrientsTwist = len(self.OrientsOfTwistJoints)
        for i in range(0,self.LenOfOrientsTwist,1):
            mc.delete(self.OrientsOfTwistJoints[i])
        
        #rename all Joints in the bind Container with FkSkeletonExtension this will not change the Orient Nmes 
        
        mc.select('jsBuilder:ct_bind_bodyroot_bone1',hi=True)
        
        self.RenameFkJointsList = mc.ls(sl=True,type='transform')
        
        self.LenOfFKListInContiner = len(self.RenameFkJointsList)
        
        for  i in range(0,self.LenOfFKListInContiner,1):#this is to rename the stuff TO bind skeleton
            mc.rename(self.RenameFkJointsList[i],self.RenameFkJointsList[i] + '_FkControlSkeleton')
     #newstuff added here to apply Fk control Joints        
        mc.select('jsBuilder:lt_Bind_Humerous_bone1_FkControlSkeleton',hi=True)
        self.LtArmJointsSel = mc.ls(sl=True,type='joint')
        self.BonesForLeftArmFkControls = [i for i  in self.LtArmJointsSel if 'bone' in i]
        self.LenOfleftArmFkCtrls = []
        #self.BonesForLeftArmFkControls = mc.ls(sl=True,type='joint')
        self.LenOfleftArmFkCtrls= len(self.BonesForLeftArmFkControls)#select a hiarchy and list it 
        self.LeftArmFkLocation = []
        self.LeftArmFkLocation.extend(range(0,self.LenOfleftArmFkCtrls))
        self.LeftArmFkRotationOrder = []
        self.LeftArmFkRotationOrder.extend(range(0,self.LenOfleftArmFkCtrls))
        self.LeftArmFkRotation = []
        self.LeftArmFkRotation.extend(range(0,self.LenOfleftArmFkCtrls))
        self.LeftArmFkLocationAxis = []
        self.LeftArmFkLocationAxis.extend(range(0,self.LenOfleftArmFkCtrls))
        mc.select(clear=True)
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.LenOfleftArmFkCtrls))

        for i in range(0,self.LenOfleftArmFkCtrls,1):
            self.LeftArmFkLocation[i] = mc.xform(self.BonesForLeftArmFkControls[i],q=True,ws=True,t=True)
            self.LeftArmFkLocationAxis[i] = mc.xform(self.BonesForLeftArmFkControls[i], q=True,ra=True)
            self.LeftArmFkRotationOrder[i] = mc.xform(self.BonesForLeftArmFkControls[i],q=True,roo=True)
            self.LeftArmFkRotation[i] = mc.xform(self.BonesForLeftArmFkControls[i],q=True,ws=True,ro=True)
            self.MoveControls[i] = mc.getAttr(self.BonesForLeftArmFkControls[i] + '.translateX')
            
        str(self.LeftArmFkRotationOrder)
        self.genericFkControl = []
        self.genericFkControl.extend(range(0,self.LenOfleftArmFkCtrls))
        
        #for i in range(0,self.LenOfleftArmFkCtrls,1):#instead of importing buidl the curve inteactively and then use those commands to rebuild it 
            #mc.file('c:/Library/StandardFkCtrl.ma',sa=True,add=True)
        #self.genericFkControl = mc.ls(sl=True)
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.LenOfleftArmFkCtrls))
        for i in range(0,self.LenOfleftArmFkCtrls,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i] / 2
            
            
        self.CreatedCurveArmControllers = []
        self.CreatedCurveArmControllers.extend(range(0,self.LenOfleftArmFkCtrls))
        self.CreatedCurveArmOffsets = []
        self.CreatedCurveArmOffsets.extend(range(0,self.LenOfleftArmFkCtrls))
        

         
        mc.select('jsBuilder:ct_Bind_spinebase_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + 'FkCtrl',p=[(19.537437, 131.679611, 8.061296), (18.445017, 131.285553, 11.135503), (17.002312, 131.189896, 13.754279), (15.103527, 131.24559, 16.035719), (10.421452, 131.196167, 19.642796), (7.833237, 131.032639, 20.849792), (5.144627, 131.125854, 21.596169), (2.478235, 131.309952, 21.759583), (0.133853, 132.084396, 22.020208), (-2.396593, 131.312897, 21.766132), (-5.120296, 131.122131, 21.626188), (-7.789712, 131.035278, 20.885956), (-10.435552, 131.209579, 19.687733), (-12.949655, 131.266403, 18.05711), (-15.18443, 131.306412, 16.061869), (-17.068089, 131.254807, 13.764997), (-18.494825, 131.339935, 11.140775), (-19.570168, 131.717926, 8.060578), (-20.012945, 132.150177, 4.697925), (-20.012945, 132.150177, 4.697925), (-19.671223, 132.393631, 1.36716), (-18.736166, 132.411819, -1.652516), (-16.666689, 133.961472, -4.612699), (-13.820146, 133.914658, -6.417686), (-10.929472, 133.787766, -7.626118), (-8.122061, 133.992599, -8.717563), (-5.288171, 134.490036, -9.58902), (-0.00784261, 135.123322, -10.285574), (2.550372, 134.945892, -10.204492), (5.304212, 134.515823, -9.734278), (8.162846, 134.061035, -8.889573), (8.162846, 134.061035, -8.889573), (11.01086, 133.854309, -7.764009), (13.922171, 133.978607, -6.504992), (16.736809, 133.967972, -4.681503), (18.748259, 132.400162, -1.680037), (19.659306, 132.376709, 1.365426), (20.000446, 132.130371, 4.702749), (19.537437, 131.679611, 8.061296), (19.591284, 129.708893, 8.320892), (19.383345, 127.690506, 8.472831), (18.901014, 126.039398, 8.703899), (16.867777, 123.980934, 12.617893), (14.379173, 123.641243, 14.941631), (13.071309, 124.250687, 16.649424), (11.422743, 124.67115, 18.206682), (9.211647, 124.5392, 19.359798), (6.890871, 124.467766, 20.39852), (4.504161, 124.888634, 21.228495), (2.201558, 125.114075, 21.473539), (0.222241, 125.155106, 21.301355), (-2.16705, 125.035896, 21.464878), (-4.563496, 124.859924, 21.311773), (-7.086006, 124.506813, 20.574707), (-9.500278, 124.640396, 19.563057), (-11.966305, 124.91925, 18.424948), (-13.80216, 124.631577, 16.76564), (-15.161036, 124.001488, 14.865781), (-17.320494, 124.168846, 12.471143), (-19.108582, 126.132469, 8.580639), (-19.645239, 127.832764, 4.516905), (-19.071949, 129.092468, 0.490369), (-17.758808, 130.279129, -2.882694), (-15.262953, 131.021484, -5.056462), (-11.681703, 130.784409, -6.620074), (-9.544989, 130.807129, -7.508105), (-7.281141, 130.879822, -8.299451), (-4.69902, 131.069092, -8.980317), (-2.138609, 131.01564, -9.44505), (0.0868796, 131.138916, -9.33481), (2.136799, 130.996002, -9.364803), (4.70121, 131.043289, -9.074614), (7.346045, 130.995911, -8.441655), (9.738814, 130.950638, -7.639713), (11.918104, 130.888626, -6.701474), (15.304102, 131.030777, -5.150705), (17.684059, 130.281937, -3.020864), (19.047665, 129.059982, 0.483629), (19.544516, 127.760323, 4.636987), (18.901014, 126.039398, 8.703899), (19.383345, 127.690506, 8.472831), (19.591284, 129.708893, 8.320892), (19.537437, 131.679611, 8.061296), (19.415634, 133.56076, 7.923638), (19.373468, 134.158493, 7.995557), (18.49715, 133.79689, 10.730019), (17.293556, 134.267029, 13.005758), (15.259331, 134.269638, 15.683678), (12.897228, 134.27124, 17.72724), (10.340284, 134.166077, 19.256367), (7.645327, 134.151917, 20.373791), (4.953649, 134.128784, 21.186563), (2.259784, 134.174057, 21.55566), (0.0434455, 134.574554, 21.524206), (-2.236433, 134.180267, 21.551147), (-4.932786, 134.136322, 21.196362), (-10.319773, 134.187881, 19.281979), (-12.916894, 134.30365, 17.769184), (-15.284954, 134.312622, 15.721148), (-15.284954, 134.312622, 15.721148), (-17.326771, 134.310257, 13.034142), (-18.543449, 133.822342, 10.757668), (-19.38715, 134.183319, 8.012358), (-19.894011, 134.597595, 4.737554), (-19.627632, 134.819489, 1.298142), (-18.548454, 134.799133, -1.951764), (-16.664165, 134.643646, -4.662004), (-13.94239, 134.551605, -6.488129), (-11.081696, 134.515106, -7.746943), (-8.236025, 134.811981, -8.862743), (-5.368511, 135.456085, -9.755206), (-2.573399, 135.934326, -10.309042), (-0.00524332, 136.109436, -10.481065), (2.575172, 135.946655, -10.364232), (5.384503, 135.498108, -9.893888), (8.275328, 134.904221, -9.037498), (11.160662, 134.606476, -7.897371), (14.051376, 134.627731, -6.582828), (18.554338, 134.805817, -1.975626), (18.554338, 134.805817, -1.975626), (19.604557, 134.814636, 1.27887), (19.869745, 134.579102, 4.723736), (19.869745, 134.579102, 4.723736), (19.373468, 134.158493, 7.995557)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123],d=1) 
            mc.CenterPivot()
            mc.move(0,0,0,rpr=True)
            mc.xform(ws=True,a=True,ro=(0,-90,90))
            mc.CenterPivot()
            mc.xform(s=(1.3,.1,1.3))
            mc.makeIdentity(a=True)
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 75:
                break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
        mc.select('jsBuilder:jsBuilder:ct_Bind_Chest_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
    
    
        mc.select('jsBuilder:lt_Bind_Femur_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(1.5,1.5,1.5))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
        mc.select('jsBuilder:rt_Bind_Femur_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(1.5,1.5,1.5))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
        
        mc.select('jsBuilder:lt_Bind_Clav_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            if i == 26:
                break
        
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),scale=(1.1,1.1,.8))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
        
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 26:
               break
               
            
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
            
            
            mc.select('jsBuilder:ct_Bind_Neck_a_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.circle(nr=(1,0,0),sw=360,r=7,fc=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrl')
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 9:
               break
               
            
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            mc.select('jsBuilder:rt_Bind_Clav_bone1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            if i == 26:
                break
        
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),scale=(.8,.8,.8))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
        
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 26:
               break
               
            
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
            
            

        mc.select('jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:ct_Bind_Head_a_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        
        mc.select('jsBuilder:ct_tng_Bind_a1_FkControlSkeleton',hi=True)#this process can be repeated for each major chunk just change the break amount accordingly
        
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = mc.ls(sl=True,type='joint')
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentFkBonesOnly)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.circle(nr=(1,0,0),sw=360,r=1,fc=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrl')
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 9:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
        
        
        mc.select('jsBuilder:lt_Bind_Index_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
        mc.select('jsBuilder:lt_Bind_Rfinger_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
        
        mc.select('jsBuilder:lt_Bind_Pinky_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
        mc.select('jsBuilder:lt_Bind_Mfinger_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
        mc.select('jsBuilder:rt_Bind_Index_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
        mc.select('jsBuilder:rt_Bind_Mfinger_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
            
        mc.select('jsBuilder:rt_Bind_Rfinger_base_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
        
        mc.select('jsBuilder:rt_Bind_Pinky_base_bone1_FkControlSkeleton',hi=True)
        
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 3:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 3:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
            
        mc.select('jsBuilder:jsBuilder:ct_bind_SpineEnd_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:rt_Bind_Thmb_c_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeletonFkCtrlOffset1')
        mc.delete()
        
        
        
        mc.select('jsBuilder:rt_Bind_Thmb_a_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 2:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)
            
        #mc.move(self.CurrentFkControllers[i],os=True,r=True,x=(self.HalfMoveAmnt[i]))
        for i in range(0,self.CurrentCountForFk,1):#parent the offsets under the controllers
            if i == 2:
               break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentFkBonesOnly[i],n=self.CurrentFkBonesOnly[i] + '_FkConstraint')
          
        del self.CurrentFkBonesOnly[:]  
        
        mc.select('jsBuilder:lt_Bind_Thmb_a_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 2:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentFkBonesOnly[i] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.xform(ro=(0,0,90),s=(.25,.06,.25))
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)        
        
       
       #making Root for All objects 
        mc.select('jsBuilder:jsBuilder:ct_bind_bodyroot_bone1_FkControlSkeleton')
        self.RootJoint = mc.ls(sl=True,type='joint')
        self.RootLocation = mc.xform(self.RootJoint[0],q=True,ws=True,a=True,t=True)
        self.RootRotation = mc.xform(self.RootJoint[0],q=True,ws=True,ro=True)
        self.RootAxis = mc.xform(self.RootJoint[0],q=True,ra=True)
        self.RootRotationOrder = mc.xform(self.RootJoint[0],q=True,roo=True)
        #make controller curve 
        mc.curve(n='RootControl', d=3, p=[( 13.200139 ,0 ,73.786966 ),( 28.142021 ,0 ,71.044301 ),( 56.472856, 0 ,56.472856 ),( 73.786966, 0 ,13.20014 ),( 73.786966 ,0 ,13.20014 ),( 73.786966, 0 ,13.20014 ),( 87.630318 ,0 ,13.200139 ),( 87.630318 ,0 ,13.200139 ),( 87.630318 ,0 ,22.000229 ),( 87.630318, 0 ,22.000229 ),( 110.663092 ,0 ,0 ),( 110.663092, 0 ,0 ),( 110.663092, 0 ,0 ),( 87.630318 ,0 ,-22.000229 ),( 87.630318 ,0 ,-22.000229 ),( 87.630318, 0 ,-13.200139 ),( 87.630318, 0 ,-13.200139 ),( 73.786966 ,0 ,-13.200139 ),( 73.786966, 0, -13.200139 ),( 71.044301, 0 ,-28.142021 ),( 56.472856, 0 ,-56.472856 ),( 28.142021, 0 ,-71.044301 ),( 13.20014 ,0 ,-73.786966 ),( 13.20014, 0, -73.786966 ),( 13.20014 ,0 ,-73.786966 ),( 13.200139 ,0, -87.630318 ),( 13.200139 ,0 ,-87.630318 ),( 13.200139, 0 ,-87.630318 ),( 22.000229, 0 ,-87.630318 ),( 22.000229 ,0 ,-87.630318 ),( 0, 0 ,-110.663092 ),( 0, 0, -110.663092 ),( -22.000229, 0 ,-87.630318 ),( -22.000229 ,0 ,-87.630318 ),( -13.200139 ,0 ,-87.630318 ),( -13.200139, 0 ,-87.630318 ),( -13.20014, 0 ,-73.786966 ),( -13.20014, 0 ,-73.786966 ),( -13.20014, 0 ,-73.786966 ),( -28.142021, 0 ,-71.044301 ),( -56.472856, 0 ,-56.472856 ),( -71.044301, 0 ,-28.142021 ),( -73.786966, 0 ,-13.20014 ),( -73.786966, 0 ,-13.20014 ),( -87.630318, 0 ,-13.200139 ),( -87.630318 ,0 ,-13.200139 ),( -87.630318, 0 ,-22.000229 ),( -87.630318 ,0 ,-22.000229 ),( -110.663092, 0 ,0 ),( -110.663092, 0, 0 ),( -87.630318 ,0 ,22.000229 ),( -87.630318, 0, 22.000229 ),( -87.630318 ,0 ,13.200139 ),( -87.630318, 0, 13.200139 ),( -73.786966, 0 ,13.200139 ),( -73.786966 ,0, 13.200139 ),( -71.044301 ,0 ,28.142021 ),( -56.472856 ,0 ,56.472856 ),( -28.142021 ,0, 71.044301 ),( -13.20014, 0 ,73.786966 ),( -13.20014, 0 ,73.786966 ),( -13.20014, 0, 73.786966 ),( -13.200139 ,0 ,87.630318 ),( -13.200139 ,0, 87.630318 ),( -13.200139 ,0, 87.630318 ),( -22.000229 ,0 ,87.630318 ),( -22.000229 ,0 ,87.630318 ),( 0, 0 ,110.663092 ),( 0, 0, 110.663092 ),( 22.000229, 0 ,87.630318 ),( 22.000229, 0 ,87.630318 ),( 13.200139, 0 ,87.630318 ),( 13.200139, 0 ,87.630318 ),( 13.200139, 0, 73.786966)],k=[ 0 , 0 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 71 , 71 ])
        mc.makeIdentity(apply=True)
        self.ControlRoot = mc.ls(sl=True)
        mc.xform(roo=(self.RootRotationOrder),t=(0,0,0))
        mc.group(em=True,n='RootControl_Offset')
        self.ControlRootOffsett = mc.ls(sl=True)
        mc.xform(roo=(self.RootRotationOrder),t=(0,0,0))
        mc.parent(self.ControlRoot,self.ControlRootOffsett)
        mc.parentConstraint(self.ControlRoot,self.RootJoint,n='RootControlConstraint',mo=True)
        mc.select(clear=True)
        
        
        
        
        
        mc.select('jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton',hi=True)
        self.WristFkJoint = mc.ls(sl=True,type='joint')
        self.WristFkLocation = mc.xform(self.WristFkJoint[0],q=True,ws=True,a=True,t=True)
        self.WristFkRotation = mc.xform(self.WristFkJoint[0],q=True,ws=True,ro=True)
        self.WristFkRotationAxis = mc.xform(self.WristFkJoint[0],q=True,ra=True)
        self.WristFkRotationOrder = mc.xform(self.WristFkJoint[0],q=True,roo=True)
        #make controller curve 
        mc.curve(n=self.WristFkJoint[0] + '_FkController',d= 1 ,p=[( 0 ,3 ,0 ),( 0 ,2 ,-2 ),( 0 ,0, -3 ),( 0 ,-2, -2 ),( 0, -3, 0 ),( 0 ,-2, 2 ),( 0, 0 ,3 ),( 0, 2, 2 ),( 0 ,3 ,0 ),( 2, 2 ,0 ),( 3, 0 ,0 ),( 2 ,-2, 0 ),( 0 ,-3 ,0 ),( -2 ,-2 ,0 ),( -3, 0 ,0 ),( -2 ,2 ,0 ),( 0, 3 ,0)], k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16])
        self.WristController = mc.ls(sl=True)
        mc.xform(s=(3,3,3))
        mc.makeIdentity(apply=True,scale=True)
        mc.xform(ro=(self.WristFkRotation[0],self.WristFkRotation[1],self.WristFkRotation[2]),roo=(self.WristFkRotationOrder),t=(self.WristFkLocation[0],self.WristFkLocation[1],self.WristFkLocation[2]),ra=(self.WristFkRotationAxis[0],self.WristFkRotationAxis[1],self.WristFkRotationAxis[2]))
        mc.group(em=True,n=self.WristFkJoint[0] + '_FkCtrlOffset')
        self.WristControllerOffset = mc.ls(sl=True)
        mc.xform(ro=(self.WristFkRotation[0],self.WristFkRotation[1],self.WristFkRotation[2]),roo=(self.WristFkRotationOrder),t=(self.WristFkLocation[0],self.WristFkLocation[1],self.WristFkLocation[2]),ra=(self.WristFkRotationAxis[0],self.WristFkRotationAxis[1],self.WristFkRotationAxis[2]))
        mc.parent(self.WristController,self.WristControllerOffset)
        mc.orientConstraint(self.WristController[0],self.WristFkJoint[0],n=self.WristFkJoint[0] + 'FkConstraint')
        mc.select(clear=True)
       #making Root for All objects 
       
        mc.select('jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton',hi=True)
        self.WristFkJoint = mc.ls(sl=True,type='joint')
        self.WristFkLocation = mc.xform(self.WristFkJoint[0],q=True,ws=True,a=True,t=True)
        self.WristFkRotation = mc.xform(self.WristFkJoint[0],q=True,ws=True,ro=True)
        self.WristFkRotationAxis = mc.xform(self.WristFkJoint[0],q=True,ra=True)
        self.WristFkRotationOrder = mc.xform(self.WristFkJoint[0],q=True,roo=True)
        #make controller curve 
        mc.curve(n=self.WristFkJoint[0] + '_FkController',d= 1 ,p=[( 0 ,3 ,0 ),( 0 ,2 ,-2 ),( 0 ,0, -3 ),( 0 ,-2, -2 ),( 0, -3, 0 ),( 0 ,-2, 2 ),( 0, 0 ,3 ),( 0, 2, 2 ),( 0 ,3 ,0 ),( 2, 2 ,0 ),( 3, 0 ,0 ),( 2 ,-2, 0 ),( 0 ,-3 ,0 ),( -2 ,-2 ,0 ),( -3, 0 ,0 ),( -2 ,2 ,0 ),( 0, 3 ,0)], k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16])
        self.WristController = mc.ls(sl=True)
        mc.xform(s=(3,3,3))
        mc.makeIdentity(apply=True,scale=True)
        mc.xform(ro=(self.WristFkRotation[0],self.WristFkRotation[1],self.WristFkRotation[2]),roo=(self.WristFkRotationOrder),t=(self.WristFkLocation[0],self.WristFkLocation[1],self.WristFkLocation[2]),ra=(self.WristFkRotationAxis[0],self.WristFkRotationAxis[1],self.WristFkRotationAxis[2]))
        mc.group(em=True,n=self.WristFkJoint[0] + '_FkCtrlOffset')
        self.WristControllerOffset = mc.ls(sl=True)
        mc.xform(ro=(self.WristFkRotation[0],self.WristFkRotation[1],self.WristFkRotation[2]),roo=(self.WristFkRotationOrder),t=(self.WristFkLocation[0],self.WristFkLocation[1],self.WristFkLocation[2]),ra=(self.WristFkRotationAxis[0],self.WristFkRotationAxis[1],self.WristFkRotationAxis[2]))
        mc.parent(self.WristController,self.WristControllerOffset)
        mc.orientConstraint(self.WristController[0],self.WristFkJoint[0],n=self.WristFkJoint[0] + 'FkConstraint')
        mc.select(clear=True)
       #making Root for All objects
        
        
        
        self.MoveControls = []
        self.HalfMoveAmnt = []
        mc.select('jsBuilder:ct_Bind_Jaw_main_bone1_FkControlSkeleton')
        self.JawFkJoint = mc.ls(sl=True,type='joint')
        self.JawChild = mc.listRelatives(c=True)
        self.JawFkLocation = mc.xform(self.JawFkJoint[0],q=True,ws=True,a=True,t=True)
        self.JawFkRotation = mc.xform(self.JawFkJoint[0],q=True,ws=True,ro=True)
        self.JawFkRotationAxis = mc.xform(self.JawFkJoint[0],q=True,ra=True)
        self.JawFkRotationOrder = mc.xform(self.JawFkJoint[0],q=True,roo=True)
        self.MoveControls = mc.getAttr(self.JawChild[0] + '.translateX')
        
        
        self.HalfMoveAmnt = self.MoveControls / 2
        
        
        
        #make controller curve 
        mc.curve(n=self.JawFkJoint[0] + '_FkController', d=1, p= [( 6.408333, 19.065957, 8.817547 ),( 10.368897 ,18.929557 ,3.368002 ),( 10.368897 ,18.760957, -3.368005 ),( 6.408331 ,18.624557 ,-8.817549 ),( 1.5e-006, 18.572456 ,-10.89909 ),( -6.40833 ,18.624557 ,-8.817549 ),( -10.368897, 18.760957, -3.368004 ),( -10.368896 ,18.929557 ,3.368004 ),( -6.408328, 19.065957 ,8.817548 ),( 2.5e-006, 19.118058 ,10.89909 ),( 6.408333, 19.065957, 8.817547 ),( 6.124416, 7.806671 ,8.708463 ),( 9.909509 ,7.676314 ,3.500356 ),( 9.909509 ,7.515183 ,-2.937217 ),( 6.124415, 7.384826 ,-8.145321 ),( 1.5e-006, 7.335034 ,-10.134642 ),( -6.124414, 7.384826 ,-8.145322 ),( -9.909508 ,7.515183 ,-2.937215 ),( -9.909507 ,7.676314, 3.500359 ),( -6.124411 ,7.806671, 8.708465 ),( 1.5e-006 ,7.856463, 10.697784 ),( 6.124416 ,7.806671 ,8.708463 ),( 5.43039, -0.917124, 7.971273 ),( 8.786554 ,-1.032709 ,3.353356 ),( 8.786552 ,-1.17558 ,-2.354704 ),( 5.430388 ,-1.291165 ,-6.97262 ),( 1.5e-006 ,-1.335314, -8.736508 ),( -5.430389 ,-1.291165, -6.972621 ),( -8.786551, -1.17558 ,-2.354703 ),( -8.786551 ,-1.032709, 3.353357 ),( -5.430385, -0.917124, 7.971275 ),( 1.5e-006 ,-0.872974, 9.735161 ),( 5.43039 ,-0.917124, 7.971273 ),( 4.646247 ,-6.597817 ,7.033841 ),( 7.517782, -6.696711, 3.082746 ),( 7.517782 ,-6.818952, -1.801075 ),( 4.646245 ,-6.917846, -5.752168 ),( 1.5e-006, -6.955621, -7.261352 ),( -4.646244, -6.917846 ,-5.752168 ),( -7.517781, -6.81895 ,-1.801074 ),( -7.517781 ,-6.696711 ,3.082747 ),( -4.646243, -6.597817 ,7.033842 ),( 1.5e-006 ,-6.560042 ,8.543025 ),( 4.646247 ,-6.597817 ,7.033841 ),( 4.161784 ,-11.589367 ,6.491764 ),( 6.733908 ,-11.67795 ,2.952649 ),( 6.733906 ,-11.787444 ,-1.421939 ),( 4.161784, -11.876027 ,-4.961053 ),( 1.5e-006 ,-11.909863 ,-6.312875 ),( -4.161783, -11.876027 ,-4.961053 ),( -6.733906, -11.787444 ,-1.421938 ),( -6.733906 ,-11.67795, 2.95265 ),( -4.161782 ,-11.589367 ,6.491765 ),( 1.5e-006 ,-11.555531 ,7.843587 ),( 4.161784 ,-11.589367 ,6.491764 ),( 4.114498 ,-18.801204, 6.607171 ),( 6.657397 ,-18.88878, 3.108266 ),( 6.657397, -18.99703 ,-1.216618 ),( 4.114498, -19.084607, -4.715521 ),( 1.5e-006 ,-19.118058, -6.051984 ),( -4.114497 ,-19.084607, -4.715522 ),( -6.657396 ,-18.99703 ,-1.216617 ),( -6.657395 ,-18.88878, 3.108267 ),( -4.114496 ,-18.801204 ,6.607172 ),( 1.5e-006 ,-18.767752, 7.943634 ),( 4.114498 ,-18.801204, 6.607171 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65])
        self.JawFkController = mc.ls(sl=True)
        mc.xform(ro=(0,0,90),scale=(.35,.35,.35))
        mc.makeIdentity(apply=True)
        mc.xform(ro=(self.JawFkRotation[0],self.JawFkRotation[1],self.JawFkRotation[2]),roo=(self.JawFkRotationOrder),t=(self.JawFkLocation[0],self.JawFkLocation[1],self.JawFkLocation[2]),ra=(self.JawFkRotationAxis[0],self.JawFkRotationAxis[1],self.JawFkRotationAxis[2]))
        mc.move(self.MoveControls,0,0,r=True,os=True,wd=True)
        mc.group(em=True,n=self.JawFkJoint[0] + '_FkCtrlOffset')
        self.JawFkControllerOffset = mc.ls(sl=True)
        mc.xform(ro=(self.JawFkRotation[0],self.JawFkRotation[1],self.JawFkRotation[2]),roo=(self.JawFkRotationOrder),t=(self.JawFkLocation[0],self.JawFkLocation[1],self.JawFkLocation[2]),ra=(self.JawFkRotationAxis[0],self.JawFkRotationAxis[1],self.JawFkRotationAxis[2]))
        mc.parent(self.JawFkController,self.JawFkControllerOffset)
        mc.select(self.JawFkController[0])
        mc.xform(piv=(self.JawFkLocation[0],self.JawFkLocation[1],self.JawFkLocation[2]),ws=True,a=True)
        mc.select(clear=True)
        
        mc.orientConstraint(self.JawFkController,self.JawFkJoint,n=self.JawFkJoint[0] + 'FkConstraint')
        mc.select(clear=True)
            
        mc.parent('jsBuilder:jsBuilder:ct_Bind_spinebase_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Clav_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:ct_Bind_spinef_bone1_FkControlSkeletonFkCtrl')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Clav_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:ct_Bind_spinef_bone1_FkControlSkeletonFkCtrl')
        
        #resuing left side code on right side 
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Thmb_a_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Index_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Mfinger_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Rfinger_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Pinky_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Thmb_a_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Index_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Mfinger_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Rfinger_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Pinky_base_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkController')
        
        #mc.parentConstraint(self.MyJointDictionary['lt_Bind_Wrst_bone\n'],'jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset',mo=True)
        #mc.parentConstraint(self.MyJointDictionary['rt_Bind_Wrst_bone\n'],'jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset',mo=True)
        #self.MyJointDictionary['ct_Bind_Jaw_main_bone\n'] sample
        
        #pareenting the fk and and offset under bind hand so that it moves with the arm fk or Ik
        mc.parent('jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton',self.MyJointDictionary['lt_Bind_Elbow_bone\n'])
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset',self.MyJointDictionary['lt_Bind_Elbow_bone\n'])
        
        
        mc.parent('jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton',self.MyJointDictionary['rt_Bind_Elbow_bone\n'])
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset',self.MyJointDictionary['rt_Bind_Elbow_bone\n'])
            
        
        mc.parent('jsBuilder:ct_Bind_Neck_a_bone1_FkControlSkeleton',self.MyJointDictionary['ct_Bind_chest_tip_bone\n'])
        mc.parent('jsBuilder:jsBuilder:ct_Bind_Neck_a_bone1_FkControlSkeletonFkCtrlOffset',self.MyJointDictionary['ct_Bind_chest_tip_bone\n'])
        
        #legsparented under the Root Move 
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Femur_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Femur_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:RootControl')
        mc.select(clear=True)
            
        
        
        mc.select('jsBuilder:FkControlSkeletonContainer')
        self.FkList = mc.container(q=True,nl=True)
        #mc.PointConstraint(self.FkList[0],self.MyJointDictionary['ct_bind_bodyroot_bone\n'],mo=False,w=1,n='RootPointConstraint')
        mc.select(self.FkList[0],add=True)
        mc.select(self.MyJointDictionary['ct_bind_bodyroot_bone\n'],add=True)
        mc.PointConstraint(mo=False,w=1,n='BindFkRootPointConstraint')
        
        
        mc.parent('jsBuilder:jsBuilder:ct_Bind_Jaw_main_bone1_FkControlSkeleton_FkCtrlOffset','jsBuilder:jsBuilder:ct_Bind_Head_base_bone1_FkControlSkeletonFkCtrl')
        mc.parent('jsBuilder:jsBuilder:ct_tng_Bind_a1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:ct_Bind_Jaw_main_bone1_FkControlSkeleton_FkController')
            
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Thmb_b_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Thmb_b_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Thmb_a_bone1_FkControlSkeleton_FkController')
        mc.delete('jsBuilder:lt_Bind_Thmb_tip_bone1FkOrientCst')
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Thmb_a_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Thmb_a_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Thmb_b_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Thmb_b_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeleton',mo=False,w=1)
        
        mc.select('jsBuilder:jsBuilder:lt_Bind_Ankle_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:rt_Bind_Ankle_bone1_FkControlSkeletonFkCtrlOffset')
        mc.delete()
        
        mc.select('jsBuilder:lt_Bind_Ankle_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 1:
                break
            
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentSelFkBones[i] + 'FkController', d=1,p=[( 9.269217 ,-0.701591 ,6.087805 ),( 8.1989, 2.657197, 4.716284 ),( 6.310343 ,4.782455 ,3.597492 ),( 3.891707, 6.091444 ,2.84966 ),( -0.0173994, 6.157435 ,2.482319 ),( -3.921681 ,6.08473 ,2.838519 ),( -6.337305 ,4.763762, 3.588083 ),( -8.205804, 2.627312, 4.709491 ),( -9.275998, -0.696036, 6.084032 ),( -8.884333 ,-3.951836 ,7.23599 ),( -7.730553 ,-6.007067 ,7.842503 ),( -5.365229 ,-7.557913 ,8.169604 ),( -0.0042051, -7.688165 ,7.932558 ),( 5.35511 ,-7.621777 ,8.169066 ),( 7.725158, -6.04582, 7.841856 ),( 8.863047 ,-3.969181, 7.238416 ),( 9.269217 ,-0.701591, 6.087805 ),( 8.65257, -0.642888 ,10.426495 ),( 7.777233, 2.755126 ,9.013116 ),( 5.781839, 5.041383, 7.799493 ),( 3.20043, 6.24176, 6.931153 ),( -0.0370595 ,6.237286, 6.532009 ),( -3.271371 ,6.251711 ,6.91549 ),( -5.79141, 4.956776 ,7.770841 ),( -7.742974, 2.676844 ,8.988221 ),( -8.632644, -0.661648 ,10.417159 ),( -8.169782 ,-3.764904, 11.583917 ),( -7.333128 ,-5.740555 ,12.201396 ),( -5.133953 ,-7.123771, 12.535655 ),( -0.00298057, -7.231261 ,12.499362 ),( 5.130555, -7.166224 ,12.545653 ),( 7.332521 ,-5.760221 ,12.207601 ),( 8.189621, -3.77533, 11.591493 ),( 8.65257 ,-0.642888 ,10.426495 ),( 7.552362 ,-0.429583, 14.754771 ),( 6.723497, 3.029135 ,13.014691 ),( 4.900374, 5.338346, 11.302464 ),( 2.475319 ,6.077049 ,10.026866 ),( -0.0462035 ,6.145922, 9.612744 ),( -2.566887, 6.106026 ,10.040743 ),( -4.96176 ,5.286373 ,11.293648 ),( -6.669708, 2.899727 ,12.949352 ),( -7.5452, -0.460237 ,14.72187 ),( -7.127336, -3.50619, 16.004398 ),( -6.549571, -5.272826, 16.649422 ),( -4.596246 ,-6.200287 ,16.90783 ),( 0.00528602 ,-6.276798 ,16.670714 ),( 4.614183, -6.230169, 16.92447 ),( 6.580556, -5.307241 ,16.673551 ),( 7.142202, -3.50725 ,16.024091 ),( 7.552362, -0.429583 ,14.754771 ),( 4.695711 ,0.0746947, 18.093236 ),( -0.0310317, 0.244437, 19.103751 ),( -4.9953, 0.0245392, 18.404837 ),( -7.5452, -0.460237 ,14.72187 ),( -6.669708, 2.899727, 12.949352 ),( -4.445163, 3.659045, 16.242108 ),( -0.048582, 3.630349, 16.957424 ),( 4.140912, 3.553092, 16.010976 ),( 6.723497 ,3.029135 ,13.014691 ),( 4.900374 ,5.338346, 11.302464 ),( 2.926793 ,5.561415 ,13.606701 ),( -0.0563391 ,5.464649,14.276591 ),( -3.139049, 5.725843 ,13.731492 ),( -4.96176, 5.286373, 11.293648 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64])
            mc.xform(r=True,ro=(0,90,0))
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            #mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True)      
            
        for i in range(0,self.CurrentCountForFk,1):
            if i ==1:
                break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentSelFkBones[i],mo=False,w=1,n=self.CurrentFkBonesOnly[i] + 'FkOrientConstraint')
            
              
            
            
        mc.select('jsBuilder:rt_Bind_Ankle_bone1_FkControlSkeleton',hi=True)
        self.CurrentSelFkBones = []
        self.CurrentSelFkBones = mc.ls(sl=True,type='joint')
        #now to remove the infuence and twist joints from this list
        self.CurrentFkBonesOnly = []
        self.CurrentFkBonesOnly = [i for i  in self.CurrentSelFkBones if 'bone' in i]
        #now getting all the information from the joints in selection 
        self.CurrentCountForFk = len(self.CurrentSelFkBones)
        self.CurrentFkLocation = []
        self.CurrentFkLocation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotation = []
        self.CurrentFkRotation.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationAxis = []
        self.CurrentFkRotationAxis.extend(range(0,self.CurrentCountForFk))
        self.CurrentFkRotationOrder = []
        self.CurrentFkRotationOrder.extend(range(0,self.CurrentCountForFk))
        self.HalfMoveAmnt = []
        self.HalfMoveAmnt.extend(range(0,self.CurrentCountForFk))
        self.MoveControls = []
        self.MoveControls.extend(range(0,self.CurrentCountForFk))
        
        for i in range(0,self.CurrentCountForFk,1):
            self.CurrentFkLocation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,t=True,a=True)
            self.CurrentFkRotation[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ws=True,ro=True)
            self.CurrentFkRotationAxis[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,ra=True)
            self.CurrentFkRotationOrder[i] = mc.xform(self.CurrentFkBonesOnly[i],q=True,roo=True)
            self.MoveControls[i] = mc.getAttr(self.CurrentFkBonesOnly[i] + '.translateX')
            
        for i in range(0,self.CurrentCountForFk,1):
            self.HalfMoveAmnt[i] = self.MoveControls[i+1] / 2
            
            if i == 1:
                break
        
        self.CurrentFkControllers = []
        self.CurrentFkControllers.extend(range(0,self.CurrentCountForFk))
        self.CurrentOffsetForFkControllers = []
        self.CurrentOffsetForFkControllers.extend(range(0,self.CurrentCountForFk))#next create ph curve
        for i in range(0,self.CurrentCountForFk-1,1):
            mc.curve(n=self.CurrentSelFkBones[i] + 'FkController', d=1,p=[( 9.269217 ,-0.701591 ,6.087805 ),( 8.1989, 2.657197, 4.716284 ),( 6.310343 ,4.782455 ,3.597492 ),( 3.891707, 6.091444 ,2.84966 ),( -0.0173994, 6.157435 ,2.482319 ),( -3.921681 ,6.08473 ,2.838519 ),( -6.337305 ,4.763762, 3.588083 ),( -8.205804, 2.627312, 4.709491 ),( -9.275998, -0.696036, 6.084032 ),( -8.884333 ,-3.951836 ,7.23599 ),( -7.730553 ,-6.007067 ,7.842503 ),( -5.365229 ,-7.557913 ,8.169604 ),( -0.0042051, -7.688165 ,7.932558 ),( 5.35511 ,-7.621777 ,8.169066 ),( 7.725158, -6.04582, 7.841856 ),( 8.863047 ,-3.969181, 7.238416 ),( 9.269217 ,-0.701591, 6.087805 ),( 8.65257, -0.642888 ,10.426495 ),( 7.777233, 2.755126 ,9.013116 ),( 5.781839, 5.041383, 7.799493 ),( 3.20043, 6.24176, 6.931153 ),( -0.0370595 ,6.237286, 6.532009 ),( -3.271371 ,6.251711 ,6.91549 ),( -5.79141, 4.956776 ,7.770841 ),( -7.742974, 2.676844 ,8.988221 ),( -8.632644, -0.661648 ,10.417159 ),( -8.169782 ,-3.764904, 11.583917 ),( -7.333128 ,-5.740555 ,12.201396 ),( -5.133953 ,-7.123771, 12.535655 ),( -0.00298057, -7.231261 ,12.499362 ),( 5.130555, -7.166224 ,12.545653 ),( 7.332521 ,-5.760221 ,12.207601 ),( 8.189621, -3.77533, 11.591493 ),( 8.65257 ,-0.642888 ,10.426495 ),( 7.552362 ,-0.429583, 14.754771 ),( 6.723497, 3.029135 ,13.014691 ),( 4.900374, 5.338346, 11.302464 ),( 2.475319 ,6.077049 ,10.026866 ),( -0.0462035 ,6.145922, 9.612744 ),( -2.566887, 6.106026 ,10.040743 ),( -4.96176 ,5.286373 ,11.293648 ),( -6.669708, 2.899727 ,12.949352 ),( -7.5452, -0.460237 ,14.72187 ),( -7.127336, -3.50619, 16.004398 ),( -6.549571, -5.272826, 16.649422 ),( -4.596246 ,-6.200287 ,16.90783 ),( 0.00528602 ,-6.276798 ,16.670714 ),( 4.614183, -6.230169, 16.92447 ),( 6.580556, -5.307241 ,16.673551 ),( 7.142202, -3.50725 ,16.024091 ),( 7.552362, -0.429583 ,14.754771 ),( 4.695711 ,0.0746947, 18.093236 ),( -0.0310317, 0.244437, 19.103751 ),( -4.9953, 0.0245392, 18.404837 ),( -7.5452, -0.460237 ,14.72187 ),( -6.669708, 2.899727, 12.949352 ),( -4.445163, 3.659045, 16.242108 ),( -0.048582, 3.630349, 16.957424 ),( 4.140912, 3.553092, 16.010976 ),( 6.723497 ,3.029135 ,13.014691 ),( 4.900374 ,5.338346, 11.302464 ),( 2.926793 ,5.561415 ,13.606701 ),( -0.0563391 ,5.464649,14.276591 ),( -3.139049, 5.725843 ,13.731492 ),( -4.96176, 5.286373, 11.293648 )],k=[ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64])
            mc.xform(r=True,ro=(0,90,0))
            self.CurrentFkControllers[i] = mc.ls(sl=True)
            mc.makeIdentity(a=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.group(em=True,n=self.CurrentFkBonesOnly[i] + 'FkCtrlOffset')
            self.CurrentOffsetForFkControllers[i]= mc.ls(sl=True)
            mc.xform(ro=(self.CurrentFkRotation[i]),roo=(self.CurrentFkRotationOrder[i]),t=(self.CurrentFkLocation[i]),ra=(self.CurrentFkRotationAxis[i]))
            mc.parent(self.CurrentFkControllers[i],self.CurrentOffsetForFkControllers[i])
            mc.select(self.CurrentFkControllers[i])
            mc.pickWalk(d='down')
            #mc.move(self.HalfMoveAmnt[i],0,0,os=True,r=True,wd=True)
            mc.pickWalk(d='up')
            mc.xform(piv=(self.CurrentFkLocation[i]),ws=True,a=True)
            mc.select(clear=True) 
            
        for i in range(0,self.CurrentCountForFk,1):
            if i ==1:
                break
            mc.parent(self.CurrentOffsetForFkControllers[i+1],self.CurrentFkControllers[i])
            mc.orientConstraint(self.CurrentFkControllers[i],self.CurrentSelFkBones[i],mo=False,w=1,n=self.CurrentFkBonesOnly[i] + 'FkOrientConstraint')
            
            
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Foot_ball_bone1_FkControlSkeletonFkController','jsBuilder:lt_Bind_Foot_ball_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Rfinger_c_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Rfinger_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Pinky_c_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Pinky_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Mfinger_c_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Mfinger_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:lt_Bind_Index_c_bone1_FkControlSkeleton_FkController','jsBuilder:lt_Bind_Index_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.delete('jsBuilder:rt_Bind_Thmb_tip_bone1FkOrientCst')
        
        mc.orientConstraint('jsBuilder:jsBuilder:rt_Bind_Rfinger_c_bone1_FkControlSkeleton_FkController','jsBuilder:rt_Bind_Rfinger_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:rt_Pinky_c_bone1_FkControlSkeleton_FkController','jsBuilder:rt_Pinky_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:rt_Bind_Mfinger_c_bone1_FkControlSkeleton_FkController','jsBuilder:rt_Bind_Mfinger_c_bone1_FkControlSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:jsBuilder:rt_Bind_Index_c_bone1_FkControlSkeleton_FkController','jsBuilder:rt_Bind_Index_c_bone1_FkControlSkeleton',mo=False,w=1)
        
        
        mc.parent('jsBuilder:jsBuilder:lt_Bind_Ankle_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:lt_Bind_Calf_bone1_FkControlSkeleton_FkController')
        mc.parent('jsBuilder:jsBuilder:rt_Bind_Ankle_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:jsBuilder:rt_Bind_Calf_bone1_FkControlSkeleton_FkController')
        
        
        
        
        mc.select(self.MyJointDictionary['ct_bind_bodyroot_bone\n'],hi=True)
        
        mc.duplicate(po=True)
        self.IkConsDeleteList = mc.ls(sl=True,type='constraint')
        self.IkConsDelAmnt = len(self.IkConsDeleteList)
        for i in range(0,self.IkConsDelAmnt,1):
            mc.delete(self.IkConsDeleteList[i])
        
        self.IkComponentsList = mc.ls(sl=True,type='transform')
        self.IkComponentsListAmnt = len(self.IkComponentsList)
        mc.select(clear=True)
        mc.container(n='IkSkeletonContainer')
        
        
        self.IkContainer = mc.ls(sl=True)
        for i in range(0,self.IkComponentsListAmnt,1):
            mc.container(self.IkContainer,e=True, an=self.IkComponentsList[i])
            
        self.IkContainerList = []
        
        self.IkContainerList = mc.container(self.IkContainer,q=True,nl=True)
            
        self.IkJointsTransforms = []
        del self.IkJointsTransforms[:]
        mc.select(self.IkContainerList[0])
        self.IkSkelRootNode = mc.ls(sl=True)[0]
        
        mc.select(self.IkSkelRootNode,hi=True,replace = True)#correct way to do rename list iteration 
        self.TransformsList = mc.ls(sl=True,type='transform')
        self.LenTransformsList = len(self.TransformsList)
        self.TransformsList.reverse()
        self.IkContainerList.reverse()
        
        for i in range(0,self.LenTransformsList,1):
            mc.rename(self.TransformsList[i],self.IkContainerList[i] + '_IkSkeleton')
        
        
        
        
                    
        mc.select('jsBuilder:jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset_IkSkeleton')
        mc.delete()
        mc.select('jsBuilder:jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_FkCtrlOffset_IkSkeleton')
        mc.delete()
        
        mc.select('jsBuilder:jsBuilder:ct_Bind_Neck_a_bone1_FkControlSkeletonFkCtrlOffset_IkSkeleton')
        mc.delete()
        
        mc.select('jsBuilder:ct_Bind_Neck_a_bone_IkSkeleton')
        mc.delete()
        
        
        mc.select('jsBuilder:ct_Bind_Neck_a_bone1_FkControlSkeleton_IkSkeleton')
        mc.delete()
        mc.select('jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton_IkSkeleton')
        mc.delete()
        mc.select('jsBuilder:lt_Bind_hand_bone1_FkControlSkeleton_IkSkeleton')
        mc.delete()
        mc.select('jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton_IkSkeleton')
        mc.select('jsBuilder:rt_Bind_Wrst_bone_IkSkeleton')
        self.ltHandtodelete = mc.listRelatives(c=True)
        mc.select('jsBuilder:lt_Bind_Wrst_bone_IkSkeleton')
        self.rtHandtodelete = mc.listRelatives(c=True)
        for i in self.ltHandtodelete:
            mc.delete(i)
        for i in self.rtHandtodelete:
            mc.delete(i)
            
        mc.select('jsBuilder:ct_Bind_spinebase_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:ct_Bind_spinea_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:ct_Bind_spinec_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:ct_Bind_spined_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:ct_Bind_spinee_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:ct_Bind_spinef_bone_IkSkeleton',add=True)
        
        self.IkSpineJoints = mc.ls(sl=True,type='joint')
        mc.select(clear=True)
        
        mc.select('jsBuilder:ct_Bind_spinebase_bone',add=True)
        mc.select('jsBuilder:ct_Bind_spinea_bone',add=True)
        mc.select('jsBuilder:ct_Bind_spinec_bone',add=True)
        mc.select('jsBuilder:ct_Bind_spined_bone',add=True)
        mc.select('jsBuilder:ct_Bind_spinee_bone',add=True)
        mc.select('jsBuilder:ct_Bind_spinef_bone',add=True)
        
        self.BindSpineJoints = mc.ls(sl=True,type='joint')
        
        mc.select('jsBuilder:ct_Bind_spinebase_bone1FkOrientCst')
        mc.delete()
        mc.select('jsBuilder:ct_Bind_spinea_bone1FkOrientCst')
        mc.delete()
        mc.select('jsBuilder:ct_Bind_spinec_bone1FkOrientCst')
        mc.delete()
        mc.select('jsBuilder:ct_Bind_spined_bone1FkOrientCst')
        mc.delete()
        mc.select('jsBuilder:ct_Bind_spinee_bone1FkOrientCst')
        mc.delete()
        mc.select('jsBuilder:ct_Bind_spinef_bone1FkOrientCst')
        mc.delete()
        
        self.LenofBindSpine = len(self.BindSpineJoints)
        mc.select(clear=True)
        #Ik to Bind Spine Constraints
        mc.orientConstraint('jsBuilder:ct_Bind_spinebase_bone_IkSkeleton', 'jsBuilder:ct_Bind_spinebase_bone',n='jsBuilder:ct_Bind_spinebase_bone' + 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinea_bone_IkSkeleton', 'jsBuilder:ct_Bind_spinea_bone',n='jsBuilder:ct_Bind_spinea_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinec_bone_IkSkeleton', 'jsBuilder:ct_Bind_spinec_bone',n='jsBuilder:ct_Bind_spinec_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spined_bone_IkSkeleton', 'jsBuilder:ct_Bind_spined_bone',n='jsBuilder:ct_Bind_spined_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinee_bone_IkSkeleton', 'jsBuilder:ct_Bind_spinee_bone',n='jsBuilder:ct_Bind_spinee_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinef_bone_IkSkeleton', 'jsBuilder:ct_Bind_spinef_bone',n='jsBuilder:ct_Bind_spinef_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_bind_SpineEnd_bone_IkSkeleton', 'jsBuilder:ct_bind_SpineEnd_bone',n='jsBuilder:ct_bind_SpineEnd_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_Chest_bone_IkSkeleton', 'jsBuilder:ct_Bind_Chest_bone',n='jsBuilder:ct_Bind_Chest_bone'+ 'IK_OrientConstraint',mo=False,w=1)
        
        #Fk to Bind Spine Constraints#do this after SpineIkis setup
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>insert spine here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        
        
       #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>insert spine here<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #World up type is object start end, object Up is the top object or end
        #bottom object is the start point
        #twist controls enabled
        #starts at spine base ends at spineF
        #joints smooth bind to curve
        #make sure it ends at the end effector not the end joint 
        #have snap enalbed
        mc.select(clear=True)#mirrror this part for the Right arm IK #makes Ik handle and puts a Pole vector to it
        mc.setAttr('jsBuilder:lt_Bind_Wrst_bone_IkSkeleton.jointOrientX',0)
        mc.setAttr('jsBuilder:lt_Bind_Wrst_bone_IkSkeleton.jointOrientY',0)
        mc.setAttr('jsBuilder:lt_Bind_Wrst_bone_IkSkeleton.jointOrientZ',0)
        #from here reuse this code to make IK arms and legs 
        mc.ikHandle(sj='jsBuilder:lt_Bind_Humerous_bone_IkSkeleton',ee='jsBuilder:lt_Bind_Wrst_bone_IkSkeleton',n='IkLtArmHandle',sol='ikRPsolver')
        mc.spaceLocator(p=(0,0,0),n='LtArmPoleVectorCtrl')
        mc.select('jsBuilder:lt_Bind_Humerous_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:lt_Bind_Wrst_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:LtArmPoleVectorCtrl',add=True)
        mc.parentConstraint(n='PoleVectorLineup')
        mc.delete('jsBuilder:PoleVectorLineup')
        mc.select('jsBuilder:LtArmPoleVectorCtrl')
        mc.move(0,0,-40,r=True,ls=True,wd=True)
        self.LtPvectTransLate = mc.xform(q=True,t=True,ws=True,a=True)
        self.LtPvectRotate = mc.xform(q=True,ro=True,ws=True,a=True)
        self.LtPvectRotateAxis = mc.xform(q=True,ra=True,ws=True,a=True)
        mc.group(em=True,n='LtArmPoleVectorCtrlOffset')
        mc.xform(t=(self.LtPvectTransLate[0],self.LtPvectTransLate[1],self.LtPvectTransLate[1]),ro=(self.LtPvectRotate[0],self.LtPvectRotate[1],self.LtPvectRotate[1]),ra=(self.LtPvectRotateAxis[0],self.LtPvectRotateAxis[1],self.LtPvectRotateAxis[2]))
        mc.parent('jsBuilder:LtArmPoleVectorCtrl','jsBuilder:LtArmPoleVectorCtrlOffset')
        
        
        mc.select(clear=True)#setting the Joint wrist tip orients to zero
        mc.setAttr('jsBuilder:rt_Bind_Wrst_bone_IkSkeleton.jointOrientX',0)
        mc.setAttr('jsBuilder:rt_Bind_Wrst_bone_IkSkeleton.jointOrientY',0)
        mc.setAttr('jsBuilder:rt_Bind_Wrst_bone_IkSkeleton.jointOrientZ',0)
        #this part takes care of the pole vectors 
        mc.ikHandle(sj='jsBuilder:rt_Bind_Humerous_bone_IkSkeleton',ee='jsBuilder:rt_Bind_Wrst_bone_IkSkeleton',n='IkRtArmHandle',sol='ikRPsolver')
        mc.spaceLocator(p=(0,0,0),n='RtArmPoleVectorCtrl')
        mc.select('jsBuilder:rt_Bind_Humerous_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:rt_Bind_Wrst_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:RtArmPoleVectorCtrl',add=True)
        mc.parentConstraint(n='PoleVectorLineup')
        mc.delete('jsBuilder:PoleVectorLineup')
        mc.select('jsBuilder:RtArmPoleVectorCtrl')
        mc.move(0,0,-40,r=True,ls=True,wd=True)
        self.RtPvectTransLate = mc.xform(q=True,t=True,ws=True,a=True)
        self.RtPvectRotate = mc.xform(q=True,ro=True,ws=True,a=True)
        self.RtPvectRotateAxis = mc.xform(q=True,ra=True,ws=True,a=True)
        mc.group(em=True,n='RtArmPoleVectorCtrlOffset')
        mc.xform(t=(self.RtPvectTransLate[0],self.RtPvectTransLate[1],self.RtPvectTransLate[1]),ro=(self.RtPvectRotate[0],self.RtPvectRotate[1],self.RtPvectRotate[1]),ra=(self.RtPvectRotateAxis[0],self.RtPvectRotateAxis[1],self.RtPvectRotateAxis[2]))
        mc.parent('jsBuilder:RtArmPoleVectorCtrl','jsBuilder:RtArmPoleVectorCtrlOffset')
        #now to zero out those positions for the control object
        mc.parent('jsBuilder:LtArmPoleVectorCtrl',w=True)
        mc.parent('jsBuilder:RtArmPoleVectorCtrl',w=True)
        
        mc.parent('jsBuilder:RtArmPoleVectorCtrlOffset','jsBuilder:RtArmPoleVectorCtrl')
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.rotateX',0)
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.rotateY',0)
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.rotateZ',0)
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.translateX',0)
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.translateY',0)
        mc.setAttr('jsBuilder:RtArmPoleVectorCtrlOffset.translateZ',0)
        
        mc.parent('jsBuilder:LtArmPoleVectorCtrlOffset','jsBuilder:LtArmPoleVectorCtrl')
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.rotateX',0)
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.rotateY',0)
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.rotateZ',0)
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.translateX',0)
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.translateY',0)
        mc.setAttr('jsBuilder:LtArmPoleVectorCtrlOffset.translateZ',0)
        
        
        
        
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorX',0)
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorY',0)
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorZ',0)
        
        
        
        mc.parent('jsBuilder:LtArmPoleVectorCtrlOffset',w=True)
        mc.parent('jsBuilder:RtArmPoleVectorCtrlOffset',w=True)
        
        mc.parent('jsBuilder:LtArmPoleVectorCtrl','jsBuilder:LtArmPoleVectorCtrlOffset')
        mc.parent('jsBuilder:RtArmPoleVectorCtrl','jsBuilder:RtArmPoleVectorCtrlOffset')
        
        
        
        mc.group(em=True,n='RTArmIkOffset')
        mc.group(em=True,n='LTArmIkOffset')
        
        mc.parent('jsBuilder:RTArmIkOffset','jsBuilder:IkRtArmHandle')
        mc.parent('jsBuilder:LTArmIkOffset','jsBuilder:IkLtArmHandle')
        
        mc.setAttr('jsBuilder:LTArmIkOffset.rotateX',0)
        mc.setAttr('jsBuilder:LTArmIkOffset.rotateY',0)
        mc.setAttr('jsBuilder:LTArmIkOffset.rotateZ',0)
        mc.setAttr('jsBuilder:LTArmIkOffset.translateX',0)
        mc.setAttr('jsBuilder:LTArmIkOffset.translateY',0)
        mc.setAttr('jsBuilder:LTArmIkOffset.translateZ',0)
        
        mc.setAttr('jsBuilder:RTArmIkOffset.rotateX',0)
        mc.setAttr('jsBuilder:RTArmIkOffset.rotateY',0)
        mc.setAttr('jsBuilder:RTArmIkOffset.rotateZ',0)
        mc.setAttr('jsBuilder:RTArmIkOffset.translateX',0)
        mc.setAttr('jsBuilder:RTArmIkOffset.translateY',0)
        mc.setAttr('jsBuilder:RTArmIkOffset.translateZ',0)
        
        mc.parent('jsBuilder:RTArmIkOffset',w=True)
        mc.parent('jsBuilder:LTArmIkOffset',w=True)
        
        mc.parent('jsBuilder:IkRtArmHandle','jsBuilder:RTArmIkOffset')
        mc.parent('jsBuilder:IkLtArmHandle','jsBuilder:LTArmIkOffset')
        
        
        
        
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorX',0)
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorY',0)
        mc.setAttr('jsBuilder:IkRtArmHandle.poleVectorZ',0)
        
        mc.select('jsBuilder:LtArmPoleVectorCtrl',add=True)
        mc.select('jsBuilder:IkLtArmHandle',add=True)
        mc.PoleVectorConstraint(n='ltArmPoleVectorConstraint')
        mc.select(clear=True)
        
        mc.select('jsBuilder:RtArmPoleVectorCtrl',add=True)
        mc.select('jsBuilder:IkRtArmHandle',add=True)
        mc.PoleVectorConstraint(n='rtArmPoleVectorConstraint')
        
        
        
        #Fk to Bind Spine Constraints#do this after SpineIkis setup Below these orient constraints for the spine the leg Ik setup  is 
        mc.orientConstraint('jsBuilder:ct_Bind_spinebase_bone1_FkControlSkeleton', 'jsBuilder:ct_Bind_spinebase_bone',n='jsBuilder:ct_Bind_spinebase_bone' + 'FK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinea_bone1_FkControlSkeleton', 'jsBuilder:ct_Bind_spinea_bone',n='jsBuilder:ct_Bind_spinea_bone'+ 'FK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinec_bone1_FkControlSkeleton', 'jsBuilder:ct_Bind_spinec_bone',n='jsBuilder:ct_Bind_spinec_bone'+ 'FK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spined_bone1_FkControlSkeleton', 'jsBuilder:ct_Bind_spined_bone',n='jsBuilder:ct_Bind_spined_bone'+ 'FK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinee_bone1_FkControlSkeleton ','jsBuilder:ct_Bind_spinee_bone',n='jsBuilder:ct_Bind_spinee_bone'+ 'FK_OrientConstraint',mo=False,w=1)
        mc.orientConstraint('jsBuilder:ct_Bind_spinef_bone1_FkControlSkeleton', 'jsBuilder:ct_Bind_spinef_bone',n='jsBuilder:ct_Bind_spinef_bone'+ 'FK_OrientConstraint',mo=False,w=1)
        
        
        
        mc.select(clear=True)#This does the left Leg arm IK #makes Ik handle and puts a Pole vector to it
        
        #from here reuse this code to make IK arms and legs  This is the left leg make  a right leg 
        mc.ikHandle(sj='jsBuilder:lt_Bind_Femur_bone_IkSkeleton',ee='jsBuilder:lt_Bind_Ankle_bone_IkSkeleton',n='IkLtLegHandle',sol='ikRPsolver')
        mc.spaceLocator(p=(0,0,0),n='LtLegPoleVectorCtrl')
        mc.select('jsBuilder:lt_Bind_Femur_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:lt_Bind_Ankle_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:LtLegPoleVectorCtrl',add=True)
        mc.parentConstraint(n='PoleVectorLineup')
        mc.delete('jsBuilder:PoleVectorLineup')
        mc.select('jsBuilder:LtLegPoleVectorCtrl')
        mc.move(0,0,50,r=True,ls=True,wd=True)
        self.LtPvectTransLate = mc.xform(q=True,t=True,ws=True,a=True)
        self.LtPvectRotate = mc.xform(q=True,ro=True,ws=True,a=True)
        self.LtPvectRotateAxis = mc.xform(q=True,ra=True,ws=True,a=True)
        mc.group(em=True,n='LtLegPoleVectorCtrlOffset')
        mc.xform(t=(self.LtPvectTransLate[0],self.LtPvectTransLate[1],self.LtPvectTransLate[1]),ro=(self.LtPvectRotate[0],self.LtPvectRotate[1],self.LtPvectRotate[1]),ra=(self.LtPvectRotateAxis[0],self.LtPvectRotateAxis[1],self.LtPvectRotateAxis[2]))
        #mc.parent('jsBuilder:LtLegPoleVectorCtrl','jsBuilder:LtLegPoleVectorCtrlOffset')
        
        #leg pole vectors down here 
        #parent the controls under the world then reverse 
       
        
        #  a right leg RIGHT LEG HERE FYI
        mc.ikHandle(sj='jsBuilder:rt_Bind_Femur_bone_IkSkeleton',ee='jsBuilder:rt_Bind_Ankle_bone_IkSkeleton',n='IkRtLegHandle',sol='ikRPsolver')
        mc.spaceLocator(p=(0,0,0),n='RtLegPoleVectorCtrl')
        mc.select('jsBuilder:rt_Bind_Femur_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:rt_Bind_Ankle_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:RtLegPoleVectorCtrl',add=True)
        mc.parentConstraint(n='PoleVectorLineup')
        mc.delete('jsBuilder:PoleVectorLineup')
        mc.select('jsBuilder:RtLegPoleVectorCtrl')
        mc.move(0,0,50,r=True,ls=True,wd=True)
        self.LtPvectTransLate = mc.xform(q=True,t=True,ws=True,a=True)
        self.LtPvectRotate = mc.xform(q=True,ro=True,ws=True,a=True)
        self.LtPvectRotateAxis = mc.xform(q=True,ra=True,ws=True,a=True)
        mc.group(em=True,n='RtLegPoleVectorCtrlOffset')
        mc.xform(t=(self.LtPvectTransLate[0],self.LtPvectTransLate[1],self.LtPvectTransLate[1]),ro=(self.LtPvectRotate[0],self.LtPvectRotate[1],self.LtPvectRotate[1]),ra=(self.LtPvectRotateAxis[0],self.LtPvectRotateAxis[1],self.LtPvectRotateAxis[2]))
        
        
        
        
        #this part make sthe pole vector this part for Right legs
        #this part setups up the offsets
        mc.parent('jsBuilder:RtLegPoleVectorCtrlOffset','jsBuilder:RtLegPoleVectorCtrl')
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.rotateX',0)
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.rotateY',0)
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.rotateZ',0)
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.translateX',0)
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.translateY',0)
        mc.setAttr('jsBuilder:RtLegPoleVectorCtrlOffset.translateZ',0)
        #left leg offsets 
        mc.parent('jsBuilder:LtLegPoleVectorCtrlOffset','jsBuilder:LtLegPoleVectorCtrl')
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.rotateX',0)
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.rotateY',0)
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.rotateZ',0)
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.translateX',0)
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.translateY',0)
        mc.setAttr('jsBuilder:LtLegPoleVectorCtrlOffset.translateZ',0)
        #after zeroed out put the pole vector controls under the offsets 
        
        
        mc.parent('jsBuilder:LtLegPoleVectorCtrlOffset',w=True)
        mc.parent('jsBuilder:RtLegPoleVectorCtrlOffset',w=True)
        
        mc.parent('jsBuilder:LtLegPoleVectorCtrl','jsBuilder:LtLegPoleVectorCtrlOffset',)
        mc.parent('jsBuilder:RtLegPoleVectorCtrl','jsBuilder:RtLegPoleVectorCtrlOffset',)
        
        #now to put a pole vector constraint to the pole vecotrs and zero out the Ik Handles ThemSelves 
        
        mc.group(em=True,n='RTLegIkOffset')
        mc.group(em=True,n='LTLegIkOffset')
        
        mc.parent('jsBuilder:RTLegIkOffset','jsBuilder:IkRtLegHandle')
        mc.parent('jsBuilder:LTLegIkOffset','jsBuilder:IkLtLegHandle')
        
        mc.setAttr('jsBuilder:LTLegIkOffset.rotateX',0)
        mc.setAttr('jsBuilder:LTLegIkOffset.rotateY',0)
        mc.setAttr('jsBuilder:LTLegIkOffset.rotateZ',0)
        mc.setAttr('jsBuilder:LTLegIkOffset.translateX',0)
        mc.setAttr('jsBuilder:LTLegIkOffset.translateY',0)
        mc.setAttr('jsBuilder:LTLegIkOffset.translateZ',0)
        
        mc.setAttr('jsBuilder:RTLegIkOffset.rotateX',0)
        mc.setAttr('jsBuilder:RTLegIkOffset.rotateY',0)
        mc.setAttr('jsBuilder:RTLegIkOffset.rotateZ',0)
        mc.setAttr('jsBuilder:RTLegIkOffset.translateX',0)
        mc.setAttr('jsBuilder:RTLegIkOffset.translateY',0)
        mc.setAttr('jsBuilder:RTLegIkOffset.translateZ',0)
        
        mc.parent('jsBuilder:RTLegIkOffset',w=True)
        mc.parent('jsBuilder:LTLegIkOffset',w=True)
        
        mc.parent('jsBuilder:IkRtLegHandle','jsBuilder:RTLegIkOffset')
        mc.parent('jsBuilder:IkLtLegHandle','jsBuilder:LTLegIkOffset')
        
        
        
        
        mc.setAttr('jsBuilder:IkLtLegHandle.poleVectorX',0)
        mc.setAttr('jsBuilder:IkLtLegHandle.poleVectorY',0)
        mc.setAttr('jsBuilder:IkLtLegHandle.poleVectorZ',0)
        
        mc.setAttr('jsBuilder:IkRtLegHandle.poleVectorX',0)
        mc.setAttr('jsBuilder:IkRtLegHandle.poleVectorY',0)
        mc.setAttr('jsBuilder:IkRtLegHandle.poleVectorZ',0)
        
        
        mc.select('jsBuilder:LtLegPoleVectorCtrl',add=True)
        mc.select('jsBuilder:IkLtLegHandle',add=True)
        mc.PoleVectorConstraint(n='ltLegPoleVectorConstraint')
        mc.select(clear=True)
        
        
        mc.select('jsBuilder:RtLegPoleVectorCtrl',add=True)
        mc.select('jsBuilder:IkRtLegHandle',add=True)
        mc.PoleVectorConstraint(n='ltRegPoleVectorConstraint')
        mc.select(clear=True)
        
        
        mc.curve(n='FKIKswitches',d=1, p=[(60.96 ,0 ,137.16), ( -45.72, 0 ,137.16),( -45.72, 0 ,182.88) ,(60.96 ,0 ,182.88), ( 60.96, 0 ,137.16)], k=[ 0 , 1 , 2 , 3 , 4])
        mc.CenterPivot()
        mc.select('jsBuilder:FKIKswitches')
        mc.addAttr(longName = 'IkSpineSwitch',at='double',min=0,max=1,dv=1,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'FKSpineSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'FKLeftArmSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'FKRightArmSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'IkLeftLegSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'IkRightLegSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'IkLeftArmSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'IkRightArmSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'FkRightFootSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'FkLeftFootSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'LeftFootReverseFootSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'RightFootReverseFootSwitch',at='double',min=0,max=1,dv=0,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'AllIkVisibility',at='double',min=0,max=1,dv=1,k=True,w=True,r=True,s=True)
        mc.addAttr(longName = 'AllFKVisibility',at='double',min=0,max=1,dv=1,k=True,w=True,r=True,s=True)
        
        mc.textCurves(f='SketchFLow Print',t='FK_IK_SWITCHBOX',n='switchtextboxCurves')
        mc.xform(s=(2,2,2))
        mc.makeIdentity(a=True)
        mc.CenterPivot()
        mc.select('jsBuilder:FKIKswitches',add=True)
        mc.select('jsBuilder:switchtextboxCurvesShape',add=True)
        mc.PointConstraint()
        #mc.parent(self.TextFKobj[0],'jsBuilder:FKIKswitches')
        
        #connect Ik Switches for spine 
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinebase_boneFK_OrientConstraint.ct_Bind_spinebase_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinea_boneFK_OrientConstraint.ct_Bind_spinea_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinec_boneFK_OrientConstraint.ct_Bind_spinec_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spined_boneFK_OrientConstraint.ct_Bind_spined_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinee_boneFK_OrientConstraint.ct_Bind_spinee_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinef_boneFK_OrientConstraint.ct_Bind_spinef_bone_IkSkeletonW0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_bind_SpineEnd_boneIK_OrientConstraint.ct_bind_SpineEnd_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.IkSpineSwitch","jsBuilder:jsBuilder:ct_Bind_Chest_boneIK_OrientConstraint.ct_Bind_Chest_bone_IkSkeletonW1")
        #fkSpineSwitches
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinebase_boneFK_OrientConstraint.ct_Bind_spinebase_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinea_boneFK_OrientConstraint.ct_Bind_spinea_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinec_boneFK_OrientConstraint.ct_Bind_spinec_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spined_boneFK_OrientConstraint.ct_Bind_spined_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinee_boneFK_OrientConstraint.ct_Bind_spinee_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_spinef_boneFK_OrientConstraint.ct_Bind_spinef_bone1_FkControlSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_bind_SpineEnd_boneIK_OrientConstraint.ct_bind_SpineEnd_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.FKSpineSwitch","jsBuilder:jsBuilder:ct_Bind_Chest_boneIK_OrientConstraint.ct_Bind_Chest_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.AllFKVisibility","jsBuilder:jsBuilder:ct_bind_bodyroot_bone1_FkControlSkeleton.visibility")
        mc.connectAttr("jsBuilder:FKIKswitches.AllIkVisibility","jsBuilder:jsBuilder:ct_bind_bodyroot_bone1_IkSkeleton.visibility")
        mc.connectAttr("jsBuilder:FKIKswitches.FkLeftFootSwitch","jsBuilder:lt_Bind_Foot_ball_bone1FkOrientCst.lt_Bind_Foot_ball_bone1W0")
        
        #mc.connectAttr(,"jsBuilder:lt_Bind_Humerous_bone1FkOrientCst.lt_Bind_Humerous_bone1W0")
        
        
        mc.orientConstraint('jsBuilder:lt_Bind_Femur_bone_IkSkeleton','jsBuilder:lt_Bind_Femur_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:lt_Bind_Calf_bone_IkSkeleton','jsBuilder:lt_Bind_Calf_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:lt_Bind_Ankle_bone_IkSkeleton','jsBuilder:lt_Bind_Ankle_bone',mo=False,w=1)
        
        
        mc.orientConstraint('jsBuilder:rt_Bind_Femur_bone_IkSkeleton','jsBuilder:rt_Bind_Femur_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:rt_Bind_Calf_bone_IkSkeleton','jsBuilder:rt_Bind_Calf_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:rt_Bind_Ankle_bone_IkSkeleton','jsBuilder:rt_Bind_Ankle_bone',mo=False,w=1)
        
        
        
        mc.orientConstraint('jsBuilder:lt_Bind_Clav_bone_IkSkeleton','jsBuilder:lt_Bind_Clav_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:lt_Bind_Humerous_bone_IkSkeleton','jsBuilder:lt_Bind_Humerous_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:lt_Bind_Elbow_bone_IkSkeleton','jsBuilder:lt_Bind_Elbow_bone',mo=False,w=1)
        
        
        mc.orientConstraint('jsBuilder:rt_Bind_Clav_bone_IkSkeleton','jsBuilder:rt_Bind_Clav_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:rt_Bind_Humerous_bone_IkSkeleton','jsBuilder:rt_Bind_Humerous_bone',mo=False,w=1)
        mc.orientConstraint('jsBuilder:rt_Bind_Elbow_bone_IkSkeleton','jsBuilder:rt_Bind_Elbow_bone',mo=False,w=1)
        
        
        #make a contorller for the Ik shoulder will be a Fk to give more control
        self.LtIkShoulderLoc = mc.xform('jsBuilder:lt_Bind_Clav_bone_IkSkeleton',q=True,ws=True,t=True,a=True)
        self.LtIkShoulderRotation = mc.xform('jsBuilder:lt_Bind_Clav_bone_IkSkeleton',q=True,ws=True,ro=True,a=True)
        self.LtIkShoulderRoo = mc.xform('jsBuilder:lt_Bind_Clav_bone_IkSkeleton',q=True,roo=True)
        self.LtIkShoulderRotationAxis = mc.xform('jsBuilder:lt_Bind_Clav_bone_IkSkeleton',q=True,ra=True)
        
        mc.circle(nr=(1,0,0),n='ltIkShoulderCtrl',r=11,fc=True,sw=360)
        mc.xform(t=(self.LtIkShoulderLoc[0],self.LtIkShoulderLoc[1],self.LtIkShoulderLoc[2]),ro=(self.LtIkShoulderRotation[0],self.LtIkShoulderRotation[1],self.LtIkShoulderRotation[2]),ra=(self.LtIkShoulderRotationAxis[0],self.LtIkShoulderRotationAxis[1],self.LtIkShoulderRotationAxis[2]),roo=(self.LtIkShoulderRoo))
        
        
        #right side shoulder
        self.RtIkShoulderLoc = mc.xform('jsBuilder:rt_Bind_Clav_bone_IkSkeleton',q=True,ws=True,t=True,a=True)
        self.RtIkShoulderRotation = mc.xform('jsBuilder:rt_Bind_Clav_bone_IkSkeleton',q=True,ws=True,ro=True,a=True)
        self.RtIkShoulderRoo = mc.xform('jsBuilder:rt_Bind_Clav_bone_IkSkeleton',q=True,roo=True)
        self.RtIkShoulderRotationAxis = mc.xform('jsBuilder:rt_Bind_Clav_bone_IkSkeleton',q=True,ra=True)
        
        mc.circle(nr=(1,0,0),n='rtIkShoulderCtrl',r=11,fc=True,sw=360)
        mc.xform(t=(self.RtIkShoulderLoc[0],self.RtIkShoulderLoc[1],self.RtIkShoulderLoc[2]),ro=(self.RtIkShoulderRotation[0],self.RtIkShoulderRotation[1],self.RtIkShoulderRotation[2]),ra=(self.RtIkShoulderRotationAxis[0],self.RtIkShoulderRotationAxis[1],self.RtIkShoulderRotationAxis[2]),roo=(self.RtIkShoulderRoo))
        
        
        
        #zeroing out the offsetts
        
        mc.group(em=True,n='rtIkShoulderOffset')
        mc.xform(t=(self.RtIkShoulderLoc[0],self.RtIkShoulderLoc[1],self.RtIkShoulderLoc[2]),ro=(self.RtIkShoulderRotation[0],self.RtIkShoulderRotation[1],self.RtIkShoulderRotation[2]),ra=(self.RtIkShoulderRotationAxis[0],self.RtIkShoulderRotationAxis[1],self.RtIkShoulderRotationAxis[2]),roo=(self.RtIkShoulderRoo))
        
        
        mc.group(em=True,n='ltIkShoulderOffset')
        mc.xform(t=(self.LtIkShoulderLoc[0],self.LtIkShoulderLoc[1],self.LtIkShoulderLoc[2]),ro=(self.LtIkShoulderRotation[0],self.LtIkShoulderRotation[1],self.LtIkShoulderRotation[2]),ra=(self.LtIkShoulderRotationAxis[0],self.LtIkShoulderRotationAxis[1],self.LtIkShoulderRotationAxis[2]),roo=(self.LtIkShoulderRoo))
        
        
        
        mc.parent('jsBuilder:rtIkShoulderCtrl','jsBuilder:rtIkShoulderOffset')
        mc.parent('jsBuilder:ltIkShoulderCtrl','jsBuilder:ltIkShoulderOffset')
        
        
        #now for the Rest of the connections
        #below Fk Arm Connection
        mc.connectAttr("jsBuilder:FKIKswitches.FKLeftArmSwitch","jsBuilder:lt_Bind_Clav_bone1FkOrientCst.lt_Bind_Clav_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FKLeftArmSwitch","jsBuilder:lt_Bind_Humerous_bone1FkOrientCst.lt_Bind_Humerous_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FKLeftArmSwitch","jsBuilder:lt_Bind_Elbow_bone1FkOrientCst.lt_Bind_Elbow_bone1W0")
        
        mc.connectAttr("jsBuilder:FKIKswitches.FKRightArmSwitch","jsBuilder:rt_Bind_Clav_bone1FkOrientCst.rt_Bind_Clav_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FKRightArmSwitch","jsBuilder:rt_Bind_Humerous_bone1FkOrientCst.rt_Bind_Humerous_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FKRightArmSwitch","jsBuilder:rt_Bind_Elbow_bone1FkOrientCst.rt_Bind_Elbow_bone1W0")
        
        #now for legs Fk switch
        
        mc.connectAttr("jsBuilder:FKIKswitches.FkLeftFootSwitch","jsBuilder:lt_Bind_Calf_bone1FkOrientCst.lt_Bind_Calf_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FkLeftFootSwitch","jsBuilder:lt_Bind_Femur_bone1FkOrientCst.lt_Bind_Femur_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FkLeftFootSwitch","jsBuilder:lt_Bind_Ankle_bone1FkOrientCst.lt_Bind_Ankle_bone1W0")
        
        mc.connectAttr("jsBuilder:FKIKswitches.FkRightFootSwitch","jsBuilder:rt_Bind_Femur_bone1FkOrientCst.rt_Bind_Femur_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FkRightFootSwitch","jsBuilder:rt_Bind_Calf_bone1FkOrientCst.rt_Bind_Calf_bone1W0")
        mc.connectAttr("jsBuilder:FKIKswitches.FkRightFootSwitch","jsBuilder:rt_Bind_Ankle_bone1FkOrientCst.rt_Bind_Ankle_bone1W0")
        
        #change the colors
        mc.setAttr("jsBuilder:jsBuilder:lt_Bind_Humerous_bone1_FkControlSkeleton_FkController.overrideEnabled", 1)
        mc.setAttr("jsBuilder:jsBuilder:lt_Bind_Humerous_bone1_FkControlSkeleton_FkController.overrideColor", 14)
        
        mc.setAttr("jsBuilder:jsBuilder:rt_Bind_Humerous_bone1_FkControlSkeleton_FkController.overrideEnabled",1)
        mc.setAttr("jsBuilder:jsBuilder:rt_Bind_Humerous_bone1_FkControlSkeleton_FkController.overrideColor",13)
        
        #Arms Ik Switches 
        
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftArmSwitch","jsBuilder:lt_Bind_Elbow_bone1FkOrientCst.lt_Bind_Elbow_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftArmSwitch","jsBuilder:lt_Bind_Clav_bone1FkOrientCst.lt_Bind_Clav_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftArmSwitch","jsBuilder:lt_Bind_Humerous_bone1FkOrientCst.lt_Bind_Humerous_bone_IkSkeletonW1")
        
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightArmSwitch","jsBuilder:rt_Bind_Clav_bone1FkOrientCst.rt_Bind_Clav_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightArmSwitch","jsBuilder:rt_Bind_Humerous_bone1FkOrientCst.rt_Bind_Humerous_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightArmSwitch","jsBuilder:rt_Bind_Elbow_bone1FkOrientCst.rt_Bind_Elbow_bone_IkSkeletonW1")
        
        #Ik Legs Switches 
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightLegSwitch","jsBuilder:rt_Bind_Ankle_bone1FkOrientCst.rt_Bind_Ankle_bone_IkSkeletonW1" )
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightLegSwitch","jsBuilder:rt_Bind_Calf_bone1FkOrientCst.rt_Bind_Calf_bone_IkSkeletonW1")
        mc.connectAttr("jsBuilder:FKIKswitches.IkRightLegSwitch","jsBuilder:rt_Bind_Femur_bone1FkOrientCst.rt_Bind_Femur_bone_IkSkeletonW1")
        
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftLegSwitch" ,"jsBuilder:lt_Bind_Ankle_bone1FkOrientCst.lt_Bind_Ankle_bone_IkSkeletonW1" )
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftLegSwitch" ,"jsBuilder:lt_Bind_Calf_bone1FkOrientCst.lt_Bind_Calf_bone_IkSkeletonW1" )
        mc.connectAttr("jsBuilder:FKIKswitches.IkLeftLegSwitch" ,"jsBuilder:lt_Bind_Femur_bone1FkOrientCst.lt_Bind_Femur_bone_IkSkeletonW1" )
        
        mc.setAttr("jsBuilder:FKIKswitches.overrideEnabled",1)
        mc.setAttr("jsBuilder:FKIKswitches.overrideColor",14)
        
        mc.orientConstraint('jsBuilder:ltIkShoulderCtrl','jsBuilder:lt_Bind_Clav_bone_IkSkeleton',mo=False,w=1)
        mc.orientConstraint('jsBuilder:rtIkShoulderCtrl','jsBuilder:rt_Bind_Clav_bone_IkSkeleton',mo=False,w=1)
        #mc.setAttr('jsBuilder:HipsIkControl.translateX',0)
        #mc.setAttr('jsBuilder:HipsIkControl.translateY',0)
        #mc.setAttr('jsBuilder:HipsIkControl.translateZ',0)
        
        #mc.select('jsBuilder:HipsIkControl',add=True)
        #mc.select('jsBuilder:jsBuilder:ct_bind_bodyroot_bone1_IkSkeleton',add=True)
        #mc.PointConstraint()
        
        #mc.parent('jsBuilder:BottomLowIkOffset','jsBuilder:RootControl')
        #mc.parent('jsBuilder:HipsIkCtrlOffset','jsBuilder:RootControl')
        #mc.parent('jsBuilder:ChestIkCtrlOffset','jsBuilder:RootControl')
        #mc.parent('jsBuilder:UpHighIkOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:LtArmPoleVectorCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:RtArmPoleVectorCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:RTArmIkOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:LTArmIkOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:LtLegPoleVectorCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:RtLegPoleVectorCtrlOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:RTLegIkOffset','jsBuilder:RootControl')
        mc.parent('jsBuilder:LTLegIkOffset','jsBuilder:RootControl')
        #mc.parent('jsBuilder:rtIkShoulderOffset','jsBuilder:ChestIkCtrlOffset')
        #mc.parent('jsBuilder:ltIkShoulderOffset','jsBuilder:ChestIkCtrlOffset')
        
        mc.setAttr("jsBuilder:switchtextboxCurvesShape_pointConstraint1.offsetX",0)
        mc.setAttr("jsBuilder:switchtextboxCurvesShape_pointConstraint1.offsetY",0)
        mc.setAttr("jsBuilder:switchtextboxCurvesShape_pointConstraint1.offsetZ",0)
        mc.select(clear=True)
        
        
        mc.file('c:/FinalDemo/ProxyGeo.ma',i=True)
        
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Place Spine Ik down  here<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 
 
 
         #mc.curve(n='IkSpineCurveSkin',d= 3, p=[( 0 ,127.405036 ,0 ),(0 ,131.6976, 2.428914 ),(0, 136.206548, 4.42769) ,( 0 ,140.907356, 5.382386) ,( 0 ,145.703799, 5.326124),(0, 151.641849 ,4.154978),( 0 ,157.414362, 2.335608)],k=[0 , 0 , 0 , 1 , 2 , 3 , 4 , 4 , 4 ]) 
        #mc.container('jsBuilder:IkSkeletonContainer',e=True,rc=True)
        mc.ikHandle(sj='jsBuilder:ct_bind_pelvis_bone_IkSkeleton',ee='jsBuilder:ct_bind_SpineEnd_bone_IkSkeleton',sol='ikSplineSolver',scv=True,n='IkSpineCurve',roc=True ,pcv=False,)
        self.SpineIkSettingsHandle = mc.ls(sl=True)
        mc.setAttr(self.SpineIkSettingsHandle[0] + '.dTwistControlEnable',1)
        mc.setAttr(self.SpineIkSettingsHandle[0] + '.dWorldUpAxis',0)
        mc.setAttr(self.SpineIkSettingsHandle[0] + '.dWorldUpType',2)
        
        mc.select('jsBuilder:ct_Bind_spinebase_bone_IkSkeleton')
        
        self.Controltarget = mc.ls(sl=True,type='joint')
        self.TargLoc = mc.xform(self.Controltarget[0],q=True,ws=True,t=True,a=True)
        self.TargRotOrder = mc.xform(self.Controltarget[0],q=True,roo=True)
        self.TargRotation = mc.xform(self.Controltarget[0],q=True,ws=True,ro=True,a=True)
        self.TargRotAxis = mc.xform(self.Controltarget[0],q=True,ra=True)
        mc.select(clear=True)
        str(self.TargRotOrder)
        mc.group(em=True,n='BottomLowIkOffset')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.select(clear=True)
        
        mc.joint(p=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]),n='BottomLowIk',rad=4)
        mc.circle(nr=(0,1,0),r=30,sw=360,fc=True,n='HipsIkControl')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.group(em=True,n='HipsIkCtrlOffset')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.parent('jsBuilder:HipsIkControl','jsBuilder:HipsIkCtrlOffset')
        mc.select('jsBuilder:HipsIkControl',add=True)
        mc.select('jsBuilder:BottomLowIk',add=True)
        mc.parentConstraint(n='HipsIkParentConstraint',mo=True)
        mc.select(clear=True)
        mc.parent('jsBuilder:BottomLowIk','jsBuilder:BottomLowIkOffset')
        mc.select('jsBuilder:ct_bind_SpineEnd_bone_IkSkeleton')
        
        self.Controltarget = mc.ls(sl=True,type='joint')
        self.TargLoc = mc.xform(self.Controltarget[0],q=True,ws=True,t=True,a=True)
        self.TargRotOrder = mc.xform(self.Controltarget[0],q=True,roo=True)
        self.TargRotation = mc.xform(self.Controltarget[0],q=True,ws=True,ro=True,a=True)
        self.TargRotAxis = mc.xform(self.Controltarget[0],q=True,ra=True,a=True)
        
        mc.select(clear=True)
        
        str(self.TargRotOrder)#chest was setup first
        mc.joint(p=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]),n='UpHighIk',rad=4,roo=(self.TargRotOrder))#setup the controllers for the ik spine
        
        #for i in self.IkSpineJoints:
            #mc.makeIdentity(i,a=True)
        
        mc.group(em=True,n='ChestIkCtrlOffset')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.circle(nr=(0,1,0),r=45,sw=360,fc=True,n='ChestIkCtrl')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.parent('jsBuilder:ChestIkCtrl','jsBuilder:ChestIkCtrlOffset')
        mc.select('jsBuilder:ChestIkCtrl',add=True)
        mc.select('jsBuilder:UpHighIk',add=True)
        mc.parentConstraint(n='chestControlParentConstraintIk',mo=True)
        mc.select(clear=True)
        
        mc.group(em=True,n='UpHighIkOffset')
        mc.xform(t=(self.TargLoc[0],self.TargLoc[1],self.TargLoc[2]))
        mc.parent('jsBuilder:UpHighIk','jsBuilder:UpHighIkOffset')
        
        #for i in self.IkSpineJoints:
            #mc.makeIdentity(i,a=True)
        
        mc.select('jsBuilder:curve1')
        mc.rename('SpineCurveForIk')
        
        mc.select(clear=True)
        mc.select('jsBuilder:lt_Bind_hand_tip1_FkControlSkeleton_IkSkeleton')
        mc.delete()
        
        
        mc.select(clear=True)
        
        mc.connectAttr('jsBuilder:UpHighIk.xformMatrix', 'jsBuilder:IkSpineCurve.dWorldUpMatrix')
        mc.connectAttr('jsBuilder:BottomLowIk.xformMatrix', 'jsBuilder:IkSpineCurve.dWorldUpMatrixEnd')#setup the up and down vecotr objects for the SpineIk spine
        mc.skinCluster('jsBuilder:ct_bind_pelvis_bone_IkSkeleton','jsBuilder:UpHighIk','jsBuilder:curve18',n='SkinforSpineIk',dr=4,tsb=True)
        
        #mc.select('jsBuilder:BottomLowIk',add=True)
        #mc.select('jsBuilder:jsBuilder:ct_bind_bodyroot_bone1_IkSkeleton',add=True)
        #mc.PointConstraint(n='hipsBasePointConsIk')
        
        mc.setAttr('jsBuilder:ct_Bind_Chest_bone1_FkControlSkeleton.rotateOrder',2)
        mc.setAttr('jsBuilder:ct_bind_SpineEnd_bone.rotateOrder',2)
        mc.setAttr('jsBuilder:ct_Bind_Chest_bone.rotateOrder',2)
        
        #constrainng clav fk to Ikfk since both will be controlled the same 
        mc.orientConstraint('jsBuilder:lt_Bind_Clav_bone1_FkControlSkeleton','jsBuilder:lt_Bind_Clav_bone_IkSkeleton')
        mc.orientConstraint('jsBuilder:rt_Bind_Clav_bone1_FkControlSkeleton','jsBuilder:rt_Bind_Clav_bone_IkSkeleton')

 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>       
        mc.container('jsBuilder:IkSkeletonContainer',e=True,rc=True)
        
        
        mc.parent('jsBuilder:FKIKswitches','jsBuilder:RootControl')
        mc.parent('jsBuilder:ltlegproxy','jsBuilder:lt_Bind_Femur_bone')
        mc.parent('jsBuilder:ltthighproxy','jsBuilder:lt_Bind_Femur_bone')
        mc.parent('jsBuilder:rtlegproxy','jsBuilder:rt_Bind_Femur_bone')
        mc.parent('jsBuilder:rtthighproxy','jsBuilder:rt_Bind_Femur_bone')
        mc.parent('jsBuilder:ctwaistproxy','jsBuilder:ct_bind_bodyroot_bone')
        mc.parent('jsBuilder:ctgeoproxyshirtbase','jsBuilder:ct_Bind_spinea_bone')
        mc.parent('jsBuilder:ctgeoproxyshirtmid','jsBuilder:ct_Bind_spinec_bone')
        mc.parent('jsBuilder:ctgeoproxyshirttop','jsBuilder:ct_Bind_Chest_bone')
        mc.parent('jsBuilder:ctgeoproxychestbase','jsBuilder:ct_Bind_spinec_bone')
        mc.parent('jsBuilder:ctgeoproxychest','jsBuilder:ct_Bind_Chest_bone')
        mc.parent('jsBuilder:ltgeoproxyshoudler','jsBuilder:lt_Bind_Clav_bone')
        mc.parent('jsBuilder:ltgeoproxybicep','jsBuilder:lt_Bind_Humerous_bone')
        mc.parent('jsBuilder:ltgeoproxyforarm','jsBuilder:lt_Bind_Elbow_bone')
        mc.parent('jsBuilder:ltgeoproxyforarm1','jsBuilder:lt_Bind_Wrst_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltgeoproxythumbbase','jsBuilder:lt_Bind_Thmb_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltgeoproxythumbtip','jsBuilder:lt_Bind_Thmb_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:geoproxyltindexbase','jsBuilder:lt_Bind_Index_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:geoproxyindexmid','jsBuilder:lt_Bind_Index_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:geoproxyindextip','jsBuilder:lt_Bind_Index_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltgeoproxymfingerbase','jsBuilder:lt_Bind_Mfinger_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltmfingergeoproxymid','jsBuilder:lt_Bind_Mfinger_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltmfingergeoproxytip','jsBuilder:lt_Bind_Mfinger_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltrfingergeoproxybase','jsBuilder:lt_Bind_Rfinger_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltrfingergeoproxymid','jsBuilder:lt_Rfinger_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltrfingergeoproxytip','jsBuilder:lt_Bind_Rfinger_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltpinkygeoproxybase','jsBuilder:lt_Pinky_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltpinkygeoproxymid','jsBuilder:lt_Pinky_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltpinkygeoproxytip','jsBuilder:lt_Pinky_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:ltcalfproxy','jsBuilder:lt_Bind_Calf_bone')
        mc.parent('jsBuilder:ltheelproxy','jsBuilder:lt_Bind_Ankle_bone')
        mc.parent('jsBuilder:ltfoottip','jsBuilder:lt_Bind_Foot_ball_bone')
        mc.parent('jsBuilder:rtcalfproxy','jsBuilder:rt_Bind_Calf_bone')
        mc.parent('jsBuilder:rtheelproxy','jsBuilder:rt_Bind_Ankle_bone')
        mc.parent('jsBuilder:rtfoottipproxy','jsBuilder:rt_Bind_Foot_ball_bone')
        mc.parent('jsBuilder:rtgeoproxyshoulder','jsBuilder:rt_Bind_Clav_bone')
        mc.parent('jsBuilder:rtgeoproxybicep','jsBuilder:rt_Bind_Humerous_bone')
        mc.parent('jsBuilder:rtgeoproxyforarm','jsBuilder:rt_Bind_Elbow_bone')
        mc.parent('jsBuilder:rtgeoproxyforarm1','jsBuilder:rt_Bind_Wrst_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxythumbbase','jsBuilder:rt_Bind_Thmb_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxythumbtip','jsBuilder:rt_Bind_Thmb_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxyindexbase','jsBuilder:rt_Bind_Index_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxyindexmid','jsBuilder:rt_Bind_Index_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxyindextip','jsBuilder:rt_Bind_Index_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtmfingergeoproxybase','jsBuilder:rt_Bind_Mfinger_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtmfingergeoproxymid','jsBuilder:rt_Bind_Mfinger_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxymfingertip','jsBuilder:rt_Bind_Mfinger_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgeoproxyrfingerbase','jsBuilder:rt_Bind_Rfinger_a_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtrfingergeoproxymid','jsBuilder:rt_Rfinger_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtgetproxyrfingertip','jsBuilder:rt_Bind_Rfinger_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtpinkybasefingerproxy','jsBuilder:rt_Pinky_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtpinkmidproxy','jsBuilder:rt_Pinky_b_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:rtpinkytipproxy','jsBuilder:rt_Pinky_c_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:cthairproxy','jsBuilder:ct_Bind_Head_base_bone1_FkControlSkeleton')
        mc.parent('jsBuilder:headproxy','jsBuilder:ct_Bind_Head_base_bone')
        
        #new parenting setup here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #mc.parent('jsBuilder:ct_Bind_Chest_bone_IkSkeleton','jsBuilder:ct_bind_SpineEnd_bone')
        mc.parent('jsBuilder:ct_Bind_Chest_bone1_FkControlSkeleton','jsBuilder:ct_bind_SpineEnd_bone')
        mc.parent('jsBuilder:jsBuilder:ct_Bind_spinef_bone1_FkControlSkeletonFkCtrlOffset','jsBuilder:ct_Bind_spinee_bone')
        
        mc.orientConstraint('jsBuilder:ct_Bind_spinef_bone1_FkControlSkeleton','jsBuilder:ct_Bind_spinef_bone_IkSkeleton')
        
        #deleting constraints to clean up chest control
        mc.delete('jsBuilder:jsBuilder:ct_Bind_Chest_boneIK_OrientConstraint')
        mc.delete('jsBuilder:jsBuilder:ct_bind_SpineEnd_boneIK_OrientConstraint')
        
        mc.select('jsBuilder:lt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        mc.select('jsBuilder:rt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        #building ReverseFoot off existing joints Duplicate this block>>>>LEFTFOOTHERE   VVVV
        mc.select('jsBuilder:lt_Bind_Ankle_bone_IkSkeleton')
        mc.duplicate()
        mc.parent(w=True)
        
        mc.select(hi=True)
        self.LtReverseFootJoints = mc.ls(sl=True,type='joint')
        
        
        self.LtReverseFootJoints.reverse()
        mc.rename(self.LtReverseFootJoints[0], 'lt_FootA')
        mc.rename(self.LtReverseFootJoints[1], 'lt_FootB')
        mc.rename(self.LtReverseFootJoints[2], 'lt_FootC')
        mc.select(clear=True)
        mc.select('jsBuilder:lt_FootA')
        mc.duplicate()
        mc.rename('lt_ReverseFootHeel')
        mc.parent(w=True)
        mc.move(0,0,-30,r=True)
        
        mc.rename('lt_ReverseFootHeel')
        mc.parent('jsBuilder:lt_FootA',w=True)
        mc.parent('jsBuilder:lt_FootB',w=True)
        mc.parent('jsBuilder:lt_FootA','jsBuilder:lt_ReverseFootHeel')
        mc.parent('jsBuilder:lt_FootB','jsBuilder:lt_FootA')
        mc.parent('jsBuilder:lt_FootC','jsBuilder:lt_FootB')
        
        #reroienting the ball
        
        
        mc.select('jsBuilder:lt_ReverseFootHeel')
        mc.joint(e=True,oj='xyz',sao='zdown',ch=True)
        
        self.LtheelLoc = mc.xform(q=True,ws=True,a=True,t=True)
        mc.group(em=True,n='LtIkFootControlOffset')
        
       
        mc.xform(t=(self.LtheelLoc[0],self.LtheelLoc[1],self.LtheelLoc[2]))
        
        mc.parent('jsBuilder:lt_ReverseFootHeel','jsBuilder:LtIkFootControlOffset')
        
        mc.orientConstraint('jsBuilder:lt_FootA','jsBuilder:lt_Bind_Foot_ball_bone',n='LtReverseBallOrientConstr',mo=True)
        mc.orientConstraint('jsBuilder:lt_FootB','jsBuilder:lt_Bind_Ankle_bone',n='ltReverseAnkleRoll',mo=True)
        mc.select(clear=True)
        mc.select('jsBuilder:lt_FootC',add=True)
        mc.select('jsBuilder:IkLtLegHandle',add=True)
        mc.PointConstraint(n='LtIkFootPointControl')
        
        mc.parent('jsBuilder:LtIkFootControlOffset','jsBuilder:RootControl')
        
        mc.delete('jsBuilder:lt_Bind_Foot_tip_bone1FkOrientCst')
        mc.delete('jsBuilder:LtReverseBallOrientConstr')
        mc.delete('jsBuilder:ltReverseAnkleRoll')
        
        mc.select('jsBuilder:lt_FootA',add=True)
        mc.select('jsBuilder:lt_Bind_Foot_ball_bone_IkSkeleton',add=True)
        mc.orientConstraint(n='Lt_OrientConsforRevFoot')
        mc.select(clear=True)
        
        mc.select('jsBuilder:lt_Bind_Ankle_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:lt_Bind_Ankle_bone',add=True)
        mc.orientConstraint(n='heelOrientConstraintReversefoot')
        mc.select(clear=True)
        mc.select('jsBuilder:lt_Bind_Ankle_bone',add=True)
        mc.select('jsBuilder:lt_Bind_Foot_ball_bone',add=True)
        mc.orientConstraint(n='Lt_footbballreversefootOrientConstraint')
        #meltopy extremely useful tool from pytmel 
        #chestcrveshapeSnapToPoint; dR_enterForSnap
        
        mc.orientConstraint('jsBuilder:ct_Bind_spinef_bone1_FkControlSkeleton','jsBuilder:ct_Bind_spinef_bone_IkSkeleton')
        
        #deleting constraints to clean up chest control
        
        
        mc.select('jsBuilder:lt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        mc.select('jsBuilder:rt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        #building ReverseFoot off existing joints Duplicate this block>>>>RIGHTFOOT_HERE   VVVV
        mc.delete('jsBuilder:rt_Bind_Foot_tip_bone1FkOrientCst')
        mc.delete('jsBuilder:rt_Bind_Foot_ball_bone1FkOrientCst')
        mc.delete('jsBuilder:rt_Bind_Ankle_bone1FkOrientCst')
        mc.select(clear=True)
        
        mc.select('jsBuilder:rt_Bind_Ankle_bone_IkSkeleton')
        mc.duplicate()
        mc.parent(w=True)
        
        mc.select(hi=True)
        self.RtReverseFootJoints = mc.ls(sl=True,type='joint')
        
        
        self.RtReverseFootJoints.reverse()
        mc.rename(self.RtReverseFootJoints[0], 'rt_FootA')
        mc.rename(self.RtReverseFootJoints[1], 'rt_FootB')
        mc.rename(self.RtReverseFootJoints[2], 'rt_FootC')
        mc.select(clear=True)
        mc.select('jsBuilder:rt_FootA')
        mc.duplicate()
        mc.rename('rt_ReverseFootHeel')
        mc.parent(w=True)
        mc.move(0,0,-30,r=True)
        
        mc.rename('rt_ReverseFootHeel')
        mc.parent('jsBuilder:rt_FootA',w=True)
        mc.parent('jsBuilder:rt_FootB',w=True)
        mc.parent('jsBuilder:rt_FootA','jsBuilder:rt_ReverseFootHeel')
        mc.parent('jsBuilder:rt_FootB','jsBuilder:rt_FootA')
        mc.parent('jsBuilder:rt_FootC','jsBuilder:rt_FootB')
        
        #reroienting the ball
        
        
        mc.select('jsBuilder:rt_ReverseFootHeel')
        mc.joint(e=True,oj='xyz',sao='zdown',ch=True)
        
        self.RtheelLoc = mc.xform(q=True,ws=True,a=True,t=True)
        mc.group(em=True,n='RtIkFootControlOffset')
        
       
        mc.xform(t=(self.RtheelLoc[0],self.RtheelLoc[1],self.RtheelLoc[2]))
        
        mc.parent('jsBuilder:rt_ReverseFootHeel','jsBuilder:RtIkFootControlOffset')
        
        mc.orientConstraint('jsBuilder:rt_FootA','jsBuilder:rt_Bind_Foot_ball_bone',n='RtReverseBallOrientConstr',mo=True)
        mc.orientConstraint('jsBuilder:rt_FootB','jsBuilder:rt_Bind_Ankle_bone',n='rtReverseAnkleRoll',mo=True)
        mc.select(clear=True)
        mc.select('jsBuilder:rt_FootC',add=True)
        mc.select('jsBuilder:IkRtLegHandle',add=True)
        mc.PointConstraint(n='RtIkFootPointControl')
        
        mc.parent('jsBuilder:RtIkFootControlOffset','jsBuilder:RootControl')
        
        #mc.delete('jsBuilder:rt_Bind_Foot_tip_bone1FkOrientCst')
        mc.delete('jsBuilder:RtReverseBallOrientConstr')
        mc.delete('jsBuilder:rtReverseAnkleRoll')
        
        mc.select('jsBuilder:rt_FootA',add=True)
        mc.select('jsBuilder:rt_Bind_Foot_ball_bone_IkSkeleton',add=True)
        mc.orientConstraint(n='Rt_OrientConsforRevFoot')
        mc.select(clear=True)
        
        mc.select('jsBuilder:rt_Bind_Ankle_bone_IkSkeleton',add=True)
        mc.select('jsBuilder:rt_Bind_Ankle_bone',add=True)
        mc.orientConstraint(n='heelOrientConstraintReversefoot')
        mc.select(clear=True)
        mc.select('jsBuilder:rt_Bind_Ankle_bone',add=True)
        mc.select('jsBuilder:rt_Bind_Foot_ball_bone',add=True)
        mc.orientConstraint(n='Rt_footbballreversefootOrientConstraint')
        
        #now setting up constraints to foot from FK feets 
        mc.select('jsBuilder:lt_Bind_Ankle_bone1_FkControlSkeleton',add=True)
        mc.select('jsBuilder:lt_Bind_Ankle_bone',add=True)
        mc.orientConstraint(n='Lt_FkFootOrientConstraintHeel')
        mc.select(clear=True)
        mc.select('jsBuilder:lt_Bind_Foot_ball_bone1_FkControlSkeleton',add=True)
        mc.select('jsBuilder:lt_Bind_Foot_ball_bone',add=True)
        mc.orientConstraint(n='Lt_Fk_BallfootOrientConstraint')
        
        mc.setAttr("jsBuilder:Lt_OrientConsforRevFoot.offsetX" ,180)
        mc.setAttr("jsBuilder:Lt_OrientConsforRevFoot.offsetZ", 180)
        mc.delete('jsBuilder:lt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        mc.delete('jsBuilder:rt_Bind_Clav_bone_IkSkeleton_orientConstraint1')
        
        mc.delete('jsBuilder:rtIkShoulderOffset')
        mc.delete('jsBuilder:ltIkShoulderOffset')
        
        mc.delete('jsBuilder:tongue_geo')
        ''
#myNamespaceObject = NameSpaceCaller()
#myTestObjectA = LocatorSetup()
#myTestObjectB = BuildSkeletonRig()

        
        
        
        
        
    
    
