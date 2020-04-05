import csv

def unqiue(filename):
    # 读取csv数据
    w = open(filename,"r")
    # w.readline()
    ret = w.readlines()
    # print(ret[:3])
    # return
    print(len(ret))
    # 去重
    ret = set(ret)
    print(len(ret))
    # 重写
    uw = open("unique"+filename, "a+")
    uw.writelines(ret)
    # csv_writer = csv.writer(uw, delimiter=",")
    # csv_writer.writerows(ret)
    uw.close()
    w.close()
    pass


if __name__ == "__main__":
    filename = "kunming.csv"
    unqiue(filename)