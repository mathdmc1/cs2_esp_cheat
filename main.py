import pymem,pymem.process,keyboard,os
import dumper
from win32api import GetSystemMetrics
import struct
import overlay
import time
import win32api
from colorama import Fore, Style, init
client = dumper.Client()
dwEntityList = client.offset('dwEntityList')
dwLocalPlayerPawn = client.offset('dwLocalPlayerPawn')
m_iIDEntIndex = client.client_dll('C_CSPlayerPawn', 'm_iIDEntIndex')
m_iTeamNum = client.client_dll('C_BaseEntity', 'm_iTeamNum')
m_iHealth = client.client_dll('C_BaseEntity', 'm_iHealth')
m_vOldOrigin=client.client_dll('C_BasePlayerPawn', 'm_vOldOrigin')
dwViewMatrix = client.offset('dwViewMatrix')
try:
    pm = pymem.Pymem("cs2.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
except:
    print("open cs2 and start the program ")
    exit()

def main():
    #########config keys##########
    Clear_mapped_entitys="+"
    Check_team_key="-"
    Exit="*"
    Hide_key="."
    ##############################

    welcome(Clear_mapped_entitys,Check_team_key,Exit,Hide_key)
    check_team=True
    hide=False
    list_entity_mapped=[]
    dibujar = overlay.ScreenDrawer()
    while True:
        if keyboard.is_pressed(Clear_mapped_entitys):
            win32api.Beep(10, 10)
            list_entity_mapped.clear()
            dibujar.root.update()
            print("entitys unmapped")
            time.sleep(0.5)
            continue

        if keyboard.is_pressed(Check_team_key):
            win32api.Beep(100, 10)
            check_team = not check_team
            print(f"check team is: {check_team}")
            time.sleep(0.5)
            continue

        if keyboard.is_pressed(Hide_key):
            win32api.Beep(100, 10)
            hide = not hide
            print(f"hide is: {hide}")
            if hide:
                dibujar.clear()
                dibujar.root.update()
            time.sleep(0.5)
            continue

        if keyboard.is_pressed(Exit):
            win32api.Beep(500, 10)
            print("exit")
            exit()
            
        if hide:
            time.sleep(0.1)
            continue
        dibujar.clear()
        try:
            player = pm.read_longlong(client + dwLocalPlayerPawn)
            playerTeam = pm.read_int(player + m_iTeamNum)
            entityId = pm.read_int(player + m_iIDEntIndex)
            enemys_pos=get_enemys_pos(list_entity_mapped)
            
            view_matrix = pm.read_bytes(client + dwViewMatrix, 64)
            matrix = struct.unpack("16f", view_matrix)
            if enemys_pos!=None:
                for i in enemys_pos:
                        screen_cords = world_to_screen(matrix, (i[0], i[1], i[2]))
                        if screen_cords:
                            dibujar.draw_canvas(int(screen_cords[0]), int(screen_cords[1]),int(screen_cords[2]))
                                      
            entList = pm.read_longlong(client + dwEntityList)
            entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
            entity = pm.read_longlong(entEntry + 112 * (entityId & 0x1FF))
            entityTeam = pm.read_int(entity + m_iTeamNum)
            
            if (entity not in list_entity_mapped) and (entityTeam == 2 or entityTeam == 3) and (entityTeam!=playerTeam or check_team==False):
                list_entity_mapped.append(entity)
        except:
            pass
        
        dibujar.root.update()
        #dibujar.root.mainloop()
def welcome(Clear_mapped_entitys,Check_team_key,Exit,Hide_key):
    os.system("cls" if os.name == "nt" else "clear")
    init(autoreset=True)
    print(f"{Fore.CYAN}═" * 50)
    print(f"{Fore.CYAN} " * 15 + "SOLAR V1")
    print(f"{Fore.CYAN}═" * 50)
    print(f"{Fore.WHITE}Welcome to the program {Fore.CYAN}SOLAR V1")
    print(f"{Fore.YELLOW}Keys:")
    print(f"{Fore.WHITE}-" * 50)
    print(f"{Fore.GREEN}[{Clear_mapped_entitys}] {Fore.WHITE}Clear mapped entitys")
    print(f"{Fore.GREEN}[{Check_team_key}] {Fore.WHITE}Check team")
    print(f"{Fore.GREEN}[{Hide_key}] {Fore.WHITE}Hide overlay")
    print(f"{Fore.GREEN}[{Exit}] {Fore.WHITE}Exit")

    print(Fore.CYAN + "\n" + "═" * 50)
def get_enemys_pos(list_entity_mapped):
    if len(list_entity_mapped) == 0:
        return None
    enemys_pos=[]
    for i in list_entity_mapped:
        if pm.read_int(i + m_iHealth) <= 0 or pm.read_int(i + m_iTeamNum) not in [2, 3]:
            continue
        pos=read_vec3(pm, i + m_vOldOrigin)
        enemys_pos.append(pos)

    return enemys_pos


def read_vec3(pm, addr):
    return (
        pm.read_float(addr),
        pm.read_float(addr + 4),
        pm.read_float(addr + 8)
    )

def world_to_screen(matrix, pos):
    z = pos[0] * matrix[12] + pos[1] * matrix[13] + (pos[2]) * matrix[14] + matrix[15]
    # person behind us
    if z < 0.01:
        return None
    x = pos[0] * matrix[0] + pos[1] * matrix[1] + pos[2] * matrix[2] + matrix[3]
    y = pos[0] * matrix[4] + pos[1] * matrix[5] + pos[2] * matrix[6] + matrix[7]
    xx = x / z
    yy = y / z
    _x = (GetSystemMetrics(0) / 2 * xx) + (xx + GetSystemMetrics(0) / 2)
    _y = (GetSystemMetrics(1) / 2) - (GetSystemMetrics(1) / 2 * yy)
    return _x, _y, z

if __name__ == "__main__":
    main()