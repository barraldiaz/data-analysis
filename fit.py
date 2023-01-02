
from matplotlib.pyplot import*
from numpy import*
import pandas as pd
import scipy.optimize as so
import os as os
from sympy import symbols
from sympy import init_session

###############################################################################################################
#Lectura del documento y correccion:
###############################################################################################################
#Si queremos movernos a otro directorio para guardar ahi todo:
#os.chdir('/home/angel/Lab')
'''
#Archivo:
archivo='/home/angel/Lab/data.ods'
data=pd.read_excel(archivo,engine='odf')
#cambiamos los NAN por ceros para que no de error:
data=data.fillna(0)

'''
#Titulos del plot y de los ejes:
title='alfaau.eps';  xaxis='$ \u03B8 (rad)$';  yaxis='$d\sigma/d\Omega (m^{-2}) $'

data=loadtxt('data.txt')

###############################################################################################################
#Ajuste a una funcion:
###############################################################################################################
x=data[:,0]
xerr=data[:,1]
y=data[:,2]
yerr=data[:,3]


def fit(x,y,xerr,yerr):
  
    #Se define la fuincion y los parametros iniciales aproximados:
    def ajuste(x,N,x0):
        f= N/(sin((x-x0)/2))**4
        return f
    init_guess=[0.0001,0.002]

    fit= so.curve_fit(ajuste, x , y , p0=(init_guess) , absolute_sigma=True,method='lm',maxfev=10000)
    ans=fit[0]; cov=fit[1]
    uncer=sqrt(diag(cov))

    #El termino fit[0] es un array con las soluciones:                               
    N,x0 = ans       
    
    #Para las incertidumbres fit[1] es la matriz de covarianza por lo que:							
    sN,sx0 = uncer
    
    #Para graficar creamos puntos de nuestra funcion:
    xm=linspace(min(x)-min(x)/10,max(x)+max(x)/10,5000)
    ym=ajuste(xm,N,x0)

    #CHI CUADRADO:
    chi=0
    for i in range(len(x)):
        chi=chi+(y[i]-ajuste(x[i],N,x0))**2/(yerr[i]**2+ajuste(x[i],N,x0)**2+2*yerr[i]*ajuste(x[i],N,x0))
    chi2=sum(chi)
    #Rutherford
    theta=linspace(-0.7,0.7,10000)
    sigma=(((4*79*1.602E-19)/(16*pi*8.85E-12*5.5E6))**2)*(1/sin(theta/2)**4)*1E28

    sigma2=(((4*79*1.602E-19)/(16*pi*8.85E-12*0.3145E6))**2)*(1/sin((theta)/2)**4)*1E28



    #Funcion representacion:
    fig,ax=subplots()
    #ax.plot(xm,ym,'-k',linewidth=1.2,mew=0.9,label='Ajuste a la sección eficaz experimental')
    ax.plot(theta,sigma,'--b',linewidth=1.2,mew=0.9,label='Sección eficaz  E=5,5MeV')
    ax.plot(theta,sigma2,'-g',linewidth=1.2,mew=0.9,label='Sección eficaz E experimentañ')
    ax.errorbar(x,y,yerr=yerr,xerr=xerr,marker='o',linestyle='none',
    capsize=1.85,elinewidth=1, ms=4,mfc='white',mec='green',mew=1,label='Puntos experimentales de la sección eficaz',ecolor='dimgrey')
    #grid(linestyle='-.')
  
    #ax.set_facecolor('lavender')#color del fondo
    ax.set_ylabel(yaxis,name='sans-serif')
    ax.set_xlabel(xaxis,name='sans-serif')
    ax.tick_params('both',direction='in',left='on',right='on',top='on',width=1,length=4)
    ax.tick_params('both',direction='in',left='on',right='on',top='on',width=1,length=7) 
    ax.yaxis.set_major_locator(MaxNLocator(8))
    ax.xaxis.set_major_locator(MaxNLocator(8))
    ax.set_ylim(-2,600000)
    ax.set_xlim(-0.8,0.8)
    ax.tick_params('x',rotation=0)
    ax.legend(loc='upper right',framealpha=0.5,fontsize='small')
    fig.tight_layout()
    #fig.suptitle(title,fontsize=14,name='sans-serif',style='italic')
    fig.subplots_adjust(top=0.88)
    #fig.savefig(title,format='jpg')
    fig.savefig(title,format='eps')
    show()
    print(ajuste)
    return ans,uncer, chi2


###############################################################################################################
#Visualizacion de los datos
###############################################################################################################

#Funcion representacion:

def graph(x,y,xerr,yerr):
    fig,ax=subplots(111)
    #ax.plot(xm,ym,'-k',linewidth=1.2,mew=0.9,label='Ajuste')
    ax.errorbar(x,y,yerr=yerr,xerr=xerr,marker='o',linestyle='none',
    capsize=1.85,elinewidth=1, ms=6,mfc='white',mec='red',mew=1,label='Haz dispersado con aluminio',ecolor='dimgrey')
    #grid(linestyle='-.')
    #ax.set_facecolor('lavender')#color del fondo
    ax.set_ylabel(yaxis,name='sans-serif')
    ax.set_xlabel(xaxis,name='sans-serif')
    ax.tick_params('both',direction='in',left='on',right='on',top='on',width=1,length=4)
    ax.tick_params('both',direction='in',left='on',right='on',top='on',width=1,length=7) 
    ax.yaxis.set_major_locator(MaxNLocator(10))
    ax.xaxis.set_major_locator(MaxNLocator(10)) 
    ax.tick_params('x',rotation=0)
    ax.legend(loc='best',fontsize='small',framealpha=0.5)
    fig.tight_layout()
    #fig.suptitle(title,fontsize=14,name='sans-serif',style='italic')
    fig.subplots_adjust(top=0.88)
    fig.savefig(title,format='eps')
    figure(1)
    return 

###############################################################################################################
#Fin
###############################################################################################################
#Reproducimos un sonido conforme ha leido el archivo
###############################################################################################################

import simpleaudio as sa
frequency = 440  # Our played note will be 440 Hz
fs = 44100  # 44100 samples per second
seconds = 1  # Note duration of 3 seconds

# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * fs, False)

# Generate a 440 Hz sine wave
note = np.sin(frequency * t * 2 * np.pi)*np.e**(-12*t)

# Ensure that highest value is in 16-bit range
audio = note * (2**15 - 1) / np.max(np.abs(note))
# Convert to 16-bit data
audio = audio.astype(np.int16)

# Start playback
play_obj = sa.play_buffer(audio, 1, 2, fs)


