import plotly
import os
import numpy as np
from PIL import Image


plotly.tools.set_credentials_file(username='superrostom', api_key='lr1c37zw81')

ListFD = ['2.0', '2.3',  '2.5']
ListSD = ['4', '5']
ListFracture = ['1', '2']
ListDis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50]


DataTable=np.zeros(((len(ListDis)*len(ListSD)*len(ListFracture)*len(ListFD)),4))
K = 0

for FD in range(0, len(ListFD)):
    for SD in range(0, len(ListSD)):
        for LF in range(len(ListFracture)):
            for x in ListDis:

                f = open(
                    '/home/miller/PycharmProjects/synthetic:fracture/database experiments/FractureDataSet.FD.' + ListFD[
                        FD] + '/FractureDataSet.SD.' + ListSD[SD] + '/Fracture' + ListFracture[
                        LF] + '/fracture.top.frt', 'r')
                mine = ''
                for line in f:
                    line = line.strip()
                    line = line.replace('  ', ',')  # a method to remove spaces and make the file readable
                    line = line.replace(' ', ',')
                    line = line.replace(',,', ',')
                    mine = mine + line + '\n'

                text_file = open("Output3.txt", "w")
                text_file.write(mine)
                text_file.close()

                mylist = np.genfromtxt('Output3.txt', delimiter=',')  # generate a list from the file

                pic = np.asarray(mylist)  # covert list into array
                b = np.zeros(2)  # number of columns
                b = np.shape(pic)  # my invention to get the columns and rows
                print(b)

                # displacement in x direction
                y = 0  # displacement in y direction

                os.mkdir(
                    '/home/miller/PycharmProjects/synthetic:fracture/Result data base3/FractureDataSet.FD.' + ListFD[
                        FD] + '/FractureDataSet.SD.' + ListSD[SD] + '/Fracture' + ListFracture[
                        LF] + '/displacement' + str(x))

                uppersurface = np.zeros([int(b[0] / 2), int(b[1] / 2)], dtype=float)  # upper surface  that will move
                lowersurface = np.zeros([int(b[0] / 2), int(b[1] / 2)], dtype=float)  # lower surface

                for i in range(int(b[0] / 2)):
                    for g in range(int(b[1] / 2)):
                        uppersurface[i, g] = pic[i + x, g + y]  # at different x uppersurface will read diferent sufrace
                        lowersurface[i, g] = pic[i, g]
                print(np.min(uppersurface))
                print(np.min(lowersurface))

                uppersurface = uppersurface + 1
                lowersurface = lowersurface + 1

                subtract = uppersurface - lowersurface
                print(subtract)

                print(np.min(subtract))

                uppersurface = uppersurface - np.min(subtract)
                aperture = uppersurface - lowersurface
                print(np.min(aperture))

                indices = np.where(aperture == aperture.min())
                print(indices[0])

                Openning = (uppersurface - lowersurface).sum()

               # Upperblock = uppersurface.sum()
                #Lowerblock = lowersurface.sum()
                porosity = Openning / (134217728)# divided by an arbitrary volume 512*512*512 pixels

                DataTable[K,0]= float(ListFD[FD])
                DataTable[K,1]= float(ListSD[SD])

                DataTable[K,2]=x
                DataTable[K,3]=porosity
                K= K+1

                el = int(np.max(uppersurface) + np.min(lowersurface)) + 10

                geometery = np.full([el + 2, (int(b[1] / 2) + 2), (int(b[0] / 2)) + 2], 2)

                for g in range(int(b[0] / 2)):
                    photo_pix = np.zeros([el, int(b[1] / 2)], dtype=np.uint8)
                    row = np.zeros(int(b[1] / 2))
                    row1 = np.zeros(int(b[1] / 2))
                    for i in range(int(b[1] / 2)):
                        row[i] = lowersurface[g, i]
                        row1[i] = uppersurface[g, i]

                    for i in range(int(b[1] / 2)):
                        z = int(row[i])
                        z1 = int(row1[i])

                        for q in range(z + 5, z1 + 5):
                            photo_pix[q, i] = 255

                            geometery[q + 1, i + 1, g + 1] = 0

                    img = Image.fromarray(photo_pix)
                    img.save(
                        '/home/miller/PycharmProjects/synthetic:fracture/Result data base3/FractureDataSet.FD.' + ListFD[
                            FD] + '/FractureDataSet.SD.' + ListSD[SD] + '/Fracture' + ListFracture[
                            LF] + '/displacement'  + str(x) + '/PhotoFracture' + str(
                            g) + '.png')

                lg = int(b[0] / 2)
                li = int(b[1] / 2)

                for g in range(1, lg + 1):
                    for i in range(1, li + 1):
                        for q in range(1, el + 1):
                            if geometery[q, i, g] == 0:

                                if geometery[q + 1, i, g] == 2:
                                    geometery[q + 1, i, g] = 1

                                if geometery[q + 1, i, g + 1] == 2:
                                    geometery[q + 1, i, g + 1] = 1

                                if geometery[q + 1, i, g - 1] == 2:
                                    geometery[q + 1, i, g - 1] = 1

                                if geometery[q + 1, i + 1, g] == 2:
                                    geometery[q + 1, i + 1, g] = 1

                                if geometery[q + 1, i + 1, g + 1] == 2:
                                    geometery[q + 1, i + 1, g + 1] = 1

                                if geometery[q + 1, i + 1, g - 1] == 2:
                                    geometery[q + 1, i + 1, g - 1] = 1

                                if geometery[q + 1, i - 1, g] == 2:
                                    geometery[q + 1, i - 1, g] = 1

                                if geometery[q + 1, i - 1, g + 1] == 2:
                                    geometery[q + 1, i - 1, g + 1] = 1

                                if geometery[q + 1, i - 1, g - 1] == 2:
                                    geometery[q + 1, i - 1, g - 1] = 1

                                #####

                                if geometery[q, i, g + 1] == 2:
                                    geometery[q, i, g + 1] = 1

                                if geometery[q, i, g - 1] == 2:
                                    geometery[q, i, g - 1] = 1

                                if geometery[q, i + 1, g] == 2:
                                    geometery[q, i + 1, g] = 1

                                if geometery[q, i + 1, g + 1] == 2:
                                    geometery[q, i + 1, g + 1] = 1

                                if geometery[q, i + 1, g - 1] == 2:
                                    geometery[q, i + 1, g - 1] = 1

                                if geometery[q, i - 1, g] == 2:
                                    geometery[q, i - 1, g] = 1

                                if geometery[q, i - 1, g + 1] == 2:
                                    geometery[q, i - 1, g + 1] = 1

                                if geometery[q, i - 1, g - 1] == 2:
                                    geometery[q, i - 1, g - 1] = 1

                                    #######
                                if geometery[q - 1, i, g] == 2:
                                    geometery[q - 1, i, g] = 1

                                if geometery[q - 1, i, g + 1] == 2:
                                    geometery[q, i, g + 1] = 1

                                if geometery[q - 1, i, g - 1] == 2:
                                    geometery[q - 1, i, g - 1] = 1

                                if geometery[q - 1, i + 1, g] == 2:
                                    geometery[q - 1, i + 1, g] = 1

                                if geometery[q - 1, i + 1, g + 1] == 2:
                                    geometery[q - 1, i + 1, g + 1] = 1

                                if geometery[q - 1, i + 1, g - 1] == 2:
                                    geometery[q, i + 1, g - 1] = 1

                                if geometery[q - 1, i - 1, g] == 2:
                                    geometery[q, i - 1, g] = 1

                                if geometery[q - 1, i - 1, g + 1] == 2:
                                    geometery[q - 1, i - 1, g + 1] = 1

                                if geometery[q - 1, i - 1, g - 1] == 2:
                                    geometery[q - 1, i - 1, g - 1] = 1

                List = []

                for g in range(1, lg + 1):
                    for i in range(1, li + 1):
                        for q in range(1, el + 1):
                            List.append(geometery[q, i, g])

                print(geometery.shape)

                print(lg, li, el)

                out = np.savetxt(
                    '/home/miller/PycharmProjects/synthetic:fracture/Result data base3/FractureDataSet.FD.' + ListFD[
                        FD] + '/FractureDataSet.SD.' + ListSD[SD] + '/Fracture' + ListFracture[
                        LF] + '/displacement'  + str(x) + '/DatFileForSimulation ' + '-' + str(li) + '-' + str(
                        el) + '-' + str(
                        lg) + '.dat', List, fmt='%d', delimiter='\n')

        ExportData = np.savetxt('./Experiment3Data.txt', DataTable, delimiter=' ')