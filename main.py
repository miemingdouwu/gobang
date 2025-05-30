# 导包
import pygame  # 导入pygame模块
import pygame.gfxdraw  # 导入pygame中的抗锯齿画图模块
import win32ui

# 初始化pygame
pygame.init()

# 棋子坐标
list1 = []  # 电脑落子坐标
list2 = []  # 玩家落子坐标
list3 = []  # 棋盘所有落子坐标
list_all = []  # 棋盘所有点
chess_arr = []  # 棋盘落子坐标，用于打印棋盘
neighbor = []  # 邻居点

next_point = [0, 0]

#  棋子数
black_sum = 0  # 黑棋数
white_sum = 0  # 白棋数

# 游戏状态
status = 1  # 1表示进行，2黑棋赢，3白棋赢
t = 1  # 黑白棋判断，1表示黑棋，2表示白棋
mode = 0  # 游戏模式，1表示pvp，2表示pve
mode1 = 0  # 控制电脑执黑执白，1表示电脑执黑先行，2表示电脑执白
player = 0  # 人机对战玩家执棋状态，1表示玩家执黑，2表示玩家执白

running = True  # 游戏状态判断
choose_mode = True  # 选择模式状态

# 博弈树参数
DEPTH = 3  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题
ratio = 1  # 进攻的系数   大于1 进攻型，  小于1 防守型

# 颜色参数
WHITE = (255, 255, 255)  # 白色，白棋
BLACK = (0, 0, 0)  # 黑色，黑棋
Chessboard_Color = (0xE3, 0x92, 0x65)  # 棋盘颜色，背景，棕色
RED = (255, 0, 0)  # 红色
BLUE = (0, 255, 255)  # 蓝色
GREEN = (78, 238, 148)  # 浅蓝色
LIGHTBLUE = (104, 131, 139)  # 亮蓝
GREY = (79, 79, 79)  # 灰色
DIMGREY = (105, 105, 105)  # 浅灰

