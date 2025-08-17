This project aims to control panning (balance left/right of the microphone) using g29 wheel pedals, this is fully working


1 - Install and configure VoiceMeeter to have microphone input in Stripe[0] (First position)

2 - Install needed package for the script (pygame, socket,ctypes,time)

3 - Connect your wheel 

4 - Change VOICEMEETER_IP & VOICEMEETER_PORT if needed

5 - Launch the script 


Issues :
May have to change dll position in this line (for 64 or 32 bits for example ) -> vmr = ctypes.cdll.LoadLibrary(r"C:\Program Files (x86)\VB\Voicemeeter\VoicemeeterRemote.dll")
