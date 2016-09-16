try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
    import tkFileDialog as filedialog
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
#from PIL import *

from PIL import Image, ImageOps, ImageFile, ImageChops, ImageFilter
from os import listdir, path, system, urandom, rename, unlink
from random import randint
import random
import time
import threading
from threading import current_thread
from shutil import copyfile

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

xsize = screen_width + 10
ysize = screen_height

# xsize = 2560
# ysize = 1080

save_path = '/home/meiji/.wallpaper/'
mosaic_path = '/home/meiji/.wallpaper/mosaic/'
folder_path = '/home/meiji/Pictures/wally/general/'
# folder_path = "/run/user/1000/gvfs/dav:host=localhost,port=42427,ssl=false,prefix=%2F1AHDWEI8RAzl%2Fwally/special/favorite/"
file = open("/home/meiji/.wallpaper/last_images.txt", "w")
feh_file = open("/home/meiji/.wallpaper/feh_images.txt", "w")



xdiv = 8
ydiv = 6
nxsize = int(xsize/xdiv)
nysize = int(ysize/ydiv)
screen_size = (xsize, ysize)

# ImageFile.LOAD_TRUNCATED_IMAGES = True

layout0 = [[ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0, 1, 1, 1, 1, 0, 0],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0, 1, 1, 1, 1, 0, 0]] # 4 quadrants

layout1 = [[ 4, 0, 4, 0, 4, 0, 4, 0],
		  [ 0, 0, 0, 0, 0, 0, 0, 0],
		  [ 4, 0, 4, 0, 4, 0, 4, 0],
		  [ 0, 0, 0, 0, 0, 0, 0, 0],
		  [ 4, 0, 4, 0, 4, 0, 4, 0],
		  [ 0, 0, 0, 0, 0, 0, 0, 0]] # large blocks

layout2 = [[ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0, 1, 1, 1, 1, 0, 0],
		  [ 1, 1, 4, 0, 4, 0, 1, 1],
		  [ 1, 1, 0, 0, 0, 0, 1, 1],
		  [ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0, 1, 1, 1, 1, 0, 0]] # 6 blocks

layout3 = [[ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1],
		  [ 1, 1, 1, 1, 1, 1, 1, 1]] # small

layout4 = [[ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0, 1, 1, 1, 1, 0, 0],
		  [ 2, 0, 4, 0, 4, 0,-2,-2],
		  [ 2, 0, 0, 0, 0, 0, 0, 0],
		  [ 4, 0, 3, 0, 0, 1, 4, 0],
		  [ 0, 0, 1, 3, 0, 0, 0, 0]] # 6 blocks

layout5 = [[ 4, 0, 1, 1, 1, 1, 4, 0],
		  [ 0, 0,16, 0, 0, 0, 0, 0],
		  [ 2, 0, 0, 0, 0, 0,-2,-2],
		  [ 2, 0, 0, 0, 0, 0, 0, 0],
		  [ 4, 0, 0, 0, 0, 0, 4, 0],
		  [ 0, 0, 1, 3, 0, 0, 0, 0]] # large center

layout6 = [[ 2, 0, 2, 0, 2, 0, 2, 0],
		  [ 1, 2, 0, 2, 0, 2, 0, 1],
		  [ 2, 0, 2, 0, 2, 0, 2, 0],
		  [ 1, 2, 0, 2, 0, 2, 0, 1],
		  [ 2, 0, 2, 0, 2, 0, 2, 0],
		  [ 1, 2, 0, 2, 0, 2, 0, 1]] # horizontal

layout7 = [[-2, 1,-2, 1,-2, 1,-2, 1],
		  [ 0,-2, 0,-2, 0,-2, 0,-2],
		  [-2, 0,-2, 0,-2, 0,-2, 0],
		  [ 0,-2, 0,-2, 0,-2, 0,-2],
		  [-2, 0,-2, 0,-2, 0,-2, 0],
		  [ 0, 1, 0, 1, 0, 1, 0, 1]] # large center

layout8 = [[-2, 1,-2, 1,-2, 1,-2, 1],
		  [ 0, 1, 0,-2, 0, 1, 0,-2],
		  [-2, 4, 0, 0,-2, 4, 0, 0],
		  [ 0, 0, 0,-2, 0, 0, 0,-2],
		  [-2, 1,-2, 0,-2, 1,-2, 0],
		  [ 0, 1, 0, 1, 0, 1, 0, 1]] # large center

layout9 = [[ 2, 0, 1,-2, 1,-2, 1,-2],
		  [ 9, 0, 0, 0,-2, 0,-2, 0],
		  [ 0, 0, 0,-2, 0, 1, 0,-2],
		  [ 0, 0, 0, 0, 9, 0, 0, 0],
		  [ 2, 0, 1,-2, 0, 0, 0,-2],
		  [ 1, 2, 0, 0, 0, 0, 0, 0]] # 2 large, random fill

