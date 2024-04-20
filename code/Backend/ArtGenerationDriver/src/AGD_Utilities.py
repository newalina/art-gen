import td;
import sys;




def onDone(timerOp, segment, interrupt):
	sys.stdout.write("TRACE: TouchDesigner Closing...\n");
	quit();
	return

def onStart(*args):

	if(len(args) > 0):
		sys.stdout.write("ERROR: More than 0 args: " + str(args) + "\n");
	
	td.op("AGD_LaunchGeneration").run()