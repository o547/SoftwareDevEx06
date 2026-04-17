import cv2
from .navi import navi

class map:

    @classmethod
    def drow_arrows(cls,path):
        input_name = "static/toyosu_campus_navi/image/map4F.png"
        output_name = "static/toyosu_campus_navi/image/output.png"
        nodes= navi.nodes
        color = (0, 0, 255)
        thickness = 2
        line_type = cv2.LINE_AA
        tipLength = 0.1  # デフォルトは0.1
        img = cv2.imread(input_name)

        for i in range (len(path)-1):
            # print(str(path[i])+"→"+str(path[i+1]))
            start = nodes[path[i]]
            end = nodes[path[i+1]]
            # 線を引く
            cv2.arrowedLine(
                img,
                start,
                end,
                color,
                thickness=thickness,
                line_type=line_type,
                tipLength=tipLength,
            )
        
        cv2.imwrite(output_name, img)