class love:
	def __init__(self):
		self.i = randint(0,300) % 10
		if self.i == 0:
			self.l = layout0
		elif self.i == 1:
			self.l = layout1
		elif self.i == 2:
			self.l = layout2
		elif self.i == 3:
			self.l = layout3
		elif self.i == 4:
			self.l = layout4
		elif self.i == 5:
			self.l = layout5
		elif self.i == 6:
			self.l = layout7
		elif self.i == 8:
			self.l = layout8
		elif self.i == 9:
			self.l = layout9
		else:
			self.l = layout9

def determine_size(code, nxsize, nysize):
	size = (0, 0)

	if code == 2:
		size = (nxsize*2, nysize)
	elif code ==  -2:
		size = (nxsize, nysize*2)
	elif code == 3:
		size = (nxsize*3, nysize)
	elif code == -3:
		size = (nxsize, nysize*3)


	# squares
	elif code == 0:
		size = (0, 0)
	elif code == 1:
		size = (nxsize, nysize)
	elif code == 4:
		size = (nxsize*2, nysize*2)
	elif code == 9:
		size = (nxsize*3, nysize*3)
	elif code == 16:
		size = (nxsize*4, nysize*4)
	elif code == 25:
		size = (nxsize*5, nysize*5)
	elif code == 36:
		size = (nxsize*6, nysize*6)
	else:
		size = (0, 0)
		print('Error: Image has no size associated.')
	return size;

def create_size_matrix(layout):
	rows = len(layout)
	cols = len(layout[0])
	size_matrix = []

	cnt = n_pictures = 0

	for x in range(0, rows):
		for y in range(0, cols):
			size = determine_size(layout[x][y], nxsize, nysize)
			# print(size)
			size_matrix.append(size)
			if size != (0, 0):
				n_pictures = n_pictures + 1

	return size_matrix;
# deprecated
def load_image(img_path):

	return Image.open(img_path);

def get_images(folder_path, num):
	inc_ext = ['jpg', 'bmp', 'png', 'gif']
	file_names = [fn for fn in listdir(folder_path) if any(fn.endswith(ext) for ext in inc_ext)]



	images = []
	if len(file_names) < num :
		print("Error: Not enough images in directory. Expect duplicates.")
		# copy list in case we run out of images
		fn_copy = file_names[:]

	# (int.from_bytes(urandom(16), byteorder='big')%num)
	# r = []

	for i in range(0, num):
		r = randint(0, 10000) % len(file_names)
		# if r[i] in r:
		# 	print("Found duplicate. Trying again.")
		# 	r[i] = int.from_bytes(urandom(16), byteorder='big') % len(file_names)
		# img = load_image(path.join(folder_path, file_names[r]))
		# print(img.verify())
		# images.append(load_image(path.join(folder_path, file_names[r])))
		images.append(Image.open(path.join(folder_path, file_names[r])))
		file.write("<" + "{:>02}".format(str(i+1)) + "> ")
		file.write(file_names[r]+'\n')
		feh_file.write(path.join(folder_path, file_names[r]+'\n'))
		copyfile(path.join(folder_path, file_names[r]), path.join(mosaic_path, "{:>02}_".format(str(i+1)) + file_names[r]))
		if len(file_names) > 1:
			file_names.pop(r)
		else:
			file_names.extend(fn_copy)
	return images;

def get_files(folder_path):
	inc_ext = ['jpg', 'bmp', 'png', 'gif']
	file_names = [fn for fn in listdir(folder_path) if any(fn.endswith(ext) for ext in inc_ext)]
	return file_names;

# deprecated
def paste_images(images):
	bg = Image.new('RGBA', screen_size)

	cnt = 0
	border = 0.00

	for y in range(0, nysize*ydiv, nysize):
		for x in range(0, nxsize*xdiv, nxsize):
			img = ImageOps.fit(images[cnt], (nxsize, nysize), Image.BICUBIC, bleed = border, centering = (0.5, 0.5))
			bg.paste(img, (x, y))
			# bg.paste(img, (x, y))
			cnt = cnt + 1
	return bg;

def threaded_images(images, size_matrix, ratio):
	print(current_thread().name)
	bg = Image.new('RGBA', screen_size, (255,255,255,0))

	cnt = 0
	border = 0.00

	error_cnt = 0

	img_cnt = 0

	for y in range(0, int(nysize*ydiv/ratio), nysize):
		for x in range(0, nxsize*xdiv, nxsize):
			if size_matrix[cnt] != (0, 0):
				success = False
				while not success:
					try:
						img = ImageOps.fit(images[img_cnt], size_matrix[cnt], Image.ANTIALIAS, bleed = border, centering = (0.5, 0.5))
						#print(size_matrix[cnt])


						# Border
						img = ImageOps.crop(img, 5)
						img = ImageOps.expand(img, 5, 0)

						# Extra settings
						# img = ImageOps.grayscale(img)
						# img = ImageOps.flip(img)
						# img = ImageOps.mirror(img)
						# img = img.filter(ImageFilter.BLUR)
						# img = img.filter(ImageFilter.DETAIL)

						# BLUR
						# CONTOUR
						# DETAIL
						# EDGE_ENHANCE
						# EDGE_ENHANCE_MORE
						# EMBOSS
						# FIND_EDGES
						# SMOOTH
						# SMOOTH_MORE
						# SHARPEN

						#There is a problem with invert and solarize and png images :()
						# img = ImageOps.solarize(img, threshold = 128)
						# img = ImageOps.invert(img)



						success = True
						img_cnt = img_cnt + 1
						error_cnt = 0
					except:
						error_cnt = error_cnt + 1
						print("Image wasn't loaded properly :(")
						if error_cnt < 30:
							pass
						else:
							print("You done fucked up.")
							break
				#paste to canvas
				bg.paste(img, (x, y))
			cnt = cnt + 1
	return bg;

