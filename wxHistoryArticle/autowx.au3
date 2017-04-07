#Region ;**** 参数创建于 ACNWrapper_GUI ****
#PRE_icon=C:\Windows\syswow64\SHELL32.dll|-131
#PRE_OutFile=autowx.exe
#PRE_UseX64=n
#PRE_Change2CUI=y
#PRE_Res_requestedExecutionLevel=None
#EndRegion ;**** 参数创建于 ACNWrapper_GUI ****

#include <Array.au3>
#Include <WinAPI.au3>
#Include <WinAPIEx.au3>
#include <ClipBoard.au3>
#include <Process.au3>

const  $SWP_NOSIZE = 0x0001
const  $SWP_NOMOVE = 0x0002
const  $SWP_NOZORDER = 0x0004
const  $SWP_NOREDRAW = 0x0008
const  $SWP_NOACTIVATE = 0x0010
const  $SWP_FRAMECHANGED = 0x0020
const  $SWP_SHOWWINDOW = 0x0040
const  $SWP_HIDEWINDOW = 0x0080
const  $SWP_NOCOPYBITS = 0x0100
const  $SWP_NOOWNERZORDER = 0x0200
const  $SWP_NOSENDCHANGING = 0x0400
const  $TOPMOST_FLAGS = $SWP_NOMOVE + $SWP_NOSIZE

If $CmdLine[0] = 1 Then
	Global $mode = $CmdLine[1]
	Global $task = 0
	Global $serverBaseUrl = "http://wx_helper_dev1.leesrobots.com"
ElseIf $CmdLine[0] = 2 Then
	Global $mode = $CmdLine[1]
	Global $task = $CmdLine[2]
	Global $serverBaseUrl = "http://wx_helper_dev1.leesrobots.com"
ElseIf $CmdLine[0] = 3 Then
	Global $mode = $CmdLine[1]
	Global $task = $CmdLine[2]
	Global $serverBaseUrl = $CmdLine[3]
Else
	Global $mode = "slave"
	Global $task = 0
	Global $serverBaseUrl = "http://wx_helper_dev1.leesrobots.com"
EndIf

HotKeySet("!z", "_Terminate") ; Alt + z 快捷键退出脚本

Global $myErrHandler = ObjEvent ( "AutoIt.Error","Err_Process" )
Global $ErrCode = 0
If $mode = "-h"  Or $mode = "/h" Or $mode = "help" Or $mode = "--help" Then
	_showUsage()
ElseIf $mode = "slave" Then
	; Slave模式
	; 重置控制台日志窗口位置
	$pid = _WinAPI_GetCurrentProcessID()
	$consoleHwnd = _ProcessGetHWnd($pid)
	If $consoleHwnd then
		_WinAPI_SetWindowPos($consoleHwnd,-1,630,0,600,500,$SWP_SHOWWINDOW)
	EndIf
	; 防止休眠
	ConsoleWrite("Start with slave model ..." & @CRLF)
	ConsoleWrite("HotKey: ALT+Z ,Quit Script!" & @CRLF & @CRLF)
	_WinAPI_SetThreadExecutionState( $ES_CONTINUOUS + $ES_SYSTEM_REQUIRED + $ES_AWAYMODE_REQUIRED ) 

	While True
		$taskList = _GetTaskPool()
		If $taskList[0] > 0 And $taskList[1] <> "" Then
			For $r = 1 to $taskList[0]
				If $taskList[$r] <> "" Then
					ConsoleWrite("Run Task:" & $taskList[$r] & @CRLF)
					$param  = StringSplit($taskList[$r],",")
					_DoTask($param[2],$param[1],$param[3])
				EndIf
			Next
		Else
			; 没有领到任务10秒后再去领
			ConsoleWrite("Task Pool is empty，Sleep 10s ..." & @CRLF)
			Sleep(10000)
		EndIf
	Wend
Else
	ConsoleWrite("Start with simple model ..." & @CRLF)
	$ret = _DoTask($mode,$task)
	Exit $ret
EndIf

Func _showUsage()
	ConsoleWrite("Usage:" & @CRLF & @ScriptName & " [slave]" & @CRLF & @ScriptName & " BIZ [TASKID] [SERVER_BASEURL]" & @CRLF & "HotKey: ALT+Z ,Quit Script!" & @CRLF)
	Exit 0
