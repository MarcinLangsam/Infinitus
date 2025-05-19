import player,fight, text_pop as tp, os
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class Settings_menu(Screen):
    def exit(self):
        quit()
    def save_game(self):
        save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
        f = open(save_path,"w")
        characters = ["player.main_player","player.companion1","player.companion2"]
        for x in range(0,len(player.team)):
           f.write(characters[x]+'.head = "'+str(player.team[x].head)+'"\n')
           f.write(characters[x]+'.name = "'+str(player.team[x].name)+'"\n')
           f.write(characters[x]+'.lv = '+str(player.team[x].lv)+'\n')
           f.write(characters[x]+'.MAX_HP = '+str(player.team[x].MAX_HP)+'\n')
           f.write(characters[x]+'.MAX_MP = '+str(player.team[x].MAX_MP)+'\n')
           f.write(characters[x]+'.MP_regen = '+str(player.team[x].MP_regen)+'\n')
           f.write(characters[x]+'.HP = '+str(player.team[x].HP)+'\n')
           f.write(characters[x]+'.MP = '+str(player.team[x].MP)+'\n')
           f.write(characters[x]+'.STR_base = '+str(player.team[x].STR_base)+'\n')
           f.write(characters[x]+'.DEX_base = '+str(player.team[x].DEX_base)+'\n')
           f.write(characters[x]+'.INT_base = '+str(player.team[x].INT_base)+'\n')
           f.write(characters[x]+'.weapon = '+str(player.team[x].weapon)+'\n')
           f.write(characters[x]+'.damage_base = '+str(player.team[x].STR_base+player.team[x].weapon)+'\n')
           f.write(characters[x]+'.defence_base = '+str(player.team[x].defence_base)+'\n')
           f.write(characters[x]+'.crit_chance_base = '+str(player.team[x].DEX*0.01)+'\n')
           f.write(characters[x]+'.dodge_chance_base = '+str(player.team[x].DEX*0.02)+'\n')
           f.write(characters[x]+'.EXP_boost = '+str(player.team[x].INT*0.01)+'\n')
           f.write(characters[x]+'.EXP = '+str(player.team[x].EXP)+'\n')
           f.write(characters[x]+'.EXP_To_Lv = '+str(player.team[x].EXP_To_Lv)+'\n')
           f.write(characters[x]+'.stat_points = '+str(player.team[x].stat_points)+'\n')
           f.write(characters[x]+'.skill_points = '+str(player.team[x].skill_points)+'\n')
           f.write(characters[x]+'.potions = '+str(player.team[x].potions)+'\n')
           f.write(characters[x]+'.potion_effect = "'+str(player.team[x].potion_effect)+'"\n')
           f.write(characters[x]+'.current_potions = '+str(player.team[x].current_potions)+'\n')
           for y in player.team[x].skill:
               temp = str(player.team[x].skill[y][3]).replace("\n","\\n")
               temp2 = str(player.team[x].skill[y][0]).replace("\n","\\n")
               f.write(characters[x]+'.skill["'+y+'"] = ["'+temp2+'",'+str(player.team[x].skill[y][1])+',"'+str(player.team[x].skill[y][2])+'","'+temp+'","'+str(player.team[x].skill[y][4])+'","'+str(player.team[x].skill[y][5])+'","'+str(player.team[x].skill[y][6])+'","'+str(player.team[x].skill[y][7])+'","'+str(player.team[x].skill[y][8])+'"]\n')
           f.write(characters[x]+'.inventory["main_hand"][2] = "'+str(player.team[x].inventory["main_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["off_hand"][2] = "'+str(player.team[x].inventory["off_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["armor"][2] = "'+str(player.team[x].inventory["armor"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory"][2] = "'+str(player.team[x].inventory["accessory"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory2"][2] = "'+str(player.team[x].inventory["accessory2"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory3"][2] = "'+str(player.team[x].inventory["accessory3"][2])+'"\n')
           f.write(characters[x]+'.inventory["potion"][2] = "'+str(player.team[x].inventory["potion"][2])+'"\n')
        for x in range(0,48):
            f.write('player.main_player.inventory['+str(x)+'][2] = "'+(player.current_player.inventory[x][2])+'"\n')
        f.write("fight.current_fight="+str(fight.current_fight)+"\n")
        f.write("fight.current_stage="+str(fight.current_stage)+"\n")
        if len(player.team)==2:
            f.write("player.team.append(player.companion1)\n")
        if len(player.team)==3:
            f.write("player.team.append(player.companion2)")
        f.write("player.gold = "+str(player.gold))
        f.close()
        Clock.schedule_once(tp.clear_pop_up,2)