# 窗口大小参数
GRID_SIZE = 50  # 棋盘格子大小
GRID_NUM = 15  # 棋盘每行/每列点数
Outer_Width = 30  # 棋盘外宽度
Border_Width = 4  # 棋盘边框两侧总宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
PIECE_SIZE = GRID_SIZE // 2 - 3  # 棋子大小
Border_Length = GRID_SIZE * (GRID_NUM - 1) + Inside_Width * 2 + Border_Width  # 棋盘边框线的长度
Start_X = Start_Y = Outer_Width + Border_Width // 2 + Inside_Width  # 网格线起点（左上角）坐标  (15+2+4, 15+2+4) 21, 21)
SCREEN_HEIGHT = GRID_SIZE * (GRID_NUM - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽
Rect_Width, Rect_Height = 125, 50  # 矩形大小
num_r = 25  # 计数器棋子半径

# 矩形窗口的坐标
# 起始坐标
Rect1_start_x, Rect1_start_y = Border_Length + 65, Start_Y + 4 * GRID_SIZE  # pvp
Rect2_start_x, Rect2_start_y = Border_Length + 65, Start_Y + 4 * GRID_SIZE + Rect_Height + 15  # pve
Rect3_start_x, Rect3_start_y = Border_Length + 65, Border_Length + Outer_Width - Rect_Height  # exit
Rect4_start_x, Rect4_start_y = Border_Length + 65, Border_Length + Outer_Width - Rect_Height * 2 - 15  # restart
Rect5_start_x, Rect5_start_y = Border_Length + 65, Border_Length + Outer_Width - Rect_Height * 3 - 15 * 2  # take back

Rect6_start_x, Rect6_start_y = Border_Length + 65, Border_Length + Outer_Width - Rect_Height * 4 - 15 * 3  #
Rect7_start_x, Rect7_start_y = Border_Length + 65, Border_Length + Outer_Width - Rect_Height * 5 - 15 * 4  #

# 末坐标
Rect1_end_x, Rect1_end_y = Rect1_start_x + Rect_Width, Rect_Height + Rect1_start_y  # pvp
Rect2_end_x, Rect2_end_y = Rect2_start_x + Rect_Width, Rect_Height + Rect2_start_y  # pve
Rect3_end_x, Rect3_end_y = Rect3_start_x + Rect_Width, Rect_Height + Rect3_start_y  # exit
Rect4_end_x, Rect4_end_y = Rect4_start_x + Rect_Width, Rect_Height + Rect4_start_y  # restart
Rect5_end_x, Rect5_end_y = Rect5_start_x + Rect_Width, Rect_Height + Rect5_start_y  # 悔棋

Rect6_end_x, Rect6_end_y = Rect6_start_x + Rect_Width, Rect_Height + Rect6_start_y
Rect7_end_x, Rect7_end_y = Rect7_start_x + Rect_Width, Rect_Height + Rect7_start_y

# 刷新率
FPS = 30  # 30帧率
clock = pygame.time.Clock()  # 时钟

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 定义窗口大小
pygame.display.set_caption("五子棋")  # 窗口名称


# 建窗口
def draw_screen():
    # 渲染窗口 背景
    screen.fill(Chessboard_Color)  # 背景色
    pygame.draw.rect(screen, BLACK, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)  # 边框

    # 画网格线
    for i in range(GRID_NUM):  # 画列
        pygame.draw.line(screen, BLACK, (Start_Y, Start_Y + GRID_SIZE * i),
                         (Start_Y + GRID_SIZE * (GRID_NUM - 1), Start_Y + GRID_SIZE * i), 1)

    for j in range(GRID_NUM):  # 画行
        pygame.draw.line(screen, BLACK, (Start_X + GRID_SIZE * j, Start_X),
                         (Start_X + GRID_SIZE * j, Start_X + GRID_SIZE * (GRID_NUM - 1)), 1)

    # 画棋盘上中心位置和其他某些交点处交点（星位）
    for i in (3, 7, 11):
        for j in (3, 7, 11):
            if i == j == 7:
                radius = 5  # 半径
            else:
                radius = 3  # 半径
            pygame.gfxdraw.aacircle(screen, Start_X + GRID_SIZE * i, Start_Y + GRID_SIZE * j, radius, BLACK)
            pygame.gfxdraw.filled_circle(screen, Start_X + GRID_SIZE * i, Start_Y + GRID_SIZE * j, radius, BLACK)

    # 画个矩阵，显示模式
    pygame.draw.rect(screen, BLUE, (Rect1_start_x, Rect1_start_y, Rect_Width, Rect_Height))  # 人人对战
    pygame.draw.rect(screen, GREEN, (Rect2_start_x, Rect2_start_y, Rect_Width, Rect_Height))  # 人机对战
    pygame.draw.rect(screen, RED, (Rect3_start_x, Rect3_start_y, Rect_Width, Rect_Height))  # 退出游戏
    pygame.draw.rect(screen, LIGHTBLUE, (Rect4_start_x, Rect4_start_y, Rect_Width, Rect_Height))  # 重新开始
    pygame.draw.rect(screen, LIGHTBLUE, (Rect5_start_x, Rect5_start_y, Rect_Width, Rect_Height))  # 悔棋
    pygame.draw.rect(screen, DIMGREY, (Rect6_start_x, Rect6_start_y, Rect_Width, Rect_Height))  # 载入棋谱
    pygame.draw.rect(screen, DIMGREY, (Rect7_start_x, Rect7_start_y, Rect_Width, Rect_Height))  # 保存棋谱


    # 写文本
    font = pygame.font.Font("images/simhei.ttf", 25)  # 初始化文本格式
    # 人人对战
    text1 = font.render("人人对战", True, BLACK)  # 处理文本
    screen.blit(text1, (Rect1_start_x + Rect_Width / 2 - text1.get_width() / 2,
                        Rect1_start_y + Rect_Height / 2 - text1.get_height() / 2))  # 描绘文本
    # 人机对战
    text2 = font.render("人机对战", True, BLACK)  # 处理文本
    screen.blit(text2, (Rect2_start_x + Rect_Width / 2 - text2.get_width() / 2,
                        Rect2_start_y + Rect_Height / 2 - text2.get_height() / 2))  # 描绘文本
    # 退出游戏
    text3 = font.render("退出游戏", True, BLACK)  # 处理文本
    screen.blit(text3, (Rect3_start_x + Rect_Width / 2 - text3.get_width() / 2,
                        Rect3_start_y + Rect_Height / 2 - text3.get_height() / 2))  # 描绘文本
    # 重新开始
    text4 = font.render("重新开始", True, BLACK)  # 处理文本
    screen.blit(text4, (Rect4_start_x + Rect_Width / 2 - text4.get_width() / 2,
                        Rect4_start_y + Rect_Height / 2 - text4.get_height() / 2))  # 描绘文本

    # 悔棋
    text5 = font.render("悔棋", True, BLACK)  # 处理文本
    screen.blit(text5, (Rect5_start_x + Rect_Width / 2 - text5.get_width() / 2,
                        Rect5_start_y + Rect_Height / 2 - text5.get_height() / 2))  # 描绘文本

    # 载入棋谱
    text6 = font.render("载入棋谱", True, BLACK)  # 处理文本
    screen.blit(text6, (Rect6_start_x + Rect_Width / 2 - text6.get_width() / 2,
                        Rect6_start_y + Rect_Height / 2 - text6.get_height() / 2))  # 描绘文本

    # 保存棋谱
    text7 = font.render("保存棋谱", True, BLACK)  # 处理文本
    screen.blit(text7, (Rect7_start_x + Rect_Width / 2 - text7.get_width() / 2,
                        Rect7_start_y + Rect_Height / 2 - text7.get_height() / 2))  # 描绘文本

    # 黑白子计数器
    font = pygame.font.Font(None, 65)  # 初始化文本格式
    # 黑棋数
    text5 = font.render("X" + str(black_sum), True, BLACK)
    screen.blit(text5, (Rect1_start_x + 2 * num_r + 10, Outer_Width + num_r * 2 - text5.get_height()))
    # 白棋数
    text6 = font.render("X" + str(white_sum), True, WHITE)
    screen.blit(text6, (Rect1_start_x + 2 * num_r + 10, Outer_Width + num_r * 4 + 15 - text5.get_height()))

    # pve模式下的选择电脑执黑执白
    if mode == 2:
        pygame.gfxdraw.aacircle(screen, Rect2_start_x + 8, Rect2_end_y + 15, 8, BLACK)  # 电脑执黑
        pygame.gfxdraw.aacircle(screen, Rect2_start_x + 8, Rect2_end_y + 40, 8, WHITE)  # 电脑执白
        font = pygame.font.Font("images/simhei.ttf", 20)
        text7 = font.render("电脑执黑", True, BLACK)  # 电脑执黑
        screen.blit(text7, (Rect2_start_x + 20, Rect2_end_y + 15 - text7.get_height() / 2))
        text8 = font.render("电脑执白", True, WHITE)  # 电脑执白
        screen.blit(text8, (Rect2_start_x + 20, Rect2_end_y + 40 - text8.get_height() / 2))

        # 选择电脑执黑
        if mode1 == 1:
            pygame.gfxdraw.aacircle(screen, Rect2_start_x + 8, Rect2_end_y + 15, 4, BLACK)  # 电脑执黑
            pygame.gfxdraw.filled_circle(screen, Rect2_start_x + 8, Rect2_end_y + 15, 4, BLACK)  # 电脑执黑
        # 选择电脑执白
        if mode1 == 2:
            pygame.gfxdraw.aacircle(screen, Rect2_start_x + 8, Rect2_end_y + 40, 4, BLACK)  # 电脑执白
            pygame.gfxdraw.filled_circle(screen, Rect2_start_x + 8, Rect2_end_y + 40, 4, BLACK)  # 电脑执白

    # 显示当前落子的一方
    pygame.gfxdraw.aacircle(screen, Rect1_start_x + 25, Outer_Width + num_r, num_r, BLACK)  # 黑子
    pygame.gfxdraw.filled_circle(screen, Rect1_start_x + 25, Outer_Width + num_r, num_r, BLACK)

    pygame.gfxdraw.aacircle(screen, Rect1_start_x + 25, Outer_Width + 3 * num_r + 15, num_r, WHITE)  # 白子
    pygame.gfxdraw.filled_circle(screen, Rect1_start_x + 25, Outer_Width + 3 * num_r + 15, num_r, WHITE)

    # 显示所有落下的棋子
    for val in chess_arr:  # 显示所有落下的棋子
        if val[2] == 1:  # 平滑的圆和填充圆，黑棋
            pygame.gfxdraw.aacircle(screen, GRID_SIZE * val[0] + Start_X, GRID_SIZE * val[1] + Start_Y, PIECE_SIZE,
                                    BLACK)
            pygame.gfxdraw.filled_circle(screen, GRID_SIZE * val[0] + Start_X, GRID_SIZE * val[1] + Start_Y, PIECE_SIZE,
                                         BLACK)
        if val[2] == 2:  # 平滑的圆和填充圆，白棋
            pygame.gfxdraw.aacircle(screen, GRID_SIZE * val[0] + Start_X, GRID_SIZE * val[1] + Start_Y, PIECE_SIZE,
                                    WHITE)
            pygame.gfxdraw.filled_circle(screen, GRID_SIZE * val[0] + Start_X, GRID_SIZE * val[1] + Start_Y, PIECE_SIZE,
                                         WHITE)

    if status != 1:  # 产生赢家
        if status == 4:
            not_text = pygame.font.Font("images/simhei.ttf", 120)  # 初始化字体
            text = '和棋'  # 和棋
            not_text = not_text.render(text, True, RED)  # 文本处理
            screen.blit(not_text, (
            SCREEN_WIDTH / 2 - not_text.get_width() / 2, SCREEN_HEIGHT / 2 - not_text.get_height() / 2))  # 文本输出
        else:
            winner_text = pygame.font.Font("images/simhei.ttf", 120)  # 初始化字体
            win_text = "%s" % ('黑子获胜!' if status == 2 else '白子获胜!')  # 判断赢家
            winner_text = winner_text.render(win_text, True, RED)  # 文本处理
            screen.blit(winner_text, (
            SCREEN_WIDTH / 2 - winner_text.get_width() / 2, SCREEN_HEIGHT / 2 - winner_text.get_height() / 2))  # 文本输出


# 获取落子的相对坐标
def get_point(click_pos):
    # （Start_X, Start_Y)棋盘左上位置坐标
    pos_x = click_pos[0] - Start_X  # 绝对坐标
    pos_y = click_pos[1] - Start_Y  # 绝对坐标
    if pos_x < -Inside_Width - Border_Width / 2 or pos_y < -Inside_Width - Border_Width / 2:  # 超出窗口
        return None
    x = pos_x // GRID_SIZE
    y = pos_y // GRID_SIZE

    # 四舍五入
    if pos_x % GRID_SIZE > PIECE_SIZE:  # 边界处理
        x += 1
    if pos_y % GRID_SIZE > PIECE_SIZE:  # 边界处理
        y += 1
    if x >= GRID_NUM or y >= GRID_NUM:  # 越界处理
        return None
    chess_x_y = (x, y)
    return chess_x_y  # 相对坐标


# 判断是否越界，点击位置是否超出棋盘
def in_chessboard_area(click_pos):
    return (Start_X - Inside_Width - Border_Width / 2 <= click_pos[0] <= Border_Length + Outer_Width) and (
            Start_Y - Inside_Width - Border_Width / 2 <= click_pos[1] <= Border_Length + Outer_Width)


# 判断棋格是否存在棋子
def in_chess_arr(point):
    if (point[0], point[1], 1) not in chess_arr and (point[0], point[1], 2) not in chess_arr:
        return True
    else:
        return False


# 判定输赢 dfs
def check_win(chess_arr):
    # 先定义一个15*15的二维数组
    bo = [[0] * GRID_NUM for i in range(GRID_NUM)]
    flag = chess_arr[-1][2]  # 最后一个子的x

    # 初始化bool数组
    for x, y, z in chess_arr:
        if z == flag:  # 筛选黑白子
            bo[y][x] = 1  # 上面有棋则标1

    # 方向数组
    direction = [[(-1, 0), (1, 0)],  # 往左＋往右
                 [(0, -1), (0, 1)],  # 往上＋往下
                 [(-1, -1), (1, 1)],  # 往左上＋往右下
                 [(-1, 1), (1, -1)]]  # 往左下＋往右上

    for dire1, dire2 in direction:  # 遍历同方向数组
        num1 = 0  # 同方向一边最长连棋
        num2 = 0  # 同方向另一边最长连棋
        dx1, dy1 = dire1  # 一个方向
        dx2, dy2 = dire2  # 另一个相对方向
        xx = chess_arr[-1][0]  # 最后一个子的x
        yy = chess_arr[-1][1]  # 最后一个子的y
        while True:  # 搜索
            xx += dx1
            yy += dy1
            num1 += 1  # 先加一
            if xx < 0 or xx >= GRID_NUM or yy < 0 or yy >= GRID_NUM or bo[yy][xx] == 0:  # 条件限制
                num1 -= 1  # 没有棋子就先减一
                break

        xx = chess_arr[-1][0]  # 最后一个子的x
        yy = chess_arr[-1][1]  # 最后一个子的y

        while True:  # 搜索
            xx += dx2
            yy += dy2
            num2 += 1  # 先加一
            if xx < 0 or xx >= GRID_NUM or yy < 0 or yy >= GRID_NUM or bo[yy][xx] == 0:  # 条件限制
                num2 -= 1  # 没有棋子就减一
                break

        if num1 + num2 + 1 >= 5:  # 判断最长连棋有没有等于或者超过5
            return True

    return False



# 判断是否同时为0
def not_zero_zero(dx, dy):
    if dx == 0 and dy == 0:
        return False
    else:
        return True



# 新增AI类：
class AI:
    def __init__(self):
        self.difficulty = 'hard'

    def evaluate_position(self, board, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        for dx, dy in directions:
            count = 1
            block = 0

            # 正向检查
            tx, ty = x + dx, y + dy
            while 0 <= tx < GRID_NUM and 0 <= ty < GRID_NUM:
                if board[tx][ty] == player:
                    count += 1
                elif board[tx][ty] is None:
                    break
                else:
                    block += 1
                    break
                tx += dx
                ty += dy

            # 反向检查
            tx, ty = x - dx, y - dy
            while 0 <= tx < GRID_NUM and 0 <= ty < GRID_NUM:
                if board[tx][ty] == player:
                    count += 1
                elif board[tx][ty] is None:
                    break
                else:
                    block += 1
                    break
                tx -= dx
                ty -= dy

            # 困难模式评分
            if count >= 5:
                score += 100000
            elif count == 4:
                if block == 0:
                    score += 10000
                elif block == 1:
                    score += 1000
            elif count == 3:
                if block == 0:
                    score += 1000
                elif block == 1:
                    score += 100
            elif count == 2:
                if block == 0:
                    score += 100
                elif block == 1:
                    score += 10

        return score

    def get_move(self):
        # 创建二维棋盘数组
        board = [[None] * GRID_NUM for _ in range(GRID_NUM)]
        for x, y, z in chess_arr:
            board[y][x] = 'black' if z == 1 else 'white'

        empty_positions = [(i, j) for i in range(GRID_NUM) for j in range(GRID_NUM)
                           if board[i][j] is None]

        if not empty_positions:
            return None

        best_score = -float('inf')
        best_move = None
        for i, j in empty_positions:
            # 进攻评分（AI执棋）
            attack_score = self.evaluate_position(board, i, j, 'white' if mode1 == 2 else 'black')
            # 防守评分（玩家执棋）
            defense_score = self.evaluate_position(board, i, j, 'black' if mode1 == 2 else 'white')
            score = attack_score + defense_score * 0.9

            # 邻近位置加分
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= i + dx < GRID_NUM and 0 <= j + dy < GRID_NUM:
                        if board[i + dx][j + dy] is not None:
                            score += 10

            if score > best_score:
                best_score = score
                best_move = (j, i)  # 注意坐标转换

        return best_move

# 修改原有的ai函数：
def ai(temp):
    ai = AI()
    x, y = ai.get_move()
    return x, y


# 保存棋谱
def save_chess(chess_list, string):
    with open("images/" + string + '.txt', 'w') as f:
        for line in chess_list:
            for line1 in line:
                f.write(str(line1))
                f.write(' ')
            f.write('\n')
    f.close()


# 载入棋谱
def load_chess():
    load = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    load.SetOFNInitialDir(r'images')  # 设置打开文件对话框中的初始显示目录
    flag = load.DoModal()
    filename = load.GetPathName()  # 获取选择的文件名称
    if flag == 1:
        print("打开棋谱", filename)
    else:
        print("打开失败!")
    f = open(filename, 'r')
    chess_list = []
    for line in f.readlines():
        line = line.strip(' \n')
        xt = [i for i in line.split(' ')]
        chess_list.append(xt)
    f.close()
    return chess_list


for i in range(15):
    for j in range(15):
        list_all.append((i, j))

# 主循环
while running:

    # 设置屏幕刷新
    clock.tick(FPS)
    # 事件执行
    for event in pygame.event.get():  # 事件判断
        if event.type == pygame.QUIT:  # 关闭按键
            running = False  # 状态转变
            pygame.quit()  # 卸载pygame模块
            exit()  # 退出窗口

        if event.type == pygame.MOUSEBUTTONDOWN and choose_mode:  # 鼠标按下
            mouse_pos = pygame.mouse.get_pos()  # 获取鼠标光标坐标

            if status == 1:
                # 选择游戏模式
                if Rect1_start_x <= mouse_pos[0] <= Rect1_end_x and Rect1_start_y <= mouse_pos[1] <= Rect1_end_y:  # pvp
                    mode = 1
                    # choose_mode = False

                if Rect2_start_x <= mouse_pos[0] <= Rect2_end_x and Rect2_start_y <= mouse_pos[1] <= Rect2_end_y:  # pve
                    mode = 2

                # 电脑执黑，玩家执白
                if (mode == 2 and Rect2_start_x + 1 <= mouse_pos[0] <= Rect2_start_x + 13) and (
                        Rect2_end_y + 10 <= mouse_pos[1] <= Rect2_end_y + 20):
                    mode1 = 1
                    player = 2
                    # choose_mode = False

                # 电脑执白，玩家执黑
                if (mode == 2 and Rect2_start_x + 1 <= mouse_pos[0] <= Rect2_start_x + 13) and (
                        Rect2_end_y + 35 <= mouse_pos[1] <= Rect2_end_y + 45):
                    mode1 = 2
                    player = 1
                    # choose_mode = False

        # 人人对战pvp
        if status == 1 and mode == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标光标坐标
                point = get_point(mouse_pos)  # 获取光标位置
                if in_chessboard_area(mouse_pos) and in_chess_arr(point):  # 判断是否越界
                    chess_point = (point[0], point[1], t)  # 处理黑白子
                    chess_arr.append(chess_point)  # 存入数组
                    list3.append((point[0], point[1]))

                    if t == 1:  # 黑棋数加一
                        list1.append((point[0], point[1]))
                        black_sum += 1
                    if t == 2:  # 白棋数加一
                        list2.append((point[0], point[1]))
                        white_sum += 1

                    if len(chess_arr) == 15 * 15:  # 和棋
                        status = 4
                    elif check_win(chess_arr):  # 判断输赢
                        status = 2 if t == 1 else 3
                    else:
                        t = 2 if t == 1 else 1

        # 人机对战pve
        if status == 1 and mode == 2:
            max_score = -1e9  # 初始化最大评分
            i = 0  # 初始化坐标
            j = 0  # 初始化坐标
            score = [[0] * GRID_NUM for m in range(GRID_NUM)]  # 定义一个初始化为0的分数二维数组
            if mode1 == 1 and len(chess_arr) == 0:  # 电脑执黑时先落子
                chess_arr.append((7, 7, t))
                list1.append((7, 7))
                list3.append((7, 7))
                black_sum += 1
                t = 2
            elif t == player:  # 玩家下棋
                if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                    mouse_pos = pygame.mouse.get_pos()  # 获取鼠标光标坐标
                    point = get_point(mouse_pos)  # 获取光标位置
                    if in_chessboard_area(mouse_pos) and in_chess_arr(point):  # 判断是否越界
                        chess_point = (point[0], point[1], t)  # 处理黑白子
                        chess_arr.append(chess_point)  # 存入数组
                        list3.append((point[0], point[1]))

                        if t == 1:  # 黑棋数加一
                            black_sum += 1
                            list1.append((point[0], point[1]))
                        if t == 2:  # 白棋数加一
                            white_sum += 1
                            list2.append((point[0], point[1]))

                        if len(chess_arr) == 15 * 15:  # 和棋
                            status = 4
                        elif check_win(chess_arr):  # 判断输赢
                            status = 2 if t == 1 else 3
                        else:
                            t = mode1 if t == player else player

            elif t == mode1:  # 电脑下棋
                # evaluate(chess_arr, score, t)  # 对当前棋盘评分
                i, j = ai(t)
                chess_arr.append((i, j, t))
                list3.append((i, j))
                if t == 1:  # 黑棋数加一
                    black_sum += 1
                    list1.append((i, j))
                if t == 2:  # 白棋数加一
                    white_sum += 1
                    list2.append((i, j))

                if len(chess_arr) == 15 * 15:  # 和棋
                    status = 4
                elif check_win(chess_arr):  # 判断输赢
                    status = 2 if t == 1 else 3
                else:
                    t = player if t == mode1 else mode1

        if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
            mouse_pos = pygame.mouse.get_pos()  # 获取鼠标光标坐标
            # 悔棋
            if Rect5_start_x <= mouse_pos[0] <= Rect5_end_x and Rect5_start_y <= mouse_pos[1] <= Rect5_end_y:
                if mode == 1 and len(chess_arr) > 0:  # 人人对战的悔棋
                    if status == 1:
                        t = 2 if t == 1 else 1  # 重新改变落子方
                        black_sum = black_sum - 1 if t == 1 else black_sum  # 计数器减一
                        white_sum = white_sum - 1 if t == 2 else white_sum  # 计数器减一
                        if t == 1:
                            list1.pop()
                        else:
                            list2.pop()
                        chess_arr.pop()  # 删除最后一个子
                        list3.pop()
                        status = 1  # 把输赢状态改变为1
                    if status == 2 or status == 3 or status == 4:
                        black_sum = black_sum - 1 if t == 1 else black_sum  # 计数器减一
                        white_sum = white_sum - 1 if t == 2 else white_sum  # 计数器减一
                        if t == 1:
                            list1.pop()
                        else:
                            list2.pop()
                        chess_arr.pop()  # 删除最后一个子
                        list3.pop()
                        status = 1  # 把输赢状态改变为1

                if mode == 2 and len(chess_arr) >= 2:  # 人机对战的悔棋
                    if status == 1:
                        chess_arr.pop()  # 删除最后一个子
                        chess_arr.pop()  # 再删除最后一个子
                        list3.pop()
                        list3.pop()
                        list1.pop()
                        list2.pop()
                        black_sum = black_sum - 1  # 计数器减一
                        white_sum = white_sum - 1  # 计数器减一
                        status = 1  # 把输赢状态改变为1
                    if status == 2 or status == 3 or status == 4:
                        t = 2 if t == 1 else 1  # 重新改变落子方
                        chess_arr.pop()  # 删除最后一个子
                        chess_arr.pop()  # 再删除最后一个子
                        list3.pop()
                        list3.pop()
                        list1.pop()
                        list2.pop()
                        black_sum = black_sum - 1  # 计数器减一
                        white_sum = white_sum - 1  # 计数器减一
                        status = 1  # 把输赢状态改变为1
                if len(chess_arr) == 0:
                    first = True

            # 载入棋谱
            if Rect6_start_x <= mouse_pos[0] <= Rect6_end_x and Rect6_start_y <= mouse_pos[1] <= Rect6_end_y:
                if len(chess_arr) == 0:
                    chess_l = load_chess()
                    for i in chess_l:
                        x = (int(i[0]), int(i[1]), int(i[2]))
                        if int(i[2]) == 1:
                            black_sum += 1
                        else:
                            white_sum += 1
                        chess_arr.append(x)
                        t = 1 if t == 2 else 2
                    print("载入成功")
                else:
                    print("载入失败")

            # 保存棋谱
            if Rect7_start_x <= mouse_pos[0] <= Rect7_end_x and Rect7_start_y <= mouse_pos[1] <= Rect7_end_y:
                if len(chess_arr) > 0:
                    save_chess(chess_arr, "chess_m")
                    print("保存成功")

            # 重新开始游戏，清空棋盘
            if Rect4_start_x <= mouse_pos[0] <= Rect4_end_x and Rect4_start_y <= mouse_pos[1] <= Rect4_end_y:
                first = True  # 重置电脑执黑先行状态
                choose_mode = True  # 重置选择模式状态
                status = 1  # 重新初始化游戏状态
                t = 1  # 重新初始化下棋方
                mode = 0  # 重新重置选择游戏模式
                mode1 = 0  # 重新重置选择电脑执黑执白
                black_sum = 0  # 重置黑棋数
                white_sum = 0  # 重置白棋数
                list3.clear()
                list1.clear()
                list2.clear()
                chess_arr.clear()  # 清理棋盘

            # 退出游戏按键
            if Rect3_start_x <= mouse_pos[0] <= Rect3_end_x and Rect3_start_y <= mouse_pos[1] <= Rect3_end_y:
                pygame.quit()  # 卸载pygame模块
                exit()  # 退出窗口

    draw_screen()  # 画窗口
    pygame.display.flip()  # 刷新窗口
