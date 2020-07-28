import math

eps = 1e-7

class point:
	x: float
	y: float
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def set(self, x, y):
		self.x = x
		self.y = y

	def len(self):
		return math.sqrt(self.x * self.x + self.y * self.y)

	def normalize(self, len):
		tek_len = self.len()
		self.x = self.x / tek_len * len
		self.y = self.y / tek_len * len

	def to_arr(self):
		return [round(self.x), round(self.y)]

	def rotate(self, angle):
		x1 = self.x
		y1 = self.y
		self.x = x1 * math.cos(angle) - y1 * math.sin(angle)
		self.y = x1 * math.sin(angle) + y1 * math.cos(angle)

	def __add__(self, other):
		return point(self.x + other.x, self.y + other.y)


	def __sub__(self, other):
		return point(self.x - other.x, self.y - other.y)

	def show(self):
		print("x: " + str(self.x) + " y: " + str(self.y))

def scal(a: point, b: point): # cos
	return a.x * b.x + a.y * b.y

def vect(a: point, b: point): # sin
	return a.x * b.y - a.y * b.x

class otr:
	def __init__(self, a: point, b: point):
		self.a = a
		self.b = b

	def set(self, a: point, b: point):
		self.a = a;
		self.b = b;

	def to_vec(self):
		return self.b - self.a

class line:
	def set(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

	def __init__(self, p1: point, p2: point):
		self.a = p2.y - p1.y
		self.b = p1.x - p2.x
		self.c = p1.x * (p1.y - p2.y) + p1.y * (p2.x - p1.x)

	def show(self):
		print("a: " + str(self.a))
		print("b: " + str(self.b))
		print("c: " + str(self.c))


def get_angle(a: point, b: point):
	return math.atan2(vect(a, b), scal(a, b))

def rotate_vector_vector(a: point, b: point):
	# start_len = b.len()
	angle = get_angle(a, b) * 2
	print("angle: " + str(angle))
	a.show()
	a.rotate(angle)
	a.show()
	# b.normalize(start_len)
	return a

def sign(a):
	if (a < 0): return -1
	if (a > 0): return 1
	return 0

def check_inter_ray_otr(ray: otr, mir: otr):
	a = ray.a - mir.a;
	b = mir.b - mir.a
	c = ray.b - mir.a
	return ((vect(a, b) * vect(a, c)) > 0) and (sign(vect(ray.to_vec(), mir.a - ray.a)) != sign(vect(ray.to_vec(), mir.b - ray.a)))

def len_pt_line(p: point, o: otr):
	l = line(o.a, o.b)
	return ((l.a * p.x + l.b * p.y + l.c) / math.sqrt(l.a * l.a + l.b * l.b))

def inter_point(ray: otr, mir: otr):
	if not(check_inter_ray_otr(ray, mir)):
		return -1
	else:
		d1 = len_pt_line(ray.a, mir)
		d2 = len_pt_line(ray.b, mir)
		tek_vec = ray.b - ray.a

		# check for div fo zero
		tek_vec.normalize(tek_vec.len() * d1 / (d1 - d2))
		ray.b = ray.a + tek_vec;
		return ray

def dist_pt_otr(p: point, o: otr):
	ab = o.b - o.a
	ba = o.a - o.b
	ap = p - o.a
	bp = p - o.b
	if ((scal(ab, ap) >= 0) and (scal(ba, bp) >= 0)):
		return abs(len_pt_line(p, o))
	else:
		return min(ap.len(), bp.len())
	
def pt_to_line(a: point, o: otr):
    return (vect(o.a - a, o.b - a) == 0)


def otr_inter(a: otr, b: otr):
    if (pt_to_line(a.a, b) and pt_to_line(a.b, b)):
        if (((max(a.a.x, a.b.x) < min(b.a.x, b.b.x)) or ((min(a.a.x, a.b.x) > max(b.a.x, b.b.x))))
        or ((max(a.a.y, a.b.y) < min(b.a.y, b.b.y)) or ((min(a.a.y, a.b.y) > max(b.a.y, b.b.y))))):
            return 0
        else:
            return 1
    t = a.b - a.a
    t2 = b.b - b.a
    return (sign(vect(t, b.a -  a.b)) != sign(vect(t, b.b - a.b))) and (sign(vect(t2, a.a - b.a)) != sign(vect(t2, a.b - b.a)))

