from PySide6.QtGui import QImage

estilo1 = '''
    #main {
    background: #14181C;
    }

    QFrame {
    
    background-color: #26282E;
    border: 1.4px solid #3A3D41;
    border-radius: 15px;

    }    
    
    #Sidebar {
    background-color: #17181C;
    border: 1px solid #171812;
    border-radius: 15px;
    
    }
    
    #pila {
    
    background-color: transparent;
    border: transparent;
    
    }
    
    #frameInterno {
    background-color: #2E3138;
    border-radius: 35px;
    }    
    

  
'''
imagenes = '''

    QLabel {
    background-color: #202123;
    border: transparent;
    };
    
'''

buttonSide = '''

    QPushButton {
    font-family: Inter;
    background-color: #2B2D31;
    border-radius: 10px;
    background-color: none; 
    border: none;
    font-size: 17px;
    text-align: left;
    padding: 9px;
    font-bold: 0px;
    
    }
    
    QPushButton:hover {
    background-color: #2B2D31;
    font-bold: 10px;
    font-size: 20px;
   
    }

'''


estado1 ="""
    background-color: #056d38;      
    color: white; 
    font-size: 35px;     
    font-weight: bold;
    border-radius: 20px;              
    padding: 5px;                    
"""
modo1 ="""
    background-color: #393a41;      
    color: white; 
    font-size: 20px;     
    font-weight: bold;
    border-radius: 14px;              
    padding: 5px;                    
"""
racha ="""
    background-color: transparent;
    border: transparent;;      
    color: white; 
    font-size: 25px;     
    font-weight: bold;
    border-radius: 11px;              
    padding: 10px;                    
"""
contadores = '''
           
           QLabel {

            font-size: 18px;     
         
            border: transparent;
            font-family: Inter;                            
            background-color: Transparent;
            font-weight: bold;
         
            
                }
 '''
contador1 = contadores + '''
QLabel {
color: white;            
                }
'''
labelGood = contadores + '''
QLabel {
color: #22b196;            
                }
'''
labelBad = contadores + '''
QLabel {
color: #c54b3a;            
                }
'''
labelRacha = contadores + '''
QLabel {
color: #dd9a3a;            
                }
'''

labelRecord = contadores + '''
    QLabel {
    color: #fdd502;            
    }
'''

contador2 = contadores + '''
QLabel {
color: white;            
                }
'''

contador3 = contadores + '''
QLabel {
color: white;
font-weight: normal;   
font-size: 16px;         
                }
'''

scrollDashboard = '''
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    width: 8px;
    background: transparent;
}

QScrollBar::handle:vertical {
    background: rgba(255,255,255,80);
    border-radius: 4px;
    min-height: 25px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255,255,255,150);
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

'''

dialogo = '''
QDialog{
    background:#202124;
}

QFrame{
    background: transparent;
    border: none;
}

QLabel#titulo{
    color:white;
    font-size:22px;
    font-weight:700;
}

QLabel{
    color:white;
    font-size:15px;
    font-weight:600;
}

QLineEdit{
    background:#2B2D31;
    border:2px solid #3A3D42;
    border-radius:12px;
    padding:10px;
    color:white;
    font-size:15px;
}

QLineEdit:focus{
    border:2px solid #4F8EF7;
}

QPushButton{
    background:#4F8EF7;
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:15px;
    font-weight:bold;
}

QPushButton:hover{
    background:#6AA5FF;
}

QPushButton:pressed{
    background:#2F6FE5;
}
'''

dialogSetTiempo = '''
QDialog{
            background:#202124;
        }
        
        QFrame{
        background: transparent;
        border: none;
        }

        QLabel#title{
            color:white;
            font-size:24px;
            font-weight:700;
        }

        QLabel#subtitle{
            color:#B8B8B8;
            font-size:18px;
            font-weight:700;
        }

        QLabel{
            color:white;
            font-size:15px;
            font-weight:600;
        }

        QLineEdit{
            background:#2B2D31;
            border:2px solid #3A3D42;
            border-radius:12px;
            padding:10px;
            color:white;
            font-size:15px;
        }

        QLineEdit:focus{
            border:2px solid #4F8EF7;
        }

        QSpinBox{
            background:#2B2D31;
            border:2px solid #3A3D42;
            border-radius:12px;

            color:white;
            font-size:26px;
            font-weight:bold;

            min-width:120px;
            min-height:45px;
        }

        QSpinBox:focus{
            border:2px solid #4F8EF7;
        }

        QSpinBox::up-button,
        QSpinBox::down-button{
            width:25px;
            height:30px;
            }
        


        QPushButton{
            background:#4F8EF7;
            color:white;
            border:none;
            border-radius:12px;
            padding:12px;
            font-size:15px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#6AA5FF;
        }

        QPushButton:pressed{
            background:#2F6FE5;
        }
'''
botonSecion = '''
QPushButton {
    background-color: #2F5D46;
    
    border: 1px solid #579C77;
    border-radius: 12px;
    padding: 6px 14px;
    font-size: 14px;
    font-weight: bold;
    
    
}

QPushButton:hover {
    background-color: #3B7155;
    border: 1px solid #5A906F;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #274D3A;
    border: 1px solid #477A5F;
}

QPushButton:disabled {
    background-color: #34433B;
    color: #7D8D84;
    border: 1px solid #46564D;
}
'''

botonAgregar = '''

        QPushButton{
        background-color: #23614a;
        font-size: 15px;
        font-weight: bold;
        }
        QPushButton:hover {
        background-color: #3a8066;
        }
        QPushButton:pressed {
        background-color: #3d9e7a;
        }
        '''
botonCompletar = '''
        QPushButton{
        background-color: #9b9696;
        font-size: 15px;
        font-weight: bold;
        }
        QPushButton:hover {
        background-color: #c2bbbb;
        }
        
        QPushButton:pressed {
        background-color: #9b9696;
        }
        '''