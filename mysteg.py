from PIL import Image

  
def cover_img(img):
    img_width,img_height= img.size
    img_c=Image.new('RGB',(img_width*2,img_height*2),color=0)
    cpixels=img_c.load()
    for h in range(img_width):
        for l in range(img_height):
            x,y=2*h,2*l
            cpixels[x,y]=img.getpixel((h,l))
    for h in range(img_width-1):
        for l in range(img_height-1):
            x,y=2*h,2*l
            omin=min(cpixels[x,y][0],cpixels[x+2,y][0],cpixels[x,y+2][0],cpixels[x+2,y+2][0])
            omax=max(cpixels[x,y][0],cpixels[x+2,y][0],cpixels[x,y+2][0],cpixels[x+2,y+2][0])
            # print("omin ",omin,"omax ", omax)
            # cpixels[x,y+1][0]=int((omax+(cpixels[x,y][0]+cpixels[x,y+2][0])/2)/2)
            # cpixels[x+1,y][0]=int((omax+(cpixels[x,y][0]+cpixels[x+2,y][0])/2)/2)
            # cpixels[x+1,y+1][0]=int((cpixels[x+1,y][0]+cpixels[x,y+1][0])/2)
    
    return img_c

def encode():
    img = input("Enter image name(with extension): ")
    img_i = Image.open(img, 'r')
    img_width,img_height= img_i.size

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
	    raise ValueError('Data is empty')

    # make Original image
    img_o=img_i.resize((int(img_width/2),int(img_height/2)))
    # make Cover image
    img_c=cover_img(img_o)
    img_c.save("coverimg.jpg")
    
	
    
def decode():
    img = input("Enter image name(with extension): ")
    img_i = Image.open(img, 'r')
    print("steg")

# Main Function		 
def main(): 
	a = int(input("1. Encode\n2. Decode\n")) 
	if (a == 1): 
		encode()
	elif (a == 2): 
		decode()
	else: 
		raise Exception("Enter correct input") 
		
# Driver Code 
if __name__ == '__main__' : 
	main() 