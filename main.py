import numpy as np
import cv2
from shutil import copyfile

import os
import re
i=1
def ReadBin(fn):
    H = 4384
    W = 6576
    # W=4096
    # H=3000
    with open(fn, 'rb+') as f:
        image_data = f.read()
        # print('image_data',image_data)
    img_raw = np.frombuffer(image_data, dtype=np.int16)
    print(img_raw.shape)
    img_raw = img_raw.reshape((H, W))
    img = img_raw.copy()
    print('Over Expose num:', len(img[img > 4090]))
    img=img*(256/(2**12))
    print(img.shape)
    print(img.dtype)
    img=img.astype(np.uint8)
    print(type(img))
    img2=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    return img


def Generate():
    data = []
    for i in range(7):
        path = f'./InPut/7_bh/{i}.bin'
        print(path)
        img = ReadBin(path)
        if i == 0:
            base_gray = img
        else:
            data.append(img)
        cv2.imwrite(f'./InPut/7_bh/{i}.png',img)
    print('Base_gray shape', base_gray.shape)
    return base_gray, data
def BinTOPng(Paths):

    for path in Paths:
        print(path)
        pathname = path[1].split('.')
        img=ReadBin(path[0]+'\\'+path[1])
        print(path[0],'=======',pathname[0],'========',pathname[1])
        #img=cv2.imread('Test8.png')
        cv2.imwrite(path[0]+f'\\{pathname[0]}.png',img)


def PNG_16bit(Path,Origin=0):
    OriginImg=cv2.imread(Path,cv2.IMREAD_UNCHANGED)
    img=OriginImg.copy()
    print('Load PNG bits:',img.dtype)
    img = img * (256 / (2 ** 12))
    print(img.shape, img.dtype)
    img = img.astype(np.uint8)
    if Origin==0:
        return img
    else:
        return img,OriginImg


def PNGViewer(Dir):
    img=cv2.imread(Dir,cv2.IMREAD_UNCHANGED)
    print(img.dtype,img.shape)
    img=img*256/2**16
    img=img.astype(np.uint8)
    cv2.imwrite('Test8.png',img)
def FindCurrentSubDir(Path):

    SubDir=[]
    for root,dirs,file in os.walk(Path):
        if len(dirs)!=0:
            for dir in dirs:
                SubDir.append(os.path.join(root,dir))

    return SubDir
def FindAllFiles(Path):
    FilesPath=[]
    CompletePath=[]
    for root,dirs,files in os.walk(Path):
        for file in files:
            print(root+'\\'+file)
            if re.match(r'.*\.bin',file) is not None:
                FilesPath.append([root,file])
                CompletePath.append(os.path.join(root,file))
                #print('HERERRRRRRRRRRRRRRR:',root,file)
    return FilesPath,CompletePath
def RenameFile(absolutePath,newname):

    os.renames(absolutePath,newname)
    print(f'Rename {newname} Files!')
    return True
def RenameAllFiles(Path,CompletePath,Format='bin'):

    samepath=Path[0][0]
    #print(samepath)
    index=0
    for  path in Path:
        if samepath!=path[0]:
            samepath = path[0]
            index = 0
        CurrentPathName=os.path.join(samepath,path[1])
        NewPathName=os.path.join(samepath,f'{index}.{Format}')
        if NewPathName not in CompletePath:
            RenameFile(CurrentPathName,NewPathName)
        index+=1


def ReadAllFile(Path):

    size=8
    filePATH=[]
    path=[]
    count=0
    for root,dir,files in os.walk(Path):
        for file in files:
                         #1 _ 1_ 1_5_00_00005_thumbnail.png
            if re.match(r'\d_\d_\d_\d_00_\d*_thumbnail\.png', file) is not None or re.match(r'.*normal.*', file) is not None:
                path.append([root,file])
                count+=1
                if count==size:
                    filePATH.append(path)
                    path=[]
                    count=0

    print(filePATH)
    return filePATH


