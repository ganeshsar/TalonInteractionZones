# this is a standalone utility which will parse PDFs into configuration files and image
# Must run a standalone script
if __name__ == "__main__":
    
    CORRECT_FOLDER_NAME = "GanzInteractionZones"
    
    import fitz  # PyMuPDF
    from PIL import Image
    import io
    import os

    def rgb2hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    def rgb2hex(c):
        return '#{:02x}{:02x}{:02x}'.format(c[0], c[1], c[2])
    def get_nice_text(s)->str:
        return s.encode("ascii","ignore").decode()
    def go_back_directory(path):
        return os.path.normpath(path + os.sep + os.pardir)

    def sort_by_len(s:str):
        return len(s)

    class Entry:
        def __init__(self,c, r, t) -> None:
            self.bgColour = c
            self.rect = r
            self.text = t
            pass
        
        def get_color_id(self)->str:
            return "%sff"%rgb2hex(self.bgColour)
        def get_text(self) -> str:
            return self.text
        
    def sort_by_entry(e:Entry):
        return e.rect.y0

    def get_rescaled_image(im:Image, width,height):
        return im.resize((width,height),Image.Resampling.NEAREST)
    
    def rescale_image(path,width,height,saveto):
        img = Image.open(path)
        sfx=width/img.width
        sfy=height/img.height
        
        txt="%s.txt"%(path[:len(path)-4])
        newData=""
        with open(txt,"r") as f:
            lines = f.readlines()
            for l in lines:
                if l[0]=="#":
                    data = l.replace("\n",'').split('|')
                    color = data[0]
                    xy = data[1].replace('(','').replace(')','').split(',')
                    centre=(float(xy[0])*sfx,float(xy[1])*sfy)
                    newData+="%s|%s\n"%(color,centre)
                    continue
                newData+=l
        with open(txt,'w') as f:
            f.write(newData)
            print("Rescaled config...")
        
        rescaled = get_rescaled_image(img,width,height)
        rescaled.save(saveto)
                    

    def parse_pdf(input_pdf, output_png, output_txt):
        # Open the PDF
        doc = fitz.open(input_pdf)
        
        page = doc.load_page(0)

        text = get_nice_text(page.get_text(sort=True))
        texts = text.split("\n")
        texts.sort(key = sort_by_len,reverse = True)

        pixmap = page.get_pixmap()
        
        colorEntriesMap = dict()
        consumedRectangles = set()
        for t in texts:
            if t.isspace() or t == '':
                continue
            rectangles = page.search_for(t)
            if rectangles==None:
                print("Failed to find")
                continue
            
            for rect in rectangles:
                if rect in consumedRectangles:
                    continue
                breaker = True
                for r in consumedRectangles:
                    if r.contains(rect):
                        breaker=False
                        break
                if not breaker:
                    continue
                
                pixel = pixmap.pixel(round(rect.x0),round(rect.y0))
                pixel2 = (pixel[0]/255, pixel[1]/255, pixel[2]/255)
                
                #page.draw_rect(rect,fill=pixel2)
                rect.x0-=0.5
                rect.x1+=0.5
                rect.y0-=0.5
                rect.y1+=0.5
                pixmap.set_rect(rect,pixel)

                if pixel not in colorEntriesMap:
                    colorEntriesMap[pixel]=list()
                colorEntriesMap[pixel].append(Entry(pixel,rect,t))
                consumedRectangles.add(rect)
                break
                
        # group together the text to form the config file
        with open(output_txt,"w+") as file:
            for c in colorEntriesMap:
                colorEntriesMap[c].sort(key = sort_by_entry)
                point = (colorEntriesMap[c][0].rect.x0, colorEntriesMap[c][0].rect.y0)
                file.write("%sff|%s\n"%(rgb2hex(c),str(point)))
                for e in colorEntriesMap[c]:
                    file.write("%s\n"%e.get_text())
                file.write("\n")
                
        # Save the page as a PNG
        pix = pixmap#.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        img = img.convert("RGBA")
        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255) or pixdata[x, y] == (0, 0, 0, 255):
                    pixdata[x, y] = (0, 0, 0, 0)
            
        img.save(output_png)

    currentDirectory =go_back_directory(__file__)
    print("Working directory %s"%currentDirectory)

    while True:
        v = input("1) Parse Pdf\n2) Resize All Images\n")
    
        correctDir = "%s%s%s%s"%(go_back_directory(go_back_directory(currentDirectory)),os.sep, CORRECT_FOLDER_NAME,os.sep)
        if not os.path.exists(correctDir):
            print("%s: path not found, move parser into a correct subdirectory..."%correctDir)
            continue
        
        if v=='1':
            v = input("Enter the name of the file without extensions (or nothing for default): ")
            if v.isspace() or v=="":
                v="default"
            path="%s%s%s.pdf"%(currentDirectory,os.sep,v)
            if not os.path.exists(path):
                print("%s: file not found."%path)
                continue
            targetpng = "%s%s.png"%(correctDir,v)
            targettxt = "%s%s.txt"%(correctDir,v)
            parse_pdf(path,targetpng, targettxt)
            print("\nSuccess, wrote to %s\n"%targetpng[:len(targetpng)-4])
        if v=='2':
            v = input("Enter resize target (width x height): ")
            v = v.replace(' ','').split('x')
            width=int(v[0])
            height=int(v[1])
            files = os.listdir(correctDir)
            for f in files:
                if f.endswith(".png"):
                    p = os.path.join(correctDir, f)
                    rescale_image(p,width,height,p)
                    print("\nRescaled %s\n"%p)