def threaded_animation(images, ratio):
	screen_size = (2560, int(1080/ratio))
	bg = Image.new('RGBA', screen_size)

	cnt = 0
	border = 0.00

	for y in range(0, int(180*6/ratio), 180):
		for x in range(0, 320*8, 320):
			img = ImageOps.fit(images[cnt], (320, 180), Image.BICUBIC, bleed = border, centering = (0.5, 0.5))
			bg.paste(img, (x, y))
			cnt = cnt + 1
	return bg;

class wp_thread (threading.Thread):
	# out = Image.new('RGBA', (2560, 1080))
	# images = []
	# ratio = 2
	# layout = []
	def __init__(self, threadID, name, counter, images, layout, ratio):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.images = images
		self.ratio = ratio
		self.layout = layout
	def run(self):
		# print('Starting ' + self.name)
		self.out = threaded_images(self.images, self.layout, self.ratio)
		# print('Exiting ' + self.name)
	def join(self):
		threading.Thread.join(self)
		return self.out;


# test_path = 'C:\\Users\\a0220950\Downloads\Python\Images'

# folder_path = test_path

# system('feh --bg-fill /home/meiji/Clouds/Dropbox/Programming/Python/saved_image.png')

# command = 'feh --bg-fill' + save_path

def batch(path):
	# screen_size = (xsize, ysize)
	bg1 = Image.new('RGBA', screen_size, (255,255,255,0))
	bg2 = Image.new('RGBA', screen_size, (255,255,255,0))
	bg3 = Image.new('RGBA', screen_size, (255,255,255,0))

	
	lay = love();

	size_matrix = create_size_matrix(lay.l)
	# images = get_images(folder_path, sum(1 for s in size_matrix if s != (0, 0)));



	# Find how many sizes each thread will take care of
	s1 = int(len(size_matrix)/3)

	# Split the matrix into equal sizes
	m1 = size_matrix[:s1]
	m2 = size_matrix[s1:s1*2]
	m3 = size_matrix[s1*2:]

	# Find the non-zero size images for each section
	nz1 = sum(1 for s in m1 if s != (0, 0))
	nz2 = sum(1 for s in m2 if s != (0, 0))
	nz3 = sum(1 for s in m3 if s != (0, 0))

	images = get_images(folder_path, sum(1 for s in size_matrix if s != (0, 0)));
	
	# Prepare threads
	thread1 = wp_thread(1, 'Thread-1', 1, images[:nz1], m1, 3)
	thread2 = wp_thread(2, 'Thread-2', 2, images[nz1:nz1+nz2], m2, 3)
	thread3 = wp_thread(3, 'Thread-3', 3, images[nz1+nz2:], m3, 3)


	# Append size matrix to the text file
	file.write('\n'+str(size_matrix))
	file.close()
	feh_file.close()

	# Start threads
	try:
		thread1.start()
		thread2.start()
		thread3.start()
	except:
		print("Error: Threads won't start.")

	t3 = thread3.join()
	t2 = thread2.join()
	t1 = thread1.join()

	# Paste the image contributions from each thread
	bg1.paste(t1, (0,0))
	bg2.paste(t2, (0,int(nysize*2)))
	bg3.paste(t3, (0,int(nysize*4)))

	# Dont remember... X_x
	bg2 = ImageChops.multiply(bg3, bg2)
	bg1 = ImageChops.multiply(bg1, bg2)

	# bg.show()
	# bg1.save(path, 'JPEG', quality=100)
	bg1.convert('RGB').save(path, 'PNG')

def main():
	global folder_path
	wait = 1;
	if len(sys.argv) < 2:
		folder_path = '/home/meiji/Pictures/wally/general/'
	elif len(sys.argv) < 3:
		folder_path = sys.argv[1]
	else:
		folder_path = sys.argv[1]
		wait = int(sys.argv[2])
	
	if not wait:
		system('feh --bg-fill ' + path.expanduser(save_path+ "saved_image" + ".png"))

	print('Working...')

	folder = mosaic_path
	for the_file in listdir(folder):
	    file_path = path.join(folder, the_file)
	    try:
	        if path.isfile(file_path):
	            unlink(file_path)
	        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)

	for n in range(0, 1):
		batch(path.expanduser(save_path+ "saved_image" + ".png"))
	print('Done!')

	if wait:
		system('feh --bg-fill ' + path.expanduser(save_path+ "saved_image" + ".png"))
	# batch(save_path)


if __name__ == '__main__':
	main()
