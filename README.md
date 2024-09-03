# MultiMove-Tool
MultiMove-Tool is a developer utility for moving multiple files
## Features
> - Moving files by a regular expression
> - Moving files by dictionary definition
> - Currently designed for windows with batch file
## Utilization
> MultiMove-Tool provides two main ways to interact with the utility
> - MultiMoveLite
>     - Built for one-liners
>     - Does not provide shell emulation
> - MultiMoveHeavy
>     - Built for extensive move operations
>     - Emulates shell environment
>     - Can run shell commands from environment
## Flag and CmdLine Args structure
> The flags currently provided with MultiMove are slightly lacking
> - Running a command with \-c saves the executed command to a log
> - Running a command with \-sd allows a user to move multiple files to a single destination
> 
> Command Line Arguments are as follows
> - reg \- Regex Specifier (you can pass multiple values to reg but be aware only the first regular expression will be used)
> - des \- Destination Specifier
> - src \- Source Specifier
>   - Source and Destination Specifiers are to be passed as lists formatted
>      `des="example.txt, example2.txt, example3.txt"`
> As the three are command line arguments, be careful with spacing, only use spaces in quotes, there should be no separation between an arg specifier, the equal sign and its value
## Extra Functionality
> undo - if move commands were cached with \-c specifier, moves can be undone
> prev - shows a preview of cached moves
> vre - verify regular expression (YET TO BE IMPLEMENTED but is included in multimove.py and can be interacted with Pythonically)
> vm - verify move (YET TO BE IMPLEMENTED but is included in multimove.py and can be interacted with Pythonically)
> quit - to quit the emulator

