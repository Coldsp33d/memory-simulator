# Memory Simulator
MU0 {compiler, execution program} with memory management simulation.

***_Disclaimer: The memory simulator has been designed and tested only on Ubuntu._***
## _Shortened Summary (for experienced users)_ 
* _**STEP 1**_ Run the program with the following command:
```python3 __main__.py ```
* _**STEP 2**_ Provide input either through files or through the in- built high-level to MU0 code compiler

* _**STEP 3**_ Set the run-time conditions by filling in the appropriate fields and check boxes

* _**STEP 4**_ Execute instructions through the use of STEP, RUN, PAUSE, or start from the beginning with RESET

## _Detailed HOWTO_
* ### STEP 1 Starting the simulator
Navigate to the directory containing all the memory simulator files, and run the file client.py using the command
```python3 ____main____.py```
Note that the client program must be run with Python v3.4 or later. Proceed to Step 2.

* ### STEP 2 Providing input
A message box pops up asking you two choose whether to (i) input MU0 programs through file storage, or (ii) write your own high-level language program. On clicking (i), proceed to OPTION A of this step. Otherwise, for (ii), proceed to OPTION B.
##### OPTION A: Providing readily availble input files 
Using this option, you can choose one or more text files containing pure MU0 instruction code. The simulator assumes that these files are syntactically correct - the simulator does not check for errors in the assembly code.
Click on the Browse button to select files, and then proceed to Step 3.
##### OPTION B: Compiling high level code into MU0 code
This option invokes the compiler.
Enter code into the console, click on COMPILE, and then, if there are no errors in the code, click on CONTINUE. Proceed to Step 3.

* ### STEP 3 Setting run-time conditions
Follow the instructions to set run-time conditions. Once all the conditions have been set, click on Submit and proceed to Step 4.

* ### STEP 4 Executing the program(s)
The new window that is created after completing Step 3 displays a lot of options.
To execute the MU0 program(s), simply press STEP or RUN until all processes have completed execution.
When all processes have terminated, a message box apprears displaying the final status for all processes. Click on OK, and then click on RESET to start again, or QUIT to quit.





