#直角三関において１つの鋭角の大きさが決まれば、
#三角形の和は180度であることから他１つの鋭角も決まり三辺の比も決まる

#
#     B
#     .
# 　／|
# ／  |
#A----C

#------------------------------------------------
#Q. Aが45度、辺ACは10cm、このときの辺ABの長さは？
#------------------------------------------------

# cosθ = AC/AB
# cosθ = 10 / x
# cos45 = 0.70
# 0.70 = 10 / x
# 0.70x = 10
# x = 10 / 0.70
# x = 14.285

import math

cos45 = math.cos(math.radians(45))
sideAC = 10
sideAB = sideAC / cos45
print("sideAB >> " + str(sideAB)) #0.7071067811865476


#------------------------------------------------
#Q. Aが20度、辺ABは20cm、このときの辺BCの長さは？
#------------------------------------------------
# sinθ = BC / AB
# sinθ = x / 20
# sin20 = 0.34
# 0.34 = x / 20
# x = 0.34 * 20
# x = 6.8 
sin20 = math.sin(math.radians(20))
sideAB = 20
sideBC = sin20 * sideAB
print("sideBC >> " + str(sideBC))  # 6.840402866513374




#------------------------------------------------
# Q. 辺ACが√３、辺BCが1の時のAの角度は？ 
#:------------------------------------------------
#     B
#   ／|
# ／  |1
#AーーC
#  3
angleA = math.atan(1/math.sqrt(3))*180/math.pi
print("angleA >> " + str(angleA))

#------------------------------------------------
# Q. Aが30度、辺ABが2、のときのAC(x)は？ 
#:------------------------------------------------
#  2  B
#   ／|
# ／  |
#AーーC
#  x\
#cosθ = x / 2
# x = cosθ *2
# cos30 = 0.15
# x = 0.866  * 2
# x = 1.73
cos30 = math.cos(math.radians(30))
sideAC = cos30 * 2
print("sideAC >> " + str(sideAC))