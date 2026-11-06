NULL POINT AUDIO - NP Vocal Suite - build & installer notes
===========================================================

Source tree:   C:\AuraVerb\NullPoint\
    Shared\                  shared UI / DSP / preset code (AuraUI.h, AuraDynamics.h, AuraPresets.h)
    NP-Verb\ NP-EQ\ NP-Comp\ NP-DeEss\ NP-Limit\ NP-Gate\ NP-Zero\
        Source\              plugin code
        JuceLibraryCode\     JUCE glue (JucePluginDefines.h holds name / codes / version)
        Builds\VisualStudio2022\<Name>.sln

Plugin identity (JucePluginDefines.h + vcxproj PreprocessorDefinitions):
    Manufacturer  Null Point Audio   code 'NulP'
    NP-Verb  NPvb   NP-EQ  NPeq   NP-Comp  NPcp   NP-DeEss NPde
    NP-Limit NPlm   NP-Gate NPgt  NP-Zero  NPzr
    Version 1.0.0   (bump in JucePluginDefines.h, the vcxproj defines and resources.rc,
                     and VERSION in installer\NullPointAudio.nsi)

Building the plug-ins
    Open each .sln in Visual Studio, Release | x64, Build Solution.
    Output:  Builds\VisualStudio2022\x64\Release\VST3\<Name>.dll     (= the VST3)
             Builds\VisualStudio2022\x64\Release\Standalone Plugin\<Name>.exe
    The projects link the static VC++ runtime (/MT) so customers do not need the
    VC++ redistributable.

Building the installer  (NSIS 3 - https://nsis.sourceforge.io)
    1. copy each <Name>.dll to installer\bin\<Name>.vst3
       copy each <Name>.exe to installer\bin\<Name>.exe
    2. makensis installer\NullPointAudio.nsi
    -> NullPointAudio_Bundle_Setup_v1.0.0.exe

What the installer does
    * VST3 plug-ins -> C:\Program Files\Common Files\VST3\   (every VST3 host finds them)
    * optional standalone apps -> C:\Program Files\Null Point Audio\  + Start-menu shortcuts
    * removes the old AuraAudio-branded builds (Nimbus/PrismEQ/Grip/Hush/Apex/Veil/Still.vst3)
    * Add/Remove Programs entry + uninstaller
    * user presets / theme choice live in %APPDATA%\NullPointAudio\ and are kept on uninstall

Code signing (recommended before public release)
    Unsigned installers trigger Windows SmartScreen "unknown publisher" warnings.
    Sign the .exe/.vst3 files and the installer with an Authenticode certificate:
        signtool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a <file>
