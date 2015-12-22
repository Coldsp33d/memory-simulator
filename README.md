# Memory Simulator
MU0 {compiler, execution program} with memory management simulation.

***_Disclaimer: The memory simulator has been designed and tested only on Ubuntu._***
## _Shortened Summary (for experienced users)_ 
* _**STEP 1**_ Run the program with the following command:
```python3 __main__.py ```
* _**STEP 2**_ Provide input either through files or through the in- built high-level to MU0 code compiler

* _**STEP 3**_ Set the run-time conditions by filling in the appropriate fields and check boxes (do not enable prefetching if you choose to use the Clock algorithm)

* _**STEP 4**_ Execute instructions through the use of STEP, RUN, PAUSE, or start from the beginning with RESET

## _Detailed HOWTO_
1. ### _STEP 1_ Starting the simulator
 Navigate to the directory containing all the memory simulator files, and run the file client.py using the command
 ```python3 __main__.py```
 Note that the client program must be run with Python v3.4 or later. Proceed to Step 2.

2. ### _STEP 2_ Providing input
 A message box pops up asking you two choose whether to (i) input MU0 programs through file storage, or (ii) write your own high-level language program. On clicking (i), proceed to OPTION A of this step. Otherwise, for (ii), proceed to OPTION B.
 ##### OPTION A: Providing readily availble input files 
 Using this option, you can choose one or more text files containing pure MU0 instruction code. The simulator assumes that these files are syntactically correct - the simulator does not check for errors in the assembly code.
 Click on the Browse button to select files, and then proceed to Step 3.
 ##### OPTION B: Compiling high level code into MU0 code
 This option invokes the compiler, which consists of the following:
  *	A large white console through enters high level instructions
  *	HELP button provides the user with all details regarding the nature of the high-level language instructions and constructs that the compiler generates target code for. The nature of the high level language is enumerated in Section 6.1.1 in System Design.
  *	COMPILE button that compiles the code entered inside the console. Compilation result is desplayed inside the ERROR STATUS window. A program can be compiled any number of times until CONTINUE is pressed
  *	ERROR STATUS window indicates whether the last compilation process caused any errors or not
  *	CLEAR SCREEN button 
  *	CONTINUE button, to be clicked only when the last compilation caused no errors and the user is satisfied with his or her program, and
  *	QUIT button to exit the simulator.
 
 Enter code into the console, click on COMPILE, and then, if there are no errors in the code, click on CONTINUE. Proceed to Step 3.

3. ### _STEP 3_ Setting run-time conditions
 Set run-time conditions:
  * "Choose the no. of physical memory frames": The size of the memory can be set to 4, 8, or 16.
  * "Enter timeout period": This is the timeslice given to each process for Round Robin scheduling, measured in terms of instructions executed (assuming each instruction takes one unit time to execute in an ideal system).
  * "Choose your replacement algorithm": You can choose one of FIFO, Random, Clock, LRU, or Optimal. Only the Clock algorithm does not support prefetching.
  
 Once all the conditions have been set, click on Submit and proceed to Step 4.

4. ### _STEP 4_ Executing the program(s)
 The new window that is created after completing Step 3 displays a lot of options, enumerated below:
  *	RESET button, to exit the current session and restart. On clicking this button, the user has the option to return to either Step 1 or Step 3
  *	STEP button which only performs ONE action at a time (either instruction execution, page swapping or process switching)
  *	RUN button causes instructions to run automatically without user intervention. When RUN is pressed, STEP is disabled, and can only be stopped by pressing PAUSE
  *	PAUSE button has the reverse effect of RUN
  *	QUIT button to exit the simulator.
  *	STATUS WINDOW which displays to the user, all relevant information regarding the run-time environment for the current process, the number of page faults, and other information 
 
 To execute the MU0 program(s), simply press STEP or RUN until all processes have completed execution.
 When all processes have terminated, a message box apprears displaying the final status for all processes. Click on OK, and then click on RESET to start again, or QUIT to quit.