EndFunc

Func _Terminate()
	ConsoleWrite(@CRLF & "F4 Pushed,User Stop Script ..." & @CRLF)
	Exit 0
EndFunc


Func _DoTask($biz,$task_id = 0,$last_sync_time = 0)
	ConsoleWrite("beigen task, biz:" & $biz & ",task_id:" & $task_id & @CRLF)

	$qqBrowserWin = "[REGEXPCLASS:QQBrowser;INSTANCE:1]"
	;$qqBrowserWin = "[CLASS:WeChatMain;INSTANCE:1]"
	$winExist = WinExists($qqBrowserWin,"微信")
	If Not $winExist Then
		Exit 2;
	EndIf

	$hWnd = WinGetHandle($qqBrowserWin)
	WinActivate($hWnd)
	WinWaitActive($hWnd)
	; qq浏览器至于坐标 0，0位置 并重置窗口大小
	_WinAPI_SetWindowPos($hWnd,-1,0,0,630,500,$SWP_SHOWWINDOW)
	WinSetOnTop($hWnd, "", 1)
	SendKeepActive($hWnd)
	$browserPos = WinGetPos($hWnd)
	$wxPos = ControlGetPos($hWnd,"","WeChatMain1")
	_ClipBoard_SetData ("filehelper")
	MouseClick("left",77 + $browserPos[0] + $wxPos[0],$browserPos[1] + $wxPos[1]+80,1) ; 点击搜索输入框
	Send("^v") 
	Sleep(500)
	MouseClick("left",77 + $browserPos[0] + $wxPos[0],$browserPos[1] + $wxPos[1]+125,1); 第一个联系人坐标
	$wxPos = ControlGetPos($hWnd,"","WeChatMain1")

	MouseClick("left",$browserPos[0] + $wxPos[0] + $wxPos[2] - 150,$browserPos[1] + $wxPos[1] + $wxPos[3] - 60,1) ; 点击聊天输入框
	
	_ClipBoard_SetData ("http://mp.weixin.qq.com/mp/getmasssendmsg?task_id=" & $task_id & "&last_sync_time=" & $last_sync_time & "&__biz=" & $biz & "#wechat_redirect")
	Send("^v")
	Send("{ENTER}")
	;LoadKeyboardLayout("04090409", $hWnd) ; 设置为英文键盘
	;Send("http://mp.weixin.qq.com/mp/getmasssendmsg?task_id=" & $task_id & "&last_sync_time=" & $last_sync_time & "&__biz=" & $biz & "#wechat_redirect",1)
	;MouseClick("left",$browserPos[0] + $wxPos[0] + $wxPos[2] - 50,$browserPos[1] + $wxPos[1] + $wxPos[3] -25 ,1); 点击发送按钮
	MouseClick("left",$browserPos[0] + $wxPos[0] + $wxPos[2] - 180,$browserPos[1] + $wxPos[1] + $wxPos[3] -250,1 ) ; 点击历史记录链接
	ConsoleWrite("end task" & @CRLF)
	Return 0
EndFunc

Func Err_Process()
	$errMsg ="We intercepted a COM Error !"   & @CRLF & _
             "err.description is: "    & @TAB & $myErrHandler.description    & @CRLF & _
             "err.windescription:"     & @TAB & $myErrHandler.windescription & @CRLF & _
             "err.number is: "         & @TAB & hex($myErrHandler.number,8)  & @CRLF & _
             "err.lastdllerror is: "   & @TAB & $myErrHandler.lastdllerror   & @CRLF & _
             "err.scriptline is: "     & @TAB & $myErrHandler.scriptline     & @CRLF & _
             "err.source is: "         & @TAB & $myErrHandler.source         & @CRLF & _
             "err.helpfile is: "       & @TAB & $myErrHandler.helpfile       & @CRLF & _
             "err.helpcontext is: "    & @TAB & $myErrHandler.helpcontext & @CRLF & @CRLF 
	ConsoleWrite($errMsg)
	$ErrCode = $myErrHandler.number
EndFunc

