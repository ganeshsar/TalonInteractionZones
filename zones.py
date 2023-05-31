from talon.skia import Paint
import time
from .helpers import rgba2hex,TriggerType
from .settings import *

class Zone:
    def __init__(self,color,centre,name,ttype,action,warmup,repeatTime,modifiers) -> None:
        self.color=color
        self.centre=centre
        self.name=name
        self.triggerType=ttype
        self.action=action
        self.warmup=warmup
        self.repeatTime=repeatTime
        self.modifiers = modifiers
        
        self.modifierStartAwake = "start awake" in modifiers
        # at present the below modifier has no effect, for now all zones block input, makes it easier to use zoom mouse
        # 'allow input' might be a better modifier
        self.modifierBlockInput = "block input" in modifiers
        
        self.wasHovering = False
        self.startTimer = 0
        if self.modifierStartAwake:
            self.repeatTimer=0
        else:
            self.repeatTimer=float("inf")
        self.textColor=rgba2hex(255,255,255,ZONES_TEXT_ALPHA)
        self.sinceInteractedTimer = 0
        
    def interact(self):
        self.sinceInteractedTimer = time.time()
   
    def fire_interaction(self, action:str): 
        from .master import primative_interaction     
        primative_interaction(action)
                  
    def update(self,isHovering:bool):
        if self.wasHovering!=isHovering:
            self.on_hover_change(isHovering)
            
        self.textColor = rgba2hex(255,255,255,ZONES_TEXT_ALPHA)
        if time.time() - self.sinceInteractedTimer <= min(0.5, max(self.repeatTime,0.15))-0.05:
            self.textColor = rgba2hex(255,0,0,ZONES_TEXT_ALPHA)
                    
        self.wasHovering=isHovering
    
    def on_hover_change(self,isHovering:bool):
        if self.triggerType != TriggerType.HOVER:
            return
        pass
    
    def click(self):
        return
        if not self.configured:
            return
        # immediately set up the conditions for interaction to occur in the update method
        if self.type==TriggerType.CLICK:
            self.dirtyTrigger = True    
            self.startTimer = time.time()
            self.repeatTimer = 0
        pass
    
    def draw(self, canvas):
        
        paint = canvas.paint
        paint.text_align = canvas.paint.TextAlign.LEFT
        paint.textsize = 25
        paint.color = self.textColor
        paint.style = Paint.Style.FILL
        text = self.name
        tr = paint.measure_text(text)[1]
        
        x=self.centre[0]
        y=self.centre[1]
        
        canvas.draw_text(text,x,y-tr.y)
        pass
    
    def deactivate(self):
        self.repeatTimer=float("inf")
        self.startTimer=float("inf")
        pass  
    
    def clear_timers(self):
        self.repeatTimer=float("inf")
        self.startTimer=float("inf")
    def start_timers(self):
        self.startTimer = time.time()
        self.repeatTimer = 0
    
class TriggerZone(Zone):
    def __init__(self, color, centre, name, ttype, action, warmup, repeatTime,modifiers:str,action2) -> None:
        super().__init__(color, centre, name, ttype, action, warmup, repeatTime,modifiers)
        self.action2 = action2
        self.triggerValue = False
        self.dirtyTrigger=False
        self.modifierForceOffRepeat = "force off repeat" in modifiers.lower()
        self.modifierForceOnRepeat = "force on repeat" in modifiers.lower()
        
    def interact(self):
        super().interact()
        
        if self.dirtyTrigger:
            self.triggerValue = not self.triggerValue
            self.dirtyTrigger = False
        
        if self.triggerValue:
            self.fire_interaction(self.action)
        else:
            self.fire_interaction(self.action2)
            
    def update(self, isHovering: bool):
        super().update(isHovering)   
        
        if (self.triggerValue):
            self.textColor = rgba2hex(255,0,0,255)

        if (time.time()-self.repeatTimer>=self.repeatTime and time.time()-self.startTimer>=self.warmup):            
            self.interact()
            
            if self.triggerValue==True:
                if (self.repeatTime>0 or self.modifierForceOnRepeat):
                    self.repeatTimer = time.time()
                else:
                    self.clear_timers()
                    
            if self.triggerValue==False:
                if (not self.modifierForceOffRepeat):
                    self.clear_timers()
                        
    def on_hover_change(self,isHovering: bool):
        super().on_hover_change(isHovering)
        if self.triggerType != TriggerType.HOVER:
            return
        
        if isHovering:
            self.dirtyTrigger=True
            self.start_timers()
        else:
            if time.time()-self.startTimer<self.warmup:
                self.dirtyTrigger=False
                if not self.modifierForceOffRepeat and not self.triggerValue:
                    self.clear_timers()
            
    def click(self):
        super().click()
        if self.triggerType!=TriggerType.CLICK:
            return
        self.dirtyTrigger=True
        self.start_timers()

    def deactivate(self):
        super().deactivate()
        if self.triggerValue == True:
            self.dirtyTrigger = True
            self.interact()

class SimpleZone(Zone):
    def __init__(self, color, centre, name, ttype, action, warmup, repeatTime,modifiers:str) -> None:
        super().__init__(color, centre, name, ttype, action, warmup, repeatTime,modifiers)
        
    def interact(self):
        super().interact()
    
        self.fire_interaction(self.action)
            
    def update(self, isHovering: bool):
        super().update(isHovering)   

        if (time.time()-self.repeatTimer>=self.repeatTime and time.time()-self.startTimer>=self.warmup):            
            self.interact()
            
            if self.triggerType==TriggerType.HOVER:
                self.repeatTimer = time.time()
            else:
                self.clear_timers()
                        
    def on_hover_change(self,isHovering: bool):
        super().on_hover_change(isHovering)
        if self.triggerType != TriggerType.HOVER:
            return
        
        if isHovering:
            self.start_timers()
        else:
            self.clear_timers()
            
    def click(self):
        super().click()
        if self.triggerType!=TriggerType.CLICK:
            return
        self.start_timers()

    
