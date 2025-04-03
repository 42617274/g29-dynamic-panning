import time
import pygame
import socket
import ctypes

# Voicemeeter settings
VOICEMEETER_IP = "192.168.1.14"
VOICEMEETER_PORT = 6980  # Default VBAN port
DEADZONE = 0.1  # Deadzone to avoid unintended variations
vmr = ctypes.cdll.LoadLibrary(r"C:\Program Files (x86)\VB\Voicemeeter\VoicemeeterRemote.dll")


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def init_voicemeeter():
    vmr.VBVMR_Login()


def set_micro_pan(pan_value):
    pan_value = max(-1, min(1, pan_value))  # Ensure values are between -1 and 1
    vmr.VBVMR_SetParameterFloat(b"Stripe[0].Pan_x", ctypes.c_float(pan_value))  # Apply to the bus
    print(f"✅ Panning updated : {pan_value:.2f}")
    
def apply_deadzone(value, deadzone):
    return value if abs(value) > deadzone else 0

def main():
    
    log("🕹 Init Voicemeeter...")
    init_voicemeeter()
    log("🕹 Init Pygame...")
    pygame.init()
    pygame.joystick.init()

    joystick_count = pygame.joystick.get_count()
    log(f"🔍 Joystick count : {joystick_count}")

    if joystick_count == 0:
        log("❌ No wheel detected.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    log(f"🎮 wheel detected : {joystick.get_name()}")

    log("🎙️ Synchronization between wheel and panning...")

    while True:
        pygame.event.pump()  # Update joystick events

        clutch = joystick.get_axis(3)  # Clutch axis
        accel = joystick.get_axis(1)   # Accelerator axis

        # Apply deadzone to avoid small unwanted movements
        clutch = apply_deadzone(clutch, DEADZONE)
        accel = apply_deadzone(accel, DEADZONE)

        # Panning calculation
        pan = clutch - accel  
        pan = max(-1, min(1, pan))  # Clamp between -1 and 1
        
        #log(f"🎛️ Pedal status - Clutch: {clutch:.2f} | Accelerator: {accel:.2f} | Balance: {pan:.2f}")
        set_micro_pan(pan)  # Apply balance to the microphone
        
        time.sleep(0.1)  # Pause to avoid CPU overload

if __name__ == "__main__":
    log("🚀 Launching script...")
    main()
