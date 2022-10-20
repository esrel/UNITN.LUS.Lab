================================================================================
Instructions to setup for LUS 2017-18 Course Lab
================================================================================

A Unix-based machine (MacOS or Linux (examples are debian/ubuntu)) is required.
Optionally, you can install Linux in a VirtualBox (https://www.virtualbox.org/)

================================================================================
Installation of OpenFST and OpenGRM tools
================================================================================

Download:
(a) OpenFST from http://www.openfst.org/
(b) OpenGRM from http://www.opengrm.org/

--------------------------------------------------------------------------------
MacOS Instructions
--------------------------------------------------------------------------------

1. Install Command Line Tools (if Xcode is not installed)

   type "xcode-select --install" in terminal & follow instructions
   
2. Follow the instructions for compiling OpenFST and OpenGRM in README/INSTALL 
   files in the downloaded archives
   configure OpenFST with '--enable-far' and '--enable-grm' options
   
3. For visualization using graphviz [optional]:
   
   install graphviz using 
     macports (https://www.macports.org/) or 
     homebrew (https://brew.sh/)

--------------------------------------------------------------------------------
Linux Instructions
--------------------------------------------------------------------------------
(Tested with Debian 8.7 and Ubuntu 16.04)

1. Install build-essential (g++, make, etc.), if not installed
   sudo apt-get install build-essential
   
2. Set environment variables in .bashrc, if not set already
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
   export CPATH=$CPATH:/usr/local/include (optional, but better)

3. Follow the instructions for compiling OpenFST and OpenGRM in README/INSTALL 
   files in the downloaded archives
   configure OpenFST with '--enable-far' and '--enable-grm' options

4. For visualization using graphviz [optional]:
   install graphviz from repository

--------------------------------------------------------------------------------
Test installation of the tools
--------------------------------------------------------------------------------

in terminal go into test directory and execute the following:

   (a) Compilation (test for FST tools)
   fstcompile --acceptor --isymbols=A.lex A.txt A.fsa
   
   (b) Visualization [in case graphviz is installed]
   fstdraw --acceptor --isymbols=A.lex A.fsa | dot -Tpng > test.png
   
   You should see a figure similar to that of A.png
   
   (c) Graph (dot format output, just for test)
   fstdraw --acceptor --isymbols=A.lex A.fsa
   
   You should see something like:
   
digraph FST {
rankdir = LR;
size = "8.5,11";
label = "";
center = 1;
orientation = Landscape;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0", shape = circle, style = bold, fontsize = 14]
	0 -> 0 [label = "red/0.5", fontsize = 14];
	0 -> 1 [label = "green/0.3", fontsize = 14];
1 [label = "1", shape = circle, style = solid, fontsize = 14]
	1 -> 2 [label = "blue", fontsize = 14];
	1 -> 2 [label = "yellow/0.6", fontsize = 14];
2 [label = "2/0.8", shape = doublecircle, style = solid, fontsize = 14]
}


