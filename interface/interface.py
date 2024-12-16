# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from interface.video_view import VideoView
from interface.figure_panel import Figure_Panel
import wx
import wx.xrc
import wx.aui
import wx.grid

###########################################################################
## Class Main_Frame
###########################################################################

class Main_Frame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1165,900 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )

		self.m_menubar2 = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.m_menubar2.Append( self.file_menu, u"File" )

		self.camera_menu = wx.Menu()
		self.m_menubar2.Append( self.camera_menu, u"Camera" )

		self.help_menu = wx.Menu()
		self.m_menubar2.Append( self.help_menu, u"Help" )

		self.SetMenuBar( self.m_menubar2 )

		self.statusbar = self.CreateStatusBar( 4, wx.STB_SIZEGRIP, wx.ID_ANY )
		fgSizer6 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer6.AddGrowableCol( 0, 1 )
		fgSizer6.AddGrowableRow( 0, 2 )
		fgSizer6.AddGrowableRow( 1, 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer16 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer16.AddGrowableCol( 0, 100 )
		fgSizer16.AddGrowableCol( 1, 1 )
		fgSizer16.AddGrowableRow( 0, 1 )
		fgSizer16.SetFlexibleDirection( wx.VERTICAL )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer16.SetMinSize( wx.Size( 640,400 ) )
		self.camera_notebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.cam_one_panel = wx.Panel( self.camera_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer43 = wx.BoxSizer( wx.VERTICAL )

		self.video_panel1 = VideoView( self.cam_one_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer43.Add( self.video_panel1, 1, wx.EXPAND|wx.ALL, 5 )

		self.m_toolBar5 = wx.ToolBar( self.cam_one_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.start_btn1 = self.m_toolBar5.AddTool( wx.ID_ANY, u"Start Camera", wx.Bitmap( u"interface/icons/24px/003-play-button.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.scrshot_btn1 = self.m_toolBar5.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"interface/icons/24px/007-camera.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.vid_btn1 = self.m_toolBar5.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"interface/icons/24px/002-camera.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.setting_btn1 = self.m_toolBar5.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"interface/icons/24px/008-gear.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_toolBar5.AddSeparator()

		self.min_max_disp = wx.StaticText( self.m_toolBar5, wx.ID_ANY, u"Min: Max: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.min_max_disp.Wrap( -1 )

		self.m_toolBar5.AddControl( self.min_max_disp )
		self.m_toolBar5.Realize()

		bSizer43.Add( self.m_toolBar5, 0, wx.EXPAND, 5 )


		self.cam_one_panel.SetSizer( bSizer43 )
		self.cam_one_panel.Layout()
		bSizer43.Fit( self.cam_one_panel )
		self.camera_notebook.AddPage( self.cam_one_panel, u"Camera One", False, wx.NullBitmap )

		fgSizer16.Add( self.camera_notebook, 1, wx.EXPAND |wx.ALL, 5 )

		self.settings_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_RIGHT )
		self.settings_notebook.SetMinSize( wx.Size( 330,-1 ) )
		self.settings_notebook.SetMaxSize( wx.Size( 330,-1 ) )

		self.stage_set_page = wx.Panel( self.settings_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel25 = wx.Panel( self.stage_set_page, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel25.SetMinSize( wx.Size( 300,-1 ) )
		self.m_panel25.SetMaxSize( wx.Size( 300,-1 ) )

		bSizer511 = wx.BoxSizer( wx.VERTICAL )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		bSizer172 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText32 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Fine control", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		bSizer172.Add( self.m_staticText32, 0, 0, 5 )


		bSizer15.Add( bSizer172, 0, 0, 5 )

		bSizer49 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText46 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Travel to (X, Y, Z) [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )

		bSizer49.Add( self.m_staticText46, 0, wx.ALL, 5 )

		bSizer50 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText48 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"(", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText48.Wrap( -1 )

		bSizer50.Add( self.m_staticText48, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.x_field = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer50.Add( self.x_field, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText49 = wx.StaticText( self.m_panel25, wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )

		bSizer50.Add( self.m_staticText49, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.y_field = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer50.Add( self.y_field, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText50 = wx.StaticText( self.m_panel25, wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )

		bSizer50.Add( self.m_staticText50, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.z_field = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer50.Add( self.z_field, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText51 = wx.StaticText( self.m_panel25, wx.ID_ANY, u")", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		bSizer50.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer50.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.travel_btn = wx.Button( self.m_panel25, wx.ID_ANY, u"Go!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer50.Add( self.travel_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer49.Add( bSizer50, 1, wx.EXPAND, 5 )


		bSizer15.Add( bSizer49, 0, wx.EXPAND, 5 )

		bSizer48 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText42 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Step size [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		bSizer48.Add( self.m_staticText42, 0, wx.ALL, 5 )

		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer29 = wx.BoxSizer( wx.VERTICAL )


		bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText52 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"XY: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )

		bSizer29.Add( self.m_staticText52, 0, wx.ALL, 5 )

		self.m_staticText521 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Z: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText521.Wrap( -1 )

		bSizer29.Add( self.m_staticText521, 0, wx.ALL, 5 )


		bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer51.Add( bSizer29, 1, wx.EXPAND, 5 )

		bSizer291 = wx.BoxSizer( wx.VERTICAL )

		self.xy_step_size = wx.SpinCtrlDouble( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0.01, 100, 1, 1 )
		self.xy_step_size.SetDigits( 2 )
		bSizer291.Add( self.xy_step_size, 1, wx.ALL, 5 )

		self.z_step_size = wx.SpinCtrlDouble( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0.01, 100, 0.010000, 1 )
		self.z_step_size.SetDigits( 2 )
		bSizer291.Add( self.z_step_size, 1, wx.ALL, 5 )


		bSizer51.Add( bSizer291, 1, wx.EXPAND, 5 )

		bSizer35 = wx.BoxSizer( wx.VERTICAL )

		self.dxy_frac = wx.Button( self.m_panel25, wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer35.Add( self.dxy_frac, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dz_frac = wx.Button( self.m_panel25, wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer35.Add( self.dz_frac, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer51.Add( bSizer35, 1, wx.EXPAND, 5 )

		bSizer351 = wx.BoxSizer( wx.VERTICAL )

		self.dxy_sngl = wx.Button( self.m_panel25, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer351.Add( self.dxy_sngl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dz_sngl = wx.Button( self.m_panel25, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer351.Add( self.dz_sngl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer51.Add( bSizer351, 1, wx.EXPAND, 5 )

		bSizer352 = wx.BoxSizer( wx.VERTICAL )

		self.dxy_dec = wx.Button( self.m_panel25, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer352.Add( self.dxy_dec, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dz_dec = wx.Button( self.m_panel25, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer352.Add( self.dz_dec, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer51.Add( bSizer352, 1, wx.EXPAND, 5 )

		bSizer353 = wx.BoxSizer( wx.VERTICAL )

		self.dxy_huge = wx.Button( self.m_panel25, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer353.Add( self.dxy_huge, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dz_huge = wx.Button( self.m_panel25, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer353.Add( self.dz_huge, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer51.Add( bSizer353, 1, wx.EXPAND, 5 )


		bSizer48.Add( bSizer51, 1, wx.EXPAND, 5 )


		bSizer15.Add( bSizer48, 0, wx.EXPAND, 5 )


		bSizer511.Add( bSizer15, 0, wx.EXPAND, 5 )

		fgSizer19 = wx.FlexGridSizer( 2, 5, 0, 0 )
		fgSizer19.AddGrowableCol( 0, 1 )
		fgSizer19.AddGrowableCol( 1, 1 )
		fgSizer19.AddGrowableCol( 2, 1 )
		fgSizer19.AddGrowableCol( 3, 1 )
		fgSizer19.AddGrowableCol( 4, 100 )
		fgSizer19.AddGrowableRow( 0, 1 )
		fgSizer19.AddGrowableRow( 1, 1 )
		fgSizer19.SetFlexibleDirection( wx.BOTH )
		fgSizer19.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.hidden_m_button64 = wx.Button( self.m_panel25, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		self.hidden_m_button64.Hide()

		fgSizer19.Add( self.hidden_m_button64, 0, wx.ALL, 5 )

		self.x_up_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.x_up_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/001-up-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.x_up_btn, 0, wx.ALL, 5 )

		self.hidden_m_button648 = wx.Button( self.m_panel25, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		self.hidden_m_button648.Hide()

		fgSizer19.Add( self.hidden_m_button648, 0, wx.ALL, 5 )

		self.z_up_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.z_up_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/001-up-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.z_up_btn, 0, wx.ALL, 5 )


		fgSizer19.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.y_left_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )

		self.y_left_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/002-left-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.y_left_btn, 0, wx.ALL, 5 )

		self.x_down_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.x_down_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/004-down-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.x_down_btn, 0, wx.ALL, 5 )

		self.y_right_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )

		self.y_right_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/003-right-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.y_right_btn, 0, wx.ALL, 5 )

		self.z_down_btn = wx.Button( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.z_down_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/004-down-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer19.Add( self.z_down_btn, 0, wx.ALL, 5 )


		fgSizer19.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer511.Add( fgSizer19, 0, wx.EXPAND, 5 )

		bSizer432 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer44 = wx.BoxSizer( wx.VERTICAL )

		self.home_coord_txt2 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Home [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.home_coord_txt2.Wrap( -1 )

		bSizer44.Add( self.home_coord_txt2, 0, 0, 5 )

		self.home_coord_txt = wx.StaticText( self.m_panel25, wx.ID_ANY, u"( 0.0,  0.0,  0.0)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.home_coord_txt.Wrap( -1 )

		bSizer44.Add( self.home_coord_txt, 0, 0, 5 )


		bSizer432.Add( bSizer44, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer432.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer451 = wx.BoxSizer( wx.VERTICAL )

		self.set_home_btn = wx.Button( self.m_panel25, wx.ID_ANY, u"Set Home", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer451.Add( self.set_home_btn, 0, wx.ALIGN_RIGHT, 5 )

		self.rtrn_home_btn = wx.Button( self.m_panel25, wx.ID_ANY, u"Return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rtrn_home_btn.Enable( False )

		bSizer451.Add( self.rtrn_home_btn, 0, wx.ALIGN_RIGHT, 5 )


		bSizer432.Add( bSizer451, 1, wx.EXPAND, 5 )


		bSizer511.Add( bSizer432, 0, wx.EXPAND, 5 )


		self.m_panel25.SetSizer( bSizer511 )
		self.m_panel25.Layout()
		bSizer511.Fit( self.m_panel25 )
		bSizer13.Add( self.m_panel25, 0, wx.EXPAND, 5 )

		self.m_collapsiblePane1 = wx.CollapsiblePane( self.stage_set_page, wx.ID_ANY, u"Coarse control", wx.DefaultPosition, wx.Size( 300,-1 ), wx.CP_DEFAULT_STYLE )
		self.m_collapsiblePane1.Collapse( True )

		self.m_collapsiblePane1.SetMinSize( wx.Size( 300,-1 ) )
		self.m_collapsiblePane1.SetMaxSize( wx.Size( 300,-1 ) )

		bSizer5111 = wx.BoxSizer( wx.VERTICAL )

		bSizer151 = wx.BoxSizer( wx.VERTICAL )

		bSizer482 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText421 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Step size [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText421.Wrap( -1 )

		bSizer482.Add( self.m_staticText421, 0, wx.ALL, 5 )

		bSizer512 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer292 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5211 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Z: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5211.Wrap( -1 )

		bSizer292.Add( self.m_staticText5211, 0, wx.ALL, 5 )


		bSizer512.Add( bSizer292, 1, wx.EXPAND, 5 )

		bSizer2911 = wx.BoxSizer( wx.VERTICAL )

		self.z_step_size_coar = wx.SpinCtrlDouble( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0.01, 2e+06, 1.000000, 1 )
		self.z_step_size_coar.SetDigits( 2 )
		bSizer2911.Add( self.z_step_size_coar, 0, wx.ALL, 5 )


		bSizer512.Add( bSizer2911, 1, wx.EXPAND, 5 )

		bSizer355 = wx.BoxSizer( wx.VERTICAL )

		self.dz_frac_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"0.5", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer355.Add( self.dz_frac_coar, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer512.Add( bSizer355, 1, wx.EXPAND, 5 )

		bSizer3511 = wx.BoxSizer( wx.VERTICAL )

		self.dz_sngl_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer3511.Add( self.dz_sngl_coar, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer512.Add( bSizer3511, 1, wx.EXPAND, 5 )

		bSizer3521 = wx.BoxSizer( wx.VERTICAL )

		self.dz_dec_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer3521.Add( self.dz_dec_coar, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer512.Add( bSizer3521, 1, wx.EXPAND, 5 )

		bSizer3531 = wx.BoxSizer( wx.VERTICAL )

		self.dz_huge_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 28,-1 ), 0 )
		bSizer3531.Add( self.dz_huge_coar, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer512.Add( bSizer3531, 1, wx.EXPAND, 5 )


		bSizer482.Add( bSizer512, 1, wx.EXPAND, 5 )


		bSizer151.Add( bSizer482, 0, wx.EXPAND, 5 )

		bSizer491 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText461 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Travel to (X, Y, Z) [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText461.Wrap( -1 )

		self.m_staticText461.Hide()

		bSizer491.Add( self.m_staticText461, 0, wx.ALL, 5 )

		bSizer501 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText481 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"(", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText481.Wrap( -1 )

		self.m_staticText481.Hide()

		bSizer501.Add( self.m_staticText481, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.x_field1 = wx.TextCtrl( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self.x_field1.Enable( False )
		self.x_field1.Hide()

		bSizer501.Add( self.x_field1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText491 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText491.Wrap( -1 )

		self.m_staticText491.Hide()

		bSizer501.Add( self.m_staticText491, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.y_field1 = wx.TextCtrl( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self.y_field1.Enable( False )
		self.y_field1.Hide()

		bSizer501.Add( self.y_field1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText501 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText501.Wrap( -1 )

		self.m_staticText501.Hide()

		bSizer501.Add( self.m_staticText501, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.z_field_coar = wx.TextCtrl( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self.z_field_coar.Hide()

		bSizer501.Add( self.z_field_coar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText511 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u")", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )

		self.m_staticText511.Hide()

		bSizer501.Add( self.m_staticText511, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer501.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.travel_btn_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Go!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.travel_btn_coar.Hide()

		bSizer501.Add( self.travel_btn_coar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer491.Add( bSizer501, 1, wx.EXPAND, 5 )


		bSizer151.Add( bSizer491, 0, wx.EXPAND, 5 )


		bSizer5111.Add( bSizer151, 0, wx.EXPAND, 5 )

		fgSizer192 = wx.FlexGridSizer( 2, 5, 0, 0 )
		fgSizer192.AddGrowableCol( 0, 1 )
		fgSizer192.AddGrowableCol( 1, 1 )
		fgSizer192.AddGrowableCol( 2, 1 )
		fgSizer192.AddGrowableCol( 3, 1 )
		fgSizer192.AddGrowableCol( 4, 100 )
		fgSizer192.AddGrowableRow( 0, 1 )
		fgSizer192.AddGrowableRow( 1, 1 )
		fgSizer192.SetFlexibleDirection( wx.BOTH )
		fgSizer192.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText125 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"LServo:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText125.Wrap( -1 )

		fgSizer192.Add( self.m_staticText125, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.ls_up_btn = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.ls_up_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/001-up-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer192.Add( self.ls_up_btn, 0, wx.ALL, 5 )

		self.m_staticText124 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"RServo:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText124.Wrap( -1 )

		fgSizer192.Add( self.m_staticText124, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.rs_up_btn = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.rs_up_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/001-up-arrow.png", wx.BITMAP_TYPE_ANY ) )
		self.rs_up_btn.Enable( False )

		fgSizer192.Add( self.rs_up_btn, 0, wx.ALL, 5 )

		self.m_checkBox8 = wx.CheckBox( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Sync", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox8.SetValue(True)
		fgSizer192.Add( self.m_checkBox8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer192.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.ls_down_btn = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.ls_down_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/004-down-arrow.png", wx.BITMAP_TYPE_ANY ) )
		fgSizer192.Add( self.ls_down_btn, 0, wx.ALL, 5 )

		self.y_right_btn2 = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )

		self.y_right_btn2.SetBitmap( wx.Bitmap( u"interface/icons/24px/003-right-arrow.png", wx.BITMAP_TYPE_ANY ) )
		self.y_right_btn2.Hide()

		fgSizer192.Add( self.y_right_btn2, 0, wx.ALL, 5 )

		self.rs_down_btn = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )

		self.rs_down_btn.SetBitmap( wx.Bitmap( u"interface/icons/24px/004-down-arrow.png", wx.BITMAP_TYPE_ANY ) )
		self.rs_down_btn.Enable( False )

		fgSizer192.Add( self.rs_down_btn, 0, wx.ALL, 5 )


		fgSizer192.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer5111.Add( fgSizer192, 0, wx.EXPAND, 5 )

		bSizer4322 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer442 = wx.BoxSizer( wx.VERTICAL )

		self.home_coord_txt22 = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Set Point [um]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.home_coord_txt22.Wrap( -1 )

		bSizer442.Add( self.home_coord_txt22, 0, 0, 5 )

		self.home_coord_txt_coar = wx.StaticText( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"( 0.0,  0.0,  0.0)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.home_coord_txt_coar.Wrap( -1 )

		bSizer442.Add( self.home_coord_txt_coar, 0, 0, 5 )


		bSizer4322.Add( bSizer442, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4322.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer4512 = wx.BoxSizer( wx.VERTICAL )

		self.set_home_btn_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4512.Add( self.set_home_btn_coar, 0, wx.ALIGN_RIGHT, 5 )

		self.rtrn_home_btn_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rtrn_home_btn_coar.Enable( False )

		bSizer4512.Add( self.rtrn_home_btn_coar, 0, wx.ALIGN_RIGHT, 5 )


		bSizer4322.Add( bSizer4512, 1, wx.EXPAND, 5 )


		bSizer5111.Add( bSizer4322, 0, wx.EXPAND, 5 )

		self.m_staticline4 = wx.StaticLine( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5111.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer58 = wx.BoxSizer( wx.VERTICAL )

		self.go_home_btn_coar = wx.Button( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, u"Home", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer58.Add( self.go_home_btn_coar, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer5111.Add( bSizer58, 1, wx.EXPAND, 5 )


		self.m_collapsiblePane1.GetPane().SetSizer( bSizer5111 )
		self.m_collapsiblePane1.GetPane().Layout()
		bSizer13.Add( self.m_collapsiblePane1, 1, wx.EXPAND |wx.ALL, 5 )


		self.stage_set_page.SetSizer( bSizer13 )
		self.stage_set_page.Layout()
		bSizer13.Fit( self.stage_set_page )
		self.settings_notebook.AddPage( self.stage_set_page, u"Stage", False )
		self.lockin_setting = wx.Panel( self.settings_notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer131 = wx.BoxSizer( wx.VERTICAL )

		self.lock_param_grid = wx.grid.Grid( self.lockin_setting, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )

		# Grid
		self.lock_param_grid.CreateGrid( 14, 1 )
		self.lock_param_grid.EnableEditing( True )
		self.lock_param_grid.EnableGridLines( True )
		self.lock_param_grid.EnableDragGridSize( False )
		self.lock_param_grid.SetMargins( 0, 0 )

		# Columns
		self.lock_param_grid.SetColSize( 0, 140 )
		self.lock_param_grid.EnableDragColMove( False )
		self.lock_param_grid.EnableDragColSize( False )
		self.lock_param_grid.SetColLabelSize( 0 )
		self.lock_param_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.lock_param_grid.SetRowSize( 0, 0 )
		self.lock_param_grid.AutoSizeRows()
		self.lock_param_grid.EnableDragRowSize( False )
		self.lock_param_grid.SetRowLabelValue( 0, u" " )
		self.lock_param_grid.SetRowLabelValue( 1, u"Reference range [um]" )
		self.lock_param_grid.SetRowLabelValue( 2, u"Reference step size [um]" )
		self.lock_param_grid.SetRowLabelValue( 3, u"Mode" )
		self.lock_param_grid.SetRowLabelValue( 4, u"Axis" )
		self.lock_param_grid.SetRowLabelValue( 5, u"Move amplitude [um]" )
		self.lock_param_grid.SetRowLabelValue( 6, u"Move time" )
		self.lock_param_grid.SetRowLabelValue( 7, u"Peak fit" )
		self.lock_param_grid.SetRowLabelValue( 8, u"Sample lock active axes" )
		self.lock_param_grid.SetRowLabelValue( 9, u"Scale factors" )
		self.lock_param_grid.SetRowLabelValue( 10, u"Settling time [s]" )
		self.lock_param_grid.SetRowLabelValue( 11, u"k_P" )
		self.lock_param_grid.SetRowLabelValue( 12, u"k_I" )
		self.lock_param_grid.SetRowLabelValue( 13, u"k_I2" )
		self.lock_param_grid.SetRowLabelSize( wx.grid.GRID_AUTOSIZE )
		self.lock_param_grid.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.lock_param_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )
		self.lock_param_grid.SetMinSize( wx.Size( 300,275 ) )

		bSizer131.Add( self.lock_param_grid, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer401 = wx.BoxSizer( wx.VERTICAL )

		bSizer38 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText89 = wx.StaticText( self.lockin_setting, wx.ID_ANY, u"Load setup:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText89.Wrap( -1 )

		bSizer38.Add( self.m_staticText89, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lock_stp_load_file = wx.FilePickerCtrl( self.lockin_setting, wx.ID_ANY, wx.EmptyString, u"Select a file", u"TXT files (*.txt)|*.txt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN )
		bSizer38.Add( self.lock_stp_load_file, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer401.Add( bSizer38, 0, wx.EXPAND, 5 )

		bSizer391 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText90 = wx.StaticText( self.lockin_setting, wx.ID_ANY, u"Save setup:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )

		bSizer391.Add( self.m_staticText90, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.lock_stp_save_file = wx.FilePickerCtrl( self.lockin_setting, wx.ID_ANY, wx.EmptyString, u"Select a file", u"TXT files (*.txt)|*.txt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		bSizer391.Add( self.lock_stp_save_file, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer401.Add( bSizer391, 0, wx.EXPAND, 5 )


		bSizer131.Add( bSizer401, 0, wx.EXPAND, 5 )

		bSizer361 = wx.BoxSizer( wx.VERTICAL )

		bSizer39 = wx.BoxSizer( wx.VERTICAL )

		bSizer40 = wx.BoxSizer( wx.HORIZONTAL )

		self.save_sl_data = wx.CheckBox( self.lockin_setting, wx.ID_ANY, u"Save data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer40.Add( self.save_sl_data, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		bSizer40.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		writing_modes_listChoices = [ u"new file", u"override", u"append" ]
		self.writing_modes_list = wx.Choice( self.lockin_setting, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, writing_modes_listChoices, 0 )
		self.writing_modes_list.SetSelection( 2 )
		self.writing_modes_list.Enable( False )
		self.writing_modes_list.Hide()

		bSizer40.Add( self.writing_modes_list, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		bSizer39.Add( bSizer40, 0, wx.EXPAND, 5 )

		bSizer481 = wx.BoxSizer( wx.HORIZONTAL )

		self.save_frm_sl = wx.CheckBox( self.lockin_setting, wx.ID_ANY, u"Save frames", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer481.Add( self.save_frm_sl, 0, wx.RIGHT|wx.LEFT, 5 )

		self.m_checkBox4 = wx.CheckBox( self.lockin_setting, wx.ID_ANY, u"Save params", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer481.Add( self.m_checkBox4, 0, wx.RIGHT|wx.LEFT, 5 )


		bSizer39.Add( bSizer481, 1, wx.EXPAND, 5 )

		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText27 = wx.StaticText( self.lockin_setting, wx.ID_ANY, u"Number of points per redraw:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		bSizer42.Add( self.m_staticText27, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.n_points = wx.SpinCtrl( self.lockin_setting, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 1 )
		bSizer42.Add( self.n_points, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		bSizer39.Add( bSizer42, 0, wx.EXPAND, 5 )

		bSizer421 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText271 = wx.StaticText( self.lockin_setting, wx.ID_ANY, u"Number of points to print:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText271.Wrap( -1 )

		bSizer421.Add( self.m_staticText271, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.data_n_points = wx.SpinCtrl( self.lockin_setting, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 100 )
		bSizer421.Add( self.data_n_points, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		bSizer39.Add( bSizer421, 0, wx.EXPAND, 5 )


		bSizer39.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer361.Add( bSizer39, 1, wx.EXPAND, 5 )


		bSizer131.Add( bSizer361, 0, wx.EXPAND, 5 )

		bSizer354 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText26 = wx.StaticText( self.lockin_setting, wx.ID_ANY, u"Working directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		bSizer354.Add( self.m_staticText26, 0, wx.ALL, 5 )

		self.working_dir = wx.DirPickerCtrl( self.lockin_setting, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer354.Add( self.working_dir, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer431 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer431.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.start_sl_btn = wx.Button( self.lockin_setting, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer431.Add( self.start_sl_btn, 0, wx.ALL, 5 )

		self.stop_sl_btn = wx.Button( self.lockin_setting, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stop_sl_btn.Enable( False )

		bSizer431.Add( self.stop_sl_btn, 0, wx.ALL, 5 )


		bSizer431.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer354.Add( bSizer431, 1, wx.EXPAND, 5 )


		bSizer131.Add( bSizer354, 1, wx.EXPAND, 5 )


		self.lockin_setting.SetSizer( bSizer131 )
		self.lockin_setting.Layout()
		bSizer131.Fit( self.lockin_setting )
		self.settings_notebook.AddPage( self.lockin_setting, u"Feedback parameters", False )
		self.cam_set_page = wx.Panel( self.settings_notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel26 = wx.Panel( self.cam_set_page, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel26.SetMaxSize( wx.Size( -1,500 ) )

		bSizer55 = wx.BoxSizer( wx.VERTICAL )

		bSizer181 = wx.BoxSizer( wx.VERTICAL )

		bSizer25 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText12 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"ROI", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer25.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticText131 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Y Limits: [...]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

		bSizer25.Add( self.m_staticText131, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer261 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer261.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText141 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Y: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText141.Wrap( -1 )

		bSizer261.Add( self.m_staticText141, 0, wx.ALL, 5 )

		self.m_staticText151 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"[", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151.Wrap( -1 )

		bSizer261.Add( self.m_staticText151, 0, wx.ALL, 5 )

		self.roi_y1 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer261.Add( self.roi_y1, 0, wx.ALL, 5 )

		self.m_staticText161 = wx.StaticText( self.m_panel26, wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText161.Wrap( -1 )

		bSizer261.Add( self.m_staticText161, 0, wx.ALL, 5 )

		self.roi_y2 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer261.Add( self.roi_y2, 0, wx.ALL, 5 )

		self.m_staticText171 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171.Wrap( -1 )

		bSizer261.Add( self.m_staticText171, 0, wx.ALL, 5 )


		bSizer261.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer25.Add( bSizer261, 1, wx.EXPAND, 5 )


		bSizer181.Add( bSizer25, 1, wx.EXPAND, 5 )

		bSizer34 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText13 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"X Limits: [...]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer34.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer26.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText14 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"X: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		bSizer26.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_staticText15 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"[", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		bSizer26.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.roi_x1 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer26.Add( self.roi_x1, 0, wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self.m_panel26, wx.ID_ANY, u",", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer26.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.roi_x2 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer26.Add( self.roi_x2, 0, wx.ALL, 5 )

		self.m_staticText17 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer26.Add( self.m_staticText17, 0, wx.ALL, 5 )


		bSizer26.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer34.Add( bSizer26, 1, wx.EXPAND, 5 )


		bSizer181.Add( bSizer34, 0, wx.EXPAND, 5 )

		self.set_roi = wx.Button( self.m_panel26, wx.ID_ANY, u"Set ROI", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer181.Add( self.set_roi, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer55.Add( bSizer181, 1, wx.EXPAND, 5 )

		bSizer32 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText29 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Exposure time [s]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		bSizer32.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer33 = wx.BoxSizer( wx.HORIZONTAL )

		self.sld_exp = wx.Slider( self.m_panel26, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer33.Add( self.sld_exp, 1, wx.ALL, 5 )

		self.text_exp = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer33.Add( self.text_exp, 0, wx.ALL, 5 )


		bSizer32.Add( bSizer33, 0, wx.EXPAND, 5 )

		self.set_exp = wx.Button( self.m_panel26, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer32.Add( self.set_exp, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer55.Add( bSizer32, 1, wx.EXPAND|wx.TOP, 5 )

		bSizer321 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText291 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Gain", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText291.Wrap( -1 )

		bSizer321.Add( self.m_staticText291, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer331 = wx.BoxSizer( wx.HORIZONTAL )

		self.sld_gain = wx.Slider( self.m_panel26, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer331.Add( self.sld_gain, 1, wx.ALL, 5 )

		self.text_gain = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer331.Add( self.text_gain, 0, wx.ALL, 5 )


		bSizer321.Add( bSizer331, 0, wx.EXPAND, 5 )

		self.set_gain = wx.Button( self.m_panel26, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer321.Add( self.set_gain, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer55.Add( bSizer321, 1, wx.EXPAND, 5 )

		bSizer20 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText91 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Save configuration:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		bSizer20.Add( self.m_staticText91, 0, wx.ALL, 5 )

		self.cam_conf_save = wx.FilePickerCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, u"Select a file", u"TXT files (*.txt)|*.txt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		bSizer20.Add( self.cam_conf_save, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer20.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer55.Add( bSizer20, 0, wx.EXPAND, 5 )


		self.m_panel26.SetSizer( bSizer55 )
		self.m_panel26.Layout()
		bSizer55.Fit( self.m_panel26 )
		bSizer17.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )


		self.cam_set_page.SetSizer( bSizer17 )
		self.cam_set_page.Layout()
		bSizer17.Fit( self.cam_set_page )
		self.settings_notebook.AddPage( self.cam_set_page, u"Camera 1", True )

		fgSizer16.Add( self.settings_notebook, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer6.Add( fgSizer16, 1, wx.EXPAND, 5 )

		self.positions_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.x_pos_panel = Figure_Panel( self.positions_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.x_pos_panel.SetMinSize( wx.Size( -1,300 ) )

		self.positions_notebook.AddPage( self.x_pos_panel, u"X Coord.", False )
		self.y_pos_panel = Figure_Panel( self.positions_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.y_pos_panel.SetMinSize( wx.Size( -1,100 ) )

		self.positions_notebook.AddPage( self.y_pos_panel, u"Y Coord.", False )
		self.z_pos_panel = Figure_Panel( self.positions_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.z_pos_panel.SetMinSize( wx.Size( -1,100 ) )

		self.positions_notebook.AddPage( self.z_pos_panel, u"Z Coord.", False )

		fgSizer6.Add( self.positions_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( fgSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.camera_notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_camera_notenook_page_change )
		self.camera_notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_camera_notebook_page_close )
		self.Bind( wx.EVT_TOOL, self.on_start_cam, id = self.start_btn1.GetId() )
		self.settings_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_settings_nb_pg_chg )
		self.travel_btn.Bind( wx.EVT_BUTTON, self.on_travel_btn )
		self.xy_step_size.Bind( wx.EVT_SPINCTRLDOUBLE, self.on_xy_step_size )
		self.xy_step_size.Bind( wx.EVT_TEXT_ENTER, self.on_xy_step_size )
		self.z_step_size.Bind( wx.EVT_SPINCTRLDOUBLE, self.on_z_step_size )
		self.z_step_size.Bind( wx.EVT_TEXT_ENTER, self.on_z_step_size )
		self.dxy_frac.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dz_frac.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dxy_sngl.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dz_sngl.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dxy_dec.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dz_dec.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dxy_huge.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.dz_huge.Bind( wx.EVT_BUTTON, self.on_step_size_btn )
		self.x_up_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.z_up_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.y_left_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.x_down_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.y_right_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.z_down_btn.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.set_home_btn.Bind( wx.EVT_BUTTON, self.on_set_home_btn )
		self.rtrn_home_btn.Bind( wx.EVT_BUTTON, self.on_rtrn_home_btn )
		self.z_step_size_coar.Bind( wx.EVT_SPINCTRLDOUBLE, self.on_z_step_size_coar )
		self.z_step_size_coar.Bind( wx.EVT_TEXT_ENTER, self.on_z_step_size )
		self.dz_frac_coar.Bind( wx.EVT_BUTTON, self.on_step_size_btn_coar )
		self.dz_sngl_coar.Bind( wx.EVT_BUTTON, self.on_step_size_btn_coar )
		self.dz_dec_coar.Bind( wx.EVT_BUTTON, self.on_step_size_btn_coar )
		self.dz_huge_coar.Bind( wx.EVT_BUTTON, self.on_step_size_btn_coar )
		self.travel_btn_coar.Bind( wx.EVT_BUTTON, self.on_travel_btn_coar )
		self.ls_up_btn.Bind( wx.EVT_BUTTON, self.on_move_btn_coar )
		self.rs_up_btn.Bind( wx.EVT_BUTTON, self.on_move_btn_coar )
		self.m_checkBox8.Bind( wx.EVT_CHECKBOX, self.on_stage_coar_sync )
		self.ls_down_btn.Bind( wx.EVT_BUTTON, self.on_move_btn_coar )
		self.y_right_btn2.Bind( wx.EVT_BUTTON, self.on_move_btn )
		self.rs_down_btn.Bind( wx.EVT_BUTTON, self.on_move_btn_coar )
		self.set_home_btn_coar.Bind( wx.EVT_BUTTON, self.on_set_home_btn_coar )
		self.rtrn_home_btn_coar.Bind( wx.EVT_BUTTON, self.on_rtrn_home_btn_coar )
		self.go_home_btn_coar.Bind( wx.EVT_BUTTON, self.on_go_home_btn_coar )
		self.lock_param_grid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_click_lock_param_grid )
		self.lock_stp_load_file.Bind( wx.EVT_FILEPICKER_CHANGED, self.on_pick_lock_stp_load_file )
		self.lock_stp_save_file.Bind( wx.EVT_FILEPICKER_CHANGED, self.on_pick_lock_stp_save_file )
		self.save_sl_data.Bind( wx.EVT_CHECKBOX, self.on_save_sl_data )
		self.writing_modes_list.Bind( wx.EVT_CHOICE, self.on_writing_modes_list )
		self.save_frm_sl.Bind( wx.EVT_CHECKBOX, self.on_save_frm_sl )
		self.m_checkBox4.Bind( wx.EVT_CHECKBOX, self.on_save_params_ckb )
		self.working_dir.Bind( wx.EVT_DIRPICKER_CHANGED, self.on_working_dir )
		self.start_sl_btn.Bind( wx.EVT_BUTTON, self.on_start_sl_btn )
		self.stop_sl_btn.Bind( wx.EVT_BUTTON, self.on_stop_sl_btn )
		self.set_roi.Bind( wx.EVT_BUTTON, self.on_set_roi )
		self.sld_exp.Bind( wx.EVT_SLIDER, self.on_sld_exp )
		self.text_exp.Bind( wx.EVT_TEXT_ENTER, self.on_text_exp )
		self.set_exp.Bind( wx.EVT_BUTTON, self.on_set_exp )
		self.sld_gain.Bind( wx.EVT_SLIDER, self.on_sld_gain )
		self.text_gain.Bind( wx.EVT_TEXT_ENTER, self.on_text_gain )
		self.set_gain.Bind( wx.EVT_BUTTON, self.on_set_gain )
		self.cam_conf_save.Bind( wx.EVT_FILEPICKER_CHANGED, self.on_cam_conf_save )
		self.positions_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changing )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_close( self, event ):
		event.Skip()

	def on_camera_notenook_page_change( self, event ):
		event.Skip()

	def on_camera_notebook_page_close( self, event ):
		event.Skip()

	def on_start_cam( self, event ):
		event.Skip()

	def on_settings_nb_pg_chg( self, event ):
		event.Skip()

	def on_travel_btn( self, event ):
		event.Skip()

	def on_xy_step_size( self, event ):
		event.Skip()


	def on_z_step_size( self, event ):
		event.Skip()


	def on_step_size_btn( self, event ):
		event.Skip()








	def on_move_btn( self, event ):
		event.Skip()






	def on_set_home_btn( self, event ):
		event.Skip()

	def on_rtrn_home_btn( self, event ):
		event.Skip()

	def on_z_step_size_coar( self, event ):
		event.Skip()


	def on_step_size_btn_coar( self, event ):
		event.Skip()




	def on_travel_btn_coar( self, event ):
		event.Skip()

	def on_move_btn_coar( self, event ):
		event.Skip()


	def on_stage_coar_sync( self, event ):
		event.Skip()




	def on_set_home_btn_coar( self, event ):
		event.Skip()

	def on_rtrn_home_btn_coar( self, event ):
		event.Skip()

	def on_go_home_btn_coar( self, event ):
		event.Skip()

	def on_click_lock_param_grid( self, event ):
		event.Skip()

	def on_pick_lock_stp_load_file( self, event ):
		event.Skip()

	def on_pick_lock_stp_save_file( self, event ):
		event.Skip()

	def on_save_sl_data( self, event ):
		event.Skip()

	def on_writing_modes_list( self, event ):
		event.Skip()

	def on_save_frm_sl( self, event ):
		event.Skip()

	def on_save_params_ckb( self, event ):
		event.Skip()

	def on_working_dir( self, event ):
		event.Skip()

	def on_start_sl_btn( self, event ):
		event.Skip()

	def on_stop_sl_btn( self, event ):
		event.Skip()

	def on_set_roi( self, event ):
		event.Skip()

	def on_sld_exp( self, event ):
		event.Skip()

	def on_text_exp( self, event ):
		event.Skip()

	def on_set_exp( self, event ):
		event.Skip()

	def on_sld_gain( self, event ):
		event.Skip()

	def on_text_gain( self, event ):
		event.Skip()

	def on_set_gain( self, event ):
		event.Skip()

	def on_cam_conf_save( self, event ):
		event.Skip()

	def on_page_changing( self, event ):
		event.Skip()