; 获取键盘输入法
Func _GetKeyboardLayout($hWnd)
    Local $ret = DllCall("user32.dll", "long", "GetWindowThreadProcessId", "hwnd", $hWnd, "ptr", 0)
	$ret = DllCall("user32.dll", "long", "GetKeyboardLayout", "long", $ret[0])
    Return Hex($ret[0], 8)
EndFunc  

; 设置键盘输入法
Func LoadKeyboardLayout($sLayoutID, $hWnd)
    Local $WM_INPUTLANGCHANGEREQUEST = 0x50
    Local $ret = DllCall("user32.dll", "long", "LoadKeyboardLayout", "str", $sLayoutID, "int", 1 + 0)
    DllCall("user32.dll", "ptr", "SendMessage", "hwnd", $hWnd, "int", $WM_INPUTLANGCHANGEREQUEST, "int", 1, "int", $ret[0])        
EndFunc   ;==>LoadKeyboardLayout

Func _HttpRequest($url,$method="GET",$data = "")
	ConsoleWrite($method & ":" & $url &@CRLF)
    $oHTTP = ObjCreate("Msxml2.ServerXMLHTTP")
    $oHTTP.Open($method, $url, False)
	ConsoleWrite("Send Request:" & $data &@CRLF)
    $oHTTP.Send($data)
	If $ErrCode Then
		ConsoleWrite("Fire Err:" & $ErrCode &@CRLF)
		$ErrCode = 0
		Return ""
	EndIf
    $return = $oHTTP.responsetext
	ConsoleWrite("Response:" & $return &@CRLF)
    Return $return
EndFunc

Func _HttpGet($url)
	Return _HttpRequest($url)
EndFunc

Func _HttpPost($url,$data = "")
	Return _HttpRequest($url,"POST",$data)
EndFunc
; 
; response（biz1,taskId1;biz2,taskId2; ...） ： "MzA5NzA3NjE1MA==,1001;NZzA5NzA3NjE1MA==,1002"
Func _GetTaskPool()
	$response = _HttpGet($serverBaseUrl & "/spider_task/get_task_list")
	
	ConsoleWrite("GetTaskPool:" & StringReplace($response,";",@CRLF) & @CRLF)
	$list = StringSplit($response,";")
	Return $list
EndFunc

; BASE64 函数
Func _Base64Decode($Data)
		Local $Opcode = "0xC81000005356578365F800E8500000003EFFFFFF3F3435363738393A3B3C3DFFFFFF00FFFFFF000102030405060708090A0B0C0D0E0F10111213141516171819FFFFFFFFFFFF1A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132338F45F08B7D0C8B5D0831D2E9910000008365FC00837DFC047D548A034384C0750383EA033C3D75094A803B3D75014AB00084C0751A837DFC047D0D8B75FCC64435F400FF45FCEBED6A018F45F8EB1F3C2B72193C7A77150FB6F083EE2B0375F08A068B75FC884435F4FF45FCEBA68D75F4668B06C0E002C0EC0408E08807668B4601C0E004C0EC0208E08847018A4602C0E00624C00A46038847028D7F038D5203837DF8000F8465FFFFFF89D05F5E5BC9C21000"
	   
		Local $CodeBuffer = DllStructCreate("byte[" & BinaryLen($Opcode) & "]")
		DllStructSetData($CodeBuffer, 1, $Opcode)

		Local $Ouput = DllStructCreate("byte[" & BinaryLen($Data) & "]")
		Local $Ret = DllCall("user32.dll", "int", "CallWindowProc", "ptr", DllStructGetPtr($CodeBuffer), _
																										"str", $Data, _
																										"ptr", DllStructGetPtr($Ouput), _
																										"int", 0, _
																										"int", 0)

		Return BinaryMid(DllStructGetData($Ouput, 1), 1, $Ret[0])
EndFunc

