# ////////////////////Demo for dual-cam synchronizing//////////////////
# Demo for dual camera capturing iamge under master-slave working mode
# load predefine setting file of master and salve camera
# Hardwere preparation must done by connecting gpio cable with resister 1k om btw master and slave camera
import numpy as np # must first import numpy before import pyspin
import PySpin
from time import sleep
import threading
#import multiprocessing
import os
import sys
import copy
import traceback # for getting object instance name

import cv2
#import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
import PIL.Image, PIL.ImageTk

#
#Global var for holding image from camera
LIMAGE = None
RIMAGE = None

class Camera(object):
    def __init__(self, cam):
        # Get name of instance
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        self.def_name = text[:text.find('=')].strip()
        #print("text content is{}".format(text))
        print("def name is {} and type {}".format(self.def_name, type(self.def_name)))
        #self.defined_name = def_name
        #self.taskrun = True
        self.cam = cam
        #self.image = None
        #self.Limage = None
        #self.Rimage = None
        #self.image_list = []
        #self.callback = callback
        t = threading.Thread(target = self.run, args = (self.cam, self.def_name,)) 
        t.daemon = True
        t.start()
        

    def run(self, cam, def_name):
        print("start while loop........")
        while True: #self.taskrun: #self.start_acquire_image: #not stop_event:
            try:
                #print("beging try clause")
                image = cam.GetNextImage()
                #print("after get next image")
                if image.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image.GetImageStatus())
                    print(image.GetTimeStamp())
                    # print("image incoming...................")
                else:
                    '''
                    # Convert to mono8 asignt to kivy global img
                    '''
                    image_converted = image.Convert(PySpin.PixelFormat_Mono8, PySpin.HQ_LINEAR)
                    imgarr = image_converted.GetNDArray()
                    #print("begin callback")
                    if def_name =='self.Lcamera':
                        #callback(imgarr, 'Lcamera')
                        #global L_cam_image, R_cam_image
                        global LIMAGE
                        LIMAGE = imgarr
                        print("Get limage now......")
                        
                    else:
                        #callback(imgarr, 'Rcamera')
                        #R_cam_image = image_converted.GetNDArray()
                        global RIMAGE
                        RIMAGE = imgarr
                        print("get r image now........")
                    #img_arr_c = copy.deepcopy(img_arr)
                    #self.count += 1
                    #image_c = copy.deepcopy(image_converted)
                    # call image proccess to fusion imaage

                    #callbacks(img_arr,self.defined_name)
                    #self.taskrun = False
                    # clear buffer from camera
                    image.Release()
                    #print('image getting success....')
            except PySpin.SpinnakerException as ex:
                print('in image event polling images!')
                print(ex)
    def __delete__(self,instance):
        #self.cam = None
        self.cam.Release()

    '''
    def get_frame(self):
        if self.def_name == 'Lcamera':
            return self.Limage
        else:
            return self.Rimage

    '''
    

class SystemEventHandler(PySpin.InterfaceEventHandler):
    def __init__(self,system):
        super(SystemEventHandler, self).__init__()

        
        self.system = system
        # self.cameras = None
        # self.system = system
    def OnDeviceArrival(self, serial_number):
        print('Device {} arrival...........'.format(serial_number))
        print('相机 %s 已经连接成功' % serial_number)
        
    def OnDeviceRemoval(self, serial_number):
        # callback_stop_this_camera(serial_number)
        print('相机 %s 失去连接!，请检查相机，连接正常后重启系统.....' % serial_number)

# Get camera serial number
def get_cam_serial(cam):
    nodemap = cam.GetTLDeviceNodeMap()

    # Retrieve device serial number
    node_device_serial_number = PySpin.CStringPtr(nodemap.GetNode('DeviceSerialNumber'))

    if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
        return node_device_serial_number.GetValue()
    else:
        return None
        print("Failed to get device number")
# Check if running camera configured position
def check_if_connected_cameras_configured_right_position(cam_serial_numbers_register,cam_serial_from_system):
    
    if cam_serial_from_system not in cam_serial_numbers_register:
        print("Please register cam first!")
        return False
        
    else:
        return True
       
    
    
     



