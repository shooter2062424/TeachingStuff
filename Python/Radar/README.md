# Radar project

### Using Arduino + Python(pygame pkg) to implement the whole system

*   Improvement:  
    *   Arduino side:  
        *   1. The sampling rate is more stable for every time  
    *   Python side:  
        *   1. Use threading to speed up pygame GUI (won't block by serial anymore)  
        *   2. Add second graph which provides:   
            *   (1)Average plot  
            *   (2)5 points average plot  
        *   you can use it by pressing "w" on your keyboard  
      
*   How to use:  
    *   Arduino side:  
        *   just upload it and it will be fine  
    *   Python side:  
        *   don't forget to change com port!  

![image](https://github.com/shooter2062424/TeachingStuff/blob/master/Python/Radar/radar.jpg)

*   Special thanks for "mohammad-ammar", who I revised the Python GUI code from  
    *   link: https://github.com/mohammad-ammar/radar/tree/master/gui  