Func _Base64Encode($Data, $LineBreak = 76)
		$Data = String($Data)
		Local $Opcode = "0x5589E5FF7514535657E8410000004142434445464748494A4B4C4D4E4F505152535455565758595A6162636465666768696A6B6C6D6E6F707172737475767778797A303132333435363738392B2F005A8B5D088B7D108B4D0CE98F0000000FB633C1EE0201D68A06880731C083F901760C0FB6430125F0000000C1E8040FB63383E603C1E60409C601D68A0688470183F90176210FB6430225C0000000C1E8060FB6730183E60FC1E60209C601D68A06884702EB04C647023D83F90276100FB6730283E63F01D68A06884703EB04C647033D8D5B038D7F0483E903836DFC04750C8B45148945FC66B80D0A66AB85C90F8F69FFFFFFC607005F5E5BC9C21000"

		Local $CodeBuffer = DllStructCreate("byte[" & BinaryLen($Opcode) & "]")
		DllStructSetData($CodeBuffer, 1, $Opcode)

		$Data = Binary($Data)
		Local $Input = DllStructCreate("byte[" & BinaryLen($Data) & "]")
		DllStructSetData($Input, 1, $Data)

		$LineBreak = Floor($LineBreak / 4) * 4
		Local $OputputSize = Ceiling(BinaryLen($Data) * 4 / 3)
		$OputputSize = $OputputSize + Ceiling($OputputSize / $LineBreak) * 2 + 4

		Local $Ouput = DllStructCreate("char[" & $OputputSize & "]")
		DllCall("user32.dll", "none", "CallWindowProc", "ptr", DllStructGetPtr($CodeBuffer), _
																										"ptr", DllStructGetPtr($Input), _
																										"int", BinaryLen($Data), _
																										"ptr", DllStructGetPtr($Ouput), _
																										"uint", $LineBreak)
		Return DllStructGetData($Ouput, 1)
EndFunc
	
	
	
;===============================================================================
;
; Function Name:    _ProcessGetHWnd
; Description:      Returns the HWND(s) owned by the specified process (PID only !).
;
; Parameter(s):     $iPid        - the owner-PID.
;                    $iOption    - Optional : return/search methods :
;                        0 - returns the HWND for the first non-titleless window.
;                        1 - returns the HWND for the first found window (default).
;                        2 - returns all HWNDs for all matches.
;
;                   $sTitle        - Optional : the title to match (see notes).
;                    $iTimeout    - Optional : timeout in msec (see notes)
;
; Return Value(s):  On Success - returns the HWND (see below for method 2).
;                        $array[0][0] - number of HWNDs
;                        $array[x][0] - title
;                        $array[x][1] - HWND
;
;                   On Failure    - returns 0 and sets @error to 1.
;
; Note(s):            When a title is specified it will then only return the HWND to the titles
;                    matching that specific string. If no title is specified it will return as
;                    described by the option used.
;
;                    When using a timeout it's possible to use WinWaitDelay (Opt) to specify how
;                    often it should wait before attempting another time to get the HWND.
;
;
; Author(s):        Helge
;
;===============================================================================
Func _ProcessGetHWnd($iPid, $iOption = 1, $sTitle = "", $iTimeout = 2000)
    Local $aReturn[1][1] = [[0]], $aWin, $hTimer = TimerInit()
     
    While 1
         
        ; Get list of windows
        $aWin = WinList($sTitle)
         
        ; Searches thru all windows
        For $i = 1 To $aWin[0][0]
             
            ; Found a window owned by the given PID
            If $iPid = WinGetProcess($aWin[$i][1]) Then
                 
                ; Option 0 or 1 used
                If $iOption = 1 OR ($iOption = 0 And $aWin[$i][0] <> "") Then
                    Return $aWin[$i][1]
                 
                ; Option 2 is used
                ElseIf $iOption = 2 Then
                    ReDim $aReturn[UBound($aReturn) + 1][2]
                    $aReturn[0][0] += 1
                    $aReturn[$aReturn[0][0]][0] = $aWin[$i][0]
                    $aReturn[$aReturn[0][0]][1] = $aWin[$i][1]
                EndIf
            EndIf
        Next
         
        ; If option 2 is used and there was matches then the list is returned
        If $iOption = 2 And $aReturn[0][0] > 0 Then Return $aReturn
         
        ; If timed out then give up
        If TimerDiff($hTimer) > $iTimeout Then ExitLoop
         
        ; Waits before new attempt
        Sleep(Opt("WinWaitDelay"))
    WEnd
     
     
    ; No matches
    SetError(1)
    Return 0
EndFunc   ;==>_ProcessGetHWnd