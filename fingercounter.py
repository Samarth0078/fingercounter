import mediapipe as mp
import cv2
mphand=mp.solutions.hands
mpdrawings=mp.solutions.drawing_utils
hand=mphand.Hands(max_num_hands=1)
video=cv2.VideoCapture(0)
while True:
    suc,image=video.read()
    image=cv2.flip(image,1)
    imgrgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    results=hand.process(imgrgb)
    tipids=[4,8,12,16,20]
    lmlist=[]
    cv2.rectangle(image,(20,350),(90,440),(123,46,67),cv2.FILLED )
    if results.multi_hand_landmarks:
        for det in results.multi_hand_landmarks:
            for id,lm in enumerate(det.landmark):
                # print(id,lm)
                cx=lm.x
                cy=lm.y
                lmlist.append([id,cx,cy])
                # print(lmlist)
                if len(lmlist)!=0 and len(lmlist)==21:
                    fingerlist=[]


                    #thumb
                    if lmlist[20][1]>lmlist[12][1]:
                        if lmlist[4][1]>lmlist[3][1]:
                            fingerlist.append(0)
                        else:
                            fingerlist.append(1)
                    else:
                        if lmlist[4][1]<lmlist[3][1]:
                            fingerlist.append(0)
                        else:
                            fingerlist.append(1)                
                        

                    for i in range(1,5):
                        if lmlist[tipids[i]][2]>lmlist[tipids[i]-2][2]:
                            fingerlist.append(0)
                        else:
                            fingerlist.append(1)
                    # print(fingerlist) 
                    if fingerlist!=0:
                        fingercount=fingerlist.count(1)
                        # print(fingercount)
                    cv2.putText(image,str(fingercount),(20,436),cv2.FONT_HERSHEY_COMPLEX,fontScale=3,color=(255,3,3),thickness=2)    


            mpdrawings.draw_landmarks(image,det,mphand.HAND_CONNECTIONS,
                                      mpdrawings.DrawingSpec(color=(400,0,0),thickness=2,circle_radius=8),
                                      mpdrawings.DrawingSpec(color=(255,15,255),thickness=2,circle_radius=8))  
    cv2.imshow("HAND",image)              
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()    
