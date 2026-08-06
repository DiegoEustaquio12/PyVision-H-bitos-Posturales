from PySide6.QtGui import QImage

estilo1 = '''
    #main {
    background: transparent;
    }

    QFrame {
    
    background-color: #2B2D31;
    border: 1.4px solid #3A3D41;
    border-radius: 16px;

    }    
    
    #Sidebar {
    background-color: #202123;
    }
    
    #pila {
    
    background-color: transparent;
    border: transparent;
    
    }
    
    #frameInterno {
    background-color: #393a41;
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
            font-size:14px;
            font-weight:700;
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