class App:
    def __init__(self, window, window_title):
        # Cameras
        self.L_cam_image = None
        self.R_cam_image = None
        self.cam_serial_numbers_register = [19060890,18260970]

        self.L_cam_serial = '18260970'
        self.R_cam_serial = '19060890'
        self.image_list = []

        # screen size
        self.width = 788*2
        self.height = 788
        # Starting cameras
        '''
        ret, self.cam = self.InitCameras()
        if ret:
            pass
        else:
            print("No camea found!")
        
        self.InitCameras()
        '''
        
         
        
        #sleep(3)
        global LIMAGE
        if self.InitCameras():
            for i in range(100):
                if LIMAGE is not None and RIMAGE is not None:
                    #print("/////////////////////////////////////////////////////////////")
                    #print("Get image size {}",format(LIMAGE.shape))
                    #(self.height, self.width) = LIMAGE.shape
                    break
                else:
                    
                    print("waiting for getting image from camera...............................")
                    sleep(1)
                    continue
            print("Image capturing failed!.....")
        
        
        # App windows
        self.window = window
        self.window.title(window_title)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.mainloop()
 
   
    def update(self):
        # Get a frame from the camera source
        global LIMAGE,RIMAGE
        # print("Shape of r image {} ".format(RIMAGE.shape))
        # chang one channel to three
        # limg = np.zeros((788,788,3))
        # limg[:,:,0] = LIMAGE
        # limg[:,:,1] = LIMAGE
        # limg[:,:,2] = LIMAGE
        # #mergeImage = np.hstack((limg,RIMAGE))

        # ray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        LIMAGE_M = cv2.merge([LIMAGE,LIMAGE,LIMAGE])
       
        # cv2LIMAGE = cv2.cvtColor(LIMAGE,cv2.COLOR_GRAY2RGB)
        cv2RIMAGE = cv2.cvtColor(RIMAGE,cv2.COLOR_BGR2RGB)
        # Horizontal concate images
        mergeImage = cv2.hconcat([cv2RIMAGE,LIMAGE_M])
        #img2 = cv2.cvtColor(RIMAGE,cv2.COLOR_RGBA2RGB)
        # convert to 3 channel for display
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(mergeImage))#,cv2.COLOR_GRAY2RGB)))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)
 
    def clearCameras(self):
        self.system.UnregisterInterfaceEventHandler(self.sys_event_handler)
        #self.cam = None
        if self.cam is not None:
            del self.cam

        # Clear camera list before releasing system
        self.cam_list.Clear()
        # Release system instance
        self.system.ReleaseInstance()

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
    # Load user setting file to camera    
    def loadUsrSetting(self,cam):
        result = True
        try:
            cam.Init()
            nodemap = cam.GetNodeMap()
            # set usr set file 0 as default
            node_file_selector = PySpin.CEnumerationPtr(nodemap.GetNode('FileSelector'))
            node_user_set_0 = node_file_selector.GetEntryByName('UserSet0')
            user_set_value = node_user_set_0.GetValue()
            node_file_selector.SetIntValue(user_set_value)
            cam.UserSetLoad()
            # wait for system config settings
            sleep(200/1000)
            cam.BeginAcquisition()
            return result
            
        except PySpin.SpinnakerException as ex:
            #print('Poweroff camera and plugin try again!')
            print(ex)
            #alerting(str(ex),'cameraerror')
            return False

    def InitCameras(self):
        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()
        # Register handler to take care of camera removal or connecting
        self.sys_event_handler = SystemEventHandler(self.system)
        self.system.RegisterInterfaceEventHandler(self.sys_event_handler)
        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()
        num_cameras = self.cam_list.GetSize()
        print('Number of cameras detected: %d' % num_cameras)
        # Finish if there are no cameras
        if num_cameras == 0:
            self.clearCameras()
            #return False, None
            print("No camera found!........")
            return False
        # Run example on each camera
        for i, camp in enumerate(self.cam_list):
            serial = get_cam_serial(camp)
            print('Get str name {} type of {}'.format(serial,type(serial)) )
            if serial is not None:
                print('Running example for camera %d...' % i)
                camp.Init()
                camp.BeginAcquisition()
                # sleep(1)
                # if self.loadUsrSetting(camp):
                #     # camp.BeginAcquisition()
                #     continue
                # else:
                #     print("Camera device {} Load setting file failed!....".format(serial))
                #     break
            # Set camera position by device serial
            if self.L_cam_serial == serial:
                self.Lcamera = Camera(camp)
                print("Lcamera created!")
            else:
                self.Rcamera = Camera(camp)
               
        print('Camera %d example running... \n' % i)
        return True
            
    # Release the video source when the object is destroyed
    def __delete__(self,instance):
        #
        #del self.cam
        #self.camp = None
        del self.Lcamera,self.Rcamera
        self.clearCameras()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Dual cam synchorizing image")    