#
# Copyright 2020 K7cl
#
'''***********************************************************************************************
   ***                              I N T E R N A L  ---  K 7 C L                              ***
   ***********************************************************************************************
   *                                                                                             *
   *                 Project Name : Sdorica Dialog Beautify Tool                                 *
   *                                                                                             *
   *                    File Name : sdo-dialog-beautify.py                                       *
   *                                                                                             *
   *                   Programmer : K7                                                           *
   *                                                                                             *
   *                   Start Date : June 14, 2020                                                *
   *                                                                                             *
   *                  Last Update : June 15, 2020                                                *
   *                                                                                             *
   *---------------------------------------------------------------------------------------------*'''


# 用法：将本程序置于AssetStudio导出的对白txt文件目录下运行即可，将自动遍历目录下所有中文简体对白文件并美化和编码后写入output文件。

# 依赖库
import json
import re
import os
import argparse

banner = 'sdorica对白美化工具 By K7'
parser = argparse.ArgumentParser(description=banner)
parser.add_argument("-o","--output", type=str, default='output.txt', metavar='path', help='设置导出文件路径(默认: output.txt)')
args = parser.parse_args()

# 遍历目录
for root,dirs,files in os.walk(os.getcwd()):
	for file in files:
		filename = os.path.join(file)
		# 匹配需要美化的文件名特征
		if filename.find("dialog_chinesesimplified.txt") != -1:
			print('[*]Contain: ' + filename)
			print('Reading ' + filename + '.....')
			with open(filename,"r") as f:
				text = f.read()
			p = r'(?<=content":).+?(?=}")'
			pattern = re.compile(p)
			matcher1 = re.search(pattern,text)
			newtext = matcher1.group(0)
			jsondic = json.loads(newtext.replace('sfxVolume":.','sfxVolume":0.'))
			p = r'(?<=main_).+?(?=_dialog_chinesesimplified)'
			pattern = re.compile(p)
			matcher1 = re.search(pattern,filename)
			filename = matcher1.group(0)
			n = 0
			a = 1
			while a == 1:
				try:
					del jsondic[n]["ID"]
					del jsondic[n]["SpeakerAssetName"]
					del jsondic[n]["IconName"]
					del jsondic[n]["IconLocate"]
					del jsondic[n]["sfxName"]
					del jsondic[n]["sfxVolume"]
					n = n + 1
				except:
					a = 0
			print('Write ' + args.output + '.....')
			# 追加写输出到文件
			with open(args.output,"a",encoding="utf-8") as f:
				f.write('\n')
				f.write(filename)
				f.write('\n\n')
				n = 0
				a = 1
				while a == 1:
					try:
						f.write(jsondic[n]["SpeakerName"] + ':\n' + jsondic[n]["Text"])
						f.write('\n\n')
						n = n + 1
					except:
						a = 0
			print('Done!')
		else:
			print('[*]Except: ' + filename)