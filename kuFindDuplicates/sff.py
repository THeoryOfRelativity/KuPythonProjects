# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def resource_path(self, relative):
		print "TEST !!!!!!!!!"
		import os
		return str(os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(".")), relative))	

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1056,707 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)
		
		self.panelTop = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.panelTop, wx.aui.AuiPaneInfo() .Name( u"auiPanelTop" ).Top() .CaptionVisible( False ).CloseButton( False ).Movable( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ).Floatable( False ).MinSize( wx.Size( -1,150 ) ) )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self.panelTop, wx.ID_ANY, u"PRIMARY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer11.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bpButton4 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"add_16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer13.Add( self.m_bpButton4, 0, wx.ALL, 5 )
		
		self.m_bpButton9 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"add_16_dis.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer13.Add( self.m_bpButton9, 0, wx.ALL, 5 )
		
		self.m_bpButton5 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"remove_16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer13.Add( self.m_bpButton5, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		m_checkList2Choices = []
		self.m_checkList2 = wx.CheckListBox( self.panelTop, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList2Choices, 0 )
		bSizer3.Add( self.m_checkList2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer111 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText21 = wx.StaticText( self.panelTop, wx.ID_ANY, u"SECONDARY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer16.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
		
		bSizer16.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_checkBox_SecondaryFlag = wx.CheckBox( self.panelTop, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_SecondaryFlag.SetValue(True) 
		bSizer16.Add( self.m_checkBox_SecondaryFlag, 0, wx.ALL, 5 )
		
		
		bSizer111.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bpButton6 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"add_16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer15.Add( self.m_bpButton6, 0, wx.ALL, 5 )
		
		self.m_bpButton10 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"add_16_dis.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer15.Add( self.m_bpButton10, 0, wx.ALL, 5 )
		
		self.m_bpButton7 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( u"remove_16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer15.Add( self.m_bpButton7, 0, wx.ALL, 5 )
		
		
		bSizer111.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer111, 0, wx.EXPAND, 5 )
		
		m_checkList3Choices = []
		self.m_checkList3 = wx.CheckListBox( self.panelTop, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList3Choices, 0 )
		bSizer4.Add( self.m_checkList3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.panelTop.SetSizer( bSizer2 )
		self.panelTop.Layout()
		bSizer2.Fit( self.panelTop )
		self.panelMiddle = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.panelMiddle, wx.aui.AuiPaneInfo() .Name( u"auiPanelMiddle" ).Center() .CaptionVisible( False ).CloseButton( False ).Movable( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ).Floatable( False ).Row( 1 ) )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		m_checkList1Choices = []
		self.m_checkList1 = wx.CheckListBox( self.panelMiddle, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList1Choices, 0 )
		bSizer22.Add( self.m_checkList1, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bpButton1 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( u"copyok_24.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.m_bpButton1, 0, wx.ALL, 5 )
		
		self.m_bpButton2 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( u"copyok_24_dis.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.m_bpButton2, 0, wx.ALL, 5 )
		
		self.m_bpButton3 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( u"refresh_24.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.m_bpButton3, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button9 = wx.Button( self.panelMiddle, wx.ID_ANY, u"Save to File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button9, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( self.panelMiddle, wx.ID_ANY, u"Load from File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button10, 0, wx.ALL, 5 )
		
		self.m_button12 = wx.Button( self.panelMiddle, wx.ID_ANY, u"Append from File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button12, 0, wx.ALL, 5 )
		
		
		bSizer22.Add( bSizer10, 0, wx.ALIGN_TOP|wx.EXPAND|wx.FIXED_MINSIZE, 1 )
		
		
		self.panelMiddle.SetSizer( bSizer22 )
		self.panelMiddle.Layout()
		bSizer22.Fit( self.panelMiddle )
		self.panelBottom = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.panelBottom, wx.aui.AuiPaneInfo() .Name( u"auiPanelBottom" ).Bottom() .CaptionVisible( False ).CloseButton( False ).Movable( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ).Floatable( False ).Row( 5 ).MinSize( wx.Size( -1,220 ) ) )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button4 = wx.Button( self.panelBottom, wx.ID_ANY, u"SEARCH  DUPLICATES", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_button4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_button4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		bSizer8.Add( self.m_button4, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panelSearchOptions = wx.Panel( self.panelBottom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5 = wx.StaticText( self.panelSearchOptions, wx.ID_ANY, u"Search Options", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer17.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_checkBox_CompFileNames = wx.CheckBox( self.panelSearchOptions, wx.ID_ANY, u"Compare File Names", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_CompFileNames.SetValue(True) 
		bSizer17.Add( self.m_checkBox_CompFileNames, 0, wx.ALL, 5 )
		
		self.m_checkBox_CompFileDateTime = wx.CheckBox( self.panelSearchOptions, wx.ID_ANY, u"Compare File DateTime", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_CompFileDateTime.SetValue(True) 
		bSizer17.Add( self.m_checkBox_CompFileDateTime, 0, wx.ALL, 5 )
		
		self.m_checkBox_CompFileHashes = wx.CheckBox( self.panelSearchOptions, wx.ID_ANY, u"Compare File Hashes", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_CompFileHashes, 0, wx.ALL, 5 )
		
		self.m_checkBox_BindDupl2Dir = wx.CheckBox( self.panelSearchOptions, wx.ID_ANY, u"Bind duplicates to mutual directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_BindDupl2Dir.SetValue(True) 
		bSizer17.Add( self.m_checkBox_BindDupl2Dir, 0, wx.ALL, 5 )
		
		
		self.panelSearchOptions.SetSizer( bSizer17 )
		self.panelSearchOptions.Layout()
		bSizer17.Fit( self.panelSearchOptions )
		bSizer8.Add( self.panelSearchOptions, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.panelRemovingOptions = wx.Panel( self.panelBottom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6 = wx.StaticText( self.panelRemovingOptions, wx.ID_ANY, u"Removing Options", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer18.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		m_radioBox1Choices = [ u"Remove to RecycleBin", u"Remove Permanently", u"Move to another Directory" ]
		self.m_radioBox1 = wx.RadioBox( self.panelRemovingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox1.SetSelection( 0 )
		bSizer18.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button11 = wx.Button( self.panelRemovingOptions, wx.ID_ANY, u"Change Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button11.Enable( False )
		
		bSizer19.Add( self.m_button11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.panelRemovingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.Enable( False )
		
		bSizer19.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		
		bSizer18.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		self.m_button41 = wx.Button( self.panelRemovingOptions, wx.ID_ANY, u"Remove Selected Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button41.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer18.Add( self.m_button41, 0, wx.ALL, 5 )
		
		
		self.panelRemovingOptions.SetSizer( bSizer18 )
		self.panelRemovingOptions.Layout()
		bSizer18.Fit( self.panelRemovingOptions )
		bSizer8.Add( self.panelRemovingOptions, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		
		self.panelBottom.SetSizer( bSizer6 )
		self.panelBottom.Layout()
		bSizer6.Fit( self.panelBottom )
		self.panelFooter = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panelFooter.SetExtraStyle( wx.WS_EX_VALIDATE_RECURSIVELY )
		
		self.m_mgr.AddPane( self.panelFooter, wx.aui.AuiPaneInfo() .Bottom() .CaptionVisible( False ).CloseButton( False ).Movable( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ).Floatable( False ).Row( 7 ).MinSize( wx.Size( -1,50 ) ).Layer( 10 ) )
		
		bSizer191 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_gauge1 = wx.Gauge( self.panelFooter, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 ) 
		self.m_gauge1.Hide()
		
		bSizer191.Add( self.m_gauge1, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_gauge2 = wx.Gauge( self.panelFooter, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge2.SetValue( 0 ) 
		self.m_gauge2.Hide()
		
		bSizer191.Add( self.m_gauge2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panelFooter.SetSizer( bSizer191 )
		self.panelFooter.Layout()
		bSizer191.Fit( self.panelFooter )
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.m_mgr.Update()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnFrameClose )
		self.m_bpButton4.Bind( wx.EVT_BUTTON, self.OnAddDirectory_Primary )
		self.m_bpButton9.Bind( wx.EVT_BUTTON, self.OnAddExcludeDirectory_Primary )
		self.m_bpButton5.Bind( wx.EVT_BUTTON, self.OnRemoveDirectory_Primary )
		self.m_checkList2.Bind( wx.EVT_CHECKLISTBOX, self.OnCheckToggledDirsPrimary )
		self.m_checkBox_SecondaryFlag.Bind( wx.EVT_CHECKBOX, self.OnCheck_SecondaryFlag )
		self.m_bpButton6.Bind( wx.EVT_BUTTON, self.OnAddDirectory_Secondary )
		self.m_bpButton10.Bind( wx.EVT_BUTTON, self.OnAddExcludeDirectory_Secondary )
		self.m_bpButton7.Bind( wx.EVT_BUTTON, self.OnRemoveDirectory_Secondary )
		self.m_checkList3.Bind( wx.EVT_CHECKLISTBOX, self.OnCheckToggledDirsSecondary )
		self.m_bpButton1.Bind( wx.EVT_BUTTON, self.SelectAll )
		self.m_bpButton2.Bind( wx.EVT_BUTTON, self.SelectNone )
		self.m_bpButton3.Bind( wx.EVT_BUTTON, self.SelectInvert )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnSaveListToFile )
		self.m_button10.Bind( wx.EVT_BUTTON, self.OnLoadListFromFile )
		self.m_button12.Bind( wx.EVT_BUTTON, self.OnAppendListFromFile )
		self.m_button4.Bind( wx.EVT_BUTTON, self.SearchDuplicates )
		self.m_checkBox_CompFileNames.Bind( wx.EVT_CHECKBOX, self.OnCheck_CompFileNames )
		self.m_checkBox_CompFileDateTime.Bind( wx.EVT_CHECKBOX, self.OnCheck_CompFileDateTime )
		self.m_checkBox_CompFileHashes.Bind( wx.EVT_CHECKBOX, self.OnCheck_CompFileHashes )
		self.m_checkBox_BindDupl2Dir.Bind( wx.EVT_CHECKBOX, self.OnCheck_BindDupl2Dir )
		self.m_radioBox1.Bind( wx.EVT_RADIOBOX, self.OnRemovingOptions )
		self.m_button11.Bind( wx.EVT_BUTTON, self.OnChangeMovingDir )
		self.m_button41.Bind( wx.EVT_BUTTON, self.RemoveSelectedFiles )
	
#		self.m_bpButton4 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('add_16.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton9 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('add_16_dis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton5 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('remove_16.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton6 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('add_16.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton10 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('add_16_dis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton7 = wx.BitmapButton( self.panelTop, wx.ID_ANY, wx.Bitmap( self.resource_path('remove_16.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton1 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( self.resource_path('copyok_24.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton2 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( self.resource_path('copyok_24_dis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
#		self.m_bpButton3 = wx.BitmapButton( self.panelMiddle, wx.ID_ANY, wx.Bitmap( self.resource_path('refresh_24.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.LoadConfig()

	def __del__( self ):
		self.m_mgr.UnInit()
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSaveListToFile( self, event ):
		import datetime
		if not self.parameters.has_key('SaveDuplFileListDir'):
			self.parameters['SaveDuplFileListDir']="\\".join(self.CfgFileFullName.split('\\')[:-1])
	        dialog = wx.FileDialog(None, "Save Duplicated List As", self.parameters['SaveDuplFileListDir'] , 'Duplicated_Files_List_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.dat', "Duplicate Files List files (*.dat)|*.dat", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
	        if dialog.ShowModal():
			f=open(dialog.GetPath(),'w')
			dtemp={}
			dtemp['DuplicatedFiles']=self.duplicatedfiledict
			dtemp['DuplicatedDirs']=self.duplicateddirdict
			f.write(str(dtemp))
			f.close()
			self.parameters['SaveDuplFileListDir']='\\'.join(dialog.GetPath().split('\\')[:-1])
			MyMessageBox=wx.MessageDialog(self,'Duplicated files and directories list saved sucessfully.','Message', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
	        dialog.Destroy() 
	
	def OnLoadListFromFile( self, event ):
		if not self.parameters.has_key('LoadDuplFileListDir'):
			self.parameters['LoadDuplFileListDir']="\\".join(self.CfgFileFullName.split('\\')[:-1])
	        dialog = wx.FileDialog(None, "Open Duplicated List file", self.parameters['LoadDuplFileListDir'] , "", "Duplicate Files List files (*.dat)|*.dat", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	        if dialog.ShowModal():
			f=open(dialog.GetPath(),'r')
			dtemp = eval(f.read())
			self.duplicatedfiledict=dtemp['DuplicatedFiles']
			self.duplicateddirdict=dtemp['DuplicatedDirs']
			f.close()
			self.parameters['LoadDuplFileListDir']='\\'.join(dialog.GetPath().split('\\')[:-1])
			self.m_checkList1.Clear()
			for key, value in self.duplicatedfiledict.items():
				self.m_checkList1.Append('FILE: '+key+'|'+str(value['Size'])+'|'+value['ModifyDateTime']+'|'+value['Hash']+'| duplicated of '+value['DuplicatedOf'])
				self.Update()
			for key in self.duplicateddirdict.keys():
				self.m_checkList1.Append('DIR: '+key)
				self.Update()
			MyMessageBox=wx.MessageDialog(self,'Duplicated files and directories list opened and loaded sucessfully.','Message', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
	        dialog.Destroy() 

	def OnAppendListFromFile( self, event ):
		if not self.parameters.has_key('LoadDuplFileListDir'):
			self.parameters['LoadDuplFileListDir']="\\".join(self.CfgFileFullName.split('\\')[:-1])
	        dialog = wx.FileDialog(None, "Open Duplicated List file", self.parameters['LoadDuplFileListDir'] , "", "Duplicate Files List files (*.dat)|*.dat", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	        if dialog.ShowModal():
			f=open(dialog.GetPath(),'r')
			dtemp = eval(f.read())
			self.duplicatedfiledict.update(dtemp['DuplicatedFiles'])
			self.duplicateddirdict.update(dtemp['DuplicatedDirs'])
			f.close()
			self.parameters['LoadDuplFileListDir']='\\'.join(dialog.GetPath().split('\\')[:-1])
			self.m_checkList1.Clear()
			for key, value in self.duplicatedfiledict.items():
				self.m_checkList1.Append('FILE: '+key+'|'+str(value['Size'])+'|'+value['ModifyDateTime']+'|'+value['Hash']+'| duplicated of '+value['DuplicatedOf'])
				self.Update()
			for key in self.duplicateddirdict.keys():
				self.m_checkList1.Append('DIR: '+key)
				self.Update()
			MyMessageBox=wx.MessageDialog(self,'Duplicated files and directories list opened and loaded sucessfully.','Message', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
	        dialog.Destroy() 


	def OnRemovingOptions( self, event ):
		self.parameters['RemovingOption']=self.m_radioBox1.GetSelection()
		if self.parameters['RemovingOption']==2:
			self.m_button11.Enable(True)
			self.m_staticText7.Enable(True)
			self.m_button41.SetLabel('Move Selected Files')
		else:
			self.m_button11.Enable(False)
			self.m_staticText7.Enable(False)
			self.m_button41.SetLabel('Remove Selected Files')

	def OnChangeMovingDir( self, event ):
	        dialog = wx.DirDialog(None, "Choose a directory for moving files there",
                	               style=wx.DD_DEFAULT_STYLE)
	        if dialog.ShowModal() == wx.ID_OK:
			self.m_staticText7.SetLabel(dialog.GetPath())
			self.parameters['RemovingOptionMovingDir']=dialog.GetPath()
	        dialog.Destroy() 
		event.Skip()

	def OnAddDirectory_Primary( self, event ):
	        dialog = wx.DirDialog(None, "Choose a directory",
                	               style=wx.DD_CHANGE_DIR)
	        if dialog.ShowModal() == wx.ID_OK:
			self.m_checkList2.Append(dialog.GetPath())
			self.parameters['DirDictPrimary'][dialog.GetPath()]=False
	        dialog.Destroy() 
	
	def OnAddDirectory_Secondary( self, event ):
	        dialog = wx.DirDialog(None, "Choose a directory",
                	               style=wx.DD_CHANGE_DIR)
	        if dialog.ShowModal() == wx.ID_OK:
			self.m_checkList3.Append(dialog.GetPath())
			self.parameters['DirDictSecondary'][dialog.GetPath()]=False
	        dialog.Destroy() 

	def OnRemoveDirectory_Primary( self, event ):
	        dialog = wx.MessageDialog(self, "Are you sure to remove all selected directories from the Primary Panel?", "Confirmation", wx.YES_NO | wx.ICON_INFORMATION)
	        if dialog.ShowModal() == wx.ID_YES:
			for i in xrange(self.m_checkList2.GetCount()):
				if self.m_checkList2.IsChecked(i):
					del self.parameters['DirDictPrimary'][self.m_checkList2.GetString(i)]
					self.m_checkList2.Delete(i)
	        dialog.Destroy() 
	
	def OnRemoveDirectory_Secondary( self, event ):
	        dialog = wx.MessageDialog(self, "Are you sure to remove all selected directories from the Secondary Panel?", "Confirmation", wx.YES_NO | wx.ICON_INFORMATION)
	        if dialog.ShowModal() == wx.ID_YES:
			for i in xrange(self.m_checkList3.GetCount()):
				if self.m_checkList3.IsChecked(i):
					del self.parameters['DirDictSecondary'][self.m_checkList3.GetString(i)]
					self.m_checkList3.Delete(i)
	        dialog.Destroy() 

	def OnAddExcludeDirectory_Primary( self, event ):
	        dialog = wx.DirDialog(None, "Choose a directory",
                	               style=wx.DD_CHANGE_DIR)
	        if dialog.ShowModal() == wx.ID_OK:
			self.m_checkList2.Append('EXCLUDED: '+dialog.GetPath())
			self.parameters['DirExcludeDictPrimary'][dialog.GetPath()]=False
	        dialog.Destroy() 
	
	def OnAddExcludeDirectory_Secondary( self, event ):
	        dialog = wx.DirDialog(None, "Choose a directory",
                	               style=wx.DD_CHANGE_DIR)
	        if dialog.ShowModal() == wx.ID_OK:
			self.m_checkList3.Append('EXCLUDED: '+dialog.GetPath())
			self.parameters['DirExcludeDictSecondary'][dialog.GetPath()]=False
	        dialog.Destroy() 




	def OnCheck_SecondaryFlag( self, event ):
		self.m_staticText21.Enable(self.m_checkBox_SecondaryFlag.IsChecked())
		self.m_checkList3.Enable(self.m_checkBox_SecondaryFlag.IsChecked())
		self.m_bpButton6.Enable(self.m_checkBox_SecondaryFlag.IsChecked())
		self.m_bpButton7.Enable(self.m_checkBox_SecondaryFlag.IsChecked())

	def OnCheckToggledDirsPrimary( self, event ):
		self.parameters['DirDictPrimary']={}
		for i in xrange(self.m_checkList2.GetCount()):
			self.parameters['DirDictPrimary'][self.m_checkList2.GetString(i)]=self.m_checkList2.IsChecked(i)

	def OnCheckToggledDirsSecondary( self, event ):
		self.parameters['DirDictSecondary']={}
		for i in xrange(self.m_checkList3.GetCount()):
			self.parameters['DirDictSecondary'][self.m_checkList3.GetString(i)]=self.m_checkList3.IsChecked(i)

	def OnCheck_CompFileNames( self, event ):
		self.parameters['CompareFileNames']=self.m_checkBox_CompFileNames.IsChecked()
	
	def OnCheck_BindDupl2Dir( self, event ):
		self.parameters['BindDupl2Dir']=self.m_checkBox_BindDupl2Dir.IsChecked()
	
	def OnCheck_CompFileDateTime( self, event ):
		self.parameters['m_checkBox_CompFileDateTime']=self.m_checkBox_CompFileDateTime.IsChecked()
	
	def OnCheck_CompFileHashes( self, event ):
		self.parameters['CompareFileHashes']=self.m_checkBox_CompFileHashes.IsChecked()
	
	def OnFrameClose( self, event ):
		self.SaveConfig()
		event.Skip()

	def LoadConfig( self ):
		self.m_statusBar1.SetStatusText('Loading Configuration ...',0)
		import os
		self.duplicatedfiledict={}
		self.duplicateddirdict={}
		self.parameters={}
		self.CfgFileFullName=os.path.dirname(os.path.realpath(__file__))+'\\'+'sff.cfg'
		try:
			f=open(self.CfgFileFullName,'r')
			self.parameters=eval(f.read())
			f.close()
		except:
			pass
		if self.parameters.has_key('CompareFileNames'): self.m_checkBox_CompFileNames.SetValue(self.parameters['CompareFileNames'])
		if self.parameters.has_key('BindDupl2Dir'): self.m_checkBox_BindDupl2Dir.SetValue(self.parameters['BindDupl2Dir'])
		if self.parameters.has_key('CompareFileDateTime'): self.m_checkBox_CompFileDateTime.SetValue(self.parameters['CompareFileDateTime'])
		if self.parameters.has_key('CompareFileHashes'): self.m_checkBox_CompFileHashes.SetValue(self.parameters['CompareFileHashes'])
		if self.parameters.has_key('SecondaryPanelFlag'):
			self.m_checkBox_SecondaryFlag.SetValue(self.parameters['SecondaryPanelFlag'])
			self.OnCheck_SecondaryFlag(None)

		self.m_checkList2.Clear()
		if self.parameters.has_key('DirDictPrimary'):
			for key, value in self.parameters['DirDictPrimary'].items():
				self.m_checkList2.Append(key)
				self.m_checkList2.Check(self.m_checkList2.GetCount()-1,value)
		else:
			self.parameters['DirDictPrimary']={}

		if self.parameters.has_key('DirExcludeDictPrimary'):
			for key, value in self.parameters['DirExcludeDictPrimary'].items():
				self.m_checkList2.Append('EXCLUDED: '+key)
				self.m_checkList2.Check(self.m_checkList2.GetCount()-1,value)
		else:
			self.parameters['DirExcludeDictPrimary']={}

		self.m_checkList3.Clear()
		if self.parameters.has_key('DirDictSecondary'):
			for key, value in self.parameters['DirDictSecondary'].items():
				self.m_checkList3.Append(key)
				self.m_checkList3.Check(self.m_checkList3.GetCount()-1,value)
		else:
			self.parameters['DirDictSecondary']={}
		if self.parameters.has_key('DirExcludeDictSecondary'):
			for key, value in self.parameters['DirExcludeDictSecondary'].items():
				self.m_checkList3.Append('EXCLUDED: '+key)
				self.m_checkList3.Check(self.m_checkList3.GetCount()-1,value)
		else:
			self.parameters['DirExcludeDictSecondary']={}


		if self.parameters.has_key('RemovingOption'):
			self.m_radioBox1.SetSelection(self.parameters['RemovingOption'])
		else:
			self.parameters['RemovingOption']=0
		self.OnRemovingOptions(None)
		if self.parameters.has_key('RemovingOptionMovingDir'):
			self.m_staticText7.SetLabel(self.parameters['RemovingOptionMovingDir'])
		else:
			self.parameters['RemovingOptionMovingDir']=''
		self.Update()
		self.m_statusBar1.SetStatusText('Loading Configuration finished',0)

	def SaveConfig( self ):
		import os
		self.parameters['CompareFileNames']=self.m_checkBox_CompFileNames.IsChecked()
		self.parameters['CompareFileDateTime']=self.m_checkBox_CompFileDateTime.IsChecked()
		self.parameters['CompareFileHashes']=self.m_checkBox_CompFileHashes.IsChecked()
		self.parameters['BindDupl2Dir']=self.m_checkBox_BindDupl2Dir.IsChecked()
		self.parameters['SecondaryPanelFlag']=self.m_checkBox_SecondaryFlag.GetValue()
		self.parameters['DirDictPrimary']={}
		for i in xrange(self.m_checkList2.GetCount()):
			if self.m_checkList2.GetString(i).find('EXCLUDED: ')<>0:
				self.parameters['DirDictPrimary'][self.m_checkList2.GetString(i)]=self.m_checkList2.IsChecked(i)
			else:
				self.parameters['DirExcludeDictPrimary'][self.m_checkList2.GetString(i).replace('EXCLUDED: ','')]=self.m_checkList2.IsChecked(i)
		self.parameters['DirDictSecondary']={}
		for i in xrange(self.m_checkList3.GetCount()):
			if self.m_checkList3.GetString(i).find('EXCLUDED: ')<>0:
				self.parameters['DirDictSecondary'][self.m_checkList3.GetString(i)]=self.m_checkList3.IsChecked(i)
			else:
				self.parameters['DirExcludeDictSecondary'][self.m_checkList3.GetString(i).replace('EXCLUDED: ','')]=self.m_checkList3.IsChecked(i)


		self.parameters['RemovingOption']=self.m_radioBox1.GetSelection()
		self.parameters['RemovingOptionMovingDir']=self.m_staticText7.GetLabel()

		f=open(self.CfgFileFullName,'w')
		f.write(str(self.parameters))
		f.close()

	def SelectAll( self, event ):
		for i in xrange(self.m_checkList1.GetCount()):
			self.m_checkList1.Check(i,True)
	
	def SelectNone( self, event ):
		for i in xrange(self.m_checkList1.GetCount()):
			self.m_checkList1.Check(i,False)
	
	def SelectInvert( self, event ):
		for i in xrange(self.m_checkList1.GetCount()):
			self.m_checkList1.Check(i,not (self.m_checkList1.IsChecked(i)))



	def gaugeStart(self, gaugeIndex, valueMax):
		self.gauge_max=valueMax
		if self.gauge_max>=2147483647.0:
			self.gauge_coef=2147483647.0/self.gauge_max
		else:
			self.gauge_coef=1
		self.m_gauge1.SetRange(self.gauge_max*self.gauge_coef)
		self.gauge_counter=0
		self.m_gauge1.SetValue(0)
		self.m_gauge1.Show()
		self.Layout()
		self.Update()
	
	def gaugeInc(self, gaugeIndex, valueInc):
		self.gauge_counter+=valueInc

	def gaugeUpd(self, gaugeIndex):
		self.m_gauge1.SetValue(self.gauge_counter*self.gauge_coef)
		wx.Yield()
		self.Update()

	def gaugeEnd(self, gaugeIndex):
		self.m_gauge1.Hide()
		self.m_gauge1.SetValue(0)
		wx.Yield()
#		self.Layout()
		self.Update()



	def GetFilesDictFromPath(self, path):
		import os
		import datetime
		filesdict={}
		for root, dirs, files in os.walk(path.decode('utf8')):
			for name in files:
				sz=os.stat('\\\\?\\'+root+'\\'+name).st_size
				mt=datetime.datetime.fromtimestamp(os.stat('\\\\?\\'+root+'\\'+name).st_mtime)
				filesdict[root+'\\'+name]={}
				filesdict[root+'\\'+name]['Name']=name
				filesdict[root+'\\'+name]['Directory']=root
				filesdict[root+'\\'+name]['Size']=sz
				filesdict[root+'\\'+name]['ModifyDateTime']=mt.strftime('%Y%m%d%H%M%S')
				filesdict[root+'\\'+name]['Hash']=''
		return filesdict

	def GetFileSHA256FromFilename(self, filename):
		import hashlib
		sha256=hashlib.sha256()
		f=open('\\\\?\\'+filename,'rb')
		while True:
			data=f.read(256)
			if not data: break
			sha256.update(data)
		f.close()
		return sha256.hexdigest()

	def GetFileMD5FromFilename(self, filename):
		import hashlib
		md5=hashlib.md5()
		f=open('\\\\?\\'+filename,'rb')
		while True:
			data=f.read(256)
			if not data: break
			md5.update(data)
		f.close()
		return md5.hexdigest()

	def SearchDuplicates( self, event ):
		import os
		import sys
		import datetime
		import send2trash
		import shutil

		self.m_statusBar1.SetStatusText('Search Duplicated Files started',0)

		try:
			os.stat('D:\\test_find_files_wx_debug_dir')
			send2trash.send2trash('D:\\test_find_files_wx_debug_dir')
			os.mkdir('D:\\test_find_files_wx_debug_dir')
		except:
			os.mkdir('D:\\test_find_files_wx_debug_dir')

		self.m_checkList1.Clear()
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 01'
		if len(self.m_checkList2.GetChecked())<=0:
			MyMessageBox=wx.MessageDialog(self,'No any PRIMARY Path is checked.','Error', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
			return None
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 02'
		if self.m_checkBox_SecondaryFlag.IsChecked() and len(self.m_checkList3.GetChecked())<=0:
			MyMessageBox=wx.MessageDialog(self,'No any SECONDARY Path is checked.','Error', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
			return None
		self.filesdict_primary={}
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 03'
		self.m_statusBar1.SetStatusText('Search Duplicated Files: build files list of primary part',0)
		self.Update()
		for key, value in self.parameters['DirDictPrimary'].items():
			if value:
				path=key
				self.filesdict_primary.update(self.GetFilesDictFromPath(path))
		self.m_statusBar1.SetStatusText('Search Duplicated Files: excluding files of primary part',0)
		self.Update()
		for ekey, evalue in self.parameters['DirExcludeDictPrimary'].items():
			if evalue:
				for key in self.filesdict_primary.keys():
					if key.find(ekey)==0: del self.filesdict_primary[key]

		f=open('D:\\test_find_files_wx_debug_dir\\self.filesdict_primary.dat','w')
		f.write(str(self.filesdict_primary))
		f.close()

		self.filesdict_secondary={}
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 04'
		if self.m_checkBox_SecondaryFlag.IsChecked():
			self.m_statusBar1.SetStatusText('Search Duplicated Files: build files list of secondary part',0)
			self.Update()
			for key, value in self.parameters['DirDictSecondary'].items():
				if value:
					path=key
					self.filesdict_secondary.update(self.GetFilesDictFromPath(path))
			self.m_statusBar1.SetStatusText('Search Duplicated Files: excluding files of secondary part',0)
			self.Update()
			for ekey, evalue in self.parameters['DirExcludeDictSecondary'].items():
				if evalue:
					for key in self.filesdict_secondary.keys():
						if key.find(ekey)==0: del self.filesdict_secondary[key]
		f=open('D:\\test_find_files_wx_debug_dir\\self.filesdict_secondary.dat','w')
		f.write(str(self.filesdict_secondary))
		f.close()

		self.duplicatedfiledict={}
		self.originalfiledict={}
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 05'

		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Started Sorting Primary List'
		self.m_statusBar1.SetStatusText('Search Duplicated Files: build additional files list of primary part',0)
		self.Update()
		self.filesdict_primary_keys=[]
		self.filesdict_primary_sizes=[]
		for key, value in self.filesdict_primary.items():
			self.filesdict_primary_keys.append(key)
			self.filesdict_primary_sizes.append(value['Size'])

		from operator import itemgetter
		self.m_statusBar1.SetStatusText('Search Duplicated Files: sort files list of primary part',0)
		self.Update()
		if len(self.filesdict_primary_sizes):
			self.filesdict_primary_sizes, self.filesdict_primary_keys = [list(x) for x in zip(*sorted(zip(self.filesdict_primary_sizes, self.filesdict_primary_keys), key=itemgetter(0)))]
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Finished Sorting Primary List'
		if self.m_checkBox_SecondaryFlag.IsChecked():
			print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Started Sorting Secondary List'
			self.m_statusBar1.SetStatusText('Search Duplicated Files: build additional files list of secondary part',0)
			self.Update()
			self.filesdict_secondary_keys=[]
			self.filesdict_secondary_sizes=[]
			for key, value in self.filesdict_secondary.items():
				self.filesdict_secondary_keys.append(key)
				self.filesdict_secondary_sizes.append(value['Size'])
			self.m_statusBar1.SetStatusText('Search Duplicated Files: sort files list of secondary part',0)
			self.Update()
			if len(self.filesdict_secondary_sizes):
				self.filesdict_secondary_sizes, self.filesdict_secondary_keys = [list(x) for x in zip(*sorted(zip(self.filesdict_secondary_sizes, self.filesdict_secondary_keys), key=itemgetter(0)))]
			print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Finished Sorting Secondary List'


		if self.m_checkBox_SecondaryFlag.IsChecked():
			self.m_statusBar1.SetStatusText('Search Duplicated Files: started comparing files in primary and secondary lists',0)
			print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 06'

			self.gaugeStart(1,len(self.filesdict_primary_sizes) * len(self.filesdict_secondary_sizes))
			for i in xrange(len(self.filesdict_primary_sizes)):
				self.gaugeUpd(1)
				for j in xrange(len(self.filesdict_secondary_sizes)):
					self.gaugeInc(1,1)
					if self.filesdict_secondary_sizes[j]>self.filesdict_primary_sizes[i]:
						self.gaugeInc(1,len(self.filesdict_secondary_sizes)-j-1)
						break
					if self.filesdict_secondary_sizes[j]<>self.filesdict_primary_sizes[i] or self.filesdict_secondary_keys[j]==self.filesdict_primary_keys[i] or self.filesdict_primary_keys[i] in self.originalfiledict.keys() or self.filesdict_secondary_keys[j] in self.duplicatedfiledict.keys(): continue
					if self.parameters['CompareFileNames']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Name']<>self.filesdict_secondary[self.filesdict_secondary_keys[j]]['Name']: continue
					if self.parameters['CompareFileDateTime']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['ModifyDateTime']<>self.filesdict_secondary[self.filesdict_secondary_keys[j]]['ModifyDateTime']: continue
					if self.parameters['CompareFileHashes']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Hash']=='': self.GetFileSHA256FromFilename(self.filesdict_primary_keys[i])
						if self.filesdict_secondary[self.filesdict_secondary_keys[j]]['Hash']=='': self.GetFileSHA256FromFilename(self.filesdict_secondary_keys[j])
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Hash']<>self.filesdict_secondary[self.filesdict_secondary_keys[j]]['Hash']: continue
					self.duplicatedfiledict[self.filesdict_secondary_keys[j]]=self.filesdict_secondary[self.filesdict_secondary_keys[j]]
					self.duplicatedfiledict[self.filesdict_secondary_keys[j]]['DuplicatedOf']=self.filesdict_primary_keys[i]
					self.originalfiledict[self.filesdict_primary_keys[i]]=self.filesdict_primary[self.filesdict_primary_keys[i]]
			self.m_statusBar1.SetStatusText('Search Duplicated Files: finished comparing files in primary and secondary lists',0)
		else:
			self.m_statusBar1.SetStatusText('Search Duplicated Files: started comparing files in primary list',0)
			print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 07'
			self.gaugeStart(1,len(self.filesdict_primary_sizes) * len(self.filesdict_primary_sizes))
			for i in xrange(len(self.filesdict_primary_sizes)):
				self.gaugeUpd(1)
				for j in xrange(len(self.filesdict_primary_sizes)):
					self.gaugeInc(1,1)
					if self.filesdict_primary_sizes[j]>self.filesdict_primary_sizes[i]:
						self.gaugeInc(1,len(self.filesdict_primary_sizes)-j-1)
						break
					if self.filesdict_primary_sizes[j]<>self.filesdict_primary_sizes[i] or self.filesdict_primary_keys[j]==self.filesdict_primary_keys[i] or self.filesdict_primary_keys[i] in self.originalfiledict.keys() or self.filesdict_primary_keys[j] in self.duplicatedfiledict.keys(): continue
					if self.parameters['CompareFileNames']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Name']<>self.filesdict_primary[self.filesdict_primary_keys[j]]['Name']: continue
					if self.parameters['CompareFileDateTime']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['ModifyDateTime']<>self.filesdict_primary[self.filesdict_primary_keys[j]]['ModifyDateTime']: continue
					if self.parameters['CompareFileHashes']:
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Hash']=='': self.GetFileSHA256FromFilename(self.filesdict_primary_keys[i])
						if self.filesdict_primary[self.filesdict_primary_keys[i]]['Hash']<>self.filesdict_primary[self.filesdict_primary_keys[j]]['Hash']: continue
					self.duplicatedfiledict[self.filesdict_primary_keys[j]]=self.filesdict_primary[self.filesdict_primary_keys[j]]
					self.duplicatedfiledict[self.filesdict_primary_keys[j]]['DuplicatedOf']=self.filesdict_primary_keys[i]
					self.originalfiledict[self.filesdict_primary_keys[i]]=self.filesdict_primary[self.filesdict_primary_keys[i]]
			self.m_statusBar1.SetStatusText('Search Duplicated Files: finished comparing files in primary list',0)


		self.gaugeEnd(1)

		f=open('D:\\test_find_files_wx_debug_dir\\self.duplicatedfiledict.dat','w')
		f.write(str(self.duplicatedfiledict))
		f.close()
		f=open('D:\\test_find_files_wx_debug_dir\\self.originalfiledict.dat','w')
		f.write(str(self.originalfiledict))
		f.close()

		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 08'
		self.allfilesdict=self.filesdict_primary
		self.allfilesdict.update(self.filesdict_secondary)
		f=open('D:\\test_find_files_wx_debug_dir\\self.allfilesdict.dat','w')
		f.write(str(self.allfilesdict))
		f.close()

		self.duplicateddirdict={}
		if self.parameters['BindDupl2Dir']:
			self.m_statusBar1.SetStatusText('Search Duplicated Files: started binding duplicated files to mutual directories',0)
			print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 09'
			self.gaugeStart(1,len(self.duplicatedfiledict.keys()))
#			dupl_dir_index=0
			for key in self.duplicatedfiledict.keys():
				self.gaugeUpd(1)
				self.gaugeInc(1,1)
				already_processed=False
				for keydir in self.duplicateddirdict.keys():
					if keydir in '\\'.join(key.split('\\')[:-1]): already_processed=True
				if already_processed: continue
				dirname=self.CheckDuplicateDirectories('\\'.join(key.split('\\')[:-1]))
				if dirname<>'':
#					dupl_dir_index+=1
					self.duplicateddirdict[dirname]=''
#					stemp=dirname.split('\\')[-1]
#					stemp='D:\\test_find_files_wx_debug_dir\\dir_'+str(dupl_dir_index).rjust(3,'0')+'_'+stemp.replace(':','_DISK')
#					try:
#						os.stat(stemp)
#						send2trash.send2trash(stemp)
#						os.mkdir(stemp)
#					except:
#						os.mkdir(stemp)
					for key in self.duplicatedfiledict.keys():
						if dirname in key:
#							if dupl_dir_index<=4: shutil.copy(self.duplicatedfiledict[key]['DuplicatedOf'],stemp+'\\')
							del self.duplicatedfiledict[key]
			self.m_statusBar1.SetStatusText('Search Duplicated Files: finished binding duplicated files to mutual directories',0)
			
			self.gaugeEnd(1)

		f=open('D:\\test_find_files_wx_debug_dir\\self.duplicateddirdict.dat','w')
		f.write(str(self.duplicateddirdict))
		f.close()
		f=open('D:\\test_find_files_wx_debug_dir\\self.duplicatedfiledict2.dat','w')
		f.write(str(self.duplicatedfiledict))
		f.close()

		self.m_statusBar1.SetStatusText('Search Duplicated Files: started loading duplicated files list on form',0)
		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 10'

		self.gaugeStart(1,len(self.duplicatedfiledict.keys()))
		for key, value in self.duplicatedfiledict.items():
			self.gaugeUpd(1)
			self.gaugeInc(1,1)
			self.m_checkList1.Append('FILE: '+key+'|'+str(value['Size'])+'|'+value['ModifyDateTime']+'|'+value['Hash']+'| duplicated of '+value['DuplicatedOf'])
			self.Update()

		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 11'
		self.gaugeStart(1,len(self.duplicateddirdict.keys()))
		for key in self.duplicateddirdict.keys():
			self.gaugeUpd(1)
			self.gaugeInc(1,1)
			self.m_checkList1.Append('DIR: '+key)
			self.Update()
		self.m_statusBar1.SetStatusText('Search Duplicated Files: finished loading duplicated files list on form',0)

		self.gaugeEnd(1)

		print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' *** Debug 12'
		self.m_statusBar1.SetStatusText('Search Duplicated Files finished',0)
		MyMessageBox=wx.MessageDialog(self,'Duplicated Files search finished.','Message', wx.OK | wx.ICON_INFORMATION)
		MyMessageBox.ShowModal()
		self.m_statusBar1.SetStatusText('',0)


	def CheckDuplicateDirectories( self, dirname ):
#		return ''
		result=dirname
		for key in self.allfilesdict.keys():
			if dirname in '\\'.join(key.split('\\')[:-1]) and not key in self.duplicatedfiledict.keys():
				result=''
				break
		if '\\' in result:
			dirname2=self.CheckDuplicateDirectories('\\'.join(result.split('\\')[:-1]))
		else:
			dirname2=''
		if dirname2<>'':
			return dirname2
		else:
			return result

	
	def RemoveSelectedFiles( self, event ):
		if len(self.m_checkList1.GetChecked())<=0: return
		import os
		import send2trash
		import shutil
		import datetime
		MessageText='Are you sure to remove all selected files and directories'
		if self.parameters['RemovingOption']==0:
			MessageText=MessageText+' to Recycle Bin?'
			MessageTextConf='All files and directories removed to Recycle Bin sucessfully.'
		if self.parameters['RemovingOption']==1:
			MessageText=MessageText+' PERMANENTLY?'
			MessageTextConf='All files and directories removed PERMANENTLY sucessfully.'
		if self.parameters['RemovingOption']>=2:
			MovedDir=self.parameters['RemovingOptionMovingDir']+'\\MOVED_'+datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
			MessageText='Are you sure to move all selected files and directories'+' to "'+self.parameters['RemovingOptionMovingDir']+'" directory?'
			MessageTextConf='All files and directories moved to "'+MovedDir+'" directory sucessfully.'

	        dialog = wx.MessageDialog(self, MessageText, "Confirmation", wx.YES_NO | wx.ICON_INFORMATION)
	        if dialog.ShowModal() == wx.ID_YES:
			for i in xrange(self.m_checkList1.GetCount()):
				if self.m_checkList1.IsChecked(i):
					stemp2=self.m_checkList1.GetString(i)
					if 'DIR: ' in self.m_checkList1.GetString(i):
						stemp=self.m_checkList1.GetString(i).replace('DIR: ','')
						del self.duplicateddirdict[stemp]
					else:
						if 'FILE: ' in self.m_checkList1.GetString(i):
							stemp=self.m_checkList1.GetString(i).split('|')[0].replace('FILE: ','')
							del self.duplicatedfiledict[stemp]
					if self.parameters['RemovingOption']==0:
						try:
							os.stat(stemp)
							send2trash.send2trash(stemp)
						except:
							pass
					if self.parameters['RemovingOption']==1:
						if 'DIR: ' in stemp2:
							try:
								os.stat(stemp)
								shutil.rmtree(stemp)
							except:
								pass
						if 'FILE: ' in stemp2:
							try:
								os.stat(stemp)
								os.remove(stemp)
							except:
								pass
					if self.parameters['RemovingOption']>=2:
						try:
							os.stat(MovedDir)
						except:
							os.mkdir(MovedDir)
						try:
							os.stat(stemp)
							shutil.move(stemp,MovedDir+'\\')
						except:
							pass

			self.m_checkList1.Clear()
			for key, value in self.duplicatedfiledict.items():
				self.m_checkList1.Append('FILE: '+key+'|'+str(value['Size'])+'|'+value['ModifyDateTime']+'|'+value['Hash']+'| duplicated of '+value['DuplicatedOf'])
				self.Update()
			for key in self.duplicateddirdict.keys():
				self.m_checkList1.Append('DIR: '+key)
				self.Update()
			MyMessageBox=wx.MessageDialog(self,MessageTextConf,'Message', wx.OK | wx.ICON_INFORMATION)
			MyMessageBox.ShowModal()
	        dialog.Destroy() 
	
	

app=wx.App(False)
frame=MyFrame1(None)
frame.Show(True)
app.MainLoop()
