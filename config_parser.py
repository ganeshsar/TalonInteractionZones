from .zones import Zone, TriggerZone,SimpleZone
from .helpers import is_float,TriggerType,ZoneType

def is_line_newzone(l:str) -> bool:
    return l[0]=='#'

def is_line_endzone(l:str) -> bool:
    return l[0].isspace()

def parse_zone(data:str) -> Zone:
    
    try:
        l = data.split("\n")
        
        if l[0][0]=='#':
            data = l[0].replace("\n",'').split('|')
            color = data[0]
            xy = data[1].replace('(','').replace(')','').split(',')
            centre=(float(xy[0]),float(xy[1]))
        else:
            raise Exception("failed to get zone color")
            
        i = 1
            
        name = l[i]

        if l[i+1].lower()[:8]=="on hover":
            triggerType=TriggerType.HOVER
        elif l[i+1].lower()[:8]=="on click":
            triggerType=TriggerType.CLICK
        else:
            raise Exception("failed to parse zone type")
        
        if l[i+1].lower()[9:16]=="trigger":
            action=l[i+2]
            action2=l[i+3]
            zoneType = ZoneType.TRIGGER
        else:
            action=l[i+2]
            zoneType = ZoneType.SIMPLE
        
        timeLoc = 17 if zoneType == ZoneType.TRIGGER else 9
        timings = l[i+1].lower()[timeLoc:]
        timing_phrases = timings.split(' ')
        warmup=0
        repeatTime=0
        if len(timing_phrases) >= 1:
            if is_float(timing_phrases[0]):
                warmup=float(timing_phrases[0])
        if len(timing_phrases) >= 2:
            if is_float(timing_phrases[1]):
                repeatTime=float(timing_phrases[1])
            
        modifiers=""
        elen = 6 if zoneType == ZoneType.TRIGGER else 5
        if len(l)>=elen:
            modifiers=l[elen-1]
            
        if zoneType==ZoneType.TRIGGER:
            return TriggerZone(color,centre,name,triggerType,action,warmup,repeatTime,modifiers,action2)
        if zoneType==ZoneType.SIMPLE:
            return SimpleZone(color,centre,name,triggerType,action,warmup,repeatTime,modifiers)
    
    except Exception as ex:
        print(str(ex))
        return None
    pass
