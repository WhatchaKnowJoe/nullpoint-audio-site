; ---------------------------------------------------------------------------
;  Null Point Audio - NP Vocal Suite installer (NSIS 3, Modern UI 2)
;  Build:  makensis NullPointAudio.nsi
;  Expects the plugin binaries in .\bin\  (NP-*.vst3 and NP-*.exe)
; ---------------------------------------------------------------------------
Unicode true
!include "MUI2.nsh"
!include "x64.nsh"
!include "LogicLib.nsh"
!include "Sections.nsh"

!define COMPANY      "Null Point Audio"
!define SUITE        "NP Vocal Suite"
!define VERSION      "1.0.0"
!define WEBSITE      "https://www.nullpointaudio.com"
!define REGKEY       "Software\${COMPANY}\${SUITE}"
!define UNINSTKEY    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${SUITE}"

Name                 "${COMPANY} - ${SUITE} ${VERSION}"
OutFile              "..\NullPointAudio_Bundle_Setup_v${VERSION}.exe"
BrandingText         "${COMPANY}  -  ${SUITE} ${VERSION}"
InstallDir           "$PROGRAMFILES64\${COMPANY}"
InstallDirRegKey HKLM "${REGKEY}" "InstallDir"
RequestExecutionLevel admin
SetCompressor /SOLID lzma
ShowInstDetails      show
ShowUninstDetails    show

VIProductVersion     "${VERSION}.0"
VIAddVersionKey      "ProductName"     "${SUITE}"
VIAddVersionKey      "CompanyName"     "${COMPANY}"
VIAddVersionKey      "FileDescription" "${SUITE} Installer"
VIAddVersionKey      "FileVersion"     "${VERSION}"
VIAddVersionKey      "ProductVersion"  "${VERSION}"
VIAddVersionKey      "LegalCopyright"  "(c) 2026 ${COMPANY}"

; ---- UI ------------------------------------------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON   "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEPAGE_TITLE "Welcome to the ${SUITE} Setup"
!define MUI_WELCOMEPAGE_TEXT  "This will install the ${COMPANY} vocal-chain plug-ins on your computer:$\r$\n$\r$\nNP-Verb (reverb)   NP-EQ (equalizer)   NP-Comp (compressor)$\r$\nNP-DeEss (de-esser)   NP-Limit (limiter)   NP-Gate (gate)   NP-Zero (noise / room)$\r$\n$\r$\nVST3 plug-ins are installed to the standard system folder so every VST3 host (FL Studio, Ableton Live, Cubase, Studio One, Reaper, Pro Tools 2024+ ...) finds them automatically.$\r$\n$\r$\nPlease close your DAW before continuing."
!define MUI_COMPONENTSPAGE_SMALLDESC
!define MUI_FINISHPAGE_TITLE  "Installation complete"
!define MUI_FINISHPAGE_TEXT   "The ${SUITE} has been installed.$\r$\n$\r$\nOpen your DAW and rescan plug-ins if the new plug-ins do not appear right away."
!define MUI_FINISHPAGE_LINK          "www.nullpointaudio.com"
!define MUI_FINISHPAGE_LINK_LOCATION "${WEBSITE}"
!define MUI_DIRECTORYPAGE_TEXT_TOP "Setup will install the optional standalone applications in the folder below. VST3 plug-ins always go to the system VST3 folder ($$COMMONFILES64\VST3)."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

; ---- helpers --------------------------------------------------------------
Var VST3DIR

!macro InstallPlugin NAME
  SetOutPath "$VST3DIR"
  File "bin\${NAME}.vst3"
  WriteRegStr HKLM "${REGKEY}\Plugins" "${NAME}" "$VST3DIR\${NAME}.vst3"
!macroend

!macro InstallStandalone NAME
  SetOutPath "$INSTDIR"
  File "bin\${NAME}.exe"
  CreateShortcut "$SMPROGRAMS\${COMPANY}\${NAME}.lnk" "$INSTDIR\${NAME}.exe"
!macroend

; ---- sections -------------------------------------------------------------
SectionGroup /e "VST3 plug-ins" GRP_VST3
  Section "NP-Verb  -  reverb"        SEC_VERB
    !insertmacro InstallPlugin "NP-Verb"
  SectionEnd
  Section "NP-EQ  -  equalizer"       SEC_EQ
    !insertmacro InstallPlugin "NP-EQ"
  SectionEnd
  Section "NP-Comp  -  compressor"    SEC_COMP
    !insertmacro InstallPlugin "NP-Comp"
  SectionEnd
  Section "NP-DeEss  -  de-esser"     SEC_DEESS
    !insertmacro InstallPlugin "NP-DeEss"
  SectionEnd
  Section "NP-Limit  -  limiter"      SEC_LIMIT
    !insertmacro InstallPlugin "NP-Limit"
  SectionEnd
  Section "NP-Gate  -  gate"          SEC_GATE
    !insertmacro InstallPlugin "NP-Gate"
  SectionEnd
  Section "NP-Zero  -  noise / room"  SEC_ZERO
    !insertmacro InstallPlugin "NP-Zero"
  SectionEnd
SectionGroupEnd

SectionGroup "Standalone applications (optional)" GRP_STANDALONE
  Section /o "NP-Verb standalone"   SEC_SA_VERB
    !insertmacro InstallStandalone "NP-Verb"
  SectionEnd
  Section /o "NP-EQ standalone"     SEC_SA_EQ
    !insertmacro InstallStandalone "NP-EQ"
  SectionEnd
  Section /o "NP-Comp standalone"   SEC_SA_COMP
    !insertmacro InstallStandalone "NP-Comp"
  SectionEnd
  Section /o "NP-DeEss standalone"  SEC_SA_DEESS
    !insertmacro InstallStandalone "NP-DeEss"
  SectionEnd
  Section /o "NP-Limit standalone"  SEC_SA_LIMIT
    !insertmacro InstallStandalone "NP-Limit"
  SectionEnd
  Section /o "NP-Gate standalone"   SEC_SA_GATE
    !insertmacro InstallStandalone "NP-Gate"
  SectionEnd
  Section /o "NP-Zero standalone"   SEC_SA_ZERO
    !insertmacro InstallStandalone "NP-Zero"
  SectionEnd