def PNG_16TO8(savepath, file):
    img ,Origin= PNG_16bit(file[0] + '\\' + file[1],Origin=1)
    filenames = file[1].split('_')

    cv2.imwrite(savepath + f'\\{filenames[3]}.jpg', img)
    cv2.imwrite(savepath + f'\\{filenames[3]}.png', Origin)
    # for path in Paths:
    #     print(path)
    #     pathname = path[1].split('.')
    #     img=PNG_16bit(path[0]+'\\'+path[1])
    #     print(path[0],'=======',pathname[0],'========',pathname[1])
    #     cv2.imwrite(path[0]+f'\\{pathname[0]}.png',img)


def MkdirAndSave(SavePath,files):

    for idx,file in enumerate(files):
        if os.path.exists(SavePath + f'\\{idx}') is False:
            os.mkdir(SavePath + f'\\{idx}')
        for idy ,f in enumerate(file):
            if idy<7:

                PNG_16TO8(SavePath+f'\\{idx}',f)
            else:
                print(SavePath+f'\\{idx}')
                copyfile(f[0]+'\\'+f[1],SavePath+f'\\{idx}\\'+f[1])
def CROP(img,dstX=3500,dstY=3000,Center=1,Height=120,Postion=(0,0)):
    img2 = img.copy()
    # if len(img.shape)==3:
    #     img2=cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)
    if Center==1:
        h, w ,_= img2.shape
        c_y = h / 2
        c_x = w / 2

        img2=img2[int(c_y - dstY / 2): int(c_y + dstY / 2), int(c_x - dstX / 2): int(c_x + dstX / 2),:]
        print(img2.shape)
    elif Center==2:
        x,y=Postion
        img2=img[y:y+Height,x:x+Height,:]


    return img2
def ConvertFromBin(Dir2):


    FilePath,CompletePath=FindAllFiles(Dir2)

    RenameAllFiles(FilePath,CompletePath)
    NewFilePath,_=FindAllFiles(Dir2)

    BinTOPng(NewFilePath)
def ConvertFromPNG(Dir,savepath):

   files=ReadAllFile(Dir)
   MkdirAndSave(savepath,files)


def CropMutiPics():
    Path=r'C:\Users\vrlab\Documents\YklabData\YklabData\PlaneHead\SideToSun\3_6'
    OrignSurface=cv2.imread(Path+'/grad30-13-152-10.png')
    crop_origin=CROP(OrignSurface)
    cv2.imwrite('./CropOutput/origin.png',crop_origin)

    Position=(3311,2557)
    grad=cv2.imread(Path+r'\grad8000-13-152-10.png')
    normal=cv2.imread(Path+r'\normal-_GRAD8000-RS8_13-152-10.png')

    c_crop_origin=CROP(crop_origin,Center=2,Postion=Position)
    c_grad=CROP(grad,Center=2,Postion=Position)
    c_normal = CROP(normal, Center=2, Postion=Position)

    cv2.imwrite('./CropOutput/flaw_origin.png',c_crop_origin)
    cv2.imwrite('./CropOutput/flaw_grad.png', c_grad)
    cv2.imwrite('./CropOutput/flaw_normal.png', c_normal)
if __name__ == '__main__':
    # Dir=r'C:\Users\vrlab\Documents\YklabData\现场数据\12.22\TestHole\left_mid\1\1_1_1_6_00_00006_thumbnail.png'
    Dir=r'C:\Users\vrlab\Documents\YklabData\HistoryData\12.31\TestOnTheBoard'
    Dir = r'C:\Users\vrlab\Documents\YklabData\HistoryData\12.31\TestOnTheBoard\TestOriginData'
    Dir2=r'E:\Comac\1_6\HeadTop\2'
    savepath=r'C:\Users\vrlab\Documents\YklabData\HistoryData\12.31\TestOnTheBoard\TestSave'
    CropDir=r'C:\Users\vrlab\Documents\YklabData\RivetDetection\res3_6.png'
    img=cv2.imread(r'C:\Users\vrlab\Desktop\TestAdaptive\adaptive\vis_mask_before.png')
    #
    # img=CROP(img,Center=2,Height=100,Postion=(205,205))
    # img=cv2.imwrite(r'C:\Users\vrlab\Desktop\TestAdaptive\16_mask_area.png',img)

    CropMutiPics()
   # img2=CROP(img,Center=2,Postion=(1958,1017))
   # cv2.imwrite(f'./CropOutput/4.png',img2)
   # i+=1



