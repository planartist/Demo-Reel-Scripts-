Demo-Reel-Scripts-
==================

primeBuildRigRev2  Rig Builder based on Location position
 Note First put all docs into your python scripts folder based on Your environment variable.
 Also there is no default environment serach within maya, so the file paths in the pyscript need to be
 hardcoded to your locations
 
 Then Import the script into your scene
 
  import primeBuildRigRev2
 
 usage first call to set the namespace make an object call to the first Class 
 
 
 setMynamespaceplease = NameSpaceCaller()
 
 
 
 then an object reference call to the Locator setup
 
 setupMylocators = LocatorSetup()
 
 
 Position the locators where you want the joints to be Orientation is setup for a default standup a pose person rig
 
 when ready launch the builder with another object call to the class
 
 buildMyrig = BuildSkeletonRig()
 
 
