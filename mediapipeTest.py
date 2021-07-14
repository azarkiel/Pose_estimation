# https://youtu.be/brwgBf6VB0I
# JOINTS: https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
import PoseModule as pm
import getopt, sys
import cv2
import time, os, psutil
# import cProfile, pstats
# from perfmetrics import metric
import Metrikas as met
import logging

def main(argv):
    mi_logger = met.prepareLog('Log_'+sys.argv[0] + '.log', logging.INFO)
    process = psutil.Process(os.getpid())

    try:  # tratamos los argumentos
        opts, args = getopt.getopt(argv, "hi:nm", ["help", "noview", "printmetrics", "inputfile="])
    except getopt.GetoptError:
        print('mediapipeTest.py -n -m -i <inputfile>')
        sys.exit(2)
    view_option = True
    print_metrics = False
    mode = "camera"
    for opt, arg in opts:
        if opt == '-h':
            print('mediapipeTest.py -nv -i <inputfile>')
            sys.exit()
        elif opt in ("-n", "--noview"):
            view_option = False
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
            mode = "video"
        elif opt in ("-m", "--printmetrics"):
            print_metrics = True

    if mode == "camera":
        cap = cv2.VideoCapture(0)
    elif mode == "video":
        cap = cv2.VideoCapture(inputfile)

    detector = pm.poseDetector()
    success, img = cap.read()
    p_time = 0
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_actual = 1
    fps_list = []
    cpu_list = []
    mem_list = []
    while success:
        success = False
        success, img = cap.read()
        frame_actual += 1

        if success:
            img = detector.findPose(img, draw=True)
            lm_list = detector.findPosition(img, draw=True)

            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            fps_list.append(fps)
            # print("FPS="+str(fps))
            # sys.stdout.write("\rFPS="+str(fps))
            # sys.stdout.flush()

            if view_option:
                if print_metrics:
                    cv2.imshow("Image", met.printMetrics(img, frame_actual, num_frames, fps, round(met.Average(fps_list), 1), round(max(fps_list), 1)))
                else:
                    cv2.imshow("Image", img)

        if cv2.waitKey(1) == ord('q'):
            break

        # memory_temp = process.memory_info()
        # memoria_dict = dict(psutil.virtual_memory()._asdict())

        mem_list.append(process.memory_info()[0])
        # cpu_porcentaje=process.cpu_percent()
        cpu_porcentaje = round(process.cpu_percent() / psutil.cpu_count(), 1)
        cpu_list.append(cpu_porcentaje)
    #
        # sys.stdout.write("\rFrame " + str(frame_actual) + "/" + str(int(num_frames)) + " " + str(
        #     round(100 * frame_actual / num_frames, 1)) + "%"
        #                  + "\tUsedMemory=" + str(round(process.memory_info()[0] / (1024 ** 2), 1)) + "MB"
        #                  + "\tUsedCPU=" + str(cpu_porcentaje) + "%")
        # sys.stdout.flush()

    fps_list = [i for i in fps_list if i > 0.5]
    mem_list = [i for i in mem_list if i > 0.5]
    cpu_list = [i for i in cpu_list if i > 0.5]
    resumen=('\nARGS=' + ' '.join(str(e) for e in sys.argv)
          + '\nPROGRAM= ' + sys.argv[0]
          + '\nFILENAME= ' + inputfile
          + '\nFPS_AVG= ' + str(round(met.Average(fps_list), 1))
          + '\nFPS_MAX= ' + str(round(max(fps_list), 1))
          + '\nFPS_MIN= ' + str(round(min(fps_list), 1))
          + '\nMEM_AVG= ' + str(round(met.Average(mem_list) / (1024 ** 2), 1)) + 'MB'  # in bytes
          + '\nMEM_MAX= ' + str(round(max(mem_list) / (1024 ** 2), 1)) + 'MB'  # in bytes
          + '\nMEM_MIN= ' + str(round(min(mem_list) / (1024 ** 2), 1)) + 'MB'  # in bytes
          + '\nCPU_AVG= ' + str(round(met.Average(cpu_list), 1)) + '%'
          + '\nCPU_MAX= ' + str(round(max(cpu_list), 1)) + '%'
          + '\nCPU_MIN= ' + str(round(min(cpu_list), 1)) + '%'
          +'\n')
    print(resumen)
    mi_logger.info(resumen)

if __name__ == "__main__":
    main(sys.argv[1:])
