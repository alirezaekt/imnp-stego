#Steganography IMNP
#GrayScale Version
from PIL import Image
import math


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def cover_img(img):
    img_width,img_height= img.size
    img_c=Image.new('L',(img_width*2,img_height*2),color=0)
    cpixels=img_c.load()
    for h in range(img_width):
        for l in range(img_height):
            x,y=2*h,2*l
            cpixels[x,y]=img.getpixel((h,l))
    for h in range(img_width-1):
        for l in range(img_height-1):
            x,y=2*h,2*l
            omax=max(cpixels[x,y],cpixels[x+2,y],cpixels[x,y+2],cpixels[x+2,y+2])
            cpixels[x,y+1]=int((omax+(cpixels[x,y]+cpixels[x,y+2])/2)/2)
            cpixels[x+1,y]=int((omax+(cpixels[x,y]+cpixels[x+2,y])/2)/2)
            cpixels[x+1,y+1]=int((cpixels[x+1,y]+cpixels[x,y+1])/2)
    
    return img_c

def steg_img(img,data):
    img_width,img_height= img.size
    spixels=img.load()
    bdata=tobits(data)
    # print("messagein ",bdata)
    dpointer=0
    for h in range(int((img_width/2)-1)):
        for l in range(int((img_height/2)-1)):
            x,y=2*h,2*l
            omin=min(spixels[x,y],spixels[x+2,y],spixels[x,y+2],spixels[x+2,y+2])

            v1=spixels[x,y+1]-omin
            v2=spixels[x+1,y]-omin
            v3=spixels[x+1,y+1]-omin
            # a1
            if v1==0:
                a1=0
            else:
                a1=int(math.log(v1,2))
            if a1>0:
                if (dpointer+a1)<(len(bdata)):
                    dpointer=dpointer+a1
                    sum=0
                    m=1
                    for i in range(a1):
                        sum=sum+(m*bdata[(dpointer)-(i+1)])
                        m=m*2 
                    spixels[x,y+1]=max(spixels[x,y], spixels[x,y+2])-sum
                    
                else:
                    return img
            # a2
            if v2==0:
                a2=0
            else:
                a2=int(math.log(v2,2))
            if a2>0:
                if (dpointer+a2)<(len(bdata)):
                    dpointer=dpointer+a2
                    sum=0
                    m=1
                    for i in range(a2):
                        sum=sum+(m*bdata[(dpointer)-(i+1)])
                        m=m*2 
                    spixels[x+1,y]=max(spixels[x,y], spixels[x+2,y])-sum
                    
                else:
                    return img
            # a3
            if v3==0:
                a3=0
            else:
                a3=int(math.log(v3,2))
            if a3>0:
                if (dpointer+a3)<(len(bdata)):
                    dpointer=dpointer+a3
                    sum=0
                    m=1
                    for i in range(a3):
                        sum=sum+(m*bdata[(dpointer)-(i+1)])
                        m=m*2 
                    spixels[x+1,y+1]=max(spixels[x+1,y], spixels[x,y+1])-sum
                    
                else:
                    return img
            
            
    return img

def encode():
    img = input("Enter image name(with extension): ")
    img_i = Image.open(img, 'r').convert('L')
    img_width,img_height= img_i.size
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
	    raise ValueError('Data is empty')
    # make Original image
    img_o=img_i.resize((int(img_width/2),int(img_height/2)))
    # make Cover image
    img_c=cover_img(img_o)
    img_c.save("coverimg.png") 
    # make Stego image
    img_s=steg_img(img_c,data)
    img_s.save("stegoimg.png")
    print("stegpimg.png created.")
	
    
def decode():
    img = input("Enter image name(with extension): ")
    img_i = Image.open(img, 'r')
    img_width,img_height= img_i.size
    spixels=img_i.load()
    message=[]
    for h in range(int((img_width/2)-1)):
        for l in range(int((img_height/2)-1)):
            x,y=2*h,2*l
            omin=min(spixels[x,y],spixels[x+2,y],spixels[x,y+2],spixels[x+2,y+2])
            omax=max(spixels[x,y],spixels[x+2,y],spixels[x,y+2],spixels[x+2,y+2])
            
            v1=int((omax+(spixels[x,y]+spixels[x,y+2])/2)/2)-omin
            v2=int((omax+(spixels[x,y]+spixels[x+2,y])/2)/2)-omin
            v3=int((int((omax+(spixels[x,y]+spixels[x,y+2])/2)/2)+int((omax+(spixels[x,y]+spixels[x+2,y])/2)/2))/2)-omin
            # a1
            if v1==0:
                a1=0
            else:
                a1=int(math.log(v1,2))
            if a1>0:
                sum = max(spixels[x,y], spixels[x,y+2]) - spixels[x,y+1]
                temp=[0,0,0,0,0,0,0,0]
                for i in range(a1):
                    temp[a1-(i+1)] = sum % 2
                    sum=int(sum/2)
                for i in range(a1):
                    message.append(temp[i])
            # a2
            if v2==0:
                a2=0
            else:
                a2=int(math.log(v2,2))
            if a2>0:
                sum = max(spixels[x,y], spixels[x+2,y]) - spixels[x+1,y]
                temp=[0,0,0,0,0,0,0,0]
                for i in range(a2):
                    temp[a2-(i+1)] = sum % 2
                    sum=int(sum/2)
                for i in range(a2):
                    message.append(temp[i])
            # a3
            if v3==0:
                a3=0
            else:
                a3=int(math.log(v3,2))
            if a3>0:
                sum = max(spixels[x+1,y], spixels[x,y+1]) - spixels[x+1,y+1]
                temp=[0,0,0,0,0,0,0,0]
                for i in range(a3):
                    temp[a3-(i+1)] = sum % 2
                    sum=int(sum/2)
                for i in range(a3):
                    message.append(temp[i])
            
                        
            if len(message)>128:
                # print("messageout ",message)
                print("steg data is: ",frombits(message))
                return

    # print(frombits(message))
            


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