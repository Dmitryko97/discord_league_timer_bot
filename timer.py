import time

def sek_to_time_string(millis: int):
    mins = int(round(millis / 60))
    sek = int(round(millis % 60))
    time_string = ''
    
    if mins < 10 and sek < 10:
        time_string = f'0{mins}:0{sek}'
    elif mins < 10:
        time_string = f'0{mins}:{sek}'
    elif sek < 10:
        time_string = f'{mins}:0{sek}'
    else:
        time_string = f'{mins}:{sek}'

    return time_string

def time_string_to_millis(time_string: str):
    split = time_string.split(':')
    return int(split[0] * 60) + int(split[1])

class timer:

    def __init__(self):
        self.start = time.time()
        self.cooldowns = {'top': [['', 0], ['', 0]], 'jungle': [['', 0], ['', 0]], 'mid': [['', 0], ['', 0]], 'adc': [['', 0], ['', 0]], 'support': [['', 0], ['', 0]]}
        self.spell_cooldowns = {'heal': 240, 'ghost': 180, 'barrier': 180, 'exhaust': 210, 'clarity': 240, 'flash': 300, 'teleport': 360, 'cleanse': 210, 'ignite': 210}
    
    def get_match_time(self) -> int:
        return sek_to_time_string(time.time() - self.start)

    def start_cooldowns_for_spells(self, role: str, spell: str):
        t = time.time()

        if self.cooldowns[role][0][0] == spell:
            self.cooldowns[role][0][1] = t + self.spell_cooldowns[spell]
            
        elif self.cooldowns[role][1][0] == spell:
            self.cooldowns[role][1][1] = t + self.spell_cooldowns[spell]

        elif self.cooldowns[role][0][0] == '':
            self.cooldowns[role][0][0] = spell
            self.cooldowns[role][0][1] = t + self.spell_cooldowns[spell]

        elif self.cooldowns[role][1][0] == '':
            self.cooldowns[role][1][0] = spell
            self.cooldowns[role][1][1] = t + self.spell_cooldowns[spell]

        else:
            self.cooldowns[role][0][0] = spell
            self.cooldowns[role][0][1] = t + self.spell_cooldowns[spell]

    def get_cooldowns_for_spells(self, role: str) -> str:
        t = time.time()
        cd = ''

        for s in self.cooldowns[role]:
            if not(s[0] == ''):
                if s[1] <= t:
                    cd += f'{s[0]}: {sek_to_time_string(0)}\n'
                else:
                    cd += f'{s[0]}: {sek_to_time_string(s[1] - time)}\n'

        return cd
    
    def get_spells_uptime(self, role: str) -> str:
        t = time.time()
        cd = ''

        for s in self.cooldowns[role]:
            if not(s[0] == ''):
                if s[1] <= t:
                    cd += f'{s[0]}: Ready!\n'
                else:
                    cd += f'{s[0]}: {sek_to_time_string((s[1] - self.start))}\n'
        
        return cd
    
    def get_spells_uptime_all(self):
        cd = ''

        for role in ['top', 'jungle', 'mid', 'adc', 'support']:
            cd += f'{role}: \n'
            cd += f'{self.get_spells_uptime(role)}\n'

        return cd