SectionGroupEnd

Section "-post"  ; hidden: uninstaller + registry
  SetOutPath "$INSTDIR"
  File "LICENSE.txt"
  WriteUninstaller "$INSTDIR\Uninstall ${SUITE}.exe"
  CreateDirectory "$SMPROGRAMS\${COMPANY}"
  CreateShortcut  "$SMPROGRAMS\${COMPANY}\Uninstall ${SUITE}.lnk" "$INSTDIR\Uninstall ${SUITE}.exe"

  WriteRegStr   HKLM "${REGKEY}" "InstallDir" "$INSTDIR"
  WriteRegStr   HKLM "${REGKEY}" "Version"    "${VERSION}"
  WriteRegStr   HKLM "${UNINSTKEY}" "DisplayName"     "${COMPANY} ${SUITE}"
  WriteRegStr   HKLM "${UNINSTKEY}" "DisplayVersion"  "${VERSION}"
  WriteRegStr   HKLM "${UNINSTKEY}" "Publisher"       "${COMPANY}"
  WriteRegStr   HKLM "${UNINSTKEY}" "URLInfoAbout"    "${WEBSITE}"
  WriteRegStr   HKLM "${UNINSTKEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr   HKLM "${UNINSTKEY}" "UninstallString" '"$INSTDIR\Uninstall ${SUITE}.exe"'
  WriteRegStr   HKLM "${UNINSTKEY}" "DisplayIcon"     "$INSTDIR\Uninstall ${SUITE}.exe"
  WriteRegDWORD HKLM "${UNINSTKEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINSTKEY}" "NoRepair" 1
  ; estimated size (KB)
  SectionGetSize ${SEC_VERB} $0
  IntOp $0 $0 * 14
  WriteRegDWORD HKLM "${UNINSTKEY}" "EstimatedSize" $0
SectionEnd

; ---- descriptions ----------------------------------------------------------
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_VST3}       "The seven NP plug-ins in VST3 format, installed to the system VST3 folder."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_VERB}       "Algorithmic FDN vocal reverb with early reflections, modulation and freeze."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_EQ}         "Analog-matched parametric EQ with up to 8 bands and spectrum display."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_COMP}       "Vocal compressor with program-dependent release, sidechain filter and mix."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_DEESS}      "Split-band de-esser with listen mode and Linkwitz-Riley crossover."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_LIMIT}      "True-peak look-ahead brickwall limiter - guaranteed no overshoot."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_GATE}       "Noise gate / expander with hysteresis, look-ahead and sidechain filter."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_ZERO}       "Noise and room-tone reduction for cleaning up vocal recordings."
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_STANDALONE} "Run the plug-ins as standalone Windows applications (no DAW needed). Not required for use inside a DAW."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; ---- init ------------------------------------------------------------------
Function .onInit
  ${IfNot} ${RunningX64}
    MessageBox MB_OK|MB_ICONSTOP "The ${SUITE} requires 64-bit Windows 10 or later."
    Abort
  ${EndIf}
  SetRegView 64
  StrCpy $VST3DIR "$COMMONFILES64\VST3"
  ; remove previous AuraAudio-branded builds of the same plug-ins if present
  Delete "$VST3DIR\Nimbus.vst3"
  Delete "$VST3DIR\PrismEQ.vst3"
  Delete "$VST3DIR\Grip.vst3"
  Delete "$VST3DIR\Hush.vst3"
  Delete "$VST3DIR\Apex.vst3"
  Delete "$VST3DIR\Veil.vst3"
  Delete "$VST3DIR\Still.vst3"
FunctionEnd

Function un.onInit
  SetRegView 64
  StrCpy $VST3DIR "$COMMONFILES64\VST3"
FunctionEnd

; ---- uninstall -------------------------------------------------------------
Section "Uninstall"
  Delete "$VST3DIR\NP-Verb.vst3"
  Delete "$VST3DIR\NP-EQ.vst3"
  Delete "$VST3DIR\NP-Comp.vst3"
  Delete "$VST3DIR\NP-DeEss.vst3"
  Delete "$VST3DIR\NP-Limit.vst3"
  Delete "$VST3DIR\NP-Gate.vst3"
  Delete "$VST3DIR\NP-Zero.vst3"

  Delete "$INSTDIR\NP-Verb.exe"
  Delete "$INSTDIR\NP-EQ.exe"
  Delete "$INSTDIR\NP-Comp.exe"
  Delete "$INSTDIR\NP-DeEss.exe"
  Delete "$INSTDIR\NP-Limit.exe"
  Delete "$INSTDIR\NP-Gate.exe"
  Delete "$INSTDIR\NP-Zero.exe"
  Delete "$INSTDIR\LICENSE.txt"
  Delete "$INSTDIR\Uninstall ${SUITE}.exe"
  RMDir  "$INSTDIR"

  RMDir /r "$SMPROGRAMS\${COMPANY}"

  DeleteRegKey HKLM "${UNINSTKEY}"
  DeleteRegKey HKLM "${REGKEY}"
  DeleteRegKey /ifempty HKLM "Software\${COMPANY}"

  ; user presets & theme settings are kept (in %APPDATA%\NullPointAudio) so
  ; they survive a reinstall.  Users can delete that folder manually.
SectionEnd
