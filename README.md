# MFV: Application software for the visualization and characterization of the DC magnetic field distribution in circular coil systems

For information, usage and applications please visit http://arxiv.org/abs/1904.04327.


Installation
============

Linux and Mac OS X
-------------------

On Linux and Mac OS X operating systems, MFV does not require to be built or installed in order to be executed. You just have to <a href="https://github.com/pcm-ca/MFV/tree/master/Executables">download</a> and run the corresponding stand-alone executable.

Windows
-------

In order to run MFV on Windows, you need to install PyGObject, GTK and their depencies, along with some other python libraries. Follow the instructions below.

1. Go to http://www.msys2.org/ and download the x86_64 installer
2. Follow the instructions on the page for setting up the basic environment
3. Run C:\msys64\mingw64.exe - a terminal window should pop up
4. Execute <code>pacman -Suy</code>
5. Execute <code>pacman -S git mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python3-numpy mingw-w64-x86_64-python3-scipy mingw-w64-x86_64-python3-matplotlib mingw-w64-x86_64-python3-openpyxl</code>
6. Execute <code>git clone https://github.com/pcm-ca/MFV.git</code>
7. Execute <code>cd MFV/src/</code>
8. Execute <code>python3 interface.py - the MFV input parameters window should appear</code>


