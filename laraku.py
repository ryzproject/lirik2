import pygame, random, math, time
pygame.init()
pygame.mixer.init()
try: pygame.mixer.music.load("laraku.mp3")
except: pass

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W, H = screen.get_width(), screen.get_height()
clock = pygame.time.Clock()
font_main = pygame.font.Font(None, 85)
font_sub = pygame.font.Font(None, 52)

CX, CY = W//2 + 250, H//2 + 20
OFFSET = 0.0 
LOVE_SCALE_MULT = 0.95

BASE_LYRICS = [
    (0.0, "Ah-ah, oh-oh"),
    (3.0, "Dengar laraku"),
    (9.5, "Suara hati ini"),
    (12.0, "memanggil namamu"),
    (15.5, "Kar'na separuh aku"),
    (21.5, "Menyentuh laramu"),
    (28.5, "Semua lukamu"),
    (30.5, "t'lah menjadi lirihku"),
    (35.0, "Kar'na separuh aku"),
    (41.0, "Dirimu"),
]

def heart(t, scale, cx, cy):
    x = 16 * math.sin(t)**3
    y = 13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
    return cx + x*scale, cy - y*scale

class Thread:
    def __init__(self, scale):
        self.scale = scale * LOVE_SCALE_MULT
        ang = random.uniform(0, 6.28); r = random.uniform(5, 70)
        self.x = CX + math.cos(ang)*r; self.y = CY + math.sin(ang)*r
        self.vx = random.uniform(-2,2); self.vy = random.uniform(-2,2)
        self.t = random.uniform(0, 6.28); self.speed = random.uniform(0.025, 0.045)
        self.off = random.uniform(0, 1000); self.trail = [(self.x, self.y)]
    def update(self):
        self.off += 0.05; self.t += self.speed
        tx, ty = heart(self.t, 22*self.scale, CX, CY)
        tx += math.sin(self.off)*9; ty += math.cos(self.off*1.3)*9
        dx = tx - self.x; dy = ty - self.y
        self.vx += dx * 0.12; self.vy += dy * 0.12
        self.vx *= 0.80; self.vy *= 0.80
        self.x += self.vx; self.y += self.vy
        self.trail.append((self.x, self.y))
        if len(self.trail) > 145: self.trail.pop(0)
    def draw(self, surf):
        if len(self.trail) > 10:
            pygame.draw.aalines(surf, (255,255,255), False, self.trail)

stars = [[random.uniform(0,W), random.uniform(0,H), random.uniform(0.2,0.9)] for _ in range(250)]
shooting_stars = []; fireworks=[]; last_fw=0
def spawn_shooting():
    shooting_stars.append([random.uniform(W*0.6, W+100), random.uniform(0, H*0.4), random.uniform(-14, -8), random.uniform(2.5, 4.5), 60])

threads=[]
for scale, count in [(1.0, 24), (0.74, 20), (0.52, 16), (0.34, 12), (0.20, 10)]:
    for _ in range(count): threads.append(Thread(scale))

try: pygame.mixer.music.play()
except: pass
start=time.time(); idx=0; shown_text=""; last_show=0; running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE): running=False
    elapsed=time.time()-start
    screen.fill((0,0,0))
    for s in stars:
        pygame.draw.circle(screen, (100,100,100), (int(s[0]), int(s[1])), 1)
        s[1]+=s[2]
        if s[1]>H: s[1]=-5; s[0]=random.uniform(0,W)
    if random.random() < 0.05: spawn_shooting()
    for sh in shooting_stars[:]:
        pygame.draw.line(screen, (255,255,255), (sh[0], sh[1]), (sh[0]+30, sh[1]-10), 2)
        sh[0]+=sh[2]; sh[1]+=sh[3]; sh[4]-=1
        if sh[4]<=0 or sh[0]<-100: shooting_stars.remove(sh)
    if elapsed-last_fw>0.75:
        fx = random.randint(100, W-100); fy = random.randint(50, 350)
        col=random.choice([(255,230,120),(120,220,255),(255,120,160)])
        for _ in range(35):
            a=random.uniform(0,6.28); sp=random.uniform(1.8,5.0)
            fireworks.append([fx,fy, math.cos(a)*sp, math.sin(a)*sp, 0, col, 4])
        last_fw=elapsed
    for fw in fireworks[:]:
        fw[0]+=fw[2]; fw[1]+=fw[3]; fw[3]+=0.06; fw[4]+=1
        if fw[4]>38: fireworks.remove(fw)
        else: pygame.draw.circle(screen, fw[5], (int(fw[0]), int(fw[1])), fw[6])
    for th in threads: th.update(); th.draw(screen)
    pygame.draw.circle(screen, (180,230,255), (CX, CY-5), 5)

    LYRICS = [(t + OFFSET, txt) for t, txt in BASE_LYRICS]
    if idx < len(LYRICS) and elapsed >= LYRICS[idx][0]:
        shown_text = LYRICS[idx][1]
        last_show = elapsed
        idx+=1
    if shown_text and elapsed - last_show < 6.0:
        surf=font_main.render(shown_text, True, (255,255,255))
        screen.blit(surf, (70, H//2 - 180))

    pygame.display.flip()
    clock.tick(90)
    if elapsed > 70: running=False
pygame.quit